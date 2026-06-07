def capitalize_words(text):
    if not text:
        return ""
    return " ".join(word.capitalize() for word in text.split())


def pluralize(count, singular, plural=None):
    if count == 1:
        return singular
    return plural or f"{singular}s"


def status_badge(status):
    colors = {
        "Pending": "warning",
        "In Progress": "info",
        "Completed": "success",
        "Overdue": "danger",
    }
    return colors.get(status, "secondary")
