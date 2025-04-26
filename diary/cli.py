from datetime import datetime

import click

from diary.entries import edit_entry, list_entries, add_metadata


def today() -> datetime:
    return datetime.now()


def get_name(stamp: datetime) -> str:
    return str(stamp.date())


@click.command(name='write')
@click.argument(
    'date',
    type=click.DateTime(formats=['%Y-%m-%d', '%d-%m-%Y']),
    default=today,
    metavar='DATE',
)
@click.option(
    '-n', '--name',
    type=click.STRING,
    help='Add name to the entry',
)
@click.option(
    '-t', '--tags',
    type=click.STRING,
    multiple=True,
    help='Add tags to the entry (accepting one or more)',
)
def write(date: datetime, name: str, tags: tuple[str]):
    """
    Write an entry

    Provide standart format date in DATE to write entry for a specific day.
    Edits today's entry by default.
    """

    entry_name = get_name(date)
    edit_entry(entry_name)
    if name or tags:
        add_metadata(entry_name=entry_name, title=name, tags=tags)


@click.command(name='list')
@click.option(
    '-t', '--tags',
    type=click.STRING,
    multiple=True,
    help='List entries with any of these tags (accepting one or more)',
)
@click.option(
    '-p', '--pages',
    is_flag=True,
    help='Paginate entries',
)
@click.option(
    '-n', '--noedit',
    is_flag=True,
    help='Do not prompt for entry to edit',
)
def list_(tags: tuple[str], pages: bool, noedit: bool):
    """List existing entries"""

    entries_map = list_entries(tags=tags, pages=pages, no_return=noedit)
    if entries_map:
        entry_num = click.prompt('Entry # to edit', default=0)
        if entry_num and (entry_name := entries_map.get(entry_num)):
            edit_entry(entry_name=entry_name)


@click.group()
def cli():
    """A CLI tool for documenting your life"""
    pass


cli.add_command(write)
cli.add_command(list_)
