import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def show_page():
    st.title("🧠 Update Actuals / Forecast & Billing / Attendance")

    # 📄 Sheet Selector
    sheet_choice = st.radio("Select Sheet to Edit", ["Sheet1 - Actuals/Forecast", "Sheet2 - Billing/Attendance"])
    sheet_map = {
        "Sheet1 - Actuals/Forecast": "Sheet1",
        "Sheet2 - Billing/Attendance": "Sheet2"
    }
    sheet_name = sheet_map[sheet_choice]
    excel_file = "BaseDatasheet.xlsx"

    # 🧾 Load sheet
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl")
    except Exception as e:
        st.error(f"❌ Failed to load {sheet_name}: {e}")
        return

    if "AssociateID" in df.columns:
        df["AssociateID"] = df["AssociateID"].astype(str)

    # 🔍 Filter by project
    project_filter = st.text_input("Filter by Project Name (Exact Match)", placeholder="Type exact project name")
    filtered_df = df[df["Project Name"] == project_filter] if project_filter and "Project Name" in df.columns else df.copy()

    # 🧠 Init session state
    if "working_df" not in st.session_state:
        st.session_state.working_df = filtered_df.copy()
    if "history" not in st.session_state:
        st.session_state.history = []

    # ✨ Highlighting options
    st.markdown("### 🎨 Table Styling")
    highlight_color = st.color_picker("Pick cell background color", "#f9f9f9")
    text_size = st.selectbox("Text size", ["Small", "Medium", "Large"])
    size_map = {"Small": "12px", "Medium": "16px", "Large": "20px"}

    # 🗑️ Row Deletion
    st.markdown("### 🚮 Delete Rows")
    selected_indices = st.multiselect("Select row indices to delete", options=list(st.session_state.working_df.index))
    if st.button("Delete Selected"):
        if selected_indices:
            st.session_state.history.append(st.session_state.working_df.copy())
            st.session_state.working_df.drop(index=selected_indices, inplace=True)
            st.session_state.working_df.reset_index(drop=True, inplace=True)
            st.success(f"Deleted {len(selected_indices)} row(s).")
        else:
            st.info("No rows selected.")

    # ➕ Insert Blank Row
    st.markdown("### ➕ Insert Blank Row")
    insert_index = st.number_input("Target index", min_value=0, max_value=len(st.session_state.working_df), step=1)
    direction = st.radio("Insert row", ["Above", "Below"])
    if st.button("Insert Blank Row"):
        st.session_state.history.append(st.session_state.working_df.copy())
        blank_row = pd.DataFrame([{col: "" for col in st.session_state.working_df.columns}])
        if direction == "Above":
            top = st.session_state.working_df.iloc[:insert_index]
            bottom = st.session_state.working_df.iloc[insert_index:]
        else:
            top = st.session_state.working_df.iloc[:insert_index + 1]
            bottom = st.session_state.working_df.iloc[insert_index + 1:]
        st.session_state.working_df = pd.concat([top, blank_row, bottom], ignore_index=True)
        st.success(f"Inserted blank row {direction.lower()} index {insert_index}")

    # 🔙 Undo last action
    if st.button("Undo Last Change"):
        if st.session_state.history:
            st.session_state.working_df = st.session_state.history.pop()
            st.success("Reverted to previous state.")
        else:
            st.info("No history available.")

    # 📝 Display Editor
    st.markdown("### ✍️ Editable Table")
    styled_df = st.session_state.working_df.style.set_properties(**{
        "background-color": highlight_color,
        "font-size": size_map[text_size]
    })
    edited_df = st.data_editor(
        st.session_state.working_df,
        num_rows="fixed",
        use_container_width=True
    )

    # 🧠 Apply live edits to working_df
    st.session_state.working_df = edited_df.copy()

    # 💾 Save to Excel
    if st.button("💾 Save Changes"):
        try:
            wb = load_workbook(excel_file)
            if sheet_name in wb.sheetnames:
                wb.remove(wb[sheet_name])
            ws = wb.create_sheet(sheet_name)
            ws.append(st.session_state.working_df.columns.tolist())
            for r in dataframe_to_rows(st.session_state.working_df, index=False, header=False):
                ws.append(r)
            wb.save(excel_file)
            st.success(f"✅ Changes saved to {sheet_name}")
        except Exception as e:
            st.error(f"❌ Save failed: {e}")
