import streamlit as st
import Authenticate
import LandingPage
import Common

cookie = Common.cookie_manager.get(Common.cookie_name)
#print('****', cookie)
# Check authentication status first
if not Common.is_authenticated():
    Authenticate.show_page()
else:
    LandingPage.show_page()
