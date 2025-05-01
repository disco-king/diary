from datetime import datetime

import click

from diary import config
from diary.utils.cli import today, get_name, complete_date, complete_filename
from diary.media.entries import (
    add_entry_media, view_entry_media, update_media_meta, delete_media
)


date_option = click.option(
    '-d', '--date',
    type=click.DateTime(formats=['%Y-%m-%d', '%d-%m-%Y']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
)
file_argument = click.argument(
    'file',
    type=click.STRING,
    metavar='FILE',
    shell_complete=complete_filename,
)


@click.command(name='add')
@click.option(
    '-n', '--name',
    type=click.STRING,
    metavar='NAME',
    help='New name for file. Replaces everything before the last extention.'
)
@click.option(
    '-c', '--comment',
    type=click.STRING,
    metavar='COMMENT',
    help='Short description of file contents.',
)
@date_option
@click.argument(
    'file',
    type=click.Path(exists=True, dir_okay=False),
    metavar='FILE',
)
def add_media(date: datetime, file: str, name: str, comment: str):
    """
    Add media to an entry.

    Provide a file path in the FILE param.
    The file will be added to the entry DATE or today's entry by default.
    The file can be named via NAME and described via COMMENT options - useful for later management.
    """

    entry_name = get_name(date)
    description = comment.strip() if comment else comment
    add_entry_media(entry_name=entry_name, file_path=file, file_name=name, description=description)


@click.command(name='view')
@date_option
@file_argument
def view_media(date: datetime, file: str):
    """View entry media file."""

    entry_name = get_name(date)
    view_entry_media(entry_name=entry_name, file=file)


@click.command(name='edit-meta')
@date_option
@file_argument
def edit_meta(file: str, date: datetime):
    """Edit file metadata."""

    entry_name = get_name(date)
    update_media_meta(entry_name=entry_name, file_name=file)


@click.command(name='delete')
@date_option
@file_argument
@click.confirmation_option(prompt='Delete the file with all its metadata?')
def delete(file: str, date: datetime):
    """Delete a file."""

    entry_name = get_name(date)
    delete_media(entry_name=entry_name, file=file)


@click.group()
def media():
    """
    Manage entry media.

    All commands in this group take a required argument FILE which determines the managed file.
    It is either a local file path to add to an entry, or a name of a file that belongs to an entry.
    """

    pass


media.add_command(add_media)
media.add_command(view_media)
media.add_command(edit_meta)
media.add_command(delete)
