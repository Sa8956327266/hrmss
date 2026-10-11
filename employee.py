import streamlit as st
from database import get_conn
from pdf_generator import generate_offer_letter, generate_salary_slip

def employee_dashboard(user):
    st.header(f"Employee Dashboard - {user['name']}")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        ["Attendance", "Leave", "Payroll", "Requests", "Location Logs", "Offer Letter", "Salary Slip"]
    )

    # Attendance (manual + biometric/face source)
    with tab1:
        st.markdown("### Mark Attendance")
        status = st.selectbox("Status", ["Present", "Absent", "Late"])
        source = st.selectbox("Source", ["manual", "biometric", "face"])
        check_in = st.time_input("Check-in time")
        check_out = st.time_input("Check-out time")
        date_val = st.date_input("Date")
        if st.button("Save Attendance"):
            conn = get_conn()
            c = conn.cursor()
            c.execute("""
                INSERT INTO attendance (user_id, date, status, check_in_time, check_out_time, source)
                VALUES (?,?,?,?,?,?)
            """, (user["id"], date_val.isoformat(), status, str(check_in), str(check_out), source))
            conn.commit()
            conn.close()
            st.success("Attendance saved (hook ready for real biometric/face).")

    # Leave
    with tab2:
        from_date = st.date_input("From")
        to_date = st.date_input("To")
        reason = st.text_area("Reason")
        if st.button("Apply Leave"):
            conn = get_conn()
            c = conn.cursor()
            c.execute("""
                INSERT INTO leaves (user_id, from_date, to_date, reason, status)
                VALUES (?,?,?,?,?)
            """, (user["id"], from_date.isoformat(), to_date.isoformat(), reason, "Pending"))
            conn.commit()
            conn.close()
            st.success("Leave Applied")

    # Payroll (auto calc concept)
    with tab3:
        st.markdown("### Payroll Summary")
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT month, basic, hra, allowances, deductions, net_pay, status
            FROM payroll WHERE user_id=? ORDER BY month DESC
        """, (user["id"],))
        st.table(c.fetchall())
        conn.close()

    # Requests
    with tab4:
        req_type = st.selectbox("Type", ["Salary", "Leave", "Location", "Other"])
        msg = st.text_area("Message")
        if st.button("Raise Request"):
            conn = get_conn()
            c = conn.cursor()
            c.execute("""
                INSERT INTO requests (user_id, type, message, status, created_at)
                VALUES (?,?,?,?,datetime('now'))
            """, (user["id"], req_type, msg, "Pending"))
            conn.commit()
            conn.close()
            st.success("Request Raised")

    # Location logs (GPS style)
    with tab5:
        st.markdown("### Add Location Log (GPS style)")
        lat = st.number_input("Latitude", format="%.6f")
        lon = st.number_input("Longitude", format="%.6f")
        addr = st.text_area("Address / Notes")
        if st.button("Save Location"):
            conn = get_conn()
            c = conn.cursor()
            c.execute("""
                INSERT INTO location_logs (user_id, latitude, longitude, address, timestamp)
                VALUES (?,?,?,?,datetime('now'))
            """, (user["id"], lat, lon, addr))
            conn.commit()
            conn.close()
            st.success("Location saved.")
        st.markdown("### My Location History")
        conn = get_conn()
        c = conn.cursor()
        c.execute("""
            SELECT latitude, longitude, address, timestamp
            FROM location_logs WHERE user_id=? ORDER BY timestamp DESC
        """, (user["id"],))
        st.table(c.fetchall())
        conn.close()

    # Offer Letter
    with tab6:
        if st.button("Download Offer Letter"):
            pdf = generate_offer_letter(user)
            st.download_button("Download PDF", pdf, "offer_letter.pdf")

    # Salary Slip
    with tab7:
        month = st.text_input("Month (e.g. 2026-10)")
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        if st.button("Generate Salary Slip"):
            pdf = generate_salary_slip(user, month, amount)
            st.download_button("Download Salary Slip", pdf, "salary_slip.pdf")
