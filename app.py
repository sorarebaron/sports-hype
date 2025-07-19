
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# App title
st.title("DraftKings Ownership Visualizer")

# File uploader
uploaded_file = st.file_uploader("Upload DraftKings CSV", type="csv")

if uploaded_file:
    # Read specific columns by Excel-style letters
    df_raw = pd.read_csv(uploaded_file, usecols=["H", "J"], skiprows=[0])
    df_raw.columns = ["Player", "%Drafted"]  # Rename columns for consistency

    # Clean data
    df = df_raw.dropna()
    df = df.drop_duplicates()
    df["%Drafted"] = df["%Drafted"].astype(str).str.replace('%', '').astype(float)

    # Sort and select top/bottom
    df_sorted = df.sort_values(by="%Drafted", ascending=False)
    top_15 = df_sorted.head(15)
    bottom_15 = df_sorted.tail(15)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    # Headers
    ax.text(0.02, 1.05, "PLAYER", fontsize=16, color='orange', fontweight='bold', transform=ax.transAxes)
    ax.text(0.28, 1.05, "%DRAFTED", fontsize=16, color='lime', fontweight='bold', transform=ax.transAxes)
    ax.text(0.52, 1.05, "PLAYER", fontsize=16, color='orange', fontweight='bold', transform=ax.transAxes)
    ax.text(0.78, 1.05, "%DRAFTED", fontsize=16, color='lime', fontweight='bold', transform=ax.transAxes)

    # Rows
    for i in range(15):
        y = 1 - (i + 1) * 0.06
        ax.text(0.02, y, top_15.iloc[i]["Player"], fontsize=14, color='white', transform=ax.transAxes)
        ax.text(0.28, y, f'{top_15.iloc[i]["%Drafted"]:.2f}%', fontsize=14, color='lime', transform=ax.transAxes)

        ax.text(0.52, y, bottom_15.iloc[i]["Player"], fontsize=14, color='white', transform=ax.transAxes)
        ax.text(0.78, y, f'{bottom_15.iloc[i]["%Drafted"]:.2f}%', fontsize=14, color='lime', transform=ax.transAxes)

    ax.axis("off")
    st.pyplot(fig)

    # PNG download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    st.download_button("Download PNG", data=buf.getvalue(), file_name="draftkings_ownership.png", mime="image/png")
