import os
import shutil

import click

from diary import config
from diary.utils.entries import (
    get_entry_path, get_metadata_path, get_metadata, upsert_metadata,
)
from diary.utils.models import Entry
from diary.utils.editing import (
    prompt_metadata_update, UserInputError, EmptyMetadataError, EditAbort
)


def get_entry_names() -> list[str] | None:
    if not os.path.exists(config.DATA_DIR):
        click.echo('no entries exist')
        return

    return os.listdir(config.DATA_DIR)


def edit_entry(entry_name: str):
    entry_path = get_entry_path(entry_name=entry_name, create=True)
    if entry_path is None:
        click.echo(f'could not create entry in {config.DATA_DIR}, check access')
    else:
        click.edit(filename=str(entry_path))


def _iterate_over_entries(
        entries: list[str],
        result_map: dict[int, str],
        tags: set[str] = None,
        no_tip: bool = False
):

    index = 1
    for entry in entries:
        entry_metadata = get_metadata(entry_name=entry) or Entry()

        if tags:
            entry_tags = set(entry_metadata.tags)
            if not entry_tags.intersection(tags):
                continue

        displayed_entry = f'{click.style(str(index) + ".", fg="green")} {entry}'
        if entry_metadata.title:
            displayed_entry += f' - {entry_metadata.title}'
        displayed_entry += '\n'

        result_map[index] = entry
        if index == 1 and not no_tip:
            yield 'Choose entry number:\n'
        yield displayed_entry

        index += 1


def list_entries(tags: tuple[str], pages: bool, no_return: bool) -> dict[int, str] | None:

    entries = get_entry_names()
    if not entries:
        return None

    entries.sort(reverse=True)
    entry_count = len(entries)

    tags = set(tags)
    result_map = {}

    entries = list(_iterate_over_entries(entries=entries, result_map=result_map, tags=tags, no_tip=no_return))
    if pages or entry_count > config.NON_PAGED_ENTRY_COUNT:
        click.echo_via_pager(entries)
    else:
        for entry in entries:
            click.echo(entry, nl=False)

    return result_map if not no_return else None


def add_metadata(entry_name: str, title: str = None, tags: tuple[str] = None):
    if not title and not tags:
        return
    tags = list(tags)

    metadata_path = get_metadata_path(entry_name=entry_name, create=True)

    if metadata_path is None:
        click.echo(f'could not edit metadata in {config.DATA_DIR}, check access')
        return

    upsert_metadata(str(metadata_path), entry_data=Entry(title=title, tags=tags))


def update_entry_meta(entry_name: str):

    if not get_entry_path(entry_name=entry_name):
        click.echo('entry not found, cannot edit metadata')
        return

    metadata_path = get_metadata_path(entry_name=entry_name, create=True)

    if metadata_path is None:
        click.echo(f'could not edit metadata in {config.DATA_DIR}, check access')
        return

    try:
        prompt_metadata_update(metadata_path=str(metadata_path))
    except (UserInputError, EmptyMetadataError) as e:
        click.echo(f'error: {e}')
    except EditAbort as e:
        click.echo(e)
    else:
        click.echo(f'successfully updated metada for entry {entry_name}')


def view_entry(entry_name: str, short: bool):
    entry_path = get_entry_path(entry_name=entry_name)

    if entry_path is None:
        click.echo(f'could not find entry {entry_name}')
        return

    metadata = get_metadata(entry_name=entry_name)
    with open(str(entry_path), 'r') as f:
        entry_text = f.read()

    if metadata is None and not entry_text:
        click.echo(f'{entry_name} is empty')
        return

    metadata = metadata if metadata is not None else Entry()
    add_spacing = not short

    click.echo(nl=add_spacing)
    click.echo(f'{click.style("Title:", fg="green")} {metadata.title or ""}')
    click.echo(nl=add_spacing)
    click.echo(f'{click.style("Tags:", fg="green")} {", ".join(metadata.tags)}')
    if metadata.media:
        click.echo(nl=add_spacing)
        click.echo(click.style("Media:", fg="green"))
        for media_file in metadata.media:
            fname = media_file.file_name
            click.echo(
                f'{click.style("Name:", fg="green")} {fname}'.ljust(config.META_ATTR_WIDTH),
                nl=False
            )
            if media_file.description:
                description = f' {click.style("Description:", fg="green")} {media_file.description}'
                click.echo(description.ljust(config.META_ATTR_WIDTH), nl=False)
            click.echo()
    if entry_text:
        click.echo(nl=add_spacing)
        click.echo(click.style("Entry:", fg="green"), nl=add_spacing)
        if short:
            entry_text = entry_text[:config.SHORT_TEXT_SYMBOL_LIMIT] + '...'
        click.echo(entry_text)
    click.echo(nl=add_spacing)


def delete_entry(entry_name: str):
    entry_path = get_entry_path(entry_name=entry_name)

    if entry_path is None:
        click.echo(f'could not find entry {entry_name}')
        return

    try:
        shutil.rmtree(entry_path.parent)
    except Exception:
        click.echo(f'could not delete entry from {config.DATA_DIR}')
        return

    click.echo(f'successfully deleted entry {entry_name}')


def list_entry_tags():

    entries = get_entry_names()

    tags = set()
    for entry in entries:
        if not (metadata := get_metadata(entry_name=entry)):
            continue
        entry_tags = set(metadata.tags)
        tags.update(entry_tags)

    if tags:
        tags = list(tags)
        tags.sort()
        for tag in tags:
            click.echo(tag)
    else:
        click.echo('no tags found')
