import sys
import os
from controller.data_downloader import get_stations_map, get_all_stations_results
import streamlit as st
import pydeck as pdk

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

st.set_page_config(page_title="Jakość powietrza w Polsce", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# UI
page_title = ":blue[Stacje pomiaru jakości powietrza w Polsce]"
page_helper = "Dane dotyczące jakości powietrza w całej Polsce. Dzięki opcjom bocznego menu możesz:"
st.title(page_title)
st.write(page_helper)

# MAP - STATIONS ONLY
# MAP
map_df = get_stations_map()
# Define custom layer for displaying station markers
layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position=["lon", "lat"],
    get_color=[255, 0, 0],
    get_radius=500,
    pickable=True,
)
# Define custom tooltip for displaying station names
tooltip = {"html": "<b>{station_name}</b>", "style": {"color": "white"}}
# Create pydeck chart and add custom layer and tooltip
view_state = pdk.ViewState(latitude=map_df["lat"].mean(), longitude=map_df["lon"].mean(), zoom=5)
deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
# Display map with pydeck chart
st.pydeck_chart(deck)

# MAP - STATIONS WITH RESULTS
# Get station data using your method
# map_df = get_stations_map()
#
# # Get air quality data using your method
# station_results_df = get_all_stations_results()
#
# # Rename the columns for clarity and ease of use
# station_results_df.rename(columns={'station_name': 'station_name', 'lon': 'lon', 'lat': 'lat',
#                                    'sensor_code': 'sensor_code', 'timestamp': 'timestamp',
#                                    'value': 'air_quality'}, inplace=True)
#
# # Merge station_results_df with map_df
# # Merge station_results_df with map_df, keeping lat and lon from map_df
# map_df = map_df.merge(station_results_df, on="station_name", how="left", suffixes=('', '_y'))
#
# # Drop the redundant 'lat_y' and 'lon_y' columns
# map_df.drop(columns=['lat_y', 'lon_y'], inplace=True)
#
# print(map_df.head())
#
# # Define custom layer for displaying station markers
# layer = pdk.Layer(
#     "ScatterplotLayer",
#     data=map_df,
#     get_position=["lon", "lat"],
#     get_color=[255, 0, 0],
#     get_radius=500,
#     pickable=True,
# )
#
# # Define custom tooltip for displaying station names and air quality
# tooltip = {
#     "html": "<b>{station_name}</b><br>Sensor Code: {sensor_code}<br>Timestamp: {timestamp}<br>Air Quality: {air_quality}",
#     "style": {"color": "white"},
# }
#
# # Create pydeck chart and add custom layer and tooltip
# view_state = pdk.ViewState(latitude=map_df["lat"].mean(), longitude=map_df["lon"].mean(), zoom=5)
# deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
#
# # Display map with pydeck chart
# st.pydeck_chart(deck)
#



