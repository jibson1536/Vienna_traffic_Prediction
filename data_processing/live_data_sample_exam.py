import pandas as pd
import re

# Load the big file
# Note: Ensure the file is in the same folder as this script
df = pd.read_csv('/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/datsets/vienna_disruptions.csv')

# Step 1: Standardize column names (removes hidden spaces)
df.columns = df.columns.str.strip()

# Step 2: Extract the Line (U1, U6, etc.) from the 'title' column
def extract_line(text):
    if pd.isna(text): return "Unknown"
    # This looks for "U" followed by a number or the word "Linie" followed by a number
    match = re.search(r'([U]\d|Linie\s\d+)', str(text))
    return match.group(0) if match else "Other"

df['line_id'] = df['title'].apply(extract_line)

# Step 3: Convert timestamp to actual Python time objects
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Step 4: Group into unique events
# We group by the extracted 'line_id' and the 'description'
events = df.groupby(['line_id', 'description']).agg(
    start_time=('timestamp', 'min'),
    end_time=('timestamp', 'max'),
    logs_count=('timestamp', 'count')
).reset_index()

# Step 5: Calculate duration
events['duration_minutes'] = (events['end_time'] - events['start_time']).dt.total_seconds() / 60

print(f"Original Logs: {len(df)}")
print(f"Actual Unique Events identified: {len(events)}")
print("\nTop 5 longest disruptions recorded:")
print(events.sort_values(by='duration_minutes', ascending=False)[['line_id', 'duration_minutes', 'start_time']].head(5))

# Save the cleaned version
events.to_csv('cleaned_disruptions_FINAL.csv', index=False)

import pandas as pd

# Load the file you just downloaded
df_live = pd.read_csv('/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/cleaned_disruptions_FINAL.csv') # Make sure the file is in the same folder

print("--- LIVE DISRUPTION SUMMARY ---")
print(f"Total incidents caught: {len(df_live)}")
print("\nIncidents per Line:")
print(df_live['line'].value_counts())

print("\nMost common reason for delay:")
# If your column is named 'description' or 'title'
print(df_live['description'].value_counts().head(3))