import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Page setup
st.set_page_config(layout="centered", page_title="DraftKings Ownership Report")

# File uploader
uploaded_file = st.file_uploader("Upload DraftKings CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df[["Name + ID", "%Drafted"]]
    df.columns = ["PLAYER", "%DRAFTED"]
    df = df.sort_values(by="%DRAFTED", ascending=False).head(30)

    # Prepare data for columns
    midpoint = len(df) // 2
    left_df = df.iloc[:midpoint].reset_index(drop=True)
    right_df = df.iloc[midpoint:].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")
    ax.axis("off")

    # Font properties
    font = fm.FontProperties(family="monospace", size=13)

    # Headers
    ax.text(0.08, 1.0, "PLAYER", fontproperties=font, color="#ff6600", weight='bold')
    ax.text(0.34, 1.0, "%DRAFTED", fontproperties=font, color="#00ffaa", weight='bold')
    ax.text(0.60, 1.0, "PLAYER", fontproperties=font, color="#ff6600", weight='bold')
    ax.text(0.86, 1.0, "%DRAFTED", fontproperties=font, color="#00ffaa", weight='bold')

    # Rows
    row_height = 0.045
    for i in range(len(left_df)):
        y = 0.95 - i * row_height
        ax.text(0.08, y, f"{left_df.loc[i, 'PLAYER']}", fontproperties=font, color="white")
        ax.text(0.34, y, f"{left_df.loc[i, '%DRAFTED']:.2f}%", fontproperties=font, color="white", ha='right')
        ax.text(0.60, y, f"{right_df.loc[i, 'PLAYER']}", fontproperties=font, color="white")
        ax.text(0.86, y, f"{right_df.loc[i, '%DRAFTED']:.2f}%", fontproperties=font, color="white", ha='right')

    st.pyplot(fig)
