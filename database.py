import sqlite3

def init_db():
    conn = sqlite3.connect("data/hrms.db")
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

    # Attendance (for biometric hook)
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        status TEXT,
        check_in_time TEXT,
        check_out_time TEXT,
        source TEXT,      -- manual / biometric / face
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

    # Payroll (auto calculation)
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

    # Location logs (GPS style)
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
    return sqlite3.connect("data/hrms.db")
