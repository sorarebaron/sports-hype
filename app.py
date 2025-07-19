
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

def abbreviate_name(full_name):
    names = full_name.split()
    if len(names) > 1:
        return f"{names[0][0]}. {' '.join(names[1:])}"
    return full_name

st.title("DraftKings Ownership Visualizer")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Extract the relevant columns by header names in known positions
    try:
        df = df[["Player", "%Drafted"]]
    except KeyError:
        # Try to get them by column letters if needed
        df = df.iloc[1:, [7, 9]]  # H=7, J=9
        df.columns = ["Player", "%Drafted"]

    df = df.dropna(subset=["Player", "%Drafted"])
    df["Player"] = df["Player"].apply(abbreviate_name)
    df["%Drafted"] = df["%Drafted"].astype(str).str.replace('%','').astype(float)

    df = df.groupby("Player", as_index=False)["%Drafted"].mean()
    df_sorted = df.sort_values(by="%Drafted", ascending=False)
    top_15 = df_sorted.head(15)
    bottom_15 = df_sorted.tail(15)

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    # Add DraftKings logo
    try:
        logo = Image.open("draftkings_logo.png")
        fig.figimage(logo, xo=fig.bbox.xmax//2 - 150, yo=fig.bbox.ymax - 100, zorder=10)
    except FileNotFoundError:
        pass

    ax.text(0.02, 1.02, "PLAYER", fontsize=16, color='orange', fontweight='bold', transform=ax.transAxes)
    ax.text(0.28, 1.02, "%DRAFTED", fontsize=16, color='lime', fontweight='bold', transform=ax.transAxes)
    ax.text(0.72, 1.02, "%DRAFTED", fontsize=16, color='lime', fontweight='bold', transform=ax.transAxes)

    for i in range(15):
        ax.text(0.02, 0.95 - i * 0.055, top_15.iloc[i]["Player"], fontsize=13, color='white', transform=ax.transAxes)
        ax.text(0.28, 0.95 - i * 0.055, f'{top_15.iloc[i]["%Drafted"]:.2f}%', fontsize=13, color='lime', transform=ax.transAxes)

        ax.text(0.52, 0.95 - i * 0.055, bottom_15.iloc[i]["Player"], fontsize=13, color='white', transform=ax.transAxes)
        ax.text(0.72, 0.95 - i * 0.055, f'{bottom_15.iloc[i]["%Drafted"]:.2f}%', fontsize=13, color='lime', transform=ax.transAxes)

    ax.axis("off")
    st.pyplot(fig)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    st.download_button("Download PNG", data=buf.getvalue(), file_name="draftkings_ownership.png", mime="image/png")
