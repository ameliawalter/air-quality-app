"""
Module for selecting data from SQLite database.
"""

from model.base import Session
import pandas as pd

def get_stations_map():
    session = Session()
    try:
        stations_geo_query = 'SELECT station_name, lat, lon FROM stations'
        map_df = pd.read_sql_query(stations_geo_query, session.bind)
        return map_df
    finally:
        Session.remove()

def get_stations_list():
    session = Session()
    try:
        stations_list_query = 'SELECT station_id, station_name, station_address, city_name FROM stations'
        stations_list_df = pd.read_sql_query(stations_list_query, session.bind)
        return stations_list_df
    finally:
        Session.remove()

def get_station_ids_list():
    session = Session()
    try:
        stations_ids_query = 'SELECT station_id FROM stations'
        stations_ids_df = pd.read_sql_query(stations_ids_query, session.bind)
        return stations_ids_df['station_id'].tolist()
    finally:
        Session.remove()

def get_sensor_ids_list():
    session = Session()
    try:
        sensors_ids_query = 'SELECT DISTINCT sensor_id FROM sensors ORDER BY sensor_id'
        sensors_ids_df = pd.read_sql_query(sensors_ids_query, session.bind)
        return sensors_ids_df['sensor_id'].tolist()
    finally:
        Session.remove()

def get_sensors_by_station_list(station_id):
    session = Session()
    try:
        sensors_ids_query = f'SELECT sensors.sensor_id FROM stations JOIN sensors ' \
                                f'ON stations.station_id=sensors.station_id WHERE stations.station_id="{station_id}" '
        sensors_ids_df = pd.read_sql_query(sensors_ids_query, session.bind)
        return sensors_ids_df['sensor_id'].tolist()
    finally:
        Session.remove()
def get_station_details(station_id):
    session = Session()
    try:
        station_details_query = f'SELECT stations.station_name, stations.station_address, stations.city_name, ' \
                                f'sensors.sensor_id, sensors.param_name, sensors.param_id FROM stations JOIN sensors ' \
                                f'ON stations.station_id=sensors.station_id WHERE stations.station_id="{station_id}" '
        station_details_df = pd.read_sql_query(station_details_query, session.bind)
        return station_details_df
    finally:
        Session.remove()

def get_station_details_by_city(city):
    session = Session()
    try:
        station_details_query = f'SELECT stations.station_id, stations.station_name, stations.station_address, stations.city_name, ' \
                                f'sensors.sensor_id, sensors.param_name, sensors.param_id FROM stations JOIN sensors ' \
                                f'ON stations.station_id=sensors.station_id WHERE stations.city_name="{city}" '
        station_details_df = pd.read_sql_query(station_details_query, session.bind)
        return station_details_df
    finally:
        Session.remove()

def get_station_results(station_id):
    session = Session()
    try:
        station_results_query = f'''
            SELECT 
                stations.station_name, 
                stations.lon, 
                stations.lat, 
                results.sensor_code, 
                results.timestamp, 
                results.value 
            FROM 
                stations 
            LEFT JOIN 
                sensors ON stations.station_id = sensors.station_id 
            LEFT JOIN 
                results ON results.sensor_id = sensors.sensor_id 
            WHERE 
                stations.station_id="{station_id}" 
            '''

        station_results_df = pd.read_sql_query(station_results_query, session.bind)
        return station_results_df
    finally:
        Session.remove()

def get_latest_station_results(station_id):
    session = Session()
    try:
        station_results_query = f'''
            SELECT 
                stations.station_name, 
                stations.lon, 
                stations.lat, 
                results.sensor_code, 
                results.timestamp, 
                results.value 
            FROM 
                stations 
            LEFT JOIN 
                sensors ON stations.station_id = sensors.station_id 
            LEFT JOIN 
                results ON results.sensor_id = sensors.sensor_id 
            WHERE 
                stations.station_id="{station_id}" 
            AND 
                results.timestamp = (SELECT MAX(results.timestamp) FROM results)
            '''

        station_results_df = pd.read_sql_query(station_results_query, session.bind)
        return station_results_df
    finally:
        Session.remove()


def get_sensor_results(sensor_id):
    session = Session()
    try:
        results_query = f'''SELECT 
        stations.station_id, results.sensor_id, results.sensor_code, results.timestamp, results.value 
        FROM stations
        JOIN sensors ON stations.station_id=sensors.station_id
        JOIN results ON sensors.sensor_id=results.sensor_id
        WHERE results.sensor_id="{sensor_id}"'''
        results_df = pd.read_sql_query(results_query, session.bind)
        return results_df
    finally:
        Session.remove()
