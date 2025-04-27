from datetime import datetime

import click

from diary import config
from diary.utils.cli import today, get_name
from diary.media.entries import add_entry_media, view_entry_media


@click.command(name='add')
@click.option(
    '-d', '--description',
    type=click.STRING,
    metavar='DESCRIPTION',
    help='Short description of file contents.',
)
@click.option(
    '-n', '--name',
    type=click.STRING,
    metavar='NAME',
    help='New name for file. Replaces everything before the last extention.'
)
@click.argument(
    'file',
    type=click.Path(exists=True, dir_okay=False),
    metavar='FILE',
)
@click.argument(
    'date',
    type=click.DateTime(formats=['%Y-%m-%d', '%d-%m-%Y']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
)
def add_media(date: datetime, name: str, description: str, file: str):
    """
    Add media to an entry.

    Provide a file path in the FILE param.
    The file will be added to the entry DATE or today's entry by default.
    The file can be named via NAME and described via DESCRIPTION options - useful for later management.
    """

    entry_name = get_name(date)
    description = description.strip()
    add_entry_media(entry_name=entry_name, file_path=file, file_name=name, description=description)


@click.command(name='view')
@click.argument(
    'file',
    type=click.STRING,
    metavar='FILE',
)
@click.argument(
    'date',
    type=click.DateTime(formats=['%Y-%m-%d', '%d-%m-%Y']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
)
def view_media(date: datetime, file: str):
    """
    View entry media file.

    Provide a file name FILE present in entry and an entry date DATE if needed.
    """

    entry_name = get_name(date)
    view_entry_media(entry_name=entry_name, file=file)


@click.group()
def media():
    """Manage entry media."""
    pass


media.add_command(add_media)
media.add_command(view_media)
