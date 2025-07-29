# AddProject.py

import streamlit as st
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# --- Security Check ---
def is_admin():
    return st.session_state.get("role") == "Admin"

# --- Excel Configuration ---
excel_path = "BaseDatasheet.xlsx"
sheet1_name = "Sheet1"
sheet2_name = "Sheet2"

def get_header_map(ws):
    return {cell.value: idx+1 for idx, cell in enumerate(ws[1]) if cell.value}

def build_row_from_headers(ws, user_data):
    header_map = get_header_map(ws)
    total_cols = ws.max_column
    row = [""] * total_cols

    for field, value in user_data.items():
        if field in header_map:
            row[header_map[field] - 1] = value

    return row

def add_project_to_sheets(user_data):
    book = load_workbook(excel_path)

    # --- Sheet1 ---
    if sheet1_name in book.sheetnames:
        ws1 = book[sheet1_name]
        row1 = build_row_from_headers(ws1, user_data)
        ws1.append(row1)
    else:
        raise Exception("Sheet1 not found.")

    # --- Sheet2 ---
    if sheet2_name in book.sheetnames:
        ws2 = book[sheet2_name]
        row2 = build_row_from_headers(ws2, user_data)
        ws2.append(row2)
    else:
        raise Exception("Sheet2 not found.")

    book.save(excel_path)

# --- UI Page ---
def show_page():
    st.title("👷 Admin: Add New Project")
    st.markdown("---")

    if not is_admin():
        st.warning("🚫 You do not have permission to add new projects.")
        st.stop()

    with st.form("add_project_form"):
        project_name = st.text_input("Project Name")
        associate_id = st.text_input("Associate ID")
        associate_name = st.text_input("Associate Name")
        parent_customer = st.text_input("Parent Customer")
        description = st.text_area("Project Description")
        region = st.selectbox("Region", ["North America", "EU", "APAC", "India"])
        service_line = st.text_input("Service Line")
        status = st.selectbox("Active", ["Yes", "No"])
        start_date = st.date_input("Start Date")

        submitted = st.form_submit_button("Add Project")

        if submitted:
            user_data = {
                "Project Name": project_name,
                "AssociateID": associate_id,
                "AssociateName": associate_name,
                "Parent Customer": parent_customer,
                "Project description": description,
                "Region": region,
                "ServiceLine": service_line,
                "Service Line": service_line,  # if Sheet2 uses different spelling
                "Active": status,
                "Demand Start Date": start_date.strftime("%Y-%m-%d"),
                "Resource Start Date": start_date.strftime("%Y-%m-%d"),
            }

            try:
                add_project_to_sheets(user_data)
                st.success(f"✅ Project '{project_name}' added successfully to both sheets!")
            except Exception as e:
                st.error(f"⚠️ Error adding project: {e}")
