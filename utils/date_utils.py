from datetime import datetime, timezone, timedelta


def now():
    return datetime.now(timezone.utc)


def days_between(d1, d2):
    return abs((d2 - d1).days)


def is_overdue(deadline):
    if not deadline:
        return False
    return deadline < now()


def days_until(date_obj):
    if not date_obj:
        return None
    return (date_obj - now()).days
