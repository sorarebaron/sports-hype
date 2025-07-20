
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import io

st.set_page_config(layout="wide")

st.title("DraftKings MMA Ownership Report")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type="csv")
if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)

    # Extract PLAYER and %DRAFTED from columns H and J
    df = df_raw.iloc[1:, [7, 9]].copy()
    df.columns = ["PLAYER", "%DRAFTED"]
    df.dropna(inplace=True)
    df["%DRAFTED"] = df["%DRAFTED"].astype(str).str.rstrip("%").astype(float)
    df = df.sort_values(by="%DRAFTED", ascending=False).reset_index(drop=True)

    # Split into two columns
    mid = len(df) // 2 + len(df) % 2
    df1 = df.iloc[:mid].reset_index(drop=True)
    df2 = df.iloc[mid:].reset_index(drop=True)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.axis("off")
    ax.add_patch(Rectangle((0, 1.02), 1, 0.08, color="orange", transform=ax.transAxes))

    ax.text(0.22, 1.07, "PLAYER", fontsize=12, fontweight="bold", transform=ax.transAxes)
    ax.text(0.72, 1.07, "PLAYER", fontsize=12, fontweight="bold", transform=ax.transAxes)

    for i in range(len(df1)):
        ax.text(0.05, 1 - (i + 1) * 0.04, f"{df1['PLAYER'][i]}", fontsize=10, transform=ax.transAxes)
        ax.text(0.45, 1 - (i + 1) * 0.04, f"{df1['%DRAFTED'][i]:.1f}%", fontsize=10, transform=ax.transAxes)

    for i in range(len(df2)):
        ax.text(0.55, 1 - (i + 1) * 0.04, f"{df2['PLAYER'][i]}", fontsize=10, transform=ax.transAxes)
        ax.text(0.95, 1 - (i + 1) * 0.04, f"{df2['%DRAFTED'][i]:.1f}%", fontsize=10, transform=ax.transAxes)

    st.pyplot(fig)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    st.download_button("Download PNG", data=buf.getvalue(), file_name="draftkings_ownership.png", mime="image/png")
