import os

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
    entry_path = get_entry_path(entry_name=entry_name)
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

    metadata_path = get_metadata_path(entry_name=entry_name)

    if metadata_path is None:
        click.echo(f'could not edit metadata in {config.DATA_DIR}, check access')
        return

    upsert_metadata(str(metadata_path), title=title, tags=tags)


def view_entry(entry_name: str, short: bool):
    entry_path = get_entry_path(entry_name=entry_name)

    if entry_path is None:
        click.echo(f'could not find entry {entry_name}')
        return

    metadata = get_metadata(entry_name=entry_name)
    entry_title = metadata.get(config.METADATA_TITLE_KEY)
    entry_tags = metadata.get(config.METADATA_TAGS_KEY, [])
    entry_media = metadata.get(config.METADATA_MEDIA_KEY)
    with open(str(entry_path), 'r') as f:
        entry_text = f.read()

    if not (entry_title or entry_tags or entry_media or entry_text):
        click.echo(f'{entry_name} is empty')
        return

    add_spacing = not short

    click.echo(nl=add_spacing)
    click.echo(f'{click.style("Title:", fg="green")} {entry_title}')
    click.echo(nl=add_spacing)
    click.echo(f'{click.style("Tags:", fg="green")} {", ".join(entry_tags)}')
    if entry_media:
        click.echo(nl=add_spacing)
        click.echo(click.style("Media:", fg="green"))
        for media_file in entry_media:
            click.echo(
                f'{click.style("Name:", fg="green")} {media_file.get(config.MEDIA_META_NAME_KEY)}',
                nl=False
            )
            if file_description := media_file.get(config.MEDIA_META_DESCRIPTION_KEY):
                click.echo(
                    f' {click.style("Description:", fg="green")} {file_description}',
                    nl=False
                )
            click.echo()
    if entry_text:
        click.echo(nl=add_spacing)
        click.echo(click.style("Entry:", fg="green"), nl=add_spacing)
        if short:
            entry_text = entry_text[:config.SHORT_TEXT_SYMBOL_LIMIT] + '...'
        click.echo(entry_text)
    click.echo(nl=add_spacing)


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
