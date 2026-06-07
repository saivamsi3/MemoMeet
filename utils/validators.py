import re


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_password(password):
    if len(password) < 8:
        return False
    return True


def sanitize_text(text):
    if not text:
        return ""
    import bleach
    return bleach.clean(text, tags=[], strip=True)
