import os
from pathlib import Path
import shutil

import click

from diary import config
from diary.utils.entries import get_metadata_path, get_entry_media_path, upsert_metadata


def add_entry_media(entry_name: str, file_path: str, file_name: str = None, description: str = None):
    src_path = Path(file_path)
    media_dir_path = get_entry_media_path(entry_name=entry_name)
    dest_name = ''.join([file_name, *src_path.suffixes]) if file_name else src_path.name
    dest_path = os.path.join(media_dir_path, dest_name)

    try:
        shutil.copy(file_path, dest_path)
    except Exception:
        click.echo(f'could not copy file to {media_dir_path}, check access')
        return

    metadata_path = get_metadata_path(entry_name=entry_name)
    if metadata_path is None:
        click.echo(f'could not edit metadata in {config.DATA_DIR}, check access')
        os.remove(dest_path)
        return

    file_metadata = {
        config.MEDIA_META_NAME_KEY: dest_name,
        config.MEDIA_META_DESCRIPTION_KEY: description
    }
    upsert_metadata(
        metadata_path=metadata_path,
        media_entries=[file_metadata]
    )

    click.echo(f'Added {dest_name} to entry {entry_name}')

