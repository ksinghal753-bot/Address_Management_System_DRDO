"""
Single-instance guard for ADRDE Address Management System.
Uses a PID lock file to prevent multiple simultaneous instances.
"""
import os
import sys


def _lock_path() -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, '.app.lock')


def _is_process_running(pid: int) -> bool:
    """Check if a process with the given PID is alive (Windows-compatible)."""
    try:
        import ctypes
        PROCESS_QUERY_INFORMATION = 0x0400
        handle = ctypes.windll.kernel32.OpenProcess(
            PROCESS_QUERY_INFORMATION, False, pid
        )
        if handle:
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        return False
    except Exception:
        # Fallback: try os.kill (works on POSIX)
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False


def acquire_lock() -> bool:
    """
    Try to create a lock file with the current PID.
    Returns True if this is the only running instance.
    Returns False if another instance is detected.
    """
    lock = _lock_path()
    try:
        if os.path.exists(lock):
            try:
                with open(lock, 'r') as f:
                    old_pid = int(f.read().strip())
                if old_pid != os.getpid() and _is_process_running(old_pid):
                    return False  # Another live instance exists
            except (ValueError, IOError):
                pass  # Corrupt lock file – treat as stale

        with open(lock, 'w') as f:
            f.write(str(os.getpid()))
        return True
    except Exception:
        # If we cannot determine, allow the app to start
        return True


def release_lock():
    """Remove the lock file on clean exit."""
    try:
        lock = _lock_path()
        if os.path.exists(lock):
            # Only remove if it's our PID
            try:
                with open(lock, 'r') as f:
                    stored_pid = int(f.read().strip())
                if stored_pid == os.getpid():
                    os.remove(lock)
            except Exception:
                os.remove(lock)
    except Exception:
        pass
