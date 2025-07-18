
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# DraftKings theme
bg_color = '#0D0D0D'
orange = '#FF6F00'
green = '#7ED321'
white = '#FFFFFF'

st.set_page_config(page_title="DFS MMA Ownership Report", layout="centered")
st.markdown("""
    <style>
    body {background-color: #0D0D0D; color: white;}
    .css-1d391kg, .css-1v0mbdj, .css-1dp5vir, .stMarkdown {color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("🏆 DFS MMA Ownership Report Generator")

uploaded_file = st.file_uploader("Upload your DraftKings MMA CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    ownership_df = df[df["%Drafted"].notnull()][["Player", "%Drafted"]].dropna().reset_index(drop=True)
    ownership_df["Ownership"] = ownership_df["%Drafted"].str.replace('%', '').astype(float)
    ownership_df = ownership_df.sort_values(by="Ownership", ascending=False).reset_index(drop=True)

    midpoint = (len(ownership_df) + 1) // 2
    left_col = ownership_df.iloc[:midpoint].reset_index(drop=True)
    right_col = ownership_df.iloc[midpoint:].reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 6.75))
    fig.patch.set_facecolor(bg_color)
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor=bg_color, edgecolor=orange, linewidth=6))
    ax.axis('off')

    ax.text(0.1, 0.96, "PLAYER", fontsize=18, color=orange, fontweight='bold')
    ax.text(0.4, 0.96, "%DRAFTED", fontsize=18, color=green, fontweight='bold', ha='right')
    ax.text(0.6, 0.96, "PLAYER", fontsize=18, color=orange, fontweight='bold')
    ax.text(0.9, 0.96, "%DRAFTED", fontsize=18, color=green, fontweight='bold', ha='right')

    row_fontsize = 16
    row_spacing = 0.036
    start_y = 0.91

    for i in range(len(left_col)):
        y = start_y - i * row_spacing
        ax.text(0.1, y, left_col.loc[i, "Player"], fontsize=row_fontsize, color=white)
        ax.text(0.4, y, f'{left_col.loc[i, "Ownership"]:.2f}%', fontsize=row_fontsize, color=green, ha='right')

    for i in range(len(right_col)):
        y = start_y - i * row_spacing
        ax.text(0.6, y, right_col.loc[i, "Player"], fontsize=row_fontsize, color=white)
        ax.text(0.9, y, f'{right_col.loc[i, "Ownership"]:.2f}%', fontsize=row_fontsize, color=green, ha='right')

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    st.download_button(
        label="📥 Download PNG",
        data=buf.getvalue(),
        file_name="dfs_mma_ownership.png",
        mime="image/png"
    )
