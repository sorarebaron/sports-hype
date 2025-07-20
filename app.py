import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="DraftKings Ownership Report")

st.title("📊 DraftKings Ownership Report")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show columns for debugging
    st.write("Columns found:", df.columns.tolist())

    # Auto-detect relevant columns
    name_col = next((col for col in df.columns if "name" in col.lower()), None)
    drafted_col = next((col for col in df.columns if "draft" in col.lower()), None)

    if not name_col or not drafted_col:
        st.error("Could not find the expected 'Name' or '%Drafted' columns.")
        st.stop()

    df = df[[name_col, drafted_col]]
    df.columns = ["Name", "%Drafted"]

    # Sort by drafted percentage
    df["%Drafted"] = df["%Drafted"].str.replace('%', '').astype(float)
    df = df.sort_values("%Drafted", ascending=False).reset_index(drop=True)

    # Split into two columns
    midpoint = len(df) // 2 + len(df) % 2
    left_df = df.iloc[:midpoint].reset_index(drop=True)
    right_df = df.iloc[midpoint:].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#1e1e1e')
    ax.axis('off')

    def draw_column(x_offset, data):
        ax.text(x_offset, 1.05, "PLAYER", color='orangered', fontsize=14, fontweight='bold', family='monospace')
        ax.text(x_offset + 0.25, 1.05, "%DRAFTED", color='mediumspringgreen', fontsize=14, fontweight='bold', family='monospace')

        for i, row in data.iterrows():
            y = 1 - (i + 1) * 0.065
            ax.text(x_offset, y, f"{row['Name']}", fontsize=12, color='white', family='monospace')
            ax.text(x_offset + 0.25, y, f"{row['%Drafted']:.2f}%", fontsize=12, color='white', family='monospace', ha='right')

    draw_column(0.05, left_df)
    draw_column(0.55, right_df)

    st.pyplot(fig)
