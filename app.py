
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import base64

st.set_page_config(layout="wide")

st.title("DraftKings CSV Visualizer")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Ensure required columns exist
    if "Player" in df.columns and "%Drafted" in df.columns:
        df = df.dropna(subset=["Player", "%Drafted"])

        # Sort by %Drafted descending
        df = df.sort_values(by="%Drafted", ascending=False)

        # Split into two columns
        mid_point = len(df) // 2
        left_df = df.iloc[:mid_point]
        right_df = df.iloc[mid_point:]

        # Set up the plot
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.axis('off')

        # Headers
        ax.text(0.05, 1.02, "PLAYER", color='orange', fontsize=14, fontweight='bold', transform=ax.transAxes)
        ax.text(0.35, 1.02, "%DRAFTED", color='lime', fontsize=14, fontweight='bold', transform=ax.transAxes)
        ax.text(0.60, 1.02, "PLAYER", color='orange', fontsize=14, fontweight='bold', transform=ax.transAxes)
        ax.text(0.90, 1.02, "%DRAFTED", color='lime', fontsize=14, fontweight='bold', transform=ax.transAxes)

        # Plot data
        for i, (idx, row) in enumerate(left_df.iterrows()):
            ax.text(0.05, 0.95 - i * 0.05, row["Player"], color='white', fontsize=12, transform=ax.transAxes)
            ax.text(0.35, 0.95 - i * 0.05, f'{row["%Drafted"]:.2f}%', color='lime', fontsize=12, transform=ax.transAxes)

        for i, (idx, row) in enumerate(right_df.iterrows()):
            ax.text(0.60, 0.95 - i * 0.05, row["Player"], color='white', fontsize=12, transform=ax.transAxes)
            ax.text(0.90, 0.95 - i * 0.05, f'{row["%Drafted"]:.2f}%', color='lime', fontsize=12, transform=ax.transAxes)

        st.pyplot(fig)

        # Save to buffer
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode()

        href = f'<a href="data:file/png;base64,{b64}" download="ownership_graphic.png">📥 Download PNG</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.error("CSV must contain 'Player' and '%Drafted' columns.")
