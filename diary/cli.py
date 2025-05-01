from datetime import datetime

import click

from diary import config
from diary.entries import (
    edit_entry, list_entries, add_metadata, list_entry_tags, view_entry,
    delete_entry,
)
from diary.media.cli import media
from diary.utils.cli import today, get_name, complete_date
from diary.entries import update_entry_meta


date_argument = click.argument(
    'date',
    type=click.DateTime(formats=['%Y-%m-%d']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
)


@click.command(name='write')
@date_argument
@click.option(
    '-n', '--name',
    type=click.STRING,
    help='Name the entry.',
    metavar='NAME',
)
@click.option(
    '-t', '--tag',
    type=click.STRING,
    multiple=True,
    help='Add tags to the entry (accepting one or more).',
    metavar='TAG',
)
def write(date: datetime, name: str, tag: tuple[str]):
    """
    Write an entry.

    Write a new entry or edit an existing one.
    The DATE parameter determines which entry to write,
    and additional metadata can be added via NAME and TAG options.
    """

    entry_name = get_name(date)
    edit_entry(entry_name)
    if name or tag:
        add_metadata(entry_name=entry_name, title=name, tags=tag)


@click.command(name='view')
@date_argument
@click.option(
    '-s', '--short',
    is_flag=True,
    help='Truncate entry for brevity.',
)
def view(date: datetime, short: bool):
    """View entry."""

    entry_name = get_name(date)
    view_entry(entry_name=entry_name, short=short)


@click.command(name='edit-meta')
@date_argument
def edit_meta(date: datetime):
    """Edit entry metadata."""

    entry_name = get_name(date)
    update_entry_meta(entry_name=entry_name)


@click.command(name='list')
@click.option(
    '-t', '--tag',
    type=click.STRING,
    multiple=True,
    help='List entries with any of these tags (accepting one or more).',
    metavar='TAG',
)
@click.option(
    '-p', '--pages',
    is_flag=True,
    help='Paginate entries.',
)
@click.option(
    '-e', '--edit',
    is_flag=True,
    help='Choose an entry to edit.',
)
def list_(tag: tuple[str], pages: bool, edit: bool):
    """List existing entries."""

    entries_map = list_entries(tags=tag, pages=pages, no_return=(not edit))
    if entries_map:
        entry_num = click.prompt('Entry # to edit', default=0)
        if entry_num and (entry_name := entries_map.get(entry_num)):
            edit_entry(entry_name=entry_name)


@click.command(name='delete')
@date_argument
@click.confirmation_option(prompt='Delete the entry with all its data?')
def delete(date: datetime):
    """Delete an entry."""

    entry_name = get_name(date)
    delete_entry(entry_name=entry_name)


@click.command(name='tags')
def list_tags():
    """List existing tags."""

    list_entry_tags()


@click.group(help=config.ROOT_HELP)
def cli():
    pass


cli.add_command(write)
cli.add_command(list_)
cli.add_command(list_tags)
cli.add_command(view)
cli.add_command(edit_meta)
cli.add_command(delete)
cli.add_command(media)
