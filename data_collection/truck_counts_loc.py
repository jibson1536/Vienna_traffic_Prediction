import pandas as pd

# Load new masterpiece
df = pd.read_csv('/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/datsets/master_traffic_data_FINAL.csv')

# Find the row with the maximum truck count (DTVMO)
# DTVMO is the original column name for trucks
top_truck_day = df.loc[df['DTVMO'].idxmax()]

print(f"--- TRUCK TRAFFIC INSIGHT ---")
print(f"Location: {top_truck_day['location_name']}")
print(f"Date: {top_truck_day['clean_date']}")
print(f"Truck Count: {top_truck_day['DTVMO']}")
print(f"Position: {top_truck_day['position_description']}")


import pandas as pd

# Load the modern data just created
df = pd.read_csv('/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/datsets/traffic_modern.csv')

# Count how many days of data we have for our most important locations
important_spots = ['Reichsbrücke', 'Westbahnhof', 'Karlsplatz', 'Floridsdorf-Br.']
health = df[df['location_name'].isin(important_spots)]['location_name'].value_counts()

print("--- SENSOR DATA HEALTH (Rows since 2024) ---")
print(health)