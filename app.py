
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import textwrap
import io

# DraftKings color scheme
DK_ORANGE = "#f6881f"
DK_GREEN = "#86c13d"
DK_BLACK = "#1c1c1c"
WHITE = "#ffffff"

# Layout config
st.set_page_config(layout="wide")

st.title("DraftKings Ownership Visualizer")

uploaded_file = st.file_uploader("Upload a DraftKings CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "Player" not in df.columns or "%Drafted" not in df.columns:
        st.error("CSV must contain 'Player' and '%Drafted' columns.")
    else:
        # Sort by ownership
        df = df.sort_values(by="%Drafted", ascending=False).reset_index(drop=True)

        # Shorten long names for MMA
        def abbreviate_name(name):
            parts = name.split()
            if len(name) > 20 and len(parts) >= 2:
                return f"{parts[0][0]}. {' '.join(parts[1:])}"
            return name

        df["ShortName"] = df["Player"].apply(abbreviate_name)

        # Create figure
        fig, ax = plt.subplots(figsize=(10, len(df) * 0.45 + 2))
        ax.set_facecolor(DK_BLACK)
        fig.patch.set_facecolor(DK_BLACK)

        # Add logo
        try:
            logo = Image.open("draftkings_logo.png")
            ax.imshow(logo, extent=[0.25, 1.75, len(df)*0.45 + 0.8, len(df)*0.45 + 2], aspect='auto')
        except:
            st.warning("Logo not found. Upload 'draftkings_logo.png' in the same directory as this app.")

        # Draw each player row
        for i, row in df.iterrows():
            y = len(df)*0.45 - i * 0.45
            ax.text(0.25, y, row["ShortName"], fontsize=12, color=DK_ORANGE, va="center", fontweight='bold')
            ax.text(1.75, y, f"{row['%Drafted']:.1f}%", fontsize=12, color=WHITE, va="center", ha="right")

        # Headers
        ax.text(0.25, len(df)*0.45 + 0.3, "PLAYER", fontsize=14, color=DK_ORANGE, fontweight='bold')
        ax.text(1.75, len(df)*0.45 + 0.3, "%DRAFTED", fontsize=14, color=WHITE, ha="right", fontweight='bold')

        ax.axis("off")

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", dpi=150, facecolor=fig.get_facecolor())
        st.image(buf, caption="DraftKings Ownership Chart", use_column_width=True)

        # Download button
        buf.seek(0)
        st.download_button("Download PNG", data=buf, file_name="draftkings_ownership.png", mime="image/png")
