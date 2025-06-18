# app.py

import streamlit as st
import pandas as pd
from io import BytesIO

st.title("🔗 Combine Chiller Power Data (Daily Files)")

st.markdown("""
Upload up to 31 Excel files (e.g., 1 per day), and this app will merge them into one.
""")

uploaded_files = st.file_uploader("📂 Upload Excel Files (Max 31)", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 31:
        st.error("❌ You can only upload a maximum of 31 files.")
    else:
        combined_df = pd.DataFrame()

        for file in uploaded_files:
            try:
                df = pd.read_excel(file)
                df["Source_File"] = file.name
                combined_df = pd.concat([combined_df, df], ignore_index=True)
            except Exception as e:
                st.warning(f"⚠️ Couldn't read {file.name}: {e}")

        st.success(f"✅ Combined {len(uploaded_files)} files successfully!")

        st.dataframe(combined_df.head())

        def to_excel_bytes(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='CombinedData')
            return output.getvalue()

        excel_data = to_excel_bytes(combined_df)

        st.download_button(
            label="📥 Download Combined Excel File",
            data=excel_data,
            file_name="Combined_Chiller_Power_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
