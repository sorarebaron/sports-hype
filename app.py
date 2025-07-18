
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

st.set_page_config(layout="centered", page_title="DraftKings CSV Visualizer")

st.title("DraftKings CSV Visualizer")
st.caption("Upload DraftKings CSV")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "Player" not in df.columns or "%Drafted" not in df.columns:
        st.error("CSV must include 'Player' and '%Drafted' columns.")
    else:
        df = df[["Player", "%Drafted"]]
        df = df.dropna(subset=["Player", "%Drafted"])
        df = df.sort_values(by="%Drafted", ascending=False).reset_index(drop=True)

        fig, ax = plt.subplots(figsize=(10, 12))
        ax.axis("off")

        for i, row in df.iterrows():
            y_pos = 0.95 - i * 0.035
            if y_pos < 0:
                break
            ax.text(0.01, y_pos, row["Player"], color='orange', fontsize=14, transform=ax.transAxes)
            ax.text(0.35, y_pos, f'{row["%Drafted"]:.2f}%', color='lime', fontsize=14, transform=ax.transAxes)

        ax.text(0.01, 0.98, "PLAYER", color='orange', fontsize=16, transform=ax.transAxes)
        ax.text(0.35, 0.98, "%DRAFTED", color='lime', fontsize=16, transform=ax.transAxes)

        st.pyplot(fig)

        # Convert plot to PNG for download
        buffer = BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight")
        buffer.seek(0)

        b64 = base64.b64encode(buffer.read()).decode()
        href = f'<a href="data:image/png;base64,{b64}" download="draftkings_chart.png">📥 Download PNG</a>'
        st.markdown(href, unsafe_allow_html=True)
