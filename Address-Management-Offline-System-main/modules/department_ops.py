"""
Department and User management operations.
"""

import bcrypt
from database.db_manager import db


# ── Department Operations ──────────────────────────────────────────────────────

def get_all_departments() -> list:
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM departments ORDER BY dept_name")
    return [dict(row) for row in cur.fetchall()]


def get_department_by_id(dept_id: int) -> dict | None:
    cur = db.conn.cursor()
    cur.execute("SELECT * FROM departments WHERE dept_id=?", (dept_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def add_department(dept_name: str, dept_name_hindi: str) -> tuple[bool, str]:
    try:
        db.conn.execute(
            "INSERT INTO departments (dept_name, dept_name_hindi) VALUES (?,?)",
            (dept_name.strip(), dept_name_hindi.strip())
        )
        db.conn.commit()
        return True, "Department added. / विभाग जोड़ा गया।"
    except Exception as e:
        if "UNIQUE" in str(e):
            return False, "Department name already exists. / विभाग का नाम पहले से मौजूद है।"
        return False, str(e)


def update_department(dept_id: int, dept_name: str, dept_name_hindi: str) -> tuple[bool, str]:
    try:
        db.conn.execute(
            "UPDATE departments SET dept_name=?, dept_name_hindi=? WHERE dept_id=?",
            (dept_name.strip(), dept_name_hindi.strip(), dept_id)
        )
        db.conn.commit()
        return True, "Department updated. / विभाग अपडेट किया गया।"
    except Exception as e:
        return False, str(e)


def delete_department(dept_id: int) -> tuple[bool, str]:
    cur = db.conn.cursor()
    cur.execute("SELECT COUNT(*) FROM addresses WHERE dept_id=?", (dept_id,))
    count = cur.fetchone()[0]
    if count > 0:
        return False, (
            f"Cannot delete: {count} address(es) linked to this department.\n"
            f"इस विभाग से {count} पता(ते) जुड़े हैं। हटाया नहीं जा सकता।"
        )
    try:
        db.conn.execute("DELETE FROM departments WHERE dept_id=?", (dept_id,))
        db.conn.commit()
        return True, "Department deleted. / विभाग हटाया गया।"
    except Exception as e:
        return False, str(e)


# ── User Operations ────────────────────────────────────────────────────────────

def get_all_users() -> list:
    cur = db.conn.cursor()
    cur.execute(
        "SELECT user_id, username, role, is_locked, failed_attempts, created_date, last_login "
        "FROM users ORDER BY username"
    )
    return [dict(row) for row in cur.fetchall()]


def get_user_by_id(user_id: int) -> dict | None:
    cur = db.conn.cursor()
    cur.execute(
        "SELECT user_id, username, role, is_locked, failed_attempts, created_date, last_login "
        "FROM users WHERE user_id=?",
        (user_id,)
    )
    row = cur.fetchone()
    return dict(row) if row else None


def add_user(username: str, password: str, role: str, employee_id: str = None, first_name: str = "", last_name: str = "") -> tuple[bool, str]:
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        db.conn.execute(
            "INSERT INTO users (username, password_hash, role, employee_id, first_name, last_name) VALUES (?,?,?,?,?,?)",
            (username.strip(), hashed, role, employee_id, first_name.strip(), last_name.strip())
        )
        db.conn.commit()
        return True, "User added. / उपयोगकर्ता जोड़ा गया।"
    except Exception as e:
        if "UNIQUE" in str(e):
            return False, "Username already exists. / उपयोगकर्ता नाम पहले से मौजूद है।"
        return False, str(e)


def update_user(user_id: int, username: str, role: str,
                new_password: str = "") -> tuple[bool, str]:
    try:
        if new_password:
            hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            db.conn.execute(
                "UPDATE users SET username=?, role=?, password_hash=? WHERE user_id=?",
                (username.strip(), role, hashed, user_id)
            )
        else:
            db.conn.execute(
                "UPDATE users SET username=?, role=? WHERE user_id=?",
                (username.strip(), role, user_id)
            )
        db.conn.commit()
        return True, "User updated. / उपयोगकर्ता अपडेट किया गया।"
    except Exception as e:
        if "UNIQUE" in str(e):
            return False, "Username already exists. / उपयोगकर्ता नाम पहले से मौजूद है।"
        return False, str(e)


def delete_user(user_id: int) -> tuple[bool, str]:
    try:
        db.conn.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        db.conn.commit()
        return True, "User deleted. / उपयोगकर्ता हटाया गया।"
    except Exception as e:
        return False, str(e)


def unlock_user(user_id: int) -> tuple[bool, str]:
    try:
        db.conn.execute(
            "UPDATE users SET is_locked=0, failed_attempts=0 WHERE user_id=?",
            (user_id,)
        )
        db.conn.commit()
        return True, "User unlocked. / उपयोगकर्ता अनलॉक किया गया।"
    except Exception as e:
        return False, str(e)


def reset_password(user_id: int, new_password: str) -> tuple[bool, str]:
    try:
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        db.conn.execute(
            "UPDATE users SET password_hash=?, is_locked=0, failed_attempts=0 WHERE user_id=?",
            (hashed, user_id)
        )
        db.conn.commit()
        return True, "Password reset successful. / पासवर्ड रीसेट सफल।"
    except Exception as e:
        return False, str(e)
