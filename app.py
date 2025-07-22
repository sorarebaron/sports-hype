
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Constants
BACKGROUND_COLOR = "#1a1a1a"
TEXT_COLOR = "white"
ORANGE = "#F6770E"
GREEN = "#61B50E"
MAX_FIGHTERS = 50
MAX_NAME_LENGTH = 16

# App Title
st.set_page_config(page_title="DraftKings Ownership Report", layout="centered")
st.title("👑 DraftKings Ownership Report")

# File uploader
uploaded_file = st.file_uploader("Upload DraftKings CSV", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Assume player names are in column H (index 7) and %Drafted in J (index 9)
        df = df.iloc[:, [7, 9]]
        df.columns = ["PLAYER", "%DRAFTED"]
        df.dropna(inplace=True)
        df["%DRAFTED"] = df["%DRAFTED"].str.rstrip("%").astype(float)
        df = df.sort_values(by="%DRAFTED", ascending=False).reset_index(drop=True)
        df = df.head(MAX_FIGHTERS)

        # Abbreviate long names
        def abbreviate_name(name):
            if len(name) > MAX_NAME_LENGTH:
                parts = name.split()
                if len(parts) >= 2:
                    return f"{parts[0][0]}. {' '.join(parts[1:])}"
            return name

        df["PLAYER"] = df["PLAYER"].apply(abbreviate_name)

        # Prepare for two-column layout
        half = (len(df) + 1) // 2
        left_col = df.iloc[:half].reset_index(drop=True)
        right_col = df.iloc[half:].reset_index(drop=True)

        fig, ax = plt.subplots(figsize=(10, 8), facecolor=BACKGROUND_COLOR)
        ax.set_facecolor(BACKGROUND_COLOR)
        ax.axis("off")

        # Headers
        ax.text(0.10, 0.94, "PLAYER", color=ORANGE, fontsize=16, fontweight="bold", ha="left")
        ax.text(0.42, 0.94, "DRAFT%", color=GREEN, fontsize=16, fontweight="bold", ha="right")
        ax.text(0.58, 0.94, "PLAYER", color=ORANGE, fontsize=16, fontweight="bold", ha="left")
        ax.text(0.90, 0.94, "DRAFT%", color=GREEN, fontsize=16, fontweight="bold", ha="right")

        # Draw fighter names and ownership
        for i in range(len(left_col)):
            y = 0.9 - i * 0.035
            ax.text(0.10, y, left_col.at[i, "PLAYER"], color=TEXT_COLOR, fontsize=13, ha="left")
            ax.text(0.42, y, f'{left_col.at[i, "%DRAFTED"]:.2f}%', color=TEXT_COLOR, fontsize=13, ha="right")
        for i in range(len(right_col)):
            y = 0.9 - i * 0.035
            ax.text(0.58, y, right_col.at[i, "PLAYER"], color=TEXT_COLOR, fontsize=13, ha="left")
            ax.text(0.90, y, f'{right_col.at[i, "%DRAFTED"]:.2f}%', color=TEXT_COLOR, fontsize=13, ha="right")

        # Save to file
        output_file = "draftkings_ownership_final.png"
        plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
        st.image(output_file)
        with open(output_file, "rb") as f:
            st.download_button("Download Ownership Report", f, file_name=output_file, mime="image/png")

    except Exception as e:
        st.error(f"Error processing file: {e}")
