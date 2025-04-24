import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("Datasweeper Sterling Integrator By Kulsoom Farrukh")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3!")

# File Uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file into dataframe
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            continue

        # Show file preview
        st.subheader(f"Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"Data Cleaning Options for {file.name}")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled!")

        # Column Selector
        st.subheader(f"Select Columns to Keep for {file.name}")
        selected_columns = st.multiselect(
            f"Choose columns from {file.name}",
            options=df.columns.tolist(),
            default=df.columns.tolist(),
            key=f"columns_{file.name}"
        )
        df = df[selected_columns]
        st.write("Filtered Data:")
        st.write(df)

        # Data Visualization
        st.subheader(f"Data Visualization for {file.name}")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_data = df.select_dtypes(include='number')
            if not numeric_data.empty:
                st.bar_chart(numeric_data.iloc[:, :2])
            else:
                st.warning("No numeric data available for visualization.")

        # Conversion Options
        st.subheader(f"Conversion Options for {file.name}")
        conversion_type = st.radio(
            f"Convert {file.name} to:",
            ["CSV", "Excel"],
            key=f"convert_{file.name}"
        )

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                download_filename = file.name.rsplit(".", 1)[0] + ".csv"
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                download_filename = file.name.rsplit(".", 1)[0] + ".xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=download_filename,
                mime=mime_type
            )

    st.success("All files processed successfully!")

else:
    st.info("Please upload at least one file to continue.")
