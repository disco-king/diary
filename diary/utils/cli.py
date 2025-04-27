from datetime import datetime


def today() -> datetime:
    return datetime.now()


def get_name(stamp: datetime) -> str:
    return str(stamp.date())
