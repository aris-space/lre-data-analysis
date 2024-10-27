import streamlit as st

import user_interface.uiModule as ui
import dbConnectionModule as db

# === Session Variable Initialization ===

if "selected_config_id" not in st.session_state:
    st.session_state["selected_config_id"] = None

if "plotOne" not in st.session_state:
    st.session_state["plotOne"] = {}
    st.session_state["plotTwo"] = {}
    st.session_state["plotThree"] = {}
    st.session_state["plotFour"] = {}

if "selected_plot" not in st.session_state:
    st.session_state.selected_plot = st.session_state.plotOne

ui.generate()