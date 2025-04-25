from datetime import datetime
from pathlib import Path

import click


DATA_DIR = '.data'
DEFAULT_DATE = 'today'


def today() -> datetime:
    return datetime.now()


def get_date(stamp: datetime):

    return str(stamp.date())


def check_file(fname: str):
    subdirectory = Path(DATA_DIR)
    filename = subdirectory / fname

    subdirectory.mkdir(parents=True, exist_ok=True)
    filename.touch(exist_ok=True)

    return str(filename)


def edit_entry(fname: str):
    fname = check_file(fname)
    click.edit(filename=fname)


@click.group()
def cli():
    pass


@click.command()
@click.argument('date', type=click.DateTime(), default=today)
def write(date):
    """Write an entry"""
    fname = get_date(date)
    edit_entry(fname)


cli.add_command(write)


if __name__ == '__main__':
    cli()
