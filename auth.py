from database import get_conn

def register_company(name, address):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO companies (name, address) VALUES (?,?)", (name, address))
    conn.commit()
    conn.close()

def get_companies():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name FROM companies")
    rows = c.fetchall()
    conn.close()
    return rows

def register_user(name, email, password, role, dept="", desig="", company_id=None, base_salary=0):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (company_id, name, email, password, role, department, designation, base_salary)
        VALUES (?,?,?,?,?,?,?,?)
    """, (company_id, name, email, password, role, dept, desig, base_salary))
    conn.commit()
    conn.close()

def login_user(email, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT id, company_id, name, role, department, designation, base_salary
        FROM users WHERE email=? AND password=?
    """, (email, password))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "company_id": row[1],
            "name": row[2],
            "role": row[3],
            "department": row[4],
            "designation": row[5],
            "base_salary": row[6]
        }
    return None
