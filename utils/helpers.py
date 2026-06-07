from datetime import datetime


def truncate(text, length=100):
    if not text:
        return ""
    return text[:length] + "..." if len(text) > length else text


def format_date(date_obj):
    if not date_obj:
        return ""
    return date_obj.strftime("%b %d, %Y")


def format_datetime(dt_obj):
    if not dt_obj:
        return ""
    return dt_obj.strftime("%b %d, %Y at %I:%M %p")
