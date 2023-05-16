import streamlit as st
from geopy.geocoders import Nominatim
from math import radians, cos, sin, sqrt, atan2
from sqlalchemy.orm import Session

from model.air_quality_model import Station
from model.base import Session

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
# radius = st.number_input('Enter search radius in kilometers:', min_value=1.0)
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

        # Remove the session
        Session.remove()

