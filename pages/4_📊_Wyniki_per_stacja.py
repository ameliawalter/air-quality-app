import streamlit as st
from controller.data_downloader import get_stations_list, get_station_results

st.title(":blue[Wyniki pomiarów wszystkich parametórów dla stacji]")
st.write("Wybierz z bocznego menu ID stacji. Poniżej możesz zobaczyć wyniki z ostatniej godziny dla danej stacji.")

stations_df = get_stations_list()
station_ids = stations_df['station_id'].tolist()

st.sidebar.write("Wyświetl pomiary danego sensora")

activate_search_window = st.sidebar.checkbox("Wpisz samodzielnie ID")

if activate_search_window:
    station_id = st.sidebar.text_input("Wpisz ID stacji")

    if station_id:
        station_info = get_station_results(station_id)
        if station_info.empty:
            st.write("Taka stacja nie istnieje.")
        else:
            st.write(station_info)
    else:
        st.write("Wpisz ID stacji w bocznym menu.")

else:
    selected_station_id = st.sidebar.selectbox("Wybierz ID stacji", station_ids)

    if selected_station_id:
        station_info = get_station_results(selected_station_id)
        if station_info.empty:
            st.write("Taka stacja nie istnieje.")
        else:
            st.write(station_info)
    else:
        st.write("Wybierz ID stacji w bocznym menu.")