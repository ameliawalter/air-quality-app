import sys
import os
from controller.data_downloader import get_stations_map
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



