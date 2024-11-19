# Streamlit Interface Setup
# ---------------------------------------------------------------------------------------------------
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from io import StringIO

import dbConnectionModule as db
from user_interface.plots import show_plots as plots

def plot_select():
    with st.sidebar:
        option_menu(None, options=["Plot 1", "Plot 2", "Plot 3", "Plot 4"], 
            icons=['plus-circle', 'plus-circle', 'plus-circle', 'plus-circle'], 
            menu_icon="cast", default_index=0, orientation="horizontal",
            styles={
                "container": {"padding": "0!important"},
                "icon": {"font-size": "15px"}, 
                "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px"}
            },
            key="plot_select", on_change=db.update_selected_plot)
        
def sensor_panel():
    config_options = db.get_config_ids_with_dates()

    if config_options.empty:
        config_options["config_id_date"] = ['No Sensors Available']

    col1, col2 = st.sidebar.columns(2)
    col1.selectbox(
        label="Select Config ID", 
        options=config_options["config_id_date"],
        key="config_select",
        on_change=db.update_available_sensors
        )
    
    # Initalize available sensors (only relevant when the page initially loads)
    if st.session_state["selected_config_id"] is None:
        db.update_available_sensors()

    col2.markdown(f"**Description:** \n {config_options.loc[int(st.session_state.selected_config_id), 'description']}")
    
    sensor_col1, sensor_ccol2, sensor_ccol3 = st.sidebar.columns(3)
    nr_sensors = st.session_state.available_sensors.shape[0]

    for i in range(0, nr_sensors, 3):
        id = st.session_state.available_sensors.loc[i, 'id']
        sensor_col1.checkbox(label=st.session_state.available_sensors.loc[i, 'name'], 
                             key=id,
                             on_change=db.update_selected_sensor, kwargs={'id': id})

        if i + 1 >= nr_sensors: break
        id = st.session_state.available_sensors.loc[i + 1, 'id']
        sensor_ccol2.checkbox(label=st.session_state.available_sensors.loc[i + 1, 'name'],
                              key=id,
                              on_change=db.update_selected_sensor, kwargs={'id': id})

        if i + 2 >= nr_sensors: break
        id = st.session_state.available_sensors.loc[i + 2, 'id']
        sensor_ccol3.checkbox(label=st.session_state.available_sensors.loc[i + 2, 'name'],
                              key=id,
                              on_change=db.update_selected_sensor, kwargs={'id': id})

def upload_panel():
    uploaded_file = st.sidebar.file_uploader("Upload a .csv file", type=["csv"])
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file, comment='#')
        sensorIndex = df[(df['_measurement'] == 'actuator_commands')].index
        df = df.drop(sensorIndex)
        st.session_state["csv_data"] = df

        unique_ids = df['id'].unique()

        sensor_col1, sensor_ccol2, sensor_ccol3 = st.sidebar.columns(3)
        nr_sensors = len(unique_ids)
        for i in range(0, nr_sensors, 3):
            id = unique_ids[i]
            sensor_col1.checkbox(label=id, 
                                key=id,
                                on_change=db.update_selected_sensor_csv, kwargs={'id': id})

            if i + 1 >= nr_sensors: break
            id = unique_ids[i + 1]
            sensor_ccol2.checkbox(label=id,
                                key=id,
                                on_change=db.update_selected_sensor_csv, kwargs={'id': id})

            if i + 2 >= nr_sensors: break
            id = unique_ids[i + 2]
            sensor_ccol3.checkbox(label=id,
                              key=id,
                              on_change=db.update_selected_sensor_csv, kwargs={'id': id})

def generate():
    # === Sidebar ===
    # --- Headline ---

    st.sidebar.image("./aris-logo.png", width=100,)
    st.sidebar.title("Testing Database Visualisation")
    st.sidebar.text("App Creation Date: 2024-03-13, Updated: 2024-10-27")

    st.sidebar.divider()

    # --- Controls ---

    plot_select()

    st.sidebar.divider()

    sensor_panel()

    # TODO: add actuator_panel
                
    # st.sidebar.divider()

    # actuator_panel()

    # TODO: add coefficient_panel

    # st.sidebar.divider()

    # coefficient_panel()

    # TODO: add upload panel

    st.sidebar.divider()
    upload_panel()

    # === Content ===
    # --- Plots ---
    plots()