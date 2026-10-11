import streamlit as st
from database import get_conn

def admin_dashboard(user):
    st.header("Admin Dashboard")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Employees", "Leaves", "Payroll", "Requests", "Attendance", "Audit Logs"]
    )

    # Employees
    with tab1:
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT id, name, email, role, department, designation, base_salary
            FROM users WHERE company_id=?
        """, (user["company_id"],))
        st.table(c.fetchall())
        conn.close()

    # Leaves
    with tab2:
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT leaves.id, users.name, leaves.from_date, leaves.to_date, leaves.reason, leaves.status
            FROM leaves JOIN users ON leaves.user_id = users.id
            WHERE users.company_id=?
        """, (user["company_id"],))
        st.table(c.fetchall())
        leave_id = st.number_input("Leave ID", min_value=1)
        status = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
        if st.button("Update Leave"):
            c.execute("UPDATE leaves SET status=? WHERE id=?", (status, leave_id))
            conn.commit()
            st.success("Leave updated.")
        conn.close()

    # Payroll (auto calc)
    with tab3:
        st.markdown("### Generate Payroll")
        emp_id = st.number_input("Employee ID", min_value=1)
        month = st.text_input("Month (e.g. 2026-10)")
        basic = st.number_input("Basic", min_value=0.0, step=100.0)
        hra = st.number_input("HRA", min_value=0.0, step=100.0)
        allowances = st.number_input("Allowances", min_value=0.0, step=100.0)
        deductions = st.number_input("Deductions", min_value=0.0, step=100.0)
        if st.button("Create Payroll"):
            net = basic + hra + allowances - deductions
            conn = get_conn()
            c = conn.cursor()
            c.execute("""
                INSERT INTO payroll (user_id, month, basic, hra, allowances, deductions, net_pay, status)
                VALUES (?,?,?,?,?,?,?,?)
            """, (emp_id, month, basic, hra, allowances, deductions, net, "Unpaid"))
            conn.commit()
            conn.close()
            st.success(f"Payroll created. Net Pay: {net}")

        st.markdown("### Company Payroll Records")
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT payroll.id, users.name, payroll.month, payroll.net_pay, payroll.status
            FROM payroll JOIN users ON payroll.user_id = users.id
            WHERE users.company_id=?
        """, (user["company_id"],))
        st.table(c.fetchall())
        conn.close()

    # Requests
    with tab4:
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT requests.id, users.name, requests.type, requests.message, requests.status
            FROM requests JOIN users ON requests.user_id = users.id
            WHERE users.company_id=?
        """, (user["company_id"],))
        st.table(c.fetchall())
        req_id = st.number_input("Request ID", min_value=1)
        status = st.selectbox("Request Status", ["Pending", "Resolved"])
        if st.button("Update Request"):
            c.execute("UPDATE requests SET status=? WHERE id=?", (status, req_id))
            conn.commit()
            st.success("Request updated.")
        conn.close()

    # Attendance view
    with tab5:
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT users.name, attendance.date, attendance.status,
                   attendance.check_in_time, attendance.check_out_time, attendance.source
            FROM attendance JOIN users ON attendance.user_id = users.id
            WHERE users.company_id=?
            ORDER BY attendance.date DESC
        """, (user["company_id"],))
        st.table(c.fetchall())
        conn.close()

    # Audit logs
    with tab6:
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT audit_logs.id, users.name, audit_logs.action, audit_logs.timestamp
            FROM audit_logs JOIN users ON audit_logs.user_id = users.id
            WHERE users.company_id=?
        """, (user["company_id"],))
        st.table(c.fetchall())
        conn.close()
