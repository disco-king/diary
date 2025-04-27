import os
import json

import click

from diary import config
from diary.utils.entries import (
    get_entry_path, get_metadata_path, get_metadata, upsert_metadata
)


def get_entry_names() -> list[str] | None:
    if not os.path.exists(config.DATA_DIR):
        click.echo('no entries exist')
        return

    return os.listdir(config.DATA_DIR)


def edit_entry(entry_name: str):
    entry_path = get_entry_path(entry_name)
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
        entry_metadata = get_metadata(entry_name=entry)

        if tags:
            entry_tags = set(entry_metadata.get(config.METADATA_TAGS_KEY, []))
            if not entry_tags.intersection(tags):
                continue

        displayed_entry = f'{click.style(str(index) + ".", fg="green")} {entry}'
        if title := entry_metadata.get(config.METADATA_TITLE_KEY):
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
    if pages or entry_count > config.NON_PAGED_ENTRY_COUNT:
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
        click.echo(f'could not edit metadata in {config.DATA_DIR}, check access')
        return

    upsert_metadata(str(metadata_path), title=title, tags=tags)


def list_entry_tags():

    entries = get_entry_names()

    tags = set()
    for entry in entries:
        entry_tags = set(get_metadata(entry_name=entry).get(config.METADATA_TAGS_KEY, []))
        tags.update(entry_tags)

    if tags:
        tags = list(tags)
        tags.sort()
        for tag in tags:
            click.echo(tag)
    else:
        click.echo('no tags found')
