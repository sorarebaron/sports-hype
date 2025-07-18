
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("DraftKings CSV Visualizer")
st.markdown("### Upload DraftKings CSV")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Drop rows with missing player names
    df = df.dropna(subset=["Player"])

    # Only keep necessary columns
    display_df = df[["Player", "Drafted"]].copy()

    # Sort by Drafted %
    display_df.sort_values(by="Drafted", ascending=False, inplace=True)

    # Plot
    fig, ax = plt.subplots(figsize=(8, len(display_df) * 0.4))
    bars = ax.barh(display_df["Player"], display_df["Drafted"], color="lime")
    ax.invert_yaxis()
    ax.set_xlabel("Drafted %")
    ax.set_title("Ownership Percentages by Fighter")
    for i, (name, pct) in enumerate(zip(display_df["Player"], display_df["Drafted"])):
        ax.text(pct + 0.5, i, f"{pct:.2f}%", va="center", fontsize=10, color="black")

    st.pyplot(fig)
