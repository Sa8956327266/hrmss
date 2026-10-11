import streamlit as st
from auth import login_user, register_user, register_company, get_companies
from employee import employee_dashboard
from admin import admin_dashboard
from database import init_db

st.set_page_config(page_title="HRMS System", layout="wide")

def main():
    init_db()

    st.title("Multi-Company HRMS System")

    menu = ["Login", "Register Employee", "Register Admin", "Register Company"]
    choice = st.sidebar.selectbox("Menu", menu)

    if "user" not in st.session_state:
        st.session_state["user"] = None

    if choice == "Register Company":
        st.subheader("Register Company")
        name = st.text_input("Company Name")
        addr = st.text_area("Address")
        if st.button("Save Company"):
            register_company(name, addr)
            st.success("Company Registered")

    elif choice == "Register Employee":
        st.subheader("Register Employee")
        companies = get_companies()
        company_map = {name: cid for cid, name in companies}
        company_name = st.selectbox("Company", list(company_map.keys())) if companies else None
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        dept = st.text_input("Department")
        desig = st.text_input("Designation")
        base_salary = st.number_input("Base Salary", min_value=0.0, step=100.0)
        if st.button("Register"):
            register_user(
                name, email, password, "employee",
                dept, desig,
                company_map.get(company_name), base_salary
            )
            st.success("Employee Registered")

    elif choice == "Register Admin":
        st.subheader("Register Admin")
        companies = get_companies()
        company_map = {name: cid for cid, name in companies}
        company_name = st.selectbox("Company", list(company_map.keys())) if companies else None
        name = st.text_input("Admin Name")
        email = st.text_input("Admin Email")
        password = st.text_input("Admin Password", type="password")
        if st.button("Register Admin"):
            register_user(name, email, password, "admin", company_id=company_map.get(company_name))
            st.success("Admin Registered")

    elif choice == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state["user"] = user
                st.success(f"Welcome {user['name']} ({user['role']})")
            else:
                st.error("Invalid credentials")

    st.sidebar.markdown("---")

    if st.session_state["user"]:
        user = st.session_state["user"]
        st.sidebar.write(f"Logged in as: {user['name']} ({user['role']})")
        if st.sidebar.button("Logout"):
            st.session_state["user"] = None
        else:
            if user["role"] == "employee":
                employee_dashboard(user)
            elif user["role"] == "admin":
                admin_dashboard(user)
    else:
        st.info("Login to access dashboards.")

if __name__ == "__main__":
    main()
