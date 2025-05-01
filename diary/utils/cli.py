from datetime import datetime

from diary import config


def today() -> datetime:
    return datetime.now()


def get_name(stamp: datetime) -> str:
    return str(stamp.date())


def complete_date(ctx, param, incomplete):
    return [p.stem for p in config.DATA_DIR.iterdir() if p.stem.startswith(incomplete)]


def complete_filename(ctx, param, incomplete):
    if not (date := ctx.params.get('date')):
        return []
    entry_name = get_name(date)
    media_dir = config.DATA_DIR / entry_name / config.MEDIA_SUBDIR_NAME
    if not media_dir.exists():
        return []

    return [p.name for p in media_dir.iterdir() if p.stem.startswith(incomplete)]
