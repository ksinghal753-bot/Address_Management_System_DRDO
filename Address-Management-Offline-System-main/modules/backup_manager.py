"""
Auto-backup manager for ADRDE Address Management System.
Creates timestamped SQLite backups and keeps only the latest N copies.
"""
import os
import sys
import shutil
from datetime import datetime

MAX_BACKUPS = 10


def _get_backup_dir() -> str:
    if getattr(sys, 'frozen', False):
        base = os.environ.get('LOCALAPPDATA', os.path.dirname(sys.executable))
        backup_dir = os.path.join(base, 'ADRDE_Address_Management', 'backups')
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        backup_dir = os.path.join(base, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def create_backup(label: str = 'auto') -> tuple:
    """
    Copy the SQLite database to the backups/ folder with a timestamp.
    Returns (success, path_or_error).
    """
    try:
        from database.db_manager import get_db_path, db
        db_path = get_db_path()
        if not os.path.exists(db_path):
            return False, 'Database file not found.'

        # Flush WAL before copy
        try:
            db.conn.execute('PRAGMA wal_checkpoint(PASSIVE)')
        except Exception:
            pass

        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'backup_{label}_{ts}.db'
        dest = os.path.join(_get_backup_dir(), filename)
        shutil.copy2(db_path, dest)
        _prune_old_backups()

        try:
            from modules.logger import log_action
            log_action('BACKUP_CREATED', f'File: {filename}', username='system')
        except Exception:
            pass

        return True, dest
    except Exception as e:
        try:
            from modules.logger import log_error
            log_error('backup_manager.create_backup', e)
        except Exception:
            pass
        return False, str(e)


def _prune_old_backups():
    """Remove oldest backups keeping only MAX_BACKUPS."""
    try:
        backup_dir = _get_backup_dir()
        files = sorted(
            [f for f in os.listdir(backup_dir) if f.endswith('.db')],
            key=lambda f: os.path.getmtime(os.path.join(backup_dir, f))
        )
        while len(files) > MAX_BACKUPS:
            os.remove(os.path.join(backup_dir, files.pop(0)))
    except Exception:
        pass


def startup_backup():
    """
    Called once at application startup.
    Creates a backup only if one hasn't been made today.
    """
    try:
        backup_dir = _get_backup_dir()
        today = datetime.now().strftime('%Y%m%d')
        existing = [
            f for f in os.listdir(backup_dir)
            if f.startswith(f'backup_auto_{today}') and f.endswith('.db')
        ]
        if not existing:
            create_backup('auto')
    except Exception:
        pass


def list_backups() -> list:
    """Return list of backup info dicts sorted newest first."""
    try:
        backup_dir = _get_backup_dir()
        result = []
        for f in sorted(os.listdir(backup_dir), reverse=True):
            if f.endswith('.db'):
                full = os.path.join(backup_dir, f)
                result.append({
                    'filename': f,
                    'size': os.path.getsize(full),
                    'modified': datetime.fromtimestamp(
                        os.path.getmtime(full)
                    ).strftime('%Y-%m-%d %H:%M')
                })
        return result
    except Exception:
        return []
