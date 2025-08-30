from typing import Union
from datetime import datetime, date

from diary import config
from diary.entries import get_entry_names


def today() -> str:
    return str(datetime.now().date())


def get_name(ref: Union[date, int]) -> str:
    if isinstance(ref, date):
        return str(ref)

    entry_number = ref
    entry_names = get_entry_names()
    if entry_number > len(entry_names):
        raise ValueError(f'no entry with number {entry_number}')
    entry_names.sort(reverse=True)
    return entry_names[entry_number - 1]


def complete_date(ctx, param, incomplete):
    return [p.stem for p in config.DATA_DIR.iterdir() if p.stem.startswith(incomplete)]


def complete_filename(ctx, param, incomplete):
    if not (entry := ctx.params.get('entry')):
        return []
    entry_name = get_name(entry)
    media_dir = config.DATA_DIR / entry_name / config.MEDIA_SUBDIR_NAME
    if not media_dir.exists():
        return []

    return [p.name for p in media_dir.iterdir() if p.stem.startswith(incomplete)]
