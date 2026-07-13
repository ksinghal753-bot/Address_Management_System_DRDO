"""
Address CRUD operations for ADRDE Address Management System.
"""

from datetime import datetime
from database.db_manager import db
from modules.auth import current_session

try:
    from modules.logger import log_action, log_error
except Exception:
    def log_action(*a, **kw): pass
    def log_error(*a, **kw): pass


def get_all_addresses(dept_id: int = None) -> list:
    """Fetch all addresses, optionally filtered by department."""
    cur = db.conn.cursor()
    if dept_id:
        cur.execute("""
            SELECT a.*, d.dept_name, d.dept_name_hindi
            FROM addresses a
            JOIN departments d ON a.dept_id = d.dept_id
            WHERE a.dept_id = ?
            ORDER BY a.created_date DESC
        """, (dept_id,))
    else:
        cur.execute("""
            SELECT a.*, d.dept_name, d.dept_name_hindi
            FROM addresses a
            JOIN departments d ON a.dept_id = d.dept_id
            ORDER BY a.created_date DESC
        """)
    return [dict(row) for row in cur.fetchall()]


def get_address_by_id(address_id: int) -> dict | None:
    """Fetch a single address record by ID."""
    cur = db.conn.cursor()
    cur.execute("""
        SELECT a.*, d.dept_name, d.dept_name_hindi
        FROM addresses a
        JOIN departments d ON a.dept_id = d.dept_id
        WHERE a.id = ?
    """, (address_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def search_addresses(
    dept_id: int = None,
    city: str = "",
    state: str = "",
    pin_code: str = "",
    para_no: str = "",
    date_entry: str = "",
    keyword: str = ""
) -> list:
    """Search addresses with multiple optional filters."""
    cur = db.conn.cursor()
    conditions = []
    params = []

    if dept_id:
        conditions.append("a.dept_id = ?")
        params.append(dept_id)
    if city:
        conditions.append("LOWER(a.city) LIKE ?")
        params.append(f"%{city.lower()}%")
    if state:
        conditions.append("LOWER(a.state) LIKE ?")
        params.append(f"%{state.lower()}%")
    if pin_code:
        conditions.append("a.pin_code LIKE ?")
        params.append(f"%{pin_code}%")
    if para_no:
        conditions.append("a.para_no = ?")
        params.append(para_no)
    if date_entry:
        conditions.append("a.date_entry = ?")
        params.append(date_entry)
    if keyword:
        kw = f"%{keyword.lower()}%"
        conditions.append("""(
            LOWER(a.to_field) LIKE ? OR
            LOWER(a.designation) LIKE ? OR
            LOWER(a.office_name) LIKE ? OR
            LOWER(a.addr_line1) LIKE ? OR
            LOWER(a.addr_line2) LIKE ? OR
            LOWER(d.dept_name) LIKE ?
        )""")
        params.extend([kw, kw, kw, kw, kw, kw])

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
    query = f"""
        SELECT a.*, d.dept_name, d.dept_name_hindi
        FROM addresses a
        JOIN departments d ON a.dept_id = d.dept_id
        {where_clause}
        ORDER BY a.created_date DESC
    """
    cur.execute(query, params)
    return [dict(row) for row in cur.fetchall()]


def add_address(data: dict) -> tuple[bool, str]:
    """
    Insert a new address record.
    Returns (success, message).
    """
    if db.is_address_limit_reached():
        return False, "Storage limit of 500 addresses reached!\nअधिकतम 500 पते संग्रहीत किए जा सकते हैं!"

    try:
        now = datetime.now().isoformat()
        db.conn.execute("""
            INSERT INTO addresses
                (dept_id, to_field, designation, designation_hi, office_name,
                 addr_line1, addr_line2, city, state, pin_code,
                 email, fax, contact_no, para_no, date_entry, delivery_type,
                 ref_suffix, created_by, created_date, updated_date)
            VALUES
                (?,?,?,?,?,  ?,?,?,?,?,  ?,?,?,?,?,?,  ?,?,?,?)
        """, (
            data.get("dept_id"),
            data.get("to_field", ""),
            data.get("designation", ""),
            data.get("designation_hi", ""),
            data.get("office_name", ""),
            data.get("addr_line1", ""),
            data.get("addr_line2", ""),
            data.get("city", ""),
            data.get("state", ""),
            data.get("pin_code", ""),
            data.get("email", ""),
            data.get("fax", ""),
            data.get("contact_no", ""),
            data.get("para_no", "PARA 1"),
            data.get("date_entry", datetime.now().strftime("%Y-%m-%d")),
            data.get("delivery_type", "Ordinary / साधारण"),
            data.get("ref_suffix", ""),
            current_session.user_id,
            now,
            now
        ))
        db.conn.commit()
        log_action('ADD_ADDRESS', f'Office: {data.get("office_name","")} | Dept ID: {data.get("dept_id","")}')
        return True, "Address added successfully. / पता सफलतापूर्वक जोड़ा गया।"
    except Exception as e:
        log_error('add_address', e)
        return False, f"Error adding address: {e}"


def update_address(address_id: int, data: dict) -> tuple[bool, str]:
    """Update an existing address record."""
    try:
        now = datetime.now().isoformat()
        db.conn.execute("""
            UPDATE addresses SET
                dept_id=?, to_field=?, designation=?, designation_hi=?, office_name=?,
                addr_line1=?, addr_line2=?, city=?, state=?, pin_code=?,
                email=?, fax=?, contact_no=?, para_no=?, date_entry=?, delivery_type=?,
                ref_suffix=?, updated_date=?
            WHERE id=?
        """, (
            data.get("dept_id"),
            data.get("to_field", ""),
            data.get("designation", ""),
            data.get("designation_hi", ""),
            data.get("office_name", ""),
            data.get("addr_line1", ""),
            data.get("addr_line2", ""),
            data.get("city", ""),
            data.get("state", ""),
            data.get("pin_code", ""),
            data.get("email", ""),
            data.get("fax", ""),
            data.get("contact_no", ""),
            data.get("para_no", "PARA 1"),
            data.get("date_entry", datetime.now().strftime("%Y-%m-%d")),
            data.get("delivery_type", "Ordinary / साधारण"),
            data.get("ref_suffix", ""),
            now,
            address_id
        ))
        db.conn.commit()
        log_action('EDIT_ADDRESS', f'ID: {address_id} | Office: {data.get("office_name","")}')
        return True, "Address updated successfully. / पता सफलतापूर्वक अपडेट किया गया।"
    except Exception as e:
        log_error('update_address', e)
        return False, f"Error updating address: {e}"


def delete_address(address_id: int) -> tuple:
    """Delete an address record by ID."""
    try:
        # Fetch record info for logging before deletion
        row = db.conn.execute(
            "SELECT office_name FROM addresses WHERE id=?", (address_id,)
        ).fetchone()
        office = row['office_name'] if row else 'unknown'

        db.conn.execute("DELETE FROM addresses WHERE id=?", (address_id,))
        db.conn.commit()
        log_action('DELETE_ADDRESS', f'ID: {address_id} | Office: {office}')
        return True, "Address deleted successfully. / पता सफलतापूर्वक हटाया गया।"
    except Exception as e:
        log_error('delete_address', e)
        return False, f"Error deleting address: {e}"


def get_address_stats() -> dict:
    """Return statistics about stored addresses."""
    cur = db.conn.cursor()
    cur.execute("SELECT COUNT(*) FROM addresses")
    total = cur.fetchone()[0]
    cur.execute("""
        SELECT d.dept_name, COUNT(a.id) as cnt
        FROM addresses a
        JOIN departments d ON a.dept_id = d.dept_id
        GROUP BY a.dept_id
        ORDER BY cnt DESC
    """)
    by_dept = {row[0]: row[1] for row in cur.fetchall()}
    return {"total": total, "by_department": by_dept}

import json

def export_addresses_to_json(filepath: str, records: list) -> tuple[bool, str]:
    """Export a list of address records to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=4)
        log_action('EXPORT_ADDRESSES', f'Exported {len(records)} records to {filepath}')
        return True, "Export successful."
    except Exception as e:
        log_error('export_addresses_to_json', e)
        return False, f"Export failed: {e}"

def import_addresses_from_json(filepath: str) -> dict:
    """
    Import address records from a JSON file.
    Checks for duplicates based on matching key fields or primary key.
    Returns a dict with summary stats.
    """
    stats = {
        "total": 0,
        "imported": 0,
        "skipped": 0,
        "failed": 0,
        "error": None
    }
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            records = json.load(f)
            
        if not isinstance(records, list):
            stats["error"] = "Invalid JSON format: Expected a list of records."
            return stats
            
        stats["total"] = len(records)
        cur = db.conn.cursor()
        
        for rec in records:
            try:
                if not isinstance(rec, dict):
                    stats["failed"] += 1
                    continue
                    
                # Check for duplicates
                cur.execute("""
                    SELECT id FROM addresses 
                    WHERE to_field=? AND designation=? AND office_name=? 
                    AND addr_line1=? AND city=? AND pin_code=?
                """, (
                    rec.get("to_field", ""),
                    rec.get("designation", ""),
                    rec.get("office_name", ""),
                    rec.get("addr_line1", ""),
                    rec.get("city", ""),
                    rec.get("pin_code", "")
                ))
                
                if cur.fetchone():
                    stats["skipped"] += 1
                    continue
                
                success, msg = add_address(rec)
                if success:
                    stats["imported"] += 1
                else:
                    stats["failed"] += 1
            except Exception:
                stats["failed"] += 1
                
        log_action('IMPORT_ADDRESSES', f'Imported {stats["imported"]} records from {filepath}')
        
    except json.JSONDecodeError:
        stats["error"] = "Invalid JSON file. Cannot parse contents."
    except Exception as e:
        log_error('import_addresses_from_json', e)
        stats["error"] = f"Import failed: {e}"
        
    return stats

def recover_addresses_from_db(filepath: str) -> dict:
    """
    Recover (merge) address records from a SQLite database backup.
    Checks for duplicates based on matching key fields.
    Returns a dict with summary stats.
    """
    stats = {
        "total": 0,
        "imported": 0,
        "skipped": 0,
        "failed": 0,
        "error": None
    }
    try:
        import sqlite3
        backup_conn = sqlite3.connect(filepath)
        backup_conn.row_factory = sqlite3.Row
        backup_cur = backup_conn.cursor()
        
        try:
            backup_cur.execute("SELECT * FROM addresses")
            records = [dict(row) for row in backup_cur.fetchall()]
        except sqlite3.OperationalError:
            stats["error"] = "Invalid database file: 'addresses' table not found."
            backup_conn.close()
            return stats
            
        backup_conn.close()
            
        stats["total"] = len(records)
        cur = db.conn.cursor()
        
        for rec in records:
            try:
                cur.execute("""
                    SELECT id FROM addresses 
                    WHERE to_field=? AND designation=? AND office_name=? 
                    AND addr_line1=? AND city=? AND pin_code=?
                """, (
                    rec.get("to_field", ""),
                    rec.get("designation", ""),
                    rec.get("office_name", ""),
                    rec.get("addr_line1", ""),
                    rec.get("city", ""),
                    rec.get("pin_code", "")
                ))
                
                if cur.fetchone():
                    stats["skipped"] += 1
                    continue
                
                if "id" in rec:
                    del rec["id"]
                    
                success, msg = add_address(rec)
                if success:
                    stats["imported"] += 1
                else:
                    stats["failed"] += 1
            except Exception:
                stats["failed"] += 1
                
        log_action('RECOVER_MERGE_ADDRESSES', f'Merged {stats["imported"]} records from {filepath}')
        
    except Exception as e:
        log_error('recover_addresses_from_db', e)
        stats["error"] = f"Recovery failed: {e}"
        
    return stats
