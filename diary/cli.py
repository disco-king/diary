from datetime import datetime

import click

from diary import config
from diary.entries import (
    edit_entry, list_entries, add_metadata, list_entry_tags, view_entry,
    delete_entry,
)
from diary.media.cli import media
from diary.utils.cli import today, get_name
from diary.entries import update_entry_meta


def complete_date(ctx, param, incomplete):
    return [p.stem for p in config.DATA_DIR.iterdir() if p.stem.startswith(incomplete)]


@click.command(name='write')
@click.argument(
    'date',
    type=click.DateTime(formats=['%Y-%m-%d', '%d-%m-%Y']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
)
@click.option(
    '-n', '--name',
    type=click.STRING,
    help='Add name to the entry.',
)
@click.option(
    '-t', '--tags',
    type=click.STRING,
    multiple=True,
    help='Add tags to the entry (accepting one or more).',
)
def write(date: datetime, name: str, tags: tuple[str]):
    """Write an entry."""

    entry_name = get_name(date)
    edit_entry(entry_name)
    if name or tags:
        add_metadata(entry_name=entry_name, title=name, tags=tags)


@click.command(name='view')
@click.argument(
    'date',
    type=click.DateTime(formats=['%Y-%m-%d', '%d-%m-%Y']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
)
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
@click.argument(
    'date',
    type=click.DateTime(formats=['%Y-%m-%d', '%d-%m-%Y']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
)
def edit_meta(date: datetime):
    """Edit entry metadata."""

    entry_name = get_name(date)
    update_entry_meta(entry_name=entry_name)


@click.command(name='list')
@click.option(
    '-t', '--tags',
    type=click.STRING,
    multiple=True,
    help='List entries with any of these tags (accepting one or more).',
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
def list_(tags: tuple[str], pages: bool, edit: bool):
    """List existing entries."""

    entries_map = list_entries(tags=tags, pages=pages, no_return=(not edit))
    if entries_map:
        entry_num = click.prompt('Entry # to edit', default=0)
        if entry_num and (entry_name := entries_map.get(entry_num)):
            edit_entry(entry_name=entry_name)


@click.command(name='delete')
@click.argument(
    'date',
    type=click.DateTime(formats=['%Y-%m-%d', '%d-%m-%Y']),
    default=today,
    metavar='DATE',
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
)
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
