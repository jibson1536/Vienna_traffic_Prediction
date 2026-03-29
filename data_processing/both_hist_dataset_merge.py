import pandas as pd
import os

# 1. Paths
base_path = "/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/datsets"
loc_path = os.path.join(base_path, "DAUERZAEHLOGD.csv")
count_path = os.path.join(base_path, "dauerzaehlstellen.csv")

try:
    # 2. Load with correct separators
    locations = pd.read_csv(loc_path, sep=',', encoding='latin1')
    counts = pd.read_csv(count_path, sep=';', on_bad_lines='skip', encoding='latin1')

    # Strip hidden spaces
    locations.columns = locations.columns.str.strip()
    counts.columns = counts.columns.str.strip()

    
    # 3. FIXED THE DATES (Updated for "Do,27.03." with no space)
    def fix_date(row):
        try:
            # We split by exactly "," and take the second part (27.03.)
            # .strip('.') removes the trailing dot if it exists
            day_month = str(row['TVMAXT']).split(',')[1].strip()
            
            # Now combined it with the Year from the 'JAHR' column
            full_date_str = f"{day_month}{row['JAHR']}"
            
            # Converted to actual Python date
            return pd.to_datetime(full_date_str, format='%d.%m.%Y')
        except:
            return None

    counts['clean_date'] = counts.apply(fix_date, axis=1)

    # 4. THE MERGE Only using columns 
    master_df = pd.merge(
        counts, 
        locations[['ZST_ID', 'SHAPE', 'ZST_NAME', 'LAGE']], 
        left_on='ZNR', 
        right_on='ZST_ID', 
        how='left'
    )

    # 5. FINAL CLEANUP & RENAME
    if 'ZST_ID' in master_df.columns:
        master_df = master_df.drop(columns=['ZST_ID'])

    master_df = master_df.rename(columns={
        'DTVMS': 'total_vehicles',
        'ZST_NAME': 'location_name',
        'SHAPE': 'gps_coordinates',
        'LAGE': 'position_description'
    })

    # 6. Save
    output_path = os.path.join(base_path, "master_traffic_data_FINAL.csv")
    master_df.to_csv(output_path, index=False)
    
    print("--- SUCCESS! ---")
    print(f"File saved successfully at: {output_path}")
    print(f"Sample row:\n{master_df[['clean_date', 'location_name', 'total_vehicles']].head(1)}")

except Exception as e:
    print(f"Oops! Something went wrong: {e}")

    import pandas as pd

# Load the big master file
df = pd.read_csv('/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/datsets/master_traffic_data_FINAL.csv')

# Converted the column back to actual dates so Python can compare them
df['clean_date'] = pd.to_datetime(df['clean_date'])

# Filter for the "Modern Era" (2024 to 2026)
modern_df = df[df['clean_date'] >= '2024-01-01']

# Saved this as official "Analysis Ready" file
output_path = '/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/datsets/traffic_modern.csv'
modern_df.to_csv(output_path, index=False)

print(f"Filter Complete!")
print(f"Old rows: {len(df)}")
print(f"Modern rows: {len(modern_df)}")