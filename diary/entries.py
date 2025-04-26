import os
from pathlib import Path
import json

import click

from diary.config import (
    DATA_SUBDIR, ENTRY_FILE_NAME, METADATA_FILE_NAME,
    METADATA_TITLE_KEY, METADATA_TAGS_KEY
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


def list_entries(tags: tuple[str]):
    if not os.path.exists(DATA_DIR):
        click.echo('no entries exist')
        return

    entries = os.listdir(DATA_DIR)
    entries.sort(reverse=True)

    tags = set(tags)
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
        click.echo(displayed_entry)
        index += 1


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
