import os
from pathlib import Path
import json

import click

from diary.config import DATA_SUBDIR, ENTRY_FILE_NAME, METADATA_FILE_NAME


USER_HOME = Path.home()
DATA_DIR = USER_HOME / Path(DATA_SUBDIR)


def check_file_ok(directory: Path, file: Path) -> bool:
    try:
        directory.mkdir(parents=True, exist_ok=True)
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


def list_entries():
    if not os.path.exists(DATA_DIR):
        click.echo('no entries found')
        return

    entries = os.listdir(DATA_DIR)
    entries.sort(reverse=True)
    for index, entry in enumerate(entries):
        displayed_entry = f'{click.style(str(index) + ".", fg="green")} {entry}'
        entry_metadata = get_metadata(entry_name=entry)
        if title := entry_metadata.get('title'):
            displayed_entry += f' - {title}'
        click.echo(displayed_entry)


def add_metadata(entry_name: str, title: str = None, tags: tuple[str] = None):
    if not title and not tags:
        return

    metadata_path = get_metadata_path(entry_name)

    if metadata_path is None:
        click.echo(f'could not edit metadata in {DATA_DIR}, check access')
        return

    data_upd = {}
    if title:
        data_upd['title'] = title
    if tags:
        data_upd['tags'] = tags

    with open(metadata_path, 'r') as f:
        content = f.read()

    metadata = json.loads(content) if content else {}
    if title:
        metadata['title'] = title
    if tags:
        existing_tags: list = metadata.get('tags', [])
        existing_tags.extend(tags)
        metadata['tags'] = list(set(existing_tags))

    with open(metadata_path, 'w') as f:
        f.write(json.dumps(metadata))
