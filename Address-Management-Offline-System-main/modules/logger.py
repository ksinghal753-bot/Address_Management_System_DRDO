"""
Offline Activity Logger for ADRDE Address Management System.
Logs all user actions to a local SQLite table and rotating log file.
"""
import os
import sys
import logging
import logging.handlers
from datetime import datetime


def _get_log_dir() -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


# ── File logger (rotating, 1 MB × 5 files) ──────────────────────────────────
_file_logger = logging.getLogger('adrde.activity')
_file_logger.setLevel(logging.INFO)

try:
    _log_path = os.path.join(_get_log_dir(), 'activity.log')
    _handler = logging.handlers.RotatingFileHandler(
        _log_path, maxBytes=1_048_576, backupCount=5, encoding='utf-8'
    )
    _handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    _file_logger.addHandler(_handler)
except Exception:
    pass  # Non-critical – never crash on logging setup


def _ensure_log_table():
    """Create activity_log table if not present."""
    try:
        from database.db_manager import db
        db.conn.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                log_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    NOT NULL DEFAULT 'system',
                action      TEXT    NOT NULL,
                details     TEXT,
                log_date    TEXT    NOT NULL,
                log_time    TEXT    NOT NULL
            )
        """)
        db.conn.commit()
    except Exception:
        pass


def log_action(action: str, details: str = '', username: str = None):
    """
    Record an activity entry.
    action  : SHORT_KEYWORD  e.g. 'LOGIN', 'ADD_ADDRESS', 'DELETE_ADDRESS'
    details : Human-readable description
    username: Override username (auto-detected from session if None)
    """
    try:
        from modules.auth import current_session
        uname = username or (
            current_session.username if current_session.is_authenticated else 'system'
        )
    except Exception:
        uname = username or 'system'

    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')

    # Write to rotating file
    try:
        _file_logger.info('%s | %s | %s', uname, action, details)
    except Exception:
        pass

    # Write to DB
    try:
        from database.db_manager import db
        _ensure_log_table()
        db.conn.execute(
            "INSERT INTO activity_log (username, action, details, log_date, log_time)"
            " VALUES (?,?,?,?,?)",
            (uname, action, details, date_str, time_str)
        )
        db.conn.commit()
    except Exception:
        pass


def log_error(context: str, error: Exception):
    """Log a technical error without crashing."""
    log_action('ERROR', f'{context}: {error}')
    try:
        _file_logger.error('%s: %s', context, error, exc_info=False)
    except Exception:
        pass


def get_recent_logs(limit: int = 200) -> list:
    """Return recent log entries as list of dicts."""
    try:
        from database.db_manager import db
        _ensure_log_table()
        cur = db.conn.execute(
            "SELECT * FROM activity_log ORDER BY log_id DESC LIMIT ?", (limit,)
        )
        return [dict(r) for r in cur.fetchall()]
    except Exception:
        return []
