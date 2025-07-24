import streamlit as st
import pandas as pd
import base64

# Page config
st.set_page_config(page_title="DraftKings Ownership", page_icon=":bar_chart:", layout="centered")

# Inject custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');

    .glow-container {
        margin-top: 30px;
        border: 3px solid #00FF00;
        padding: 25px 40px 10px 40px;
        border-radius: 20px;
        box-shadow: 0 0 20px #00FF00, 0 0 40px #FFA500;
        background-color: #111111;
    }

    .glow-container h3 {
        font-family: 'Roboto', sans-serif;
        color: white;
        text-align: center;
        margin-top: 0;
    }

    .dataframe {
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
        color: white;
    }

    .download-button {
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Logo Header
st.image("DraftKings Ownership.png", use_column_width=True)

# Upload Section
st.subheader("Upload DraftKings CSV")
uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df[["PLAYER", "DRAFT"]]
    df = df.sort_values(by="DRAFT", ascending=False)

    mid = len(df) // 2 + len(df) % 2
    left_df = df.iloc[:mid].reset_index(drop=True)
    right_df = df.iloc[mid:].reset_index(drop=True)

    def make_rows(ldf, rdf):
        rows = ""
        for i in range(len(ldf)):
            left_player = ldf.loc[i, "PLAYER"]
            left_draft = f"{ldf.loc[i, 'DRAFT']:.2f}%"
            if i < len(rdf):
                right_player = rdf.loc[i, "PLAYER"]
                right_draft = f"{rdf.loc[i, 'DRAFT']:.2f}%"
            else:
                right_player = ""
                right_draft = ""
            rows += f"<tr><td style='color:orange;font-weight:bold'>{left_player}</td><td style='color:limegreen;font-weight:bold'>{left_draft}</td><td style='color:orange;font-weight:bold'>{right_player}</td><td style='color:limegreen;font-weight:bold'>{right_draft}</td></tr>"
        return rows

    rows_html = make_rows(left_df, right_df)

    csv_data = uploaded_file.getvalue()
    b64_csv = base64.b64encode(csv_data).decode()

    html = f"""
    <div class="glow-container">
        <table style='width:100%; text-align:left; border-collapse:separate; border-spacing: 60px 10px'>
            <thead>
                <tr>
                    <th style='color:orange;font-size:18px;'>PLAYER</th>
                    <th style='color:limegreen;font-size:18px;'>DRAFT</th>
                    <th style='color:orange;font-size:18px;'>PLAYER</th>
                    <th style='color:limegreen;font-size:18px;'>DRAFT</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        <div class='download-button'>
            <a href="data:file/csv;base64,{b64_csv}" download="ownership_report.csv">
                <button style='background-color: #444444; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;'>Download Ownership Report</button>
            </a>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)