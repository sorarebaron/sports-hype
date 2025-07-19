import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Read the CSV file
file_path = "ownership_data.csv"
df = pd.read_csv(file_path)

# Extract PLAYER and %DRAFTED columns using known column names
df = df[['PLAYER', '%DRAFTED']].drop_duplicates()
df = df.sort_values(by='%DRAFTED', ascending=False).reset_index(drop=True)

# Convert %DRAFTED to float for sorting
df['%DRAFTED'] = df['%DRAFTED'].str.rstrip('%').astype(float)

# Sort again after conversion
df = df.sort_values(by='%DRAFTED', ascending=False)

# Reset index for display
df.reset_index(drop=True, inplace=True)

# Format %DRAFTED for display
df['%DRAFTED'] = df['%DRAFTED'].map(lambda x: f"{x:.2f}%")

# Split into two columns for display
half = len(df) // 2 + len(df) % 2
left_df = df.iloc[:half].reset_index(drop=True)
right_df = df.iloc[half:].reset_index(drop=True)

# Start plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.axis('off')

# Define column headers
headers = ['PLAYER', '%DRAFTED']

# Column positions
x_positions = [0.05, 0.45, 0.65, 0.85]

# Add headers
for i, header in enumerate(headers):
    ax.text(x_positions[i], 1.0, header, color='orange' if header == 'PLAYER' else 'lime', fontsize=14, fontweight='bold', ha='left' if i % 2 == 0 else 'right', transform=ax.transAxes)

# Add text data for left and right columns
for i in range(max(len(left_df), len(right_df))):
    y = 0.95 - i * 0.05
    if i < len(left_df):
        ax.text(x_positions[0], y, left_df.loc[i, 'PLAYER'], color='white', fontsize=12, ha='left', transform=ax.transAxes)
        ax.text(x_positions[1], y, left_df.loc[i, '%DRAFTED'], color='lime', fontsize=12, ha='right', transform=ax.transAxes)
    if i < len(right_df):
        ax.text(x_positions[2], y, right_df.loc[i, '%DRAFTED'], color='lime', fontsize=12, ha='right', transform=ax.transAxes)
        ax.text(x_positions[3], y, right_df.loc[i, 'PLAYER'], color='white', fontsize=12, ha='right', transform=ax.transAxes)

# Save the figure
output_path = "/mnt/data/draftkings_ownership_clean.py"
plt.savefig("/mnt/data/draftkings_ownership_clean.png", bbox_inches='tight', facecolor=fig.get_facecolor())

# Write the Python script file
with open(output_path, "w") as file:
    file.write(script_content)

output_path