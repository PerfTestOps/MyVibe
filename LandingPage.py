import streamlit as st
import AddingUser, ActualsByMonth
import ActualsVsForecast
import UpdatingActualsWithFilter

# ---- Sidebar Navigation ----
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add User", "Actuals Vs Forecast", "Update Actuals", "Actuals By Month", "Settings"])

# ---- Page Routing Logic ----
if page == "Home":
    st.title("🏠 Welcome to the Dashboard")
    st.write("Use the sidebar to explore different sections like project summaries, data editing, and visualizations.")

elif page == "Add User":
    #st.title("📁 User Addition Page")
    #st.write("Here you'd show summary metrics, active projects, filtered views, etc.")
    AddingUser.show_page()

elif page == "Actuals Vs Forecast":
    #st.title("📝 Edit Excel Data")
    #st.write("Load an Excel sheet, apply filters, and edit data inline.")
    ActualsVsForecast.show_page()

elif page == "Update Actuals":
    #st.title("📊 Visualize Data")
    #st.write("View dynamic charts like Forecast vs Actual comparisons.")
    UpdatingActualsWithFilter.show_page()


elif page == "Actuals By Month":
    #st.title("📊 Visualize Data")
    #st.write("View dynamic charts like Forecast vs Actual comparisons.")
    ActualsByMonth.show_page()

elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Control app preferences, theme options, or configuration.")

