import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import math
import os

# Constants
TITLE = "DraftKings UFC Ownership Report"
LOGO_PATH = "draftkings_logo.png"  # Ensure this logo exists in the same directory
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Use a bold font
FONT_SIZE = 28
LINE_HEIGHT = 40
PADDING = 50
COLUMN_GAP = 100
BG_COLOR = "white"
TEXT_COLOR = "black"
IMAGE_WIDTH = 1600

# Upload CSV
st.title(TITLE)
uploaded_file = st.file_uploader("Upload the DraftKings CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Extract player names and %Drafted columns
    if "Player" in df.columns and "%Drafted" in df.columns:
        names = df["Player"].astype(str).tolist()
        drafted = df["%Drafted"].astype(str).tolist()
    else:
        st.error("CSV must contain 'Player' and '%Drafted' columns.")
        st.stop()

    # Format %Drafted as float with 2 decimals and a % sign
    def format_pct(x):
        try:
            return f"{float(x):.2f}%"
        except:
            return x

    drafted = [format_pct(x) for x in drafted]

    players = list(zip(names, drafted))

    # Split into two columns (left gets extra if odd)
    midpoint = math.ceil(len(players) / 2)
    left_col = players[:midpoint]
    right_col = players[midpoint:]

    # Image height calculation
    row_count = max(len(left_col), len(right_col))
    image_height = PADDING * 2 + LINE_HEIGHT * row_count + 200  # Extra for title/logo

    # Create image
    img = Image.new("RGB", (IMAGE_WIDTH, image_height), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Optional logo
    logo_y_offset = 30
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo_width = 300
            logo_ratio = logo_width / logo.width
            logo = logo.resize((logo_width, int(logo.height * logo_ratio)))
            img.paste(logo, ((IMAGE_WIDTH - logo.width) // 2, logo_y_offset), logo)
            content_start_y = logo_y_offset + logo.height + 40
        except Exception as e:
            content_start_y = PADDING
    else:
        content_start_y = PADDING

    # Column coordinates
    left_x = PADDING
    right_x = IMAGE_WIDTH // 2 + COLUMN_GAP // 2

    # Draw text
    for i in range(row_count):
        if i < len(left_col):
            text = f"{left_col[i][0]} - {left_col[i][1]}"
            draw.text((left_x, content_start_y + i * LINE_HEIGHT), text, fill=TEXT_COLOR, font=font)
        if i < len(right_col):
            text = f"{right_col[i][0]} - {right_col[i][1]}"
            draw.text((right_x, content_start_y + i * LINE_HEIGHT), text, fill=TEXT_COLOR, font=font)

    # Save and display
    output_path = "ownership_report.png"
    img.save(output_path)
    st.image(img, caption="DraftKings UFC Ownership Report")
    with open(output_path, "rb") as file:
        st.download_button("Download Image", file, file_name="ownership_report.png", mime="image/png")
else:
    st.info("Please upload a CSV file to begin.")
