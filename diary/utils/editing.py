import json
from dataclasses import dataclass
from typing import Callable, Any

import click

from diary import config
from diary.utils.models import Entry, MediaEntry


@dataclass
class MetaField:
    name: str
    data: str | list | None
    handler: Callable


class UserInputError(Exception):
    pass


class EmptyMetadataError(Exception):
    pass


class EditAbort(Exception):
    UPDATE_ABORTED_TEXT = 'update aborted'


def form_tags_input(tags: list[str] | None) -> str:
    tags = tags or []
    return ','.join([i for i in tags])


def parse_tags_output(tags_output: str) -> list[str]:
    tags = []
    for tag in tags_output.split(','):
        tag = tag.strip()
        if tag:
            tags.append(tag)
    return tags


def form_str_input(value: str | None) -> str | None:
    return value or ''


def parse_str_output(value: str) -> str | None:
    return value or None


def form_input(fields: list[MetaField]) -> list[str]:
    file_lines = []
    for field in fields:
        file_lines.append(f'{field.name}: {field.handler(field.data)}')
    return file_lines


def parse_output(update_text: str, update_handlers: list[MetaField]) -> dict[str, Any]:
    data_update = {}
    update_handlers = {f.name: f.handler for f in update_handlers}
    for line in update_text.split('\n'):
        stripped_line = line.strip()
        if stripped_line.startswith('#') or not stripped_line:
            continue

        line_error = UserInputError(f'could not parse line "{line}"')
        if stripped_line.count(':') != 1:
            raise line_error

        try:
            key, value = stripped_line.split(':', maxsplit=1)
        except ValueError:
            raise line_error
        else:
            if not key:
                raise line_error

        key = key.strip()
        value = value.strip()

        if not (handler := update_handlers.get(key, None)):
            raise UserInputError(f'invalid metadata key "{key}"')

        data_update[key] = handler(value)

    return data_update


def get_media_updates(metadata: Entry, file_name: str) -> Entry:
    file = None
    media = metadata.media
    for file in media:
        if file.file_name == file_name:
            break
    if file is None:
        raise EmptyMetadataError(f'metadata not found for file {file_name}')

    prompt_lines = form_input([
        MetaField(name='file_name', data=file.file_name, handler=form_str_input),
        MetaField(name='description', data=file.description, handler=form_str_input),
    ])

    prompt_lines.insert(0, config.META_EDIT_TEXT)
    editor_text = '\n'.join(prompt_lines)

    update_text = click.edit(editor_text)

    if update_text is None:
        raise EditAbort(EditAbort.UPDATE_ABORTED_TEXT)

    output = parse_output(
        update_text=update_text,
        update_handlers=[
            MetaField(name='file_name', data=None, handler=parse_str_output),
            MetaField(name='description', data=None, handler=parse_str_output)
        ]
    )

    try:
        updated_file = MediaEntry.from_dict(output)
    except TypeError as e:
        raise UserInputError(f'could not parse metadata: {e}')

    if updated_file.file_name != file_name:
        UserInputError('cannot change file name')

    new_media = []
    for file in media:
        if file.file_name == file_name:
            new_media.append(updated_file)
        else:
            new_media.append(file)

    metadata.media = new_media

    return metadata


def get_entry_updates(metadata: Entry) -> Entry:

    prompt_lines = form_input([
        MetaField(name='title', data=metadata.title, handler=form_str_input),
        MetaField(name='tags', data=metadata.tags, handler=form_tags_input),
    ])

    prompt_lines.insert(0, config.META_EDIT_TEXT)
    editor_text = '\n'.join(prompt_lines)

    update_text = click.edit(editor_text)

    if update_text is None:
        raise EditAbort(EditAbort.UPDATE_ABORTED_TEXT)

    output = parse_output(
        update_text=update_text,
        update_handlers=[
            MetaField(name='title', data=None, handler=parse_str_output),
            MetaField(name='tags', data=None, handler=parse_tags_output)
        ]
    )

    new_metadata = Entry.from_dict(output)
    new_metadata.media = metadata.media

    return new_metadata


def prompt_metadata_update(
    metadata_path: str,
    file_name: str = None,
):
    with open(metadata_path, 'r') as f:
        content = f.read()

    metadata = Entry.from_dict(json.loads(content)) if content else Entry()
    if file_name is not None:
        metadata = get_media_updates(metadata, file_name)
    else:
        metadata = get_entry_updates(metadata)

    with open(metadata_path, 'w') as f:
        f.write(json.dumps(metadata.to_dict()))
