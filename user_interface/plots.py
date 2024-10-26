import streamlit as st

import plotly.express as px
import plotly.graph_objects as po
from plotly.subplots import make_subplots

import pandas as pd

import dbConnectionModule as db
from main import SENSOR_TYPES

def plot(data):
    fig = make_subplots(specs=[[{"secondary_y" : True}]], x_title='Time [s]')

    units = ['none']

    for _, sensor_trace in data.items():

        if sensor_trace['unit'] not in units:
            units.append(sensor_trace['unit'])
        unit = units.index(sensor_trace['unit'])

        fig.add_trace(po.Scatter(
            x=sensor_trace['data'].index,
            y=sensor_trace['data']["value_ma"],
            name=sensor_trace['name'],
            yaxis='y' + str(unit)
        ))

        fig.update_layout({"yaxis" + str(unit): {"title": f"{SENSOR_TYPES[sensor_trace['unit']]} [{'°C' if sensor_trace['unit'] == 'C' else sensor_trace['unit']}]"}})

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

# st.write(st.session_state.selected_plot)

# st.write(st.session_state.plotOne, st.session_state.plotTwo, st.session_state.plotThree, st.session_state.plotFour)

# === Create 1st Plot ===

plot(st.session_state.plotOne)