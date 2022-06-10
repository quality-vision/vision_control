from datetime import datetime


def unix_timestamp(date: datetime) -> int:
    return date.timestamp() * 1000


def maybe_pluralize(count: int, singular: str, plural: str):
    return singular if abs(count) == 1 else plural
