import streamlit as st
import plotly.express as px

import dbConnectionModule as db

import pandas as pd
import numpy as np

if st.session_state.selected_config_id:
    sensor_options = db.get_sensors_with_data(st.session_state.selected_config_id)
    selected_sensors = st.multiselect(
        "Select Sensors:", sensor_options["name"], key="sensor_select"
    )
    st.session_state.selected_sensors = selected_sensors

    x_sensor = st.selectbox(
        label='Select Sensor for x-Axis',
        options=sensor_options['name']
    )

    st.session_state.x_sensor = [x_sensor]

    # st.write(sensor_options)

if st.button(label='Show Plot'):
    sensor_ids = db.get_sensor_ids(
                    st.session_state.selected_sensors,
                    st.session_state.selected_config_id,
                )
    x_sensor_id = db.get_sensor_ids(
                    st.session_state.x_sensor,
                    st.session_state.selected_config_id,
                )
    
    y_values_ma = db.get_sensor_values_with_ma_for_multiple_sensors(sensor_ids=sensor_ids, sensor_names=st.session_state.selected_sensors)
    x_values = db.get_sensor_values(sensor_id=int(x_sensor_id[0]))
    st.write(x_values)

    # === Combine DFs ===

    st.write(x_values.loc[:10, 'value'].mean())