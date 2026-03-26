import pandas as pd

# Load the cleaned dataset
df_live = pd.read_csv('cleaned_disruptions_FINAL.csv')

# 1. Filter out the 'Other' category to see only specific lines
lines_only = df_live[df_live['line_id'] != 'Other']

# 2. Filter out the long-term construction (anything over 4 hours / 240 mins)
# This leaves us with the sudden 'shocks'
shocks = lines_only[lines_only['duration_minutes'] <= 240]

print("--- TOP TRANSPORT SHOCKS BY LINE ---")
print(shocks['line_id'].value_counts())

print("\n--- LONGEST RECENT SHOCKS ---")
print(shocks[['line_id', 'duration_minutes', 'description']].sort_values(by='duration_minutes', ascending=False).head(5))