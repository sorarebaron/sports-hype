
import streamlit as st
import pandas as pd

st.set_page_config(page_title="DraftKings MMA Ownership Report", page_icon="🥊", layout="centered")

st.markdown("<h1 style='text-align: center;'>🥊 DraftKings MMA Ownership Report</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload DraftKings CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Clean and format
    df = df[["Name + ID", "%Drafted"]]
    df = df.dropna()
    df = df[~df['Name + ID'].str.contains("Fighter 29|Fighter 30")]
    df["%Drafted"] = df["%Drafted"].astype(float).round(2).astype(str) + "%"

    # Pad player names for alignment
    df["Formatted"] = df["Name + ID"].str.pad(width=22) + df["%Drafted"]

    # Split evenly
    split_idx = len(df) // 2
    left = df.iloc[:split_idx]["Formatted"].tolist()
    right = df.iloc[split_idx:]["Formatted"].tolist()

    # Pad columns to equal length
    if len(left) > len(right):
        right += [""] * (len(left) - len(right))
    elif len(right) > len(left):
        left += [""] * (len(right) - len(left))

    # Create formatted rows
    combined_lines = [f"{l}    {r}" for l, r in zip(left, right)]

    # Display with fixed-width font
    st.markdown("<pre style='font-family: monospace; color: white;'>"
                "<span style='color: orange;'>PLAYER               </span>"
                "<span style='color: lime;'>%DRAFTED        </span>"
                "<span style='color: orange;'>PLAYER               </span>"
                "<span style='color: lime;'>%DRAFTED</span>\n" +
                "\n".join(combined_lines) +
                "</pre>", unsafe_allow_html=True)

    # Download button
    csv = df[["Name + ID", "%Drafted"]].to_csv(index=False).encode("utf-8")
    st.download_button("Download Ownership Report", data=csv, file_name="ownership_report.csv", mime="text/csv")
