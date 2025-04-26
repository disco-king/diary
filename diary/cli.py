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
    help='Add tags to the entry - several can be provided',
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
def list_():
    """List existing entries"""
    list_entries()


@click.group()
def cli():
    """A CLI tool for documenting your life"""
    pass


cli.add_command(write)
cli.add_command(list_)
