"""
SQLite Database Management
Simple database for storing users, calls, reports, and financial data
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

# Database path - use environment variable if set, otherwise default
DB_PATH_ENV = os.getenv("DATABASE_PATH")
if DB_PATH_ENV:
    DB_PATH = Path(DB_PATH_ENV)
    # Ensure parent directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
else:
    DB_PATH = Path(__file__).parent / "financebot.db"
    # Ensure directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    """Get database connection"""
    # Ensure directory exists and is writable
    try:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        # Try to create parent directory with write permissions
        import stat
        os.chmod(DB_PATH.parent, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except Exception:
        pass  # Continue even if chmod fails
    
    return sqlite3.connect(str(DB_PATH), timeout=10.0)


def init_db():
    """Initialize database with tables"""
    conn = get_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone_number TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            created_at TEXT,
            last_login TEXT
        )
    ''')
    
    # Calls table
    c.execute('''
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            call_id TEXT UNIQUE,
            tracking_id TEXT UNIQUE,
            contact_id TEXT,
            campaign_id TEXT,
            status TEXT DEFAULT 'initiated',
            created_at TEXT,
            completed_at TEXT,
            FOREIGN KEY (phone_number) REFERENCES users (phone_number)
        )
    ''')
    
    # Reports table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            phone_number TEXT,
            call_id TEXT,
            type TEXT,
            filename TEXT,
            file_path TEXT,
            created_at TEXT,
            FOREIGN KEY (phone_number) REFERENCES users (phone_number),
            FOREIGN KEY (call_id) REFERENCES calls (call_id)
        )
    ''')
    
    # Financial data table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_financial_data (
            phone_number TEXT PRIMARY KEY,
            income REAL DEFAULT 0,
            savings REAL DEFAULT 0,
            expenses REAL DEFAULT 0,
            data_json TEXT,
            updated_at TEXT,
            FOREIGN KEY (phone_number) REFERENCES users (phone_number)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")


def ensure_user_exists(phone_number, name=None):
    """Ensure user exists in database"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT phone_number FROM users WHERE phone_number = ?', (phone_number,))
    if not c.fetchone():
        c.execute('''
            INSERT INTO users (phone_number, name, created_at, last_login)
            VALUES (?, ?, ?, ?)
        ''', (phone_number, name or phone_number, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
    
    conn.close()


def get_user_reports(phone_number):
    """Get all reports for a user"""
    ensure_user_exists(phone_number)
    
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT id, type, filename, file_path, created_at 
        FROM reports 
        WHERE phone_number = ?
        ORDER BY created_at DESC
    ''', (phone_number,))
    
    reports = []
    for row in c.fetchall():
        report_type = row[1] or 'financial_planning'
        reports.append({
            'id': row[0],
            'type': report_type,
            'filename': row[2],
            'path': row[3],
            'date': row[4],
            'title': f"{report_type.replace('_', ' ').title()} Report"
        })
    
    conn.close()
    return reports


def get_user_financial_data(phone_number):
    """Get user's financial summary"""
    ensure_user_exists(phone_number)
    
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT income, savings, expenses, data_json
        FROM user_financial_data
        WHERE phone_number = ?
    ''', (phone_number,))
    
    row = c.fetchone()
    conn.close()
    
    if row and row[0] is not None:
        return {
            'income': float(row[0]) if row[0] else 75000,
            'savings': float(row[1]) if row[1] else 25000,
            'expenses': float(row[2]) if row[2] else 50000,
            'data': json.loads(row[3]) if row[3] else {}
        }
    
    # Return default dummy data if no data exists
    return {
        'income': 75000,
        'savings': 25000,
        'expenses': 50000,
        'data': {}
    }


def save_call(phone_number, call_id, contact_id=None, tracking_id=None, campaign_id=None):
    """
    Save call record with full Pixpoc response data.
    
    Args:
        phone_number: User's phone number
        call_id: Pixpoc call UUID
        contact_id: Pixpoc contact ID
        tracking_id: Pixpoc tracking ID (callSid) - used for callbacks
        campaign_id: Pixpoc campaign ID
    """
    ensure_user_exists(phone_number)
    
    conn = get_connection()
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO calls (phone_number, call_id, tracking_id, contact_id, campaign_id, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (phone_number, call_id, tracking_id, contact_id, campaign_id, 'initiated', datetime.now().isoformat()))
        conn.commit()
        print(f"✅ Call saved: {call_id} (tracking: {tracking_id})")
    except sqlite3.IntegrityError:
        # Call already exists, update with new data
        c.execute('''
            UPDATE calls 
            SET tracking_id = ?, contact_id = ?, campaign_id = ?
            WHERE call_id = ?
        ''', (tracking_id, contact_id, campaign_id, call_id))
        conn.commit()
        print(f"✅ Call updated: {call_id}")
    
    conn.close()


def update_call_status(call_id, status, contact_id=None):
    """Update call status"""
    conn = get_connection()
    c = conn.cursor()
    
    if contact_id:
        c.execute('''
            UPDATE calls 
            SET status = ?, completed_at = ?, contact_id = ?
            WHERE call_id = ?
        ''', (status, datetime.now().isoformat(), contact_id, call_id))
    else:
        c.execute('''
            UPDATE calls 
            SET status = ?, completed_at = ?
            WHERE call_id = ?
        ''', (status, datetime.now().isoformat(), call_id))
    
    conn.commit()
    conn.close()


def get_call_phone_number(call_id):
    """Get phone number associated with a call"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT phone_number FROM calls WHERE call_id = ?', (call_id,))
    row = c.fetchone()
    conn.close()
    
    return row[0] if row else None


def get_call_by_tracking_id(tracking_id):
    """
    Get call details by tracking ID (callSid).
    This is used when Pixpoc sends callbacks with tracking_id.
    
    Returns:
        dict with call_id, phone_number, contact_id, etc. or None
    """
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT call_id, phone_number, contact_id, campaign_id, status, tracking_id
        FROM calls 
        WHERE tracking_id = ?
    ''', (tracking_id,))
    
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'call_id': row[0],
            'phone_number': row[1],
            'contact_id': row[2],
            'campaign_id': row[3],
            'status': row[4],
            'tracking_id': row[5]
        }
    return None


def get_call_by_id(call_id):
    """
    Get call details by call ID.
    
    Returns:
        dict with call details or None
    """
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT call_id, phone_number, contact_id, campaign_id, status, tracking_id
        FROM calls 
        WHERE call_id = ?
    ''', (call_id,))
    
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'call_id': row[0],
            'phone_number': row[1],
            'contact_id': row[2],
            'campaign_id': row[3],
            'status': row[4],
            'tracking_id': row[5]
        }
    return None


def save_report(phone_number, report_id, call_id, report_type, filename, file_path):
    """Save report record"""
    ensure_user_exists(phone_number)
    
    conn = get_connection()
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO reports (id, phone_number, call_id, type, filename, file_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (report_id, phone_number, call_id, report_type, filename, file_path, 
              datetime.now().isoformat()))
        conn.commit()
        print(f"✅ Report saved: {filename}")
    except sqlite3.IntegrityError as e:
        print(f"⚠️  Report already exists: {report_id}")
    
    conn.close()


def update_financial_data(phone_number, income, savings, expenses, data_dict):
    """Update user's financial data"""
    ensure_user_exists(phone_number)
    
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT OR REPLACE INTO user_financial_data 
        (phone_number, income, savings, expenses, data_json, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (phone_number, float(income), float(savings), float(expenses), 
          json.dumps(data_dict), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"✅ Financial data updated for {phone_number}")


# Initialize database on import
if not DB_PATH.exists():
    print("📦 Creating database...")
    init_db()

