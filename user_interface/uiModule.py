# Streamlit Interface Setup
# ---------------------------------------------------------------------------------------------------
import streamlit as st
import plotly.express as px


def generate():
    # === Naviagation ===

    pg = st.navigation([st.Page("user_interface/home.py", title="Home", icon=":material/home:"), 
                        st.Page("user_interface/test_comparison.py", title="Compare Tests", icon=":material/lab_panel:"), 
                        st.Page("user_interface/sensor_comparison.py", title="Compare Sensores", icon=":material/speed:"), 
                        st.Page("user_interface/test_page.py", title="Playground", icon=":material/toys:")])
    pg.run()

    # === Sidebar ===

    # st.sidebar.page_link(st.Page("user_interface/home.py"), label="Dashboard", icon=":material/home:")


    st.sidebar.write("This is a sidebar")

    st.sidebar.divider()

    st.sidebar.markdown('''
        :red[Streamlit] **is interesting**
        ''')
    button = False
    button = st.sidebar.button("click me")


    st.sidebar.write(button)