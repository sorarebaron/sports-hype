
import streamlit as st
import pandas as pd

# Page config
st.set_page_config(layout="wide", page_title="DraftKings Ownership Report")

st.markdown(
    "<h1 style='text-align: center; color: #FF6600;'>DraftKings Ownership</h1>",
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Upload DraftKings CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Ensure proper column names (case-insensitive)
    df.columns = [col.strip() for col in df.columns]
    if "Name + ID" in df.columns:
        df = df.rename(columns={"Name + ID": "Player"})

    if "Player" not in df.columns or "%Drafted" not in df.columns:
        st.error("CSV must contain 'Player' and '%Drafted' columns.")
    else:
        df = df[["Player", "%Drafted"]]
        df = df.dropna()
        df["%Drafted"] = df["%Drafted"].apply(lambda x: f"{float(x):.2f}%")

        # Sort by %Drafted descending
        df = df.sort_values(by="%Drafted", ascending=False).reset_index(drop=True)

        # Split into two columns
        mid = len(df) // 2 + len(df) % 2
        left_df = df.iloc[:mid]
        right_df = df.iloc[mid:]

        col1, col2 = st.columns(2)

        def render_column(column, data, side_label):
            with column:
                st.markdown(
                    f"<div style='font-weight:bold; font-size:22px; color:#FF6600;'>PLAYER</div>"
                    f"<div style='font-weight:bold; font-size:22px; color:#00FFCC;'>%DRAFTED</div>",
                    unsafe_allow_html=True,
                )
                for i, row in data.iterrows():
                    st.markdown(
                        f"<div style='display:flex; justify-content:space-between; font-size:20px;'>"
                        f"<span style='color:white;'>{row['Player']}</span>"
                        f"<span style='color:white;'>{row['%Drafted']}</span></div>",
                        unsafe_allow_html=True,
                    )

        render_column(col1, left_df, "Left")
        render_column(col2, right_df, "Right")
