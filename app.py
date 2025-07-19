
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import os

st.set_page_config(layout="wide", page_title="DraftKings MMA Ownership")

st.title("DraftKings MMA Ownership")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Use fixed column positions H (7) and J (9)
    player_col = df.columns[7]
    drafted_col = df.columns[9]
    df = df[[player_col, drafted_col]]
    df.columns = ["PLAYER", "%DRAFTED"]

    # Remove any rows with missing or duplicate data
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Convert to numeric % for sorting
    df["%DRAFTED"] = df["%DRAFTED"].str.rstrip('%').astype(float)

    # Sort and reset index
    df.sort_values("%DRAFTED", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Pad to 20 rows if fewer
    while len(df) < 20:
        df = pd.concat([df, pd.DataFrame([{"PLAYER": "", "%DRAFTED": 0.0}])], ignore_index=True)

    # Split into two columns
    half = len(df) // 2
    left_col = df.iloc[:half]
    right_col = df.iloc[half:]

    # Start figure
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('black')
    ax.axis("off")

    # Header
    ax.text(0.1, 1.02, "PLAYER", color='orange', weight='bold', fontsize=14)
    ax.text(0.35, 1.02, "%DRAFTED", color='lime', weight='bold', fontsize=14)
    ax.text(0.6, 1.02, "%DRAFTED", color='lime', weight='bold', fontsize=14)
    ax.text(0.85, 1.02, "PLAYER", color='orange', weight='bold', fontsize=14)

    # Left column
    for i, (p, d) in enumerate(zip(left_col["PLAYER"], left_col["%DRAFTED"])):
        y = 0.95 - i * 0.045
        ax.text(0.1, y, str(p), color='white', fontsize=12)
        ax.text(0.35, y, f"{d:.2f}%", color='lime', fontsize=12)

    # Right column
    for i, (p, d) in enumerate(zip(right_col["PLAYER"].iloc[::-1], right_col["%DRAFTED"].iloc[::-1])):
        y = 0.95 - i * 0.045
        ax.text(0.6, y, f"{d:.2f}%", color='lime', fontsize=12)
        ax.text(0.85, y, str(p), color='white', fontsize=12)

    # Add logo
    logo_path = os.path.join(os.path.dirname(__file__), "draftkings_logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        fig.figimage(logo, xo=70, yo=fig.bbox.ymax - 100, alpha=1, zorder=10)

    st.pyplot(fig)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    st.download_button("Download Image", data=buf.getvalue(), file_name="draftkings_ownership.png", mime="image/png")
