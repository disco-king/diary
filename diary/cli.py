from datetime import date

import click

from diary import config
from diary.entries import (
    edit_entry, list_entries, add_metadata, list_entry_tags, view_entry,
    delete_entry,
)
from diary.media.cli import media
from diary.utils.cli import today, get_name, complete_date
from diary.entries import update_entry_meta
from diary.types import ENTRY_REF


entry_argument = click.argument(
    config.ENTRY_REF_VARNAME,
    type=ENTRY_REF,
    default=today,
    metavar=config.ENTRY_REF_METAVAR,
    envvar=config.DATE_ENV_VAR,
    shell_complete=complete_date,
)


@click.command(name='write', help=config.WRITE_HELP)
@entry_argument
@click.option(
    '-n', '--name',
    type=click.STRING,
    help='Name the entry.',
    metavar=config.NAME_OPTION_METAVAR,
)
@click.option(
    '-t', '--tag',
    type=click.STRING,
    multiple=True,
    help='Add tags to the entry (accepting one or more).',
    metavar=config.TAG_OPTION_METAVAR,
)
def write(entry: date | int, name: str, tag: tuple[str]):
    entry_name = get_name(entry)
    edit_entry(entry_name)
    if name or tag:
        add_metadata(entry_name=entry_name, title=name, tags=tag)


@click.command(name='view')
@entry_argument
@click.option(
    '-s', '--short',
    is_flag=True,
    help='Truncate entry for brevity.',
)
def view(entry: date | int, short: bool):
    """View entry."""

    entry_name = get_name(entry)
    view_entry(entry_name=entry_name, short=short)


@click.command(name='edit-meta')
@entry_argument
def edit_meta(entry: date | int):
    """Edit entry metadata."""

    entry_name = get_name(entry)
    update_entry_meta(entry_name=entry_name)


@click.command(name=config.LIST_CMDNAME)
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
@entry_argument
@click.confirmation_option(prompt='Delete the entry with all its data?')
def delete(entry: date | int):
    """Delete an entry."""

    entry_name = get_name(entry)
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
