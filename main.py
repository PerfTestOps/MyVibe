import streamlit as st
import Authenticate
import LandingPage

# Check authentication status first
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    Authenticate.show_page()
else:
    LandingPage.show_page()
