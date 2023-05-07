from sqlalchemy import Column, String, ForeignKey, create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship
import requests
from base import Base

engine = create_engine("sqlite:///airquality.db")

class Station(Base):
    __tablename__ = "stations"
    station_id = Column(String(50), primary_key=True)
    station_name = Column(String(50))
    gegr_lat = Column(String(50))
    gegr_lon = Column(String(50))
    station_address = Column(String(50))
    city_name = Column(String(50), ForeignKey("cities.city_name"))
    cities = relationship("City", back_populates="stations")
    __table_args__ = {"extend_existing": True}

    def __repr__(self):
        return "<Station(station_id='%s', station_name='%s', gegr_lat='%s', gegr_lon='%s')>" % (
            self.station_id,
            self.station_name,
            self.gegr_lat,
            self.gegr_lon,
        )

def add_all_stations():
    url = "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?size=500"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        session = Session()

        for station_dict in data['Lista stacji pomiarowych']:
            station_id = station_dict['Identyfikator stacji']
            existing_station = session.query(Station).filter(Station.station_id == station_id).first()
            if not existing_station:
                station = Station()
                station.station_id = station_dict['Identyfikator stacji']
                station.station_name = station_dict['Nazwa stacji']
                station.gegr_lat = station_dict['WGS84 λ E']
                station.gegr_lon = station_dict['WGS84 φ N']
                station.station_address = station_dict['Ulica']
                station.city_name = station_dict['Nazwa miasta']
                session.add(station)

        session.commit()
        session.close()

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

        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        session = Session()

        for city_dict in data['Lista stacji pomiarowych']:
            city_id = city_dict['Identyfikator miasta']
            existing_city = session.query(City).filter(City.city_id == city_id).first()
            if not existing_city:
                city = City()
                city.city_id = city_dict['Identyfikator miasta']
                city.city_name = city_dict['Nazwa miasta']
                city.city_commune = city_dict['Gmina']
                session.add(city)

        session.commit()
        session.close()

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

        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        session = Session()

        for commune_dict in data['Lista stacji pomiarowych']:
            commune_name = commune_dict['Gmina']
            existing_commune = session.query(Commune).filter(Commune.commune_name == commune_name).first()
            if not existing_commune:
                commune = Commune()
                commune.commune_name = commune_dict['Gmina']
                commune.district_name = commune_dict['Powiat']
                commune.province_name = commune_dict['Województwo']
                session.add(commune)

        session.commit()
        session.close()

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

if __name__ == '__main__':
    metadata = Base.metadata
    metadata.create_all(engine)
    add_all_cities()
    add_all_stations()
    add_all_communes()