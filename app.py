import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import io

st.set_page_config(layout="wide")
st.title("DraftKings MMA Ownership Visualizer")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Read specific columns by letter (H and J are index 7 and 9)
    df = df.iloc[1:, [7, 9]]
    df.columns = ["PLAYER", "%DRAFTED"]
    df = df.dropna()
    df["%DRAFTED"] = df["%DRAFTED"].astype(str).str.replace('%', '').astype(float)
    df["PLAYER"] = df["PLAYER"].astype(str)
    df = df.drop_duplicates(subset=["PLAYER"])
    df = df.sort_values(by="%DRAFTED", ascending=False).reset_index(drop=True)

    # Split into two columns
    half = len(df) // 2 + len(df) % 2
    left = df.iloc[:half].reset_index(drop=True)
    right = df.iloc[half:].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('black')
    ax.axis("off")

    # Load DraftKings logo
    logo = mpimg.imread("draftkings_logo.png")
    fig.figimage(logo, xo=fig.bbox.xmax / 2 - 100, yo=fig.bbox.ymax - 80, zorder=1)

    # Set headers
    ax.text(0.15, 0.88, "PLAYER", color="orange", fontsize=14, fontweight="bold", transform=fig.transFigure)
    ax.text(0.33, 0.88, "%DRAFTED", color="lime", fontsize=14, fontweight="bold", transform=fig.transFigure)
    ax.text(0.63, 0.88, "PLAYER", color="orange", fontsize=14, fontweight="bold", transform=fig.transFigure)
    ax.text(0.81, 0.88, "%DRAFTED", color="lime", fontsize=14, fontweight="bold", transform=fig.transFigure)

    # Add player data
    spacing = 0.03
    for i in range(len(left)):
        y = 0.85 - i * spacing
        ax.text(0.15, y, left.at[i, "PLAYER"], color="white", fontsize=12, transform=fig.transFigure)
        ax.text(0.33, y, f'{left.at[i, "%DRAFTED"]:.2f}%', color="lime", fontsize=12, transform=fig.transFigure)

    for i in range(len(right)):
        y = 0.85 - i * spacing
        ax.text(0.63, y, right.at[i, "PLAYER"], color="white", fontsize=12, transform=fig.transFigure)
        ax.text(0.81, y, f'{right.at[i, "%DRAFTED"]:.2f}%', color="lime", fontsize=12, transform=fig.transFigure)

    st.pyplot(fig)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    st.download_button("Download PNG", data=buf.getvalue(), file_name="draftkings_ownership.png", mime="image/png")
