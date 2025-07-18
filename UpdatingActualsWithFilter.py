import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import os

def show_page():
    # Load Excel data
    excel_file = "BaseDatasheet.xlsx"
    sheet_name = "Sheet1"
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    st.title("🧠 Update Actuals / Forecast Data")

    # 🔍 Filter by Project Name with exact match
    project_filter = st.text_input("Filter by Project Name (Exact Match)", placeholder="Type exact project name")

    # Convert AssociateID to string to avoid comma formatting
    df["AssociateID"] = df["AssociateID"].astype(str)

    # Apply exact match filter
    filtered_df = df[df["Project Name"] == project_filter] if project_filter else df.copy()

    # Show editable table
    edited_df = st.data_editor(filtered_df, num_rows="fixed", use_container_width=True)

    # Save changes
    if st.button("💾 Save Changes"):
        try:
            wb = load_workbook(excel_file)
            ws = wb[sheet_name]

            # Get header from original sheet
            header = [cell.value for cell in ws[1]]
            project_col_index = header.index("Project Name")

            # Remove rows matching the exact project name
            rows_to_delete = [
                i for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2)
                if str(row[project_col_index]) == project_filter
            ]
            for row_idx in reversed(rows_to_delete):
                ws.delete_rows(row_idx)

            # Append updated rows
            for row in edited_df.itertuples(index=False):
                ws.append(list(row))

            wb.save(excel_file)
            st.success(f"✅ Changes saved for project: {project_filter}")
        except Exception as e:
            st.error(f"❌ Failed to save changes: {e}")
