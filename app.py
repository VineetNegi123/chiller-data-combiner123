import streamlit as st
import pandas as pd
from io import StringIO

st.title("🔗 Combine Chiller Power Data (Daily CSV Files)")

st.markdown("""
Upload up to 31 **CSV files** (e.g., 1 per day), and this app will merge them into one file.
""")

uploaded_files = st.file_uploader("📂 Upload CSV Files (Max 31)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 31:
        st.error("❌ You can only upload a maximum of 31 files.")
    else:
        combined_df = pd.DataFrame()

        for file in uploaded_files:
            try:
                stringio = StringIO(file.getvalue().decode("utf-8"))
                df = pd.read_csv(stringio)
                df["Source_File"] = file.name  # Optional: tag source filename
                combined_df = pd.concat([combined_df, df], ignore_index=True)
            except Exception as e:
                st.warning(f"⚠️ Couldn't read {file.name}: {e}")

        st.success(f"✅ Combined {len(uploaded_files)} CSV files successfully!")

        st.dataframe(combined_df.head())

        # Download as CSV
        st.download_button(
            label="📥 Download Combined CSV File",
            data=combined_df.to_csv(index=False).encode("utf-8"),
            file_name="Combined_Chiller_Power_Data.csv",
            mime="text/csv"
        )
