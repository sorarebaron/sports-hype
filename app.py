
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Abbreviate long player names
def abbreviate_name(name, max_len=20):
    try:
        if len(name) > max_len:
            parts = name.split()
            if len(parts) >= 2:
                return f"{parts[0][0]}. {' '.join(parts[1:])}"
        return name
    except:
        return name

st.title("🏆 DFS MMA Ownership Report Generator")
st.write("Upload your DraftKings MMA CSV file")

uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Strip column names and drop missing data
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=["Player", "%Drafted"])

    # Convert %Drafted to float if it's not already
    df["%Drafted"] = df["%Drafted"].astype(str).str.replace('%','').astype(float)

    # Abbreviate long names
    df["Player"] = df["Player"].apply(abbreviate_name)

    # Sort descending by ownership and split into two columns
    df = df.sort_values(by="%Drafted", ascending=False).reset_index(drop=True)
    midpoint = len(df) // 2 + len(df) % 2
    left_df = df.iloc[:midpoint]
    right_df = df.iloc[midpoint:].reset_index(drop=True)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.axis('off')

    orange = '#FFA500'
    green = 'lime'

    ax.text(0.01, 1.02, "PLAYER", color=orange, fontsize=12, fontweight='bold', ha='left')
    ax.text(0.35, 1.02, "%DRAFTED", color=green, fontsize=12, fontweight='bold', ha='right')
    ax.text(0.55, 1.02, "PLAYER", color=orange, fontsize=12, fontweight='bold', ha='left')
    ax.text(0.88, 1.02, "%DRAFTED", color=green, fontsize=12, fontweight='bold', ha='right')

    for i in range(len(left_df)):
        y = 0.98 - i * 0.06
        ax.text(0.01, y, left_df.iloc[i]["Player"], color='white', fontsize=11, ha='left')
        ax.text(0.35, y, f'{left_df.iloc[i]["%Drafted"]:.2f}%', color='lime', fontsize=11, ha='right')

    for i in range(len(right_df)):
        y = 0.98 - i * 0.06
        ax.text(0.55, y, right_df.iloc[i]["Player"], color='white', fontsize=11, ha='left')
        ax.text(0.88, y, f'{right_df.iloc[i]["%Drafted"]:.2f}%', color='lime', fontsize=11, ha='right')

    # Insert DraftKings logo
    try:
        logo = Image.open("draftkings_logo.png")
        ax.imshow(logo, extent=[0.37, 0.63, -0.12, 0.05], aspect='auto', zorder=1)
    except Exception as e:
        st.warning(f"Could not load logo: {e}")

    st.pyplot(fig)
