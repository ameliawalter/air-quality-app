"""
Module containing models for object-relational mapping with SQLAlchemy.
"""

from sqlalchemy import Column, String, ForeignKey, Numeric, Float, Integer
from sqlalchemy.orm import relationship
from model.base import Base

class Commune(Base):
    __tablename__ = "communes"
    commune_name = Column(String(50), primary_key=True)
    district_name = Column(String(50))
    province_name = Column(String(50))
    cities = relationship("City", back_populates="communes")
    __table_args__ = {"extend_existing": True}

class City(Base):
    __tablename__ = "cities"
    city_id = Column(String(50), primary_key=True)
    city_name = Column(String(50), nullable=False)
    city_commune = Column(String(50), ForeignKey("communes.commune_name"))
    stations = relationship("Station", back_populates="cities")
    communes = relationship("Commune", back_populates="cities")
    __table_args__ = {"extend_existing": True}

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


class Result(Base):
    __tablename__ = "results"
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_code = Column(String(50))
    sensor_id = Column(String(50), ForeignKey("sensors.sensor_id"))
    timestamp = Column(String(50))
    value = Column(Numeric(20))
    sensors = relationship("Sensor", back_populates="results")
    __table_args__ = {"extend_existing": True}


class Index(Base):
    __tablename__ = "index"
    station_id = Column(String(50), ForeignKey("stations.station_id"), primary_key=True)
    timestamp = Column(String(50))
    timestamp_source_data = Column(String(50))
    index_value = Column(Numeric(20))
    critical_code = Column(String(50))
    stations = relationship("Station", back_populates="index")
    __table_args__ = {"extend_existing": True}


