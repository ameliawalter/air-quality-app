import sys
import os
from model.data_downloader import get_stations_map, get_station_ids_list
import streamlit as st
import pydeck as pdk
from model.api_handler import clear_database, add_all_communes, add_all_cities, add_all_stations, add_sensors_to_station
from model.base import Base, engine
from concurrent.futures import ThreadPoolExecutor
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Initial actions to create DB and populate it with stations
Base.metadata.create_all(engine)
# clear_database()
add_all_communes()
add_all_cities()
add_all_stations()
ids = get_station_ids_list()
with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(add_sensors_to_station, ids)

# Main page UI
st.set_page_config(page_title="Jakość powietrza w Polsce", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
st.title(":blue[Stacje pomiaru jakości powietrza w Polsce]")
st.write("Dane dotyczące jakości powietrza w całej Polsce. Dzięki opcjom bocznego menu możesz:")

# Map with all the Polish air quality measurement stations
try:
    map_df = get_stations_map()
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position=["lon", "lat"],
        get_color=[255, 0, 0],
        get_radius=500,
        pickable=True,
    )
    tooltip = {"html": "<b>{station_name}</b>", "style": {"color": "white"}}
    view_state = pdk.ViewState(latitude=map_df["lat"].mean(), longitude=map_df["lon"].mean(), zoom=5)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
    st.pydeck_chart(deck)

except SyntaxError:
    st.error("Error, data cannot be downloaded. Try reloading the page.")



