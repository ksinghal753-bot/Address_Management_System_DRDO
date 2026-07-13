"""
Database manager for ADRDE Address Management System.
Handles SQLite connection, schema creation, and initial seeding.
"""

import sqlite3
import os
import sys
import bcrypt
from datetime import datetime
from utils.constants import DEFAULT_DEPARTMENTS, MAX_ADDRESSES


def get_db_path() -> str:
    """Return path to the SQLite database file (next to executable or script)."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller bundle
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        db_dir = os.path.join(os.environ.get('LOCALAPPDATA', base), 'ADRDE_Address_Management', 'data')
    else:
        db_dir = os.path.join(base, '..', 'data')
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'address_management.db')


class DatabaseManager:
    """Singleton-style DB manager."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = None
            cls._instance._initialized = False
        return cls._instance

    def connect(self):
        """Open connection and initialise schema."""
        if self._conn is None:
            db_path = get_db_path()
            self._conn = sqlite3.connect(db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        if not self._initialized:
            self._create_schema()
            self._seed_data()
            self._initialized = True
        return self._conn

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self.connect()
        return self._conn

    def _create_schema(self):
        """Create all tables if they don't exist."""
        cur = self.conn.cursor()

        cur.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username        TEXT    NOT NULL UNIQUE COLLATE NOCASE,
                password_hash   TEXT    NOT NULL,
                role            TEXT    NOT NULL CHECK(role IN ('admin','user')),
                is_locked       INTEGER NOT NULL DEFAULT 0,
                failed_attempts INTEGER NOT NULL DEFAULT 0,
                created_date    TEXT    DEFAULT CURRENT_TIMESTAMP,
                last_login      TEXT,
                employee_id     TEXT
            );
        """)
        
        # In case the table already existed without these columns
        for col in ["employee_id", "first_name", "last_name"]:
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
            except sqlite3.OperationalError:
                pass

        cur.executescript("""
            CREATE TABLE IF NOT EXISTS departments (
                dept_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                dept_name       TEXT    NOT NULL UNIQUE,
                dept_name_hindi TEXT    NOT NULL,
                created_date    TEXT    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS addresses (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                dept_id         INTEGER NOT NULL REFERENCES departments(dept_id),
                to_field        TEXT    NOT NULL,
                designation     TEXT    NOT NULL,
                designation_hi  TEXT,
                office_name     TEXT    NOT NULL,
                addr_line1      TEXT    NOT NULL,
                addr_line2      TEXT,
                city            TEXT    NOT NULL,
                state           TEXT    NOT NULL,
                pin_code        TEXT    NOT NULL,
                email           TEXT,
                fax             TEXT,
                contact_no      TEXT,
                para_no         TEXT    NOT NULL,
                date_entry      TEXT    NOT NULL,
                delivery_type   TEXT    NOT NULL DEFAULT 'Ordinary / साधारण',
                created_by      INTEGER REFERENCES users(user_id),
                created_date    TEXT    DEFAULT CURRENT_TIMESTAMP,
                updated_date    TEXT    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_addr_dept   ON addresses(dept_id);
            CREATE INDEX IF NOT EXISTS idx_addr_para   ON addresses(para_no);
            CREATE INDEX IF NOT EXISTS idx_addr_date   ON addresses(date_entry);
            CREATE INDEX IF NOT EXISTS idx_addr_city   ON addresses(city);
            CREATE INDEX IF NOT EXISTS idx_addr_pin    ON addresses(pin_code);
            CREATE INDEX IF NOT EXISTS idx_addr_to     ON addresses(to_field);
            CREATE INDEX IF NOT EXISTS idx_addr_office ON addresses(office_name);
            CREATE INDEX IF NOT EXISTS idx_users_uname ON users(username);
            CREATE INDEX IF NOT EXISTS idx_dept_name   ON departments(dept_name);
        """)

        # Add ref_suffix to existing databases
        try:
            cur.execute("ALTER TABLE addresses ADD COLUMN ref_suffix TEXT")
        except sqlite3.OperationalError:
            pass

        self.conn.commit()

    def _seed_data(self):
        """Seed default admin user and departments on first run."""
        cur = self.conn.cursor()

        # Default admin — only if no users exist
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            hashed = bcrypt.hashpw(b"Admin@1234", bcrypt.gensalt()).decode()
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ("admin", hashed, "admin")
            )

        # Default departments — only if none exist
        cur.execute("SELECT COUNT(*) FROM departments")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO departments (dept_name, dept_name_hindi) VALUES (?, ?)",
                DEFAULT_DEPARTMENTS
            )

        self.conn.commit()

    # ── Address record count ───────────────────────────────────────────────────
    def get_address_count(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM addresses")
        return cur.fetchone()[0]

    def is_address_limit_reached(self) -> bool:
        return self.get_address_count() >= MAX_ADDRESSES

    def check_integrity(self) -> bool:
        """Run SQLite integrity_check PRAGMA. Returns True if database is OK."""
        try:
            result = self.conn.execute('PRAGMA integrity_check').fetchone()
            return result[0] == 'ok'
        except Exception:
            return False

    def checkpoint(self):
        """Flush WAL journal to the main database file."""
        try:
            self.conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
        except Exception:
            pass

    def close(self):
        if self._conn:
            self.checkpoint()
            self._conn.close()
            self._conn = None
            DatabaseManager._instance = None


# Module-level singleton access
db = DatabaseManager()
