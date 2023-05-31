'''
Some examples of tests for data_downloader.py file
'''

from unittest.mock import patch

import pandas as pd

from model import data_downloader
from model.base import Session

sample_data_map = pd.DataFrame({
    'station_name': ['Station1', 'Station2'],
    'lat': [0.0, 1.0],
    'lon': [0.0, 1.0]
})

sample_data_list = pd.DataFrame({
    'ID stacji': ['ID1', 'ID2'],
    'Nazwa stacji': ['Station1', 'Station2'],
    'Adres': ['Address1', 'Address2'],
    'Miasto': ['City1', 'City2']
})


def test_get_stations_map():
    with patch.object(Session, 'remove', return_value=None) as _fixture1:
        with patch.object(pd, 'read_sql_query', return_value=sample_data_map) as _fixture2:
            result = data_downloader.get_stations_map()
            assert result.equals(sample_data_map)


def test_get_stations_list():
    with patch.object(Session, 'remove', return_value=None) as _fixture1:
        with patch.object(pd, 'read_sql_query', return_value=sample_data_list) as _fixture2:
            result = data_downloader.get_stations_list()
            assert result.equals(sample_data_list)
