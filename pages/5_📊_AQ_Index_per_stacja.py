"""
Page allowing the user to display Air Quality Index by station as a table (tab 1) or as charts by parameter (tab 2).
"""

import streamlit as st

from model.api_handler import add_aq_index_values
from model.data_downloader import get_station_ids_list, display_legend, get_aq_index_by_station

st.title(":blue[Indeks jakości powietrza per stacja]")
st.write(
    "Wybierz z bocznego menu ID stacji. Poniżej możesz zobaczyć najnowsze wyniki indeksu jakości powietrza (Air Quality Index).")

station_ids = get_station_ids_list()

activate_search_window = st.sidebar.checkbox("Wpisz samodzielnie ID")
if activate_search_window:
    station_id = st.sidebar.text_input("Wpisz ID stacji")
    if station_id:
        add_aq_index_values(station_id)
        index_info = get_aq_index_by_station(station_id)
        st.write(index_info)
    else:
        st.write("Wpisz ID stacji w bocznym menu.")

else:
    selected_station_id = st.sidebar.selectbox("Wybierz ID stacji", station_ids)
    if selected_station_id:
        add_aq_index_values(selected_station_id)
        index_info = get_aq_index_by_station(selected_station_id)
        st.write(index_info)
    else:
        st.write("Wybierz ID stacji w bocznym menu.")

display_legend()
