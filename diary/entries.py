import os
from pathlib import Path
import json

import click

from diary.config import (
    DATA_SUBDIR, ENTRY_FILE_NAME, METADATA_FILE_NAME,
    METADATA_TITLE_KEY, METADATA_TAGS_KEY, NON_PAGED_ENTRY_COUNT
)

USER_HOME = Path.home()
DATA_DIR = USER_HOME / Path(DATA_SUBDIR)


def check_file_ok(directory: Path, file: Path = None) -> bool:
    try:
        directory.mkdir(parents=True, exist_ok=True)
        if file is not None:
            file.touch(exist_ok=True)
    except PermissionError:
        return False
    return True


def get_entry_path(entry_name: str) -> str | None:
    subdirectory = DATA_DIR / entry_name
    filename = subdirectory / ENTRY_FILE_NAME

    if not check_file_ok(directory=subdirectory, file=filename):
        return None
    return str(filename)


def get_entry_names() -> list[str] | None:
    if not os.path.exists(DATA_DIR):
        click.echo('no entries exist')
        return

    return os.listdir(DATA_DIR)


def get_metadata_path(entry_name: str) -> str | None:
    subdirectory = DATA_DIR / entry_name
    filename = subdirectory / METADATA_FILE_NAME

    if not check_file_ok(directory=subdirectory, file=filename):
        return None
    return str(filename)


def edit_entry(entry_name: str):
    entry_path = get_entry_path(entry_name)
    if entry_path is None:
        click.echo(f'could not create entry in {DATA_DIR}, check access')
    else:
        click.edit(filename=entry_path)


def get_metadata(entry_name) -> dict:
    metadata_path = get_metadata_path(entry_name)

    if metadata_path is None:
        return {}

    with open(metadata_path, 'r') as f:
        content = f.read()
    return json.loads(content) if content else {}


def _iterate_over_entries(
        entries: list[str],
        result_map: dict[int, str],
        tags: set[str] = None,
        no_tip: bool = False
):

    index = 1
    for entry in entries:
        entry_metadata = get_metadata(entry_name=entry)

        if tags:
            entry_tags = set(entry_metadata.get(METADATA_TAGS_KEY, []))
            if not entry_tags.intersection(tags):
                continue

        displayed_entry = f'{click.style(str(index) + ".", fg="green")} {entry}'
        if title := entry_metadata.get(METADATA_TITLE_KEY):
            displayed_entry += f' - {title}'
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

    entries = _iterate_over_entries(entries=entries, result_map=result_map, tags=tags, no_tip=no_return)
    if pages or entry_count > NON_PAGED_ENTRY_COUNT:
        click.echo_via_pager(entries)
    else:
        for entry in entries:
            click.echo(entry, nl=False)

    return result_map if not no_return else None


def add_metadata(entry_name: str, title: str = None, tags: tuple[str] = None):
    if not title and not tags:
        return

    metadata_path = get_metadata_path(entry_name)

    if metadata_path is None:
        click.echo(f'could not edit metadata in {DATA_DIR}, check access')
        return

    data_upd = {}
    if title:
        data_upd[METADATA_TITLE_KEY] = title
    if tags:
        data_upd[METADATA_TAGS_KEY] = tags

    with open(metadata_path, 'r') as f:
        content = f.read()

    metadata = json.loads(content) if content else {}
    if title:
        metadata[METADATA_TITLE_KEY] = title
    if tags:
        existing_tags: list = metadata.get(METADATA_TAGS_KEY, [])
        existing_tags.extend(tags)
        metadata[METADATA_TAGS_KEY] = list(set(existing_tags))

    with open(metadata_path, 'w') as f:
        f.write(json.dumps(metadata))


def list_entry_tags():

    entries = get_entry_names()

    tags = set()
    for entry in entries:
        entry_tags = set(get_metadata(entry_name=entry).get(METADATA_TAGS_KEY, []))
        tags.update(entry_tags)

    if tags:
        tags = list(tags)
        tags.sort()
        for tag in tags:
            click.echo(tag)
    else:
        click.echo('no tags found')
