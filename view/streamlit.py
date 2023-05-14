import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import sqlite3
# import streamlit_folium
# from folium.plugins import MarkerCluster

st.subheader(':blue[Air quality measurement stations in Poland]')

conn = sqlite3.connect('model/airquality.db')
stations_geo_query = 'SELECT station_name, lat, lon FROM stations'
map_df = pd.read_sql_query(stations_geo_query, conn)

stations_list_query = 'SELECT station_name, station_address, city_name FROM stations'
stations_list_df = pd.read_sql_query(stations_list_query, conn)

# Display the map of all stations
# map_df['tooltip'] = map_df['station_name']
# st.map(map_df, tooltip='tooltip')

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

# Display a list of stations
st.write(':blue[List of stations:]')
st.write(stations_list_df[['station_name', 'station_address', 'city_name']])

# Create a marker cluster layer for the map
# marker_cluster = MarkerCluster().add_to(st.map())