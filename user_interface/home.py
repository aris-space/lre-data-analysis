import streamlit as st

import dbConnectionModule as db

st.image("./aris-logo.png", width=100,)
st.title("Testing Database Visualisation")
st.text("App Creation Date: 2024-03-13, Updated: 2024-05-10")

st.metric("Tests Conducted", 100, 12)

st.write(db.test())