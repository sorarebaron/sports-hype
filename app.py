
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="DraftKings Ownership")

st.title("DraftKings Ownership Visualization")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    df["%DRAFTED"] = df["%DRAFTED"].str.rstrip("%").astype(float)
    df.sort_values("%DRAFTED", ascending=False, inplace=True)

    left_col = df.iloc[:13].copy()
    right_col = df.iloc[13:].copy()

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.axis("off")

    x0, x1, x2 = 0.01, 0.4, 0.65
    y = 0.95
    line_height = 0.055

    # Headers
    ax.text(x0, y, "PLAYER", fontsize=14, fontweight="bold", color="orange")
    ax.text(x1, y, "%DRAFTED", fontsize=14, fontweight="bold", color="lime")
    ax.text(x2, y, "%DRAFTED", fontsize=14, fontweight="bold", color="lime")
    ax.text(x2 + 0.17, y, "PLAYER", fontsize=14, fontweight="bold", color="orange")

    y -= line_height

    for i in range(len(left_col)):
        player_l = left_col.iloc[i]
        ax.text(x0, y, player_l["PLAYER"], fontsize=12, color="white")
        ax.text(x1, y, f"{player_l['%DRAFTED']:.2f}%", fontsize=12, color="lime")

        if i < len(right_col):
            player_r = right_col.iloc[i]
            ax.text(x2, y, f"{player_r['%DRAFTED']:.2f}%", fontsize=12, color="lime")
            ax.text(x2 + 0.17, y, player_r["PLAYER"], fontsize=12, color="white")
        y -= line_height

    st.pyplot(fig)

    # Add download button
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    st.download_button("Download Image", data=buf.getvalue(), file_name="draftkings_ownership.png", mime="image/png")
