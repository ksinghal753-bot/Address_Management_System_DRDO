"""
Input validation utilities for ADRDE Address Management System.
All validators return (is_valid: bool, error_message: str).
"""
import re
from datetime import datetime

# ── Field length limits ────────────────────────────────────────────────────
MAX_TEXT_LEN    = 500
MAX_NAME_LEN    = 150
MAX_EMAIL_LEN   = 100
MAX_PIN_LEN     = 10
MAX_PHONE_LEN   = 20
MAX_USERNAME_LEN = 50

# ── Patterns ───────────────────────────────────────────────────────────────
PIN_RE           = re.compile(r'^\d{6}$')
EMAIL_RE         = re.compile(r'^[\w.+\-]+@[\w\-]+\.[\w.\-]+$')
PHONE_RE         = re.compile(r'^[\d\s\-+()/]{6,20}$')
INVALID_CHARS_RE = re.compile(r"[<>\"';\\]")


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def _clean(val, max_len: int = MAX_TEXT_LEN) -> str:
    """Strip whitespace and enforce max length."""
    v = (val or '').strip()
    return v[:max_len]


def _has_invalid_chars(val: str) -> bool:
    return bool(INVALID_CHARS_RE.search(val))


# ── Address validation ─────────────────────────────────────────────────────
def validate_address(data: dict) -> tuple:
    """
    Validate address form data.
    Returns (valid: bool, error_message: str).
    """
    # Mandatory fields
    required = {
        'dept_id':     'Department / विभाग',
        'designation': 'Designation / पदनाम',
        'office_name': 'Office / Office Name',
        'addr_line1':  'Address Line 1 / पता पंक्ति 1',
        'city':        'City / शहर',
        'state':       'State / राज्य',
        'pin_code':    'PIN Code / पिन कोड',
        'para_no':     'PARA No.',
        'date_entry':  'Date / तारीख',
    }
    for field, label in required.items():
        val = data.get(field)
        if not val or (isinstance(val, str) and not val.strip()):
            return False, f'{label} is required.\n{label} आवश्यक है।'

    # Text field checks
    text_fields = [
        'to_field', 'designation', 'office_name',
        'addr_line1', 'addr_line2', 'city', 'state'
    ]
    for f in text_fields:
        v = _clean(data.get(f, ''), MAX_NAME_LEN)
        if _has_invalid_chars(v):
            return False, f'Field "{f}" contains invalid characters (< > " \' ; \\).'
        if len(v) > MAX_NAME_LEN:
            return False, f'Field "{f}" is too long (max {MAX_NAME_LEN} characters).'

    # PIN code — must be exactly 6 digits
    pin = _clean(data.get('pin_code', ''), MAX_PIN_LEN)
    if pin and not PIN_RE.match(pin):
        return False, 'PIN Code must be exactly 6 digits.\nपिन कोड 6 अंकों का होना चाहिए।'

    # Email (optional)
    email = _clean(data.get('email', ''), MAX_EMAIL_LEN)
    if email and not EMAIL_RE.match(email):
        return False, 'Email address format is invalid.\nईमेल प्रारूप अमान्य है।'

    # Phone (optional)
    phone = _clean(data.get('contact_no', ''), MAX_PHONE_LEN)
    if phone and not PHONE_RE.match(phone):
        return False, 'Contact number contains invalid characters.'

    # Date
    date_str = data.get('date_entry', '')
    try:
        datetime.strptime(str(date_str), '%Y-%m-%d')
    except (ValueError, TypeError):
        return False, 'Date is invalid. Expected format: YYYY-MM-DD.'

    return True, ''


# ── User validation ────────────────────────────────────────────────────────
def validate_user(data: dict, is_new: bool = True) -> tuple:
    """Validate user creation/update data."""
    username = _clean(data.get('username', ''), MAX_USERNAME_LEN)
    if not username:
        return False, 'Username is required.'
    if len(username) < 3:
        return False, 'Username must be at least 3 characters.'
    if _has_invalid_chars(username):
        return False, 'Username contains invalid characters.'
    if re.search(r'\s', username):
        return False, 'Username must not contain spaces.'

    if is_new:
        password = data.get('password', '')
        if not password or len(password) < 6:
            return False, 'Password must be at least 6 characters.'

    return True, ''


# ── Filename sanitisation ──────────────────────────────────────────────────
def sanitize_filename(name: str) -> str:
    """Remove characters unsafe for filenames."""
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', name)


# ── Department validation ──────────────────────────────────────────────────
def validate_department(name: str) -> tuple:
    """Validate a department name."""
    name = _clean(name, 100)
    if not name:
        return False, 'Department name is required.'
    if len(name) < 2:
        return False, 'Department name is too short.'
    if len(name) > 100:
        return False, 'Department name is too long (max 100 chars).'
    return True, ''
