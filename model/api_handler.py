"""
Module containing functions to get air quality data from API into SQLite database using SQLAlchemy model and requests library.
Function clear_database() has been included due to GIOS API's station IDs not being constant.
As they are changed on an unpredictable basis, DB needs to be cleared everytime the app is run.
"""

from sqlalchemy import inspect
import requests
from model.data_downloader import get_sensor_results
from model.air_quality_model import Commune, City, Station, Sensor, Result, Index
from model.base import Base, Session, engine

def clear_database():
    inspector = inspect(engine)
    if inspector.has_table("stations"):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    Session.remove()


def add_all_communes():
    url = "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        session = Session()
        for commune_dict in data['Lista stacji pomiarowych']:
            if None in commune_dict.values():
                continue
            commune_name = commune_dict['Gmina']
            existing_commune = session.query(Commune).filter(Commune.commune_name == commune_name).first()
            if not existing_commune:
                commune = Commune()
                commune.commune_name = commune_dict['Gmina']
                commune.district_name = commune_dict['Powiat']
                commune.province_name = commune_dict['Województwo']
                session.add(commune)
                session.commit()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
    finally:
        Session.remove()


def add_all_cities():
    url = "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        session = Session()
        for city_dict in data['Lista stacji pomiarowych']:
            if None in city_dict.values():
                continue
            city_id = city_dict['Identyfikator miasta']
            existing_city = session.query(City).filter(City.city_id == city_id).first()
            if not existing_city:
                city = City()
                city.city_id = city_dict['Identyfikator miasta']
                city.city_name = city_dict['Nazwa miasta']
                city.city_commune = city_dict['Gmina']
                session.add(city)
        session.commit()
        Session.remove()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def add_all_stations():
    url = "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        session = Session()
        for station_dict in data['Lista stacji pomiarowych']:
            # if None in station_dict.values():
            #     continue
            station_id = station_dict['Identyfikator stacji']
            existing_station = session.query(Station).filter(Station.station_id == station_id).first()
            if not existing_station:
                station = Station()
                station.station_id = station_dict['Identyfikator stacji']
                station.station_name = station_dict['Nazwa stacji']
                station.lon = station_dict['WGS84 λ E']
                station.lat = station_dict['WGS84 φ N']
                station.station_address = station_dict['Ulica']
                station.city_name = station_dict['Nazwa miasta']
                session.add(station)
        session.commit()
        Session.remove()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def add_sensors_to_station(station_id):
    # station_id
    url = f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{station_id}?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        session = Session()
        for sensor_dict in data['Lista stanowisk pomiarowych dla podanej stacji']:
            if None in sensor_dict.values():
                continue
            sensor_id = sensor_dict['Identyfikator stanowiska']
            existing_sensor = session.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()
            if not existing_sensor:
                sensor = Sensor()
                sensor.sensor_id = sensor_dict['Identyfikator stanowiska']
                sensor.station_id = sensor_dict['Identyfikator stacji']
                sensor.param_id = sensor_dict['Id wskaźnika']
                sensor.param_name = sensor_dict['Wskaźnik']
                sensor.param_formula = sensor_dict['Wskaźnik - wzór']
                sensor.param_code = sensor_dict['Wskaźnik - kod']
                session.add(sensor)
        session.commit()
        Session.remove()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


from decimal import Decimal


def add_values_by_sensor(sensor_id):
    url = f"https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/{sensor_id}?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        session = Session()
        result = None
        for result_dict in data['Lista danych pomiarowych']:
            sensor_code = result_dict['Kod stanowiska']
            timestamp = result_dict['Data']
            existing_result = session.query(Result).filter(
                Result.sensor_code == sensor_code,
                Result.timestamp == timestamp
            ).first()
            if existing_result is None:
                result = Result()
                result.result_id = None
                result.sensor_code = sensor_code
                result.sensor_id = sensor_id
                result.timestamp = timestamp
                value = result_dict['Wartość']
                result.value = Decimal(str(value)) if value is not None else None
                session.add(result)
        session.commit()

        if result is not None:
            session.refresh(result)

        session.close()

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def add_aq_index_values(station_id):
    url = f"https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/{station_id}?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        session = Session()
        timestamp = data['AqIndex']['Data wykonania obliczeń indeksu']
        existing_timestamp = session.query(Index).filter(Index.timestamp == timestamp).first()
        if not existing_timestamp:
            if data['AqIndex']['Wartość indeksu'] is not None:
                index = Index()
                index.station_id = station_id
                index.timestamp = data['AqIndex']['Data wykonania obliczeń indeksu']
                index.timestamp_source_data = data['AqIndex']['Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika st']
                index.index_value = data['AqIndex']['Wartość indeksu']
                index.critical_code = data['AqIndex']['Kod zanieczyszczenia krytycznego']
                session.add(index)
            else:
                print(f"Skipped record for station_id {station_id} due to null value.")
        session.commit()
        Session.remove()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

# if __name__ == '__main__':
#     add_values_by_sensor(49)
#     print(get_sensor_results(49))