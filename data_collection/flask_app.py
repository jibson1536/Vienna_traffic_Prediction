import requests
import csv
import os
from datetime import datetime
from flask import Flask

app = Flask(__name__)

# CONFIGURATION

CSV_FILE = "/home/Jibson/vienna_traffic_prediction/data/vienna_disruptions.csv"
API_URL = "https://www.wienerlinien.at/ogd_realtime/trafficInfoList"

def scrape_vienna_data():
    try:
        response = requests.get(API_URL)
        data = response.json()
        infos = data.get('data', {}).get('trafficInfos', [])

        # Create directory 
        os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

        file_exists = os.path.isfile(CSV_FILE)

        with open(CSV_FILE, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            # Add headers if it's a new file
            if not file_exists:
                writer.writerow(["timestamp", "title", "description"])

            for info in infos:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([timestamp, info.get('title'), info.get('description')])

        return f"Successfully logged {len(infos)} items."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    # This runs the scraper every time the website URL is visited
    status = scrape_vienna_data()
    return f"<h1>Vienna Traffic Bot</h1><p>Status: {status}</p><p>Last Check: {datetime.now()}</p>"

if __name__ == "__main__":
    app.run()