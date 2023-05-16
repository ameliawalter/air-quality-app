import streamlit as st
from controller.data_downloader import get_sensor_results, get_sensors_list

st.sidebar.write("Wyświetl pomiary danego sensora")

results_df = get_sensors_list()
sensor_ids = results_df['sensor_id'].tolist()

activate_search_window = st.sidebar.checkbox("Wpisz samodzielnie ID sensora")

if activate_search_window:
    sensor_id = st.sidebar.text_input("Wpisz ID sensora")
    if sensor_id:
        station_info = get_sensor_results(sensor_id)
        if results_df.empty:
            st.write("Brak wyników lub sensora.")
        else:
            st.write(results_df)
    else:
        st.write("Wpisz ID sensora w bocznym menu.")
else:
    selected_sensor_id = st.sidebar.selectbox("Wybierz ID sensora", sensor_ids)

    if selected_sensor_id:
        results_df = get_sensor_results(selected_sensor_id)
        if results_df.empty:
            st.write("Taka stacja nie istnieje.")
        else:
            st.write(results_df)
    else:
        st.write("Wybierz ID stacji w bocznym menu.")