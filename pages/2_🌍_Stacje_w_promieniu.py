import streamlit as st
from geopy.geocoders import Nominatim
from math import radians, cos, sin, sqrt, atan2
import geopandas as gpd
import pydeck as pdk
from shapely.geometry import Point
import pandas as pd
from model.air_quality_model import Station
from model.base import Session
from pydeck.types import String

# Function to calculate distance using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Radius of earth in kilometers
    R = 6371.0

    # calculate the result
    distance = R * c
    return distance

# Get user input
location = st.text_input('Wprowadź lokalizację:')
radius = st.slider("Promień wyszukiwania (km)", 1, 100, 10)

# Use geocoding API to get coordinates of input location
if location:
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(location)
    if location is None:
        st.error('Nie znaleziono podanej lokalizacji. Wprowadź prawidłową wartość.')
    else:
        loc_lat = location.latitude
        loc_lon = location.longitude

        # Start a new session
        session = Session()

        # Query SQLite database for stations
        stations = session.query(Station).all()

        # Filter stations based on user specified radius
        nearby_stations = []
        for station in stations:
            dist = calculate_distance(loc_lat, loc_lon, station.lat, station.lon)
            if dist <= radius:
                nearby_stations.append(station)

        # Display nearby stations
        for station in nearby_stations:
            st.write(f"ID stacji: {station.station_id}, Nazwa stacji: {station.station_name}, Odległość: {calculate_distance(loc_lat, loc_lon, station.lat, station.lon):.2f} km")

        # Create a dataframe for the nearby stations
        station_df = pd.DataFrame([{
            'station_id': station.station_id,
            'station_name': station.station_name,
            'lat': station.lat,
            'lon': station.lon
        } for station in nearby_stations])

        # Define a layer for the circle around the chosen location
        circle_layer = pdk.Layer(
            'GeoJsonLayer',
            data=gpd.GeoSeries([Point(loc_lon, loc_lat).buffer(radius/111.12)]).__geo_interface__,
            get_fill_color=[0, 0, 255, 80],
            pickable=False,
            filled=True
        )

        # Define an icon layer for the chosen location
        # icon_data = [{
        #     'Coordinates': [loc_lon, loc_lat],
        #     'icon_url': 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/icon/marker.png'
        # }]
        # icon_layer = pdk.Layer(
        #     'IconLayer',
        #     icon_data,
        #     get_icon='marker',
        #     get_size=50,
        #     size_scale=200,
        #     get_position='Coordinates'
        # )

        # Define a layer for the station markers
        scatter_layer = pdk.Layer(
            'ScatterplotLayer',
            data=station_df,
            get_position=['lon', 'lat'],
            get_color=[255, 0, 0],
            get_radius=250,
            pickable=True
        )

        # Define a scatter layer for the chosen location
        location_data = pd.DataFrame({'Coordinates': [(loc_lon, loc_lat)]})
        location_layer = pdk.Layer(
            "ScatterplotLayer",
            location_data,
            get_position='Coordinates',
            get_color=[0, 0, 255],  # Blue color
            get_radius=150,  # Adjust as needed
        )

        # Define a tooltip for displaying station names
        tooltip = {'html': '<b>{station_name}</b>', 'style': {'color': 'white'}}

        # Create a pydeck chart with the circle and scatter layers
        view_state = pdk.ViewState(latitude=loc_lat, longitude=loc_lon, zoom=10)
        # deck = pdk.Deck(layers=[circle_layer, scatter_layer, icon_layer], initial_view_state=view_state, tooltip=tooltip)
        deck = pdk.Deck(layers=[circle_layer, scatter_layer, location_layer],
                        initial_view_state=view_state,
                        tooltip=tooltip)

        # Display the map with the pydeck chart
        st.pydeck_chart(deck)

        # Remove the session
        Session.remove()
