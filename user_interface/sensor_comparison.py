import streamlit as st
import plotly.express as px
import pandas as pd

import dbConnectionModule as db

# Content for Sensor Comparison Tab
config_id_date_options = db.get_config_ids_with_dates()
if not config_id_date_options.empty:
    selected_config_id_date = st.selectbox(
        "Select a Config ID with Date:",
        config_id_date_options["config_id_date"],
        key="config_id_select",
        on_change=db.update_time_range,  # important so that when we change the test the timerange is updated again
    )

    if st.session_state.selected_config_id:
        sensor_options = db.get_sensors_with_data(st.session_state.selected_config_id)
        selected_sensors = st.multiselect(
            "Select Sensors:", sensor_options["name"], key="sensor_select"
        )
        st.session_state.selected_sensors = selected_sensors

        if selected_sensors:
            col1, col2 = st.columns(2)
            with col1:
                st.session_state["start_time"] = st.text_input(
                    "Start Time (YYYY-MM-DD HH:MM:SS)",
                    value=st.session_state["start_time"],
                    key="start_time_input",
                )
            with col2:
                st.session_state["end_time"] = st.text_input(
                    "End Time (YYYY-MM-DD HH:MM:SS)",
                    value=st.session_state["end_time"],
                    key="end_time_input",
                )

            if st.button("Show Plot"):
                sensor_ids = db.get_sensor_ids(
                    st.session_state.selected_sensors,
                    st.session_state.selected_config_id,
                )
                df_filtered = db.get_sensor_values_with_ma_for_multiple_sensors(
                    sensor_ids,
                    st.session_state.selected_sensors,
                    st.session_state["start_time"],
                    st.session_state["end_time"],
                )
                df_units = db.get_sensor_units_for_multiple_sensors(sensor_ids)

                st.write(df_units)

                if not df_filtered.empty:
                    st.plotly_chart(px.line(
                        df_filtered,
                        x="timestamp",
                        y="value_ma",
                        color="sensor_name",
                        title="Filtered Sensor Data",
                        labels={
                            "value_ma": "Sensor Value (Moving Avg)",
                            "timestamp": "Timestamp",
                        },
                    ), use_container_width=True)
                else:
                    st.error("No data found for the selected range.")
