
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# Set page config
st.set_page_config(page_title="DraftKings Ownership", layout="centered")

# Load your data
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Filter out placeholders
    df = df[~df['Name + ID'].str.contains("Fighter 29|Fighter 30")]

    # Keep only relevant columns
    df = df[["Name + ID", "%Drafted"]]

    # Convert to list of tuples
    data = list(df.itertuples(index=False, name=None))

    # Split into two columns
    midpoint = (len(data) + 1) // 2
    col1_data = data[:midpoint]
    col2_data = data[midpoint:]

    # Create image
    img_width, img_height = 960, 480
    background_color = (15, 15, 15)
    image = Image.new("RGB", (img_width, img_height), color=background_color)
    draw = ImageDraw.Draw(image)

    # Fonts
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"  # Use monospaced font
    header_font = ImageFont.truetype(font_path, 36)
    data_font = ImageFont.truetype(font_path, 28)

    # Colors
    orange = (255, 100, 0)
    green = (0, 255, 180)
    white = (255, 255, 255)

    # Header positions
    draw.text((80, 30), "PLAYER", fill=orange, font=header_font)
    draw.text((340, 30), "%DRAFTED", fill=green, font=header_font)
    draw.text((560, 30), "PLAYER", fill=orange, font=header_font)
    draw.text((820, 30), "%DRAFTED", fill=green, font=header_font)

    # Draw each row
    row_height = 40
    for i, (name, percent) in enumerate(col1_data):
        draw.text((80, 80 + i * row_height), name.ljust(20), fill=white, font=data_font)
        draw.text((340, 80 + i * row_height), percent.rjust(6), fill=white, font=data_font)
    for i, (name, percent) in enumerate(col2_data):
        draw.text((560, 80 + i * row_height), name.ljust(20), fill=white, font=data_font)
        draw.text((820, 80 + i * row_height), percent.rjust(6), fill=white, font=data_font)

    # Display image
    st.image(image, caption="DraftKings Ownership", use_column_width=False)
