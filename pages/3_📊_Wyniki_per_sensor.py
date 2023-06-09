"""
Page allowing the user to display results by sensor from the most recent 3 days as a table (tab 1) or as a chart with statistics (tab 2).
Page also contains a legend (display_legend() function) to help user determine is results fall into air quality norms.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from model.api_handler import add_values_by_sensor
from model.data_downloader import get_sensor_results, get_sensor_ids_list, display_legend

st.title(":blue[Wyniki pomiarów danego sensora z ostatnich dni]")
st.write('''Wybierz z bocznego menu ID sensora. Poniżej możesz zobaczyć wyniki z ostatnich 3 dni dla danego sensora 
(czyli danego parametru jakości powietrza w konkretnej stacji) w postaci tabeli oraz wykresu i podstawowych statystyk.''')

tab1, tab2 = st.tabs(["Tabela wyników", "Statystyki"])

with tab1:
    st.sidebar.write("Wyświetl pomiary danego sensora")
    sensor_ids = get_sensor_ids_list()
    activate_search_window = st.sidebar.checkbox("Wpisz samodzielnie ID sensora")

    if activate_search_window:
        sensor_id = st.sidebar.text_input("Wpisz ID sensora")
        if sensor_id:
            add_values_by_sensor(sensor_id)
            sensor_info = get_sensor_results(sensor_id)
            if sensor_info.empty:
                st.write("Brak wyników lub sensora.")
            else:
                st.write(sensor_info)
        else:
            st.write("Wpisz ID sensora w bocznym menu.")

    else:
        selected_sensor_id = st.sidebar.selectbox("Wybierz ID sensora", sensor_ids)
        if selected_sensor_id:
            add_values_by_sensor(selected_sensor_id)
            sensor_info = get_sensor_results(selected_sensor_id)
            if sensor_info.empty:
                st.write("Taki sensor nie istnieje.")
            else:
                st.write(sensor_info)
        else:
            st.write("Wybierz ID sensora w bocznym menu.")

    display_legend()

with tab2:
    # Write a chart for all the values for the given sensor
    import altair as alt

    chart = alt.Chart(sensor_info).mark_line().encode(
        x='Czas:T',  # :T indicates that the data are timestamps
        y='Wynik:Q'  # :Q indicates that the data are quantitative
    )
    st.altair_chart(chart)

    # Display basic statistics
    max_row = sensor_info.loc[sensor_info['Wynik'].idxmax()]
    min_row = sensor_info.loc[sensor_info['Wynik'].idxmin()]
    st.write(f"Wartość maksymalna: {max_row['Wynik']} w dniu i o godzinie: {max_row['Czas']}")
    st.write(f"Wartość minimalna: {min_row['Wynik']} w dniu i o godzinie: {min_row['Czas']}")
    mean_value = round(sensor_info['Wynik'].mean(), 3)
    st.write(f"Średnia wartość: {mean_value}")

    # Display the trend
    time = list(range(len(sensor_info)))
    # Fit a degree-1 polynomial (a line) to the data
    trend_line = np.polyfit(time, sensor_info['Wynik'], 1)
    # trend_line[0] is the slope of the fitted line (i.e., the trend)
    st.write(f"Trend: {trend_line[0]}")
    sensor_info['Czas'] = pd.to_datetime(sensor_info['Czas'], format='%Y-%m-%d %H:%M:%S')
    # Sort the dataframe by timestamp
    sensor_info = sensor_info.sort_values('Czas')
    # Create a time variable
    time = list(range(len(sensor_info)))
    # Fit a degree-1 polynomial (a line) to the data
    trend_line = np.polyfit(time, sensor_info['Wynik'], 1)
    # Create a function that represents the trend line
    trend_func = np.poly1d(trend_line)
    # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plot the original data on the axes
    ax.plot(sensor_info['Czas'], sensor_info['Wynik'], label='Oryginalne dane')
    # Plot the trend line on the axes
    ax.plot(sensor_info['Czas'], trend_func(time), 'r--', label='Trend')
    # Add labels
    ax.set_xlabel('Czas')
    ax.set_ylabel('Wartość')
    ax.legend()
    # Rotate x-axis labels to prevent overlap
    plt.xticks(rotation=45)
    # Display the plot
    st.pyplot(fig)

    display_legend()
