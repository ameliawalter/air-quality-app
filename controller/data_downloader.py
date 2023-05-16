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

def get_station_details(station_id):
    session = Session()
    try:
        # station_details_query = f'SELECT station_name, station_address, city_name FROM stations WHERE station_id="{station_id}"'
        station_details_query = f'SELECT stations.station_name, stations.station_address, stations.city_name, ' \
                                f'sensors.sensor_id, sensors.param_name, sensors.param_id FROM stations JOIN sensors ' \
                                f'ON stations.station_id=sensors.station_id WHERE stations.station_id="{station_id}" '
        station_details_df = pd.read_sql_query(station_details_query, session.bind)
        return station_details_df
    finally:
        Session.remove()

def get_sensors_list():
    session = Session()
    try:
        results_query = 'SELECT sensor_id FROM results'
        results_df = pd.read_sql_query(results_query, session.bind)
        return results_df
    finally:
        Session.remove()

def get_sensor_results(sensor_id):
    session = Session()
    try:
        results_query = f'SELECT sensor_id, sensor_code, timestamp, value FROM results WHERE sensor_id="{sensor_id}"'
        results_df = pd.read_sql_query(results_query, session.bind)
        return results_df
    finally:
        Session.remove()