"""
Input validators for ADRDE Address Management System.
"""
import re


def validate_pin_code(pin: str) -> bool:
    """Indian PIN code: exactly 6 digits."""
    return bool(re.match(r'^\d{6}$', pin.strip()))


def validate_email(email: str) -> bool:
    """Basic email format validation. Empty is also allowed (optional field)."""
    if not email.strip():
        return True
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email.strip()))


def validate_fax(fax: str) -> bool:
    """FAX number: optional, digits/spaces/hyphens allowed."""
    if not fax.strip():
        return True
    return bool(re.match(r'^[\d\s\-+()]{5,20}$', fax.strip()))


def validate_contact(contact: str) -> bool:
    """Contact number: optional, digits/spaces/hyphens allowed."""
    if not contact.strip():
        return True
    return bool(re.match(r'^[\d\s\-+()]{7,20}$', contact.strip()))


def validate_required(value: str) -> bool:
    """Check non-empty string."""
    return bool(value and value.strip())


def validate_username(username: str) -> bool:
    """Username: 3-50 alphanumeric/underscore characters."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,50}$', username.strip()))


def validate_password(password: str) -> tuple[bool, str]:
    """
    Password rules:
      - At least 8 characters
      - At least one uppercase letter
      - At least one lowercase letter
      - At least one digit
    Returns (is_valid, message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters. / पासवर्ड कम से कम 8 अक्षर का होना चाहिए।"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter. / पासवर्ड में कम से कम एक बड़ा अक्षर होना चाहिए।"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter. / पासवर्ड में कम से कम एक छोटा अक्षर होना चाहिए।"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit. / पासवर्ड में कम से कम एक अंक होना चाहिए।"
    return True, ""
