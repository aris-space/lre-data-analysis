# Streamlit Interface Setup
# ---------------------------------------------------------------------------------------------------
import streamlit as st

import dbConnectionModule as db
import pandas as pd


def generate():
    # === Naviagation ===

    pg = st.navigation([st.Page("user_interface/home.py", title="Home", icon=":material/home:"), 
                        st.Page("user_interface/test_comparison.py", title="Compare Tests", icon=":material/lab_panel:"), 
                        st.Page("user_interface/sensor_comparison.py", title="Compare Sensores", icon=":material/speed:"), 
                        st.Page("user_interface/test_page.py", title="Playground", icon=":material/toys:")])
    pg.run()

    # === Sidebar ===

    # st.sidebar.page_link(st.Page("user_interface/home.py"), label="Dashboard", icon=":material/home:")

    config_options = db.get_config_ids_with_dates()

    if config_options.empty:
        config_options["config_id_date"] = ['No Sensors Available']

    st.sidebar.selectbox(
        label="Select Config ID", 
        options=config_options["config_id_date"],
        key="config_select",
        on_change=db.update_available_sensors
        )
    
    #st.sidebar.write(st.session_state.available_sensors.shape)

    for _, row in st.session_state.available_sensors.iterrows():
        st.sidebar.checkbox(label=row['name'])

    st.sidebar.divider()

    st.sidebar.markdown('''
        :red[Streamlit] **is interesting**
        ''')
    button = False
    button = st.sidebar.button("click me")


    st.sidebar.write(button)