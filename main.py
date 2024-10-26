import streamlit as st

import user_interface.uiModule as ui

# === Session Variable Initialization ===

if "selected_config_id" not in st.session_state:
    st.session_state["selected_config_id"] = None

if "selected_sensors" not in st.session_state:
    st.session_state["selected_sensors"] = []

if "start_time" not in st.session_state:
    st.session_state["start_time"] = ""

if "end_time" not in st.session_state:
    st.session_state["end_time"] = ""

if "show_plot" not in st.session_state:
    st.session_state["show_plot"] = False

if "plotOne" not in st.session_state:
    st.session_state["plotOne"] = {}
    st.session_state["plotTwo"] = {}
    st.session_state["plotThree"] = {}
    st.session_state["plotFour"] = {}

if "selected_plot" not in st.session_state:
    st.session_state.selected_plot = st.session_state.plotOne

SENSOR_TYPES = {
    "bar": "Pressure",
    "barg": "Pressure",
    "C": "Temperature",
    "N": "Force",
    "kg": "Mass",
    "g/s": "Massflow",
    "l/s": "Volumeflow",
    "s": "Time"
}

ui.generate()