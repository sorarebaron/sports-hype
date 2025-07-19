
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import io

st.set_page_config(layout="centered")

uploaded_file = st.file_uploader("Upload DraftKings CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Extract relevant columns from the known structure (PLAYER in col H, %DRAFTED in col J)
    player_col = df.columns[7]
    drafted_col = df.columns[9]
    player_data = df[[player_col, drafted_col]].dropna()
    player_data.columns = ["PLAYER", "%DRAFTED"]

    # Clean and format data
    player_data["%DRAFTED"] = player_data["%DRAFTED"].astype(str).str.rstrip("%").astype(float)
    player_data = player_data.drop_duplicates(subset="PLAYER")
    player_data = player_data.sort_values(by="%DRAFTED", ascending=False).reset_index(drop=True)

    # Split into two columns
    half = len(player_data) // 2 + len(player_data) % 2
    left_col = player_data.iloc[:half]
    right_col = player_data.iloc[half:]

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('black')
    ax.axis("off")

    def render_column(col_data, x, align):
        ax.text(x, 1.02, "PLAYER", fontsize=16, color="orange", ha=align, weight="bold")
        ax.text(x + 0.12 if align == "left" else x - 0.12, 1.02, "%DRAFTED", fontsize=16, color="lime", ha=align, weight="bold")
        for i, row in enumerate(col_data.itertuples()):
            ax.text(x, 1 - i * 0.05, row.PLAYER, fontsize=14, color="white", ha=align,
                    path_effects=[path_effects.withStroke(linewidth=3, foreground="black")])
            ax.text(x + 0.12 if align == "left" else x - 0.12, 1 - i * 0.05, f"{row._2:.2f}%", fontsize=14, color="lime", ha=align,
                    path_effects=[path_effects.withStroke(linewidth=3, foreground="black")])

    render_column(left_col, 0.05, "left")
    render_column(right_col, 0.95, "right")

    st.pyplot(fig)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    st.download_button("Download Image", data=buf.getvalue(), file_name="draftkings_ownership.png", mime="image/png")
