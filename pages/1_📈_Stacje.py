"""
Page allowing the user to display stations details by station ID (tab 1) or by city (tab 2).
"""

import streamlit as st

from model.data_downloader import get_stations_list, get_station_details, get_station_details_by_city, \
    get_station_ids_list

tab1, tab2 = st.tabs(["Stacje po ID", "Stacje w danym mieście"])

with tab1:
    st.write(':blue[Wybierz ID stacji z bocznego menu, żeby wyświetlić szczegóły na temat mierzonych parametrów.]')

    st.sidebar.title("Szukaj")
    st.sidebar.write("Wyświetl więcej szczegółów wybranej stacji")

    station_ids = get_station_ids_list()
    activate_search_window = st.sidebar.checkbox("Wpisz samodzielnie ID")

    if activate_search_window:
        station_id = st.sidebar.text_input("Wpisz ID stacji")

        if station_id:
            station_info = get_station_details(station_id)
            if station_info.empty:
                st.write("Taka stacja nie istnieje.")
            else:
                st.write(station_info)
        else:
            st.write("Wpisz ID stacji w bocznym menu.")

    else:
        selected_station_id = st.sidebar.selectbox("Wybierz ID stacji", station_ids)

        if selected_station_id:
            station_info = get_station_details(selected_station_id)
            if station_info.empty:
                st.write("Taka stacja nie istnieje.")
            else:
                st.write(station_info)
        else:
            st.write("Wybierz ID stacji w bocznym menu.")

with tab2:
    st.write(
        ':blue[Wyszukaj wszystkie stacje w danym mieście, żeby wyświetlić szczegóły na temat mierzonych parametrów.]')
    city = st.text_input("Wpisz miasto")
    if city:
        station_info = get_station_details_by_city(city)
        if station_info.empty:
            st.write("Taka stacja nie istnieje.")
        else:
            st.write(station_info)

# Display a list of stations
list_df = get_stations_list()
st.write(':blue[Lista wszystkich stacji]')
st.write(list_df[['station_id', 'station_name', 'station_address', 'city_name']])
