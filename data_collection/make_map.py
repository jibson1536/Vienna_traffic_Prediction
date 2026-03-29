import pandas as pd
import folium

# 1. Load master data
df = pd.read_csv('/Users/admin/Desktop/Final project /final-project/Vienna_traffic_Prediction/datsets/master_traffic_data_FINAL.csv')

# 2. Get the unique sensors 
unique_sensors = df.drop_duplicates(subset=['location_name'])

# 3. Create a map centered on Vienna
# changed from the previous server to a more reliable one beause i was blocked access
vienna_map = folium.Map(
    location=[48.2082, 16.3738], 
    zoom_start=12, 
    tiles='CartoDB positron' # This uses a different, more reliable server
)

# 4. Add a marker for each sensor
for index, row in unique_sensors.iterrows():
    # We need to clean the GPS string "POINT (16.41 48.23)" to get just numbers
    try:
        coords_raw = row['gps_coordinates'].replace('POINT (', '').replace(')', '').split(' ')
        lon, lat = float(coords_raw[0]), float(coords_raw[1])
        
        folium.Marker(
            [lat, lon], 
            popup=f"Sensor: {row['location_name']}",
            tooltip=row['location_name']
        ).add_to(vienna_map)
    except:
        continue

# 5. Save the map
vienna_map.save('vienna_traffic_map.html')
print("Map created! Open 'vienna_traffic_map.html' in your browser to see it.")