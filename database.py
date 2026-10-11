import sqlite3
import os

def init_db():
    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)
    db_path = os.path.join("data", "hrms.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Companies
    c.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT
    )
    """)

    # Users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT,
        department TEXT,
        designation TEXT,
        base_salary REAL DEFAULT 0,
        FOREIGN KEY(company_id) REFERENCES companies(id)
    )
    """)

    # Attendance
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        status TEXT,
        check_in_time TEXT,
        check_out_time TEXT,
        source TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Leaves
    c.execute("""
    CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        from_date TEXT,
        to_date TEXT,
        reason TEXT,
        status TEXT
    )
    """)

    # Payroll
    c.execute("""
    CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        month TEXT,
        basic REAL,
        hra REAL,
        allowances REAL,
        deductions REAL,
        net_pay REAL,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Requests
    c.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        message TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    # Location logs
    c.execute("""
    CREATE TABLE IF NOT EXISTS location_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        latitude REAL,
        longitude REAL,
        address TEXT,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Audit logs
    c.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_conn():
    os.makedirs("data", exist_ok=True)
    db_path = os.path.join("data", "hrms.db")
    return sqlite3.connect(db_path)
