
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os

# Set page configuration
st.set_page_config(page_title="DraftKings Ownership Viewer", layout="wide")

# Upload CSV
uploaded_file = st.file_uploader("Upload DraftKings CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df[["Player", "%Drafted"]]

    # Sort by %Drafted descending
    df["%Drafted"] = df["%Drafted"].str.rstrip('%').astype(float)
    df = df.sort_values(by="%Drafted", ascending=False).reset_index(drop=True)

    # Abbreviate long player names
    def abbreviate_name(name, limit=20):
        if len(name) > limit:
            parts = name.split()
            if len(parts) > 1:
                return f"{parts[0][0]}. {' '.join(parts[1:])}"
        return name
    df["Player"] = df["Player"].apply(abbreviate_name)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    plt.axis("off")

    # Load and plot DraftKings logo
    logo_path = "draftkings_logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        ax.imshow(logo, extent=[0, 8, len(df) + 2, len(df) + 6], aspect='auto', zorder=-1)

    # Header
    ax.text(0.2, len(df) + 1, "PLAYER", fontsize=14, fontweight='bold', color='#FD652F')
    ax.text(6.5, len(df) + 1, "%DRAFTED", fontsize=14, fontweight='bold', color='white', ha='right')

    # Plot data
    for i, row in df.iterrows():
        ax.text(0.2, len(df) - i, row["Player"], fontsize=13, color='white', va='center')
        ax.text(6.5, len(df) - i, f'{row["%Drafted"]:.1f}%', fontsize=13, color='white', ha='right', va='center')

    # Save output
    output_path = "/mnt/data/ownership_graphic.png"
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.3)
    st.image(output_path, caption="Ownership Graphic", use_column_width=True)
    with open(output_path, "rb") as f:
        st.download_button("Download Image", f, file_name="ownership_graphic.png", mime="image/png")
