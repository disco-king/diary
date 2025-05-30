import os
from pathlib import Path
import shutil

import click

from diary import config
from diary.utils.entries import (
    get_metadata_path, get_entry_media_path, upsert_metadata,
    get_metadata, get_entry_path, remove_file_metadata
)
from diary.utils.editing import (
    prompt_metadata_update, UserInputError, EmptyMetadataError, EditAbort
)
from diary.utils.models import Entry, MediaEntry


def add_entry_media(entry_name: str, file_path: str, file_name: str = None, description: str = None):
    media_path = get_entry_media_path(entry_name=entry_name, create=True)
    if media_path is None:
        click.echo(f'could not add files to {config.DATA_DIR}, check access')
        return

    media_dir_path = str(media_path)
    src_path = Path(file_path)
    dest_name = ''.join([file_name, *src_path.suffixes]) if file_name else src_path.name
    dest_path = os.path.join(media_dir_path, dest_name)

    try:
        shutil.copy(file_path, dest_path)
    except Exception:
        click.echo(f'could not copy file to {media_dir_path}, check access')
        return

    metadata_path = get_metadata_path(entry_name=entry_name, create=True)
    if metadata_path is None:
        click.echo(f'could not edit metadata in {config.DATA_DIR}, check access')
        os.remove(dest_path)
        return

    metadata = Entry(media=[MediaEntry(file_name=dest_name, description=description)])
    upsert_metadata(
        metadata_path=str(metadata_path),
        entry_data=metadata
    )

    click.echo(f'Added {dest_name} to entry {entry_name}')


def view_entry_media(entry_name: str, file: str):
    metadata = get_metadata(entry_name=entry_name)
    media_dir_path = get_entry_media_path(entry_name=entry_name)

    if not metadata or not media_dir_path or not (files := [d.name for d in media_dir_path.iterdir()]):
        click.echo(f'no media data found for entry {entry_name}')
        return

    file_meta = None
    for file_meta in metadata.media:
        if file_meta.file_name == file:
            break

    if not file_meta or file not in files:
        click.echo(f'file {file} not found for entry {entry_name}')
        return

    click.echo(f'{click.style("Name:", fg="green")} {file}')
    if file_meta.description:
        click.echo(f'{click.style("Description:", fg="green")} {file_meta.description}')
    click.launch(str(media_dir_path / file))


def update_media_meta(entry_name: str, file_name: str):

    if not get_entry_path(entry_name=entry_name):
        click.echo('entry not found, cannot edit metadata')
        return

    metadata_path = get_metadata_path(entry_name=entry_name)

    if metadata_path is None:
        click.echo(f'could not edit metadata in {config.DATA_DIR}, check access')
        return

    try:
        prompt_metadata_update(metadata_path=str(metadata_path), file_name=file_name)
    except (UserInputError, EmptyMetadataError) as e:
        click.echo(f'error: {e}')
    except EditAbort as e:
        click.echo(e)
    else:
        click.echo(f'successfully updated metada for entry {entry_name}')


def delete_media(entry_name: str, file: str):
    metadata_path = get_metadata_path(entry_name=entry_name)
    media_dir_path = get_entry_media_path(entry_name=entry_name)

    if not metadata_path or not media_dir_path or not (files := [d.name for d in media_dir_path.iterdir()]):
        click.echo(f'no media data found for entry {entry_name}')
        return

    media_path = media_dir_path / file

    if not media_path.exists():
        click.echo(f'file {file} not found for entry {entry_name}')
        return

    media_path.unlink()
    remove_file_metadata(metadata_path=str(metadata_path), file_name=file)

    click.echo(f'successfully deleted file {file} for entry {entry_name}')
