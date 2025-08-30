from datetime import date

import click

from diary import config
from diary.utils.cli import today, get_name, complete_date, complete_filename
from diary.media.entries import (
    add_entry_media, view_entry_media, update_media_meta, delete_media
)
from diary.types import ENTRY_REF


entry_option = click.option(
    '-e', '--entry',
    type=ENTRY_REF,
    default=today,
    metavar=config.ENTRY_REF_METAVAR,
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
    help="Choose the entry. Today's by default."
)
file_argument = click.argument(
    config.FILE_VARNAME,
    type=click.STRING,
    metavar=config.FILE_METAVAR,
    shell_complete=complete_filename,
)


@click.command(name='add', help=config.ADD_MEDIA_HELP)
@click.argument(
    config.FILE_VARNAME,
    type=click.Path(exists=True, dir_okay=False),
    metavar=config.FILE_METAVAR,
)
@entry_option
@click.option(
    '-n', '--name',
    type=click.STRING,
    metavar=config.FILENAME_METAVAR,
    help='New name for file. Replaces everything before the extentions.'
)
@click.option(
    '-c', '--comment',
    type=click.STRING,
    metavar=config.COMMENT_METAVAR,
    help='Short description of file contents.',
)
def add_media(file: str, entry: date | int, name: str, comment: str):
    entry_name = get_name(entry)
    description = comment.strip() if comment else comment
    add_entry_media(entry_name=entry_name, file_path=file, file_name=name, description=description)


@click.command(name='view')
@file_argument
@entry_option
def view_media(file: str, entry: date | int):
    """View an entry's media file."""

    entry_name = get_name(entry)
    view_entry_media(entry_name=entry_name, file=file)


@click.command(name='edit-meta')
@file_argument
@entry_option
def edit_meta(file: str, entry: date | int):
    """Edit an entry's file metadata."""

    entry_name = get_name(entry)
    update_media_meta(entry_name=entry_name, file_name=file)


@click.command(name='delete')
@entry_option
@file_argument
@click.confirmation_option(prompt='Delete the file with all its metadata?')
def delete(file: str, entry: date | int):
    """Delete an entry's file."""

    entry_name = get_name(entry)
    delete_media(entry_name=entry_name, file=file)


@click.group(help=config.MEDIA_HELP)
def media():
    pass


media.add_command(add_media)
media.add_command(view_media)
media.add_command(edit_meta)
media.add_command(delete)
