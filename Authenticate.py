import streamlit as st
import pandas as pd


st.set_page_config(page_title="Login", page_icon="🔐")

# Load authentication data
def load_credentials():
    try:
        df = pd.read_excel("BaseDatasheet.xlsx", sheet_name="Authenticate")
        return df[["EmpID", "EmpPassword", "Role"]].dropna()
    except Exception as e:
        st.error(f"Error loading credentials: {e}")
        return pd.DataFrame()

# Authenticate user and return role
def authenticate_user(emp_id, password, auth_df):
    user = auth_df[auth_df["EmpID"].astype(str) == str(emp_id)]
    if not user.empty and user["EmpPassword"].values[0] == password:
        return True, user["Role"].values[0]
    return False, None

# Session setup
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.emp_id = None

# Login form
if not st.session_state.authenticated:
    st.title("🔐 Login to Revenue Dashboard")

    emp_id = st.text_input("Employee ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        auth_df = load_credentials()
        success, role = authenticate_user(emp_id, password, auth_df)
        if success:
            st.session_state.authenticated = True
            st.session_state.role = role
            st.session_state.emp_id = emp_id
            st.success(f"Welcome {role.capitalize()}! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")
else:
    import LandingPage
    st.switch_page("pages/LandingPage.py")
