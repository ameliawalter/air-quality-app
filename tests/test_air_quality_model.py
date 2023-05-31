'''
Some examples of tests for air_quality_model.py file
'''

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.air_quality_model import Commune, City, Station, Sensor, Result, AqIndex
from model.base import Base

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)


def setup_module():
    Base.metadata.create_all(engine)


@pytest.fixture
def session():
    session = Session()
    yield session
    session.close()


def test_add_commune(session):
    commune = Commune(commune_name='test_commune', district_name='test_district', province_name='test_province')
    session.add(commune)
    session.commit()
    assert session.query(Commune).first().commune_name == 'test_commune'


def test_add_city(session):
    city = City(city_id='test_id', city_name='test_city', city_commune='test_commune')
    session.add(city)
    session.commit()
    assert session.query(City).first().city_id == 'test_id'


# An example of a negative test case
def test_add_city_negative(session):
    city = City(city_id='test_id', city_commune='test_commune')
    session.add(city)
    with pytest.raises(Exception):
        session.commit()


def test_add_station(session):
    station = Station(station_id='test_id', station_name='test_station', lat=10.0, lon=20.5,
                      station_address='test_address', city_name='test_city')
    session.add(station)
    session.commit()
    assert session.query(Station).first().station_id == 'test_id'


def test_add_sensor(session):
    sensor = Sensor(sensor_id='test_id', station_id='test_station_id', param_id='test_param_id')
    session.add(sensor)
    session.commit()
    assert session.query(Sensor).first().sensor_id == 'test_id'


# Test case to test autoincrementation
def test_add_result(session):
    result = Result()
    session.add(result)
    session.commit()
    assert session.query(Result).first().result_id == 1


def test_add_aq_index(session):
    aq_index = AqIndex(station_id='test_station_id')
    session.add(aq_index)
    session.commit()
    assert session.query(AqIndex).first().aq_index_id == 1
    assert session.query(AqIndex).first().station_id == 'test_station_id'
