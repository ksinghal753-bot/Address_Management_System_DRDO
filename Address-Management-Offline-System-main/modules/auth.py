"""
Authentication module: login, bcrypt verification, session management.
"""

import bcrypt
from datetime import datetime
from database.db_manager import db
from utils.constants import MAX_LOGIN_ATTEMPTS


class Session:
    """Holds current logged-in user's details."""
    def __init__(self):
        self.user_id: int | None = None
        self.username: str = ""
        self.role: str = ""          # 'admin' or 'user'
        self.login_time: datetime | None = None
        self.is_authenticated: bool = False

    def set_user(self, user_id: int, username: str, role: str):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.login_time = datetime.now()
        self.is_authenticated = True

    def clear(self):
        self.__init__()

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"


# Global session singleton
current_session = Session()


class AuthResult:
    """Result object returned by login attempt."""
    def __init__(self, success: bool, message: str = "", role: str = ""):
        self.success = success
        self.message = message
        self.role = role


def attempt_login(username: str, password: str, required_role: str) -> AuthResult:
    """
    Validate credentials against DB.
    required_role: 'admin' or 'user'
    Returns AuthResult with success/failure details.
    """
    conn = db.conn
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id, username, password_hash, role, is_locked, failed_attempts "
        "FROM users WHERE username = ? COLLATE NOCASE",
        (username.strip(),)
    )
    row = cur.fetchone()

    if not row:
        try:
            from modules.logger import log_action
            log_action('LOGIN_FAILED', f'Unknown username: {username}', username=username)
        except Exception:
            pass
        return AuthResult(False, "Invalid username or password.\nअमान्य उपयोगकर्ता नाम या पासवर्ड।")

    if row["is_locked"]:
        return AuthResult(False,
            "Account locked after too many failed attempts.\nPlease contact Admin.\n"
            "बहुत अधिक असफल प्रयासों के बाद खाता लॉक हो गया।\nव्यवस्थापक से संपर्क करें।")

    # Check role matches what was selected on splash screen
    if row["role"] != required_role:
        return AuthResult(False,
            f"This account does not have '{required_role}' access.\n"
            f"इस खाते में '{required_role}' की अनुमति नहीं है।")

    # Verify password
    try:
        password_match = bcrypt.checkpw(password.encode(), row["password_hash"].encode())
    except Exception:
        password_match = False

    if not password_match:
        new_attempts = row["failed_attempts"] + 1
        should_lock = 1 if new_attempts >= MAX_LOGIN_ATTEMPTS else 0
        cur.execute(
            "UPDATE users SET failed_attempts=?, is_locked=? WHERE user_id=?",
            (new_attempts, should_lock, row["user_id"])
        )
        conn.commit()

        remaining = MAX_LOGIN_ATTEMPTS - new_attempts
        try:
            from modules.logger import log_action
            log_action('LOGIN_FAILED', f'Wrong password for {username} (attempt {new_attempts})', username=username)
        except Exception:
            pass
        if should_lock:
            return AuthResult(False,
                "Account locked after 3 failed attempts. Contact Admin.\n"
                "3 असफल प्रयासों के बाद खाता लॉक हो गया। व्यवस्थापक से संपर्क करें।")
        return AuthResult(False,
            f"Invalid password. {remaining} attempt(s) remaining.\n"
            f"अमान्य पासवर्ड। {remaining} प्रयास शेष।")

    # Success — reset attempts, update last login
    cur.execute(
        "UPDATE users SET failed_attempts=0, is_locked=0, last_login=? WHERE user_id=?",
        (datetime.now().isoformat(), row["user_id"])
    )
    conn.commit()

    current_session.set_user(row["user_id"], row["username"], row["role"])
    try:
        from modules.logger import log_action
        log_action('LOGIN', f'Successful login as {required_role}', username=row["username"])
    except Exception:
        pass
    return AuthResult(True, "Login successful.", row["role"])


def logout():
    """Clear the current session."""
    try:
        from modules.logger import log_action
        if current_session.is_authenticated:
            log_action('LOGOUT', f'User {current_session.username} logged out',
                       username=current_session.username)
    except Exception:
        pass
    current_session.clear()


def change_password(user_id: int, new_password: str) -> bool:
    """Hash and update password for given user_id."""
    try:
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        db.conn.execute(
            "UPDATE users SET password_hash=?, failed_attempts=0, is_locked=0 WHERE user_id=?",
            (hashed, user_id)
        )
        db.conn.commit()
        return True
    except Exception:
        return False


def unlock_user(user_id: int) -> bool:
    """Unlock a locked user account (admin action)."""
    try:
        db.conn.execute(
            "UPDATE users SET is_locked=0, failed_attempts=0 WHERE user_id=?",
            (user_id,)
        )
        db.conn.commit()
        return True
    except Exception:
        return False


def verify_password(username: str, password: str) -> bool:
    """
    Check a password against the stored hash without modifying session
    or attempt counters. Used for password change verification.
    """
    try:
        row = db.conn.execute(
            "SELECT password_hash FROM users WHERE username=? COLLATE NOCASE",
            (username.strip(),)
        ).fetchone()
        if not row:
            return False
        return bcrypt.checkpw(password.encode(), row['password_hash'].encode())
    except Exception:
        return False
