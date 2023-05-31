"""
Module for selecting data from SQLite database.
"""

import pandas as pd
import streamlit as st

from model.base import Session


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
        stations_list_query = '''SELECT station_id as "ID stacji", 
                                    station_name as "Nazwa stacji", 
                                    station_address as "Adres", 
                                    city_name as "Miasto" 
                                    FROM stations'''
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

def get_sensor_results(sensor_id):
    session = Session()
    try:
        results_query = f'''SELECT 
        stations.station_id as "ID stacji", 
        results.sensor_id as "ID sensora",
        results.sensor_code as "Kod sensora", 
        results.timestamp as "Czas",
        results.value as "Wynik"
        FROM stations
        JOIN sensors ON stations.station_id=sensors.station_id
        JOIN results ON sensors.sensor_id=results.sensor_id
        WHERE results.sensor_id="{sensor_id}"'''
        results_df = pd.read_sql_query(results_query, session.bind)
        return results_df
    finally:
        Session.remove()


def get_station_details(station_id):
    session = Session()
    try:
        station_details_query = f'''SELECT stations.station_name as "Nazwa stacji", 
                                        stations.station_address as "Adres",
                                         stations.city_name as "Miasto", 
                                            sensors.sensor_id as "ID sensora", 
                                            sensors.param_name as "Parametr sensora",
                                             sensors.param_id as "ID parametru"
                                              FROM stations JOIN sensors 
                                                ON stations.station_id=sensors.station_id 
                                                WHERE stations.station_id="{station_id}"'''
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
                stations.station_name as "Nazwa stacji", 
                results.sensor_code as "Kod sensora", 
                results.timestamp as "Czas", 
                results.value as "Wynik" 
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


def get_aq_index_by_station(station_id):
    session = Session()
    try:
        index_results_query = f'''
            SELECT 
                timestamp as "Czas (obliczenie indeksu)",
                timestamp_source_data as "Czas (pomiar danych)",
                index_value as "Wartość indeksu",
                index_desc as "Opis indeksu",
                so2_index_value as "Indeks SO2",
                so2_index_desc as "Opis indeksu SO2",
                no2_index_value as "Indeks NO2",
                no2_index_desc as "Opis indeksu NO2",
                pm10_index_value as "Indeks PM10",
                pm10_index_desc as "Opis indeksu PM10",
                pm25_index_value as "Indeks PM 2.5",
                pm25_index_desc as "Opis indeksu PM 2.5", 
                o3_index_value as "Indeks O3",
                o3_index_desc as "Opis indeksu O3"
            FROM 
                aq_index 
            WHERE 
                station_id="{station_id}" 
            '''
        qa_index_df = pd.read_sql_query(index_results_query, session.bind)
        html = qa_index_df.T.to_html()
        return st.write(html, unsafe_allow_html=True)
    finally:
        Session.remove()


def display_legend():
    st.write(":red[Legenda:]")
    st.markdown("- O3 - ozon")
    st.markdown(
        "- PM2.5 -  aerozole atmosferyczne (pył zawieszony) o średnicy nie większej niż 2,5 μm - poziom dopuszczalny **20 μg/m³ (uśrednienie roczne)**")
    st.markdown(
        "- PM10 - aerozole atmosferyczne (pył gruby) o średnicy nie większej niż 10 μm - poziom dopuszczalny **50 µg/m³ (uśrednienie dobowe)**; poziom informowania: 100 µg/m³ (dobowy); poziom alarmowy: 150 µg/m³ (dobowy)")
    st.markdown("- NO - tlenek azotu")
    st.markdown(
        "- NO2 - dwutlenek azotu - poziom dopuszczalny **200 µg/m³ (pomiar godzinny) lub 40 µg/m³ (uśrednienie roczne)**")
    st.markdown("- NOx - inne tlenki azotu - poziom dopuszczalny **30 µg/m³ (uśrednienie roczne)**")
    st.markdown(
        "- SO2 - dwutlenek siarki - poziom dopuszczalny **350 µg/m³ (pomiar godzinny) lub 125 µg/m³ (uśrednienie dobowe)**")
    st.markdown("- C6H6 - benzen - poziom dopuszczalny **5 µg/m³ (uśrednienie roczne)**")
    st.write(
        "Więcej informacji [na stronie GIOŚ](https://powietrze.gios.gov.pl/pjp/content/annual_assessment_air_acceptable_level)")
