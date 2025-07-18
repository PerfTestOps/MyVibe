import streamlit as st
from openpyxl import load_workbook, Workbook
import os

def show_page():

    st.title("Revenue Tracker System")

    # Create a form
    with st.form("user_form"):
        
        # Dropdown for Service Line selection
        service_line = st.selectbox(    
            "Select Service Line",
            ["QEA", "SPE", "UI/UX"]
        )
        
        
        associate_name = st.text_input("Enter Associate Name")
        associate_id = st.text_input("Enter Associate ID")
        
        project_name = st.selectbox(
            "Select Project",
            ["QTest", "Ptest", "Rtest", "Srest", "Trest", "Urest", "Vrest", "Wrest", "Xrest", "Yrest", "Zrest"]
        )


        # Dropdown for Practice Line selection
        practice_line = st.selectbox(
            "Select Practice Line",
            ["NFT", "SRE", "QTP"]
        )

        # Dropdown for Region selection 
        region_selection = st.selectbox(
            "Select Region",
            ["NA", "APAC", "EU"]
        )

        # Dropdown for Active / Not Active selection 
        active_selection = st.selectbox(
            "Is Active",
            ["Yes", "No"]
        )
            
        submitted = st.form_submit_button("Submit")

    # Excel file path
    excel_file = "BaseDatasheet.xlsx"

    # Handle form submission
    if submitted:
        st.success(f"Thanks {associate_name}, your data is now added!")

        if not os.path.exists(excel_file):
            wb = Workbook()
            ws = wb.active
            #ws.append(["Name", "Age Group", "Feedback Type", "Detailed Feedback"])  # Header
            ws.append(["service_line", "associate_name", "associate_id", "project_name","practice_line", "region_selection", "active_selection"])  # Header
        else:
            wb = load_workbook(excel_file)
            ws = wb.active

        ws.append([service_line, associate_name, associate_id, project_name, practice_line, region_selection, active_selection])  # Append the data
        wb.save(excel_file)

        st.info("Your response has been saved to Excel.")
