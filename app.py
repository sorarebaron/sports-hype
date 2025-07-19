
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

def abbreviate_name(full_name):
    names = full_name.split()
    if len(names) > 1:
        return f"{names[0][0]}. {' '.join(names[1:])}"
    return full_name

def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.getvalue()

st.title("DraftKings Ownership Visualizer")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Extract Player and %Drafted from specific columns (H and J)
    df = df.iloc[1:]  # Skip header row if needed
    df = df.reset_index(drop=True)

    df["Player"] = df.iloc[:, 7]  # Column H = index 7
    df["%Drafted"] = df.iloc[:, 9]  # Column J = index 9

    df = df.dropna(subset=["Player", "%Drafted"])
    df["Player"] = df["Player"].apply(abbreviate_name)
    df["%Drafted"] = df["%Drafted"].astype(str).str.replace('%','').astype(float)

    # Sort and split
    df_sorted = df.sort_values(by="%Drafted", ascending=False)
    top_15 = df_sorted.head(15)
    bottom_15 = df_sorted.tail(15)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    # Headers
    ax.text(0.02, 1.05, "PLAYER", fontsize=16, color='orange', fontweight='bold', transform=ax.transAxes)
    ax.text(0.28, 1.05, "%DRAFTED", fontsize=16, color='lime', fontweight='bold', transform=ax.transAxes)
    ax.text(0.52, 1.05, "PLAYER", fontsize=16, color='orange', fontweight='bold', transform=ax.transAxes)
    ax.text(0.72, 1.05, "%DRAFTED", fontsize=16, color='lime', fontweight='bold', transform=ax.transAxes)

    # Rows
    for i in range(15):
        ax.text(0.02, 1 - (i + 1) * 0.06, top_15.iloc[i]["Player"], fontsize=14, color='white', transform=ax.transAxes)
        ax.text(0.28, 1 - (i + 1) * 0.06, f'{top_15.iloc[i]["%Drafted"]:.2f}%', fontsize=14, color='lime', transform=ax.transAxes)

        ax.text(0.52, 1 - (i + 1) * 0.06, bottom_15.iloc[i]["Player"], fontsize=14, color='white', transform=ax.transAxes)
        ax.text(0.72, 1 - (i + 1) * 0.06, f'{bottom_15.iloc[i]["%Drafted"]:.2f}%', fontsize=14, color='lime', transform=ax.transAxes)

    ax.axis("off")
    st.pyplot(fig)

    # Download PNG button
    st.download_button("Download Image", data=fig_to_bytes(fig), file_name="draftkings_ownership.png", mime="image/png")
