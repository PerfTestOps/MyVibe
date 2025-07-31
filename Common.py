import streamlit as st
from extra_streamlit_components import CookieManager

cookie_manager = CookieManager()
cookie_name = "auth_cookie"

def is_authenticated():
    cookie = cookie_manager.get(cookie_name)
    if cookie and cookie.get('authenticated'):
        st.session_state.authenticated = True
        st.session_state.role = cookie.get('role')
        st.session_state.emp_id = cookie.get('emp_id')
        st.session_state.page = cookie.get('page')
        return True
    return False

def get_cookie_data():
    cookie = cookie_manager.get(cookie_name)
    if cookie:
        return cookie
    return {
        "authenticated": False,
        "role": None,
        "emp_id": None,
        "page": 0
    }

def update_page_in_cookie(new_page):
    current_cookie = get_cookie_data()
    updated_cookie = {**current_cookie, "page": new_page}
    cookie_manager.set(
        cookie_name,
        updated_cookie,
    )
