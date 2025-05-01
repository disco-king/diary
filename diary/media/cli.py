from datetime import datetime

import click

from diary import config
from diary.utils.cli import today, get_name, complete_date, complete_filename
from diary.media.entries import (
    add_entry_media, view_entry_media, update_media_meta, delete_media
)


date_option = click.option(
    '-d', '--date',
    type=click.DateTime(formats=['%Y-%m-%d']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
    help='Date of the entry. Today by default.'
)
file_argument = click.argument(
    'file',
    type=click.STRING,
    metavar='FILE',
    shell_complete=complete_filename,
)


@click.command(name='add')
@click.argument(
    'file',
    type=click.Path(exists=True, dir_okay=False),
    metavar='FILE',
)
@date_option
@click.option(
    '-n', '--name',
    type=click.STRING,
    metavar='NAME',
    help='New name for file. Replaces everything before the extentions.'
)
@click.option(
    '-c', '--comment',
    type=click.STRING,
    metavar='COMMENT',
    help='Short description of file contents.',
)
def add_media(file: str, date: datetime, name: str, comment: str):
    """
    Add media to an entry.

    Provide a local file path in the FILE param.
    The file will be added to the entry DATE or today's entry by default.
    The file can be named via NAME and described via COMMENT options - useful for later management.
    """

    entry_name = get_name(date)
    description = comment.strip() if comment else comment
    add_entry_media(entry_name=entry_name, file_path=file, file_name=name, description=description)


@click.command(name='view')
@file_argument
@date_option
def view_media(file: str, date: datetime):
    """View an entry's media file."""

    entry_name = get_name(date)
    view_entry_media(entry_name=entry_name, file=file)


@click.command(name='edit-meta')
@file_argument
@date_option
def edit_meta(file: str, date: datetime):
    """Edit an entry's file metadata."""

    entry_name = get_name(date)
    update_media_meta(entry_name=entry_name, file_name=file)


@click.command(name='delete')
@date_option
@file_argument
@click.confirmation_option(prompt='Delete the file with all its metadata?')
def delete(file: str, date: datetime):
    """Delete an entry's file."""

    entry_name = get_name(date)
    delete_media(entry_name=entry_name, file=file)


@click.group(help=config.MEDIA_HELP)
def media():
    pass


media.add_command(add_media)
media.add_command(view_media)
media.add_command(edit_meta)
media.add_command(delete)
