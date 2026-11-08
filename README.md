# Vienna Traffic & Disruption Analysis

Collecting Vienna public transport disruptions in real time and combining them with ten years of road traffic counts, as the groundwork for predicting **where disruptions happen and what causes them**.

![Map of Vienna's permanent traffic counting stations](map_screenshot.png)

## What this project does

| Step | What I built | Result |
|---|---|---|
| 1. Live data collection | A Flask app on PythonAnywhere that calls the Wiener Linien real-time API (`trafficInfoList`) every 15 minutes and appends each disruption to a CSV | ~69,000 log records, 19–29 March 2026 |
| 2. Event detection | Grouped repeated log entries into unique disruption events (by line and description) and calculated each event's duration | 336 distinct disruption events |
| 3. Historical traffic data | Merged two City of Vienna open datasets: daily traffic counts and the locations of the permanent counting stations | 45,672 rows from 70 stations, 2016–2025 |
| 4. Map | Plotted every counting station on an interactive Folium map | `vienna_traffic_map.html` |
| 5. First insights | Most-disrupted lines (U1, U3 and U6 had the most short-term "shocks"), longest disruptions, busiest truck-traffic location | see `data_processing/` |

## Data sources

- **Wiener Linien real-time open data**: `https://www.wienerlinien.at/ogd_realtime/trafficInfoList`
- **City of Vienna open data**: permanent traffic counting stations (Dauerzählstellen) and their daily counts

## Repository structure

```
data_collection/   live collector (flask_app.py), map builder, raw disruption batches
data_processing/   cleaning, event grouping, dataset merge, disruption analysis
datasets/          cleaned and merged datasets
vienna_traffic_map.html   interactive station map
```

## How to run

```bash
pip install pandas folium flask requests
python data_processing/both_hist_dataset_merge.py   # build the historical master dataset
python data_collection/make_map.py                  # build the station map
```

## Limitations and next steps

- **Short collection window.** Ten days of live data is enough to test the pipeline, not to train a model. Next: collect for at least one month.
- **Line extraction.** The current regex recognises U-Bahn lines and "Linie N" trams; most events (bus lines, network-wide notices) fall into "Other". Next: parse the API's structured line field instead of the title text.
- **Prediction model.** Next: join disruption events to nearby counting stations by time and location, add weather and calendar features, and train a classifier for disruption cause and a model for disruption risk by line and hour.

## Author

Mujeeb Odekunle, BSc Applied Data Science, Modul University Vienna — [github.com/jibson1536](https://github.com/jibson1536)
