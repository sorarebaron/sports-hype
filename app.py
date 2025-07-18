
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

st.set_page_config(page_title="DraftKings CSV Visualizer", layout="centered")

st.title("DraftKings CSV Visualizer")
st.caption("Upload DraftKings CSV")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def abbreviate_name(name):
    if isinstance(name, str):
        parts = name.split()
        if len(parts) == 0:
            return ""
        elif len(parts) == 1:
            return parts[0][:4]
        else:
            return parts[0][0] + parts[-1][:4]
    else:
        return ""

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["ShortName"] = df["Player"].apply(abbreviate_name)

    ownership_df = df.groupby("Player")["Drafted"].mean().reset_index()
    ownership_df = ownership_df.sort_values(by="Drafted", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 0.4 * len(ownership_df)))
    y_pos = range(len(ownership_df))
    ax.barh(y_pos, ownership_df["Drafted"], color="green")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ownership_df["Player"])
    ax.invert_yaxis()
    ax.set_xlabel("Ownership %")
    ax.set_title("Player Ownership")

    for i, (val, name) in enumerate(zip(ownership_df["Drafted"], ownership_df["Player"])):
        ax.text(val + 0.5, i, f"{val:.2f}%", va="center", color="black")

    st.pyplot(fig)

    # Save the plot as a PNG in memory
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="ownership_plot.png">Download Ownership Chart</a>'
    st.markdown(href, unsafe_allow_html=True)
