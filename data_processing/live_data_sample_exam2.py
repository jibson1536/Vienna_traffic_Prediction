import pandas as pd
import re

# 1. Load Batch 2 (The 4.7MB file)
df = pd.read_csv('/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/data_collection/vienna_disruptions _b2.csv')
df.columns = df.columns.str.strip()

# 2. Extract Line ID (Same logic as before)
def extract_line(text):
    if pd.isna(text): return "Other"
    match = re.search(r'([U]\d|Linie\s\d+)', str(text))
    return match.group(0) if match else "Other"

df['line_id'] = df['title'].apply(extract_line)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 3. Collapse rows into Events
# Since it's every 15 mins, this grouping is even more important
events = df.groupby(['line_id', 'description']).agg(
    start_time=('timestamp', 'min'),
    end_time=('timestamp', 'max'),
    occurrence_count=('timestamp', 'count')
).reset_index()

# 4. Calculate Duration
# If an event only appears once, we assume it lasted at least 15 mins
events['duration_minutes'] = (events['end_time'] - events['start_time']).dt.total_seconds() / 60
events.loc[events['duration_minutes'] == 0, 'duration_minutes'] = 15 

# 5. Save as Cleaned Batch 2
events.to_csv('datasets/cleaned_disruptions_b2.csv', index=False)
print(f"Batch 2 Processed: Found {len(events)} unique events.")