
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO

st.set_page_config(layout="wide")
st.title("DraftKings CSV Visualizer")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Drop rows missing player name or %Drafted (robustly handle errors)
    if "Player" not in df.columns or "%Drafted" not in df.columns:
        st.error("CSV must contain 'Player' and '%Drafted' columns.")
    else:
        df = df.dropna(subset=["Player", "%Drafted"])
        df = df.sort_values(by="%Drafted", ascending=False).reset_index(drop=True)

        fig, ax = plt.subplots(figsize=(8, len(df) * 0.4))
        ax.set_facecolor("black")
        ax.axis("off")

        for i, row in df.iterrows():
            y_pos = 0.95 - i * 0.05
            ax.text(0.05, y_pos, row["Player"], color="orange", fontsize=14, transform=ax.transAxes)
            try:
                ax.text(0.35, y_pos, f'{row["%Drafted"]:.2f}%', color="lime", fontsize=14, transform=ax.transAxes)
            except Exception:
                ax.text(0.35, y_pos, "N/A", color="red", fontsize=14, transform=ax.transAxes)

        st.pyplot(fig)
