import streamlit as st

from controller.data_downloader import get_stations_list, get_station_details

st.write(':blue[Wybierz stacje z bocznego menu, żeby wyświetlić szczegóły na temat mierzonych parametrów.]')

st.sidebar.title("Szukaj")
st.sidebar.write("Wyświetl więcej szczegółów wybranej stacji")

stations_df = get_stations_list()
station_ids = stations_df['station_id'].tolist()

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

# Display a list of stations
list_df = get_stations_list()
st.write(':blue[Lista wszystkich stacji]')
st.write(list_df[['station_id', 'station_name', 'station_address', 'city_name']])