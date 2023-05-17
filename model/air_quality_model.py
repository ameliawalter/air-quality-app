from sqlalchemy import Column, String, ForeignKey, create_engine, Table, Numeric, inspect, Float, MetaData
from sqlalchemy.orm import relationship
import requests
from controller.data_downloader import get_station_details, get_station_ids_list, get_station_results, get_sensor_ids_list
from model.base import Base, Session, engine
from concurrent.futures import ThreadPoolExecutor

class Station(Base):
    __tablename__ = "stations"
    station_id = Column(String(50), primary_key=True)
    station_name = Column(String(50))
    lat = Column(Float(50))
    lon = Column(Float(50))
    station_address = Column(String(50))
    city_name = Column(String(50), ForeignKey("cities.city_name"))
    cities = relationship("City", back_populates="stations")
    sensors = relationship("Sensor", back_populates="stations")
    index = relationship("Index", back_populates="stations")
    __table_args__ = {"extend_existing": True}


def add_all_stations():
    url = "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        session = Session()
        for station_dict in data['Lista stacji pomiarowych']:
            if None in station_dict.values():
                continue
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


class City(Base):
    __tablename__ = "cities"
    city_id = Column(String(50), primary_key=True)
    city_name = Column(String(50), unique=True, nullable=False)
    city_commune = Column(String(50), ForeignKey("communes.commune_name"))
    stations = relationship("Station", back_populates="cities")
    communes = relationship("Commune", back_populates="cities")
    __table_args__ = {"extend_existing": True}


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


class Commune(Base):
    __tablename__ = "communes"
    commune_name = Column(String(50), primary_key=True)
    district_name = Column(String(50))
    province_name = Column(String(50))
    cities = relationship("City", back_populates="communes")
    __table_args__ = {"extend_existing": True}


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


class Sensor(Base):
    __tablename__ = "sensors"
    sensor_id = Column(String(50), primary_key=True)
    station_id = Column(String(50), ForeignKey("stations.station_id"))
    param_id = Column(String(50))
    param_name = Column(String(50))
    param_formula = Column(String(50))
    param_code = Column(String(50))
    stations = relationship("Station", back_populates="sensors")
    results = relationship("Result", back_populates="sensors")
    __table_args__ = {"extend_existing": True}


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


class Result(Base):
    __tablename__ = "results"
    sensor_code = Column(String(50))
    sensor_id = Column(String(50), ForeignKey("sensors.sensor_id"))
    timestamp = Column(String(50), primary_key=True)
    value = Column(Numeric(20))
    sensors = relationship("Sensor", back_populates="results")
    __table_args__ = {"extend_existing": True}


def add_values_by_sensor(sensor_id):
    url = f"https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/{sensor_id}?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        session = Session()

        for result_dict in data['Lista danych pomiarowych']:
            if None in result_dict.values():
                continue
            timestamp = result_dict['Data']
            existing_timestamp = session.query(Result).filter(Result.timestamp == timestamp).first()
            if not existing_timestamp:
                result = Result()
                result.sensor_code = result_dict['Kod stanowiska']
                result.sensor_id = sensor_id
                result.timestamp = result_dict['Data']
                result.value = result_dict['Wartość']
                session.add(result)

        session.commit()
        Session.remove()

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


class Index(Base):
    __tablename__ = "index"
    station_id = Column(String(50), ForeignKey("stations.station_id"), primary_key=True)
    timestamp = Column(String(50))
    timestamp_source_data = Column(String(50))
    index_value = Column(Numeric(20))
    critical_code = Column(String(50))
    stations = relationship("Station", back_populates="index")
    __table_args__ = {"extend_existing": True}


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



def clear_database():
    inspector = inspect(engine)
    if inspector.has_table("stations"):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    Session.remove()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    clear_database()
    add_all_communes()
    add_all_cities()
    add_all_stations()
    ids = get_station_ids_list()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(get_station_details, ids)
        executor.map(add_sensors_to_station, ids)
        executor.map(get_station_results, ids)
    sensors = get_sensor_ids_list()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(add_values_by_sensor, sensors)
        executor.map(add_aq_index_values, sensors)
    # for station_id in ids:
    #     get_station_details(station_id)
    #     add_sensors_to_station(station_id)
    #     get_station_results(station_id)
    # sensors = get_sensor_ids_list()
    # for sensor in sensors:
    #     add_values_by_sensor(sensor)
    #     add_aq_index_values(sensor)
