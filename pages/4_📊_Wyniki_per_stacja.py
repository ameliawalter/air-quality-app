import streamlit as st
from matplotlib import pyplot as plt
from model.data_downloader import get_station_results, get_sensors_by_station_list, get_latest_station_results, get_station_ids_list
from model.api_handler import add_values_by_sensor

'''
Page allowing the user to display all sensors' last recorded results by station as a table (tab 1) or as charts by parameter (tab 2).
'''

st.title(":blue[Wyniki pomiarów wszystkich parametrów dla stacji z ostatniej godziny]")
st.write("Wybierz z bocznego menu ID stacji. Poniżej możesz zobaczyć wyniki z ostatniej godziny dla danej stacji.")

tab1, tab2 = st.tabs(["Tabela wyników", "Statystyki"])

station_ids = get_station_ids_list()
station_id = st.sidebar.selectbox("Wybierz ID stacji", station_ids)

with tab1:
    if station_id:
        sensors = get_sensors_by_station_list(station_id)
        for sensor in sensors:
            add_values_by_sensor(sensor)
        station_info = get_latest_station_results(station_id)
        if station_info.empty:
            st.write("Taka stacja nie istnieje.")
        else:
            st.write(station_info)
    else:
        st.write("Wybierz ID stacji w bocznym menu.")

with tab2:
    if station_id:
        sensors = get_sensors_by_station_list(station_id)
        for sensor in sensors:
            add_values_by_sensor(sensor)
        station_info = get_station_results(station_id)
        if station_info.empty:
            st.write("Taka stacja nie istnieje.")
        else:
            unique_sensor_codes = station_info['sensor_code'].unique()
            for sensor_code in unique_sensor_codes:
                sensor_data = station_info[station_info['sensor_code'] == sensor_code]
                plt.figure()
                plt.plot(sensor_data['timestamp'], sensor_data['value'])
                plt.title(f"Sensor Code: {sensor_code}")
                plt.xlabel("Timestamp")
                plt.ylabel("Value")
                plt.xticks(rotation=45, ha='right', fontsize=8)
                plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
                plt.tight_layout()
                st.pyplot(plt)
    else:
        st.write("Wybierz ID stacji w bocznym menu.")
