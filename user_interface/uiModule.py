# Streamlit Interface Setup
# ---------------------------------------------------------------------------------------------------
import streamlit as st
from streamlit_option_menu import option_menu

import dbConnectionModule as db
import pandas as pd


def generate():
    # === Naviagation ===

    pg = st.navigation([st.Page("user_interface/home.py", title="Home", icon=":material/home:"), 
                        st.Page("user_interface/test_comparison.py", title="Compare Tests", icon=":material/lab_panel:"), 
                        st.Page("user_interface/sensor_comparison.py", title="Compare Sensores", icon=":material/speed:"), 
                        st.Page("user_interface/test_page.py", title="Playground", icon=":material/toys:"),
                        st.Page("user_interface/plots.py", title="Plotting", icon=":material/show_chart:")])
    pg.run()

    # === Sidebar ===

    # st.sidebar.page_link(st.Page("user_interface/home.py"), label="Dashboard", icon=":material/home:")

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
                
    st.sidebar.divider()