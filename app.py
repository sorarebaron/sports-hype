
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def abbreviate_name(full_name):
    if pd.isnull(full_name):
        return ""
    names = full_name.split()
    if len(names) > 1:
        return f"{names[0][0]}. {' '.join(names[1:])}"
    return full_name

st.title("DraftKings Ownership Chart - MMA Optimized")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type="csv")

if uploaded_file is not None:
    # Load only needed columns (H and J are the 8th and 10th columns respectively, so use usecols)
    df = pd.read_csv(uploaded_file, usecols=[7, 9], skiprows=1, names=["Player", "%Drafted"])

    df.dropna(subset=["Player", "%Drafted"], inplace=True)
    df["%Drafted"] = df["%Drafted"].astype(str).str.replace('%', '').astype(float)
    df["Player"] = df["Player"].apply(abbreviate_name)

    # Sort and split
    df_sorted = df.sort_values(by="%Drafted", ascending=False)
    top_15 = df_sorted.head(15)
    bottom_15 = df_sorted.tail(15)

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    # Headers
    ax.text(0.02, 1.05, "PLAYER", fontsize=16, color='orange', fontweight='bold', transform=ax.transAxes)
    ax.text(0.28, 1.05, "%DRAFTED", fontsize=16, color='lime', fontweight='bold', transform=ax.transAxes)
    ax.text(0.72, 1.05, "PLAYER", fontsize=16, color='orange', fontweight='bold', transform=ax.transAxes)
    ax.text(0.98, 1.05, "%DRAFTED", fontsize=16, color='lime', fontweight='bold', transform=ax.transAxes, ha='right')

    # Rows
    for i in range(15):
        ax.text(0.02, 1 - (i + 1) * 0.06, top_15.iloc[i]["Player"], fontsize=14, color='white', transform=ax.transAxes)
        ax.text(0.28, 1 - (i + 1) * 0.06, f'{top_15.iloc[i]["%Drafted"]:.2f}%', fontsize=14, color='lime', transform=ax.transAxes)

        ax.text(0.72, 1 - (i + 1) * 0.06, bottom_15.iloc[i]["Player"], fontsize=14, color='white', transform=ax.transAxes)
        ax.text(0.98, 1 - (i + 1) * 0.06, f'{bottom_15.iloc[i]["%Drafted"]:.2f}%', fontsize=14, color='lime', transform=ax.transAxes, ha='right')

    ax.axis("off")
    st.pyplot(fig)
    st.download_button("Download Image", data=fig_to_bytes(fig), file_name="draftkings_ownership.png", mime="image/png")

# Helper to convert figure to bytes
def fig_to_bytes(fig):
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return buf
