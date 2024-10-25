import streamlit as st

import plotly.express as px
import plotly.graph_objects as po
from plotly.subplots import make_subplots

import pandas as pd

import dbConnectionModule as db
from main import SENSOR_TYPES

# Content for Sensor Comparison Tab
config_id_date_options = db.get_config_ids_with_dates()
if not config_id_date_options.empty:
    selected_config_id_date = st.selectbox(
        label="Select a Config ID with Date:",
        options=config_id_date_options["config_id_date"],
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
                dfs_filtered = db.get_sensor_values_with_ma_for_multiple_sensors(
                    sensor_ids,
                    st.session_state.selected_sensors,
                    st.session_state["start_time"],
                    st.session_state["end_time"],
                )

                # st.write(dfs_filtered)

                fig = make_subplots(specs=[[{"secondary_y" : True}]], x_title='Time [s]')

                ctr = 1
                names = []
                for unit, dict in dfs_filtered.items():
                    for name, df in dict.items():

                        if df.empty:
                            st.error("No data found for the selected range.")
                            continue
                        
                        fig.add_trace(po.Scatter(
                            x=df["normalized_timestamp"],
                            y=df["value_ma"],
                            name=name,
                            yaxis='y' + str(ctr)
                        ))

                    fig.update_layout({"yaxis" + str(ctr): {"title": f"{SENSOR_TYPES[unit]} [{'°C' if unit == 'C' else unit}]"}})
                    ctr += 1

                fig.update_layout(
                    yaxis2={
                        "overlaying": "y",
                        "side": "right"
                    },
                    yaxis3={
                        "anchor": "free",
                        "overlaying": "y",
                        "autoshift": True
                    },
                    yaxis4={
                        "anchor": "free",
                        "overlaying": "y",
                        "autoshift": True,
                        "side": "right"
                    },
                    yaxis5={
                        "anchor": "free",
                        "overlaying": "y",
                        "autoshift": True,
                    },
                    yaxis6={
                        "anchor": "free",
                        "overlaying": "y",
                        "autoshift": True,
                        "side": "right"
                    } 
                )
                
                st.plotly_chart(fig, use_container_width=True)
