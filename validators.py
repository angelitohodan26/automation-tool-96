import re
from functools import lru_cache

# Pre-compiled regex patterns for performance
_EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
_UUID_REGEX = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[4][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', re.I)

@lru_cache(maxsize=128)
def validate_email(email: str) -> bool:
    """Validates email format using cached regex."""
    if not email or len(email) > 254:
        return False
    return bool(_EMAIL_REGEX.match(email))

@lru_cache(maxsize=64)
def validate_uuid(uuid_str: str) -> bool:
    """Validates UUID format using cached regex."""
    return bool(_UUID_REGEX.match(uuid_str))

def batch_validate_emails(emails: list) -> list:
    """Efficiently process bulk email validation."""
    return [validate_email(e) for e in emails]

def sanitize_input(value: str) -> str:
    """Basic string sanitization to prevent injection."""
    if not isinstance(value, str):
        return ""
    return value.strip().replace('<', '').replace('>', '')