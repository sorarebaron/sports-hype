
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.title("DraftKings CSV Visualizer")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "Player" in df.columns and "%Drafted" in df.columns:
        df = df[["Player", "%Drafted"]].dropna()
        df = df.sort_values(by="%Drafted", ascending=False)

        fig, ax = plt.subplots(figsize=(6, 10))
        ax.axis("off")

        for i, row in enumerate(df.iterrows()):
            player, drafted_pct = row[1]["Player"], row[1]["%Drafted"]
            y_pos = 0.95 - i * 0.05
            ax.text(0.05, y_pos, f'{player}', color='orange', fontsize=14, fontweight='bold', transform=ax.transAxes)
            ax.text(0.8, y_pos, f'{drafted_pct:.2f}%', color='lime', fontsize=14, transform=ax.transAxes)

        st.pyplot(fig)
    else:
        st.error("CSV must include 'Player' and '%Drafted' columns.")
