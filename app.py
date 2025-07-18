
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="DraftKings CSV Visualizer")

st.title("🏈 DraftKings CSV Visualizer")
st.caption("Upload DraftKings CSV")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def abbreviate_name(name):
    if pd.isna(name) or not isinstance(name, str):
        return ""
    parts = name.split()
    if len(parts) == 1:
        return parts[0][:4]
    return parts[0][0] + parts[-1][:3]

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show DataFrame header for troubleshooting
    st.subheader("CSV Preview")
    st.dataframe(df.head())

    # Attempt to find ownership column
    possible_columns = ["Drafted", "Own%", "Ownership", "Ownership %"]
    ownership_column = None
    for col in df.columns:
        if col.strip() in possible_columns:
            ownership_column = col
            break

    if not ownership_column:
        st.error("❌ Could not find an ownership percentage column. Please ensure your CSV includes one of the following: Drafted, Own%, Ownership.")
    elif "Player" not in df.columns:
        st.error("❌ Could not find a 'Player' column. Please check your CSV formatting.")
    else:
        ownership_df = df.groupby("Player")[ownership_column].mean().reset_index()
        ownership_df["ShortName"] = ownership_df["Player"].apply(abbreviate_name)
        ownership_df = ownership_df.sort_values(by=ownership_column, ascending=True)

        fig, ax = plt.subplots(figsize=(8, max(4, 0.4 * len(ownership_df))))
        y_pos = range(len(ownership_df))
        ax.barh(y_pos, ownership_df[ownership_column], color='mediumseagreen')
        for i, (value, label) in enumerate(zip(ownership_df[ownership_column], ownership_df["ShortName"])):
            ax.text(value + 0.5, i, f"{value:.2f}%", va='center', fontsize=10)
            ax.text(0.1, i, label, va='center', fontsize=10, color='white')

        ax.set_yticks([])
        ax.set_xlim(0, max(100, ownership_df[ownership_column].max() + 10))
        ax.set_title("Player Ownership Percentages", fontsize=14)
        ax.set_xlabel("Percent Drafted")
        ax.set_facecolor("#222222")
        fig.patch.set_facecolor("#222222")
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.title.set_color('white')

        st.pyplot(fig)

        # PNG download button
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 Download Chart as PNG",
            data=buf.getvalue(),
            file_name="ownership_chart.png",
            mime="image/png"
        )
