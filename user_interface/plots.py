import streamlit as st

import plotly.graph_objects as po
from plotly.subplots import make_subplots

SENSOR_TYPES = {
    "bar": "Pressure",
    "barg": "Pressure",
    "C": "Temperature",
    "N": "Force",
    "kg": "Mass",
    "g/s": "Massflow",
    "l/s": "Volumeflow",
    "s": "Time",
    "-": "No Unit"
}

def plot(data, key):
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
    st.plotly_chart(fig, use_container_width=True, key=key)

# === Create Content ===
def show_plots():    
    col1, col2 = st.columns(2)

    with col1:
        plot(st.session_state.plotOne, 'one')
        plot(st.session_state.plotThree, 'three')

    with col2:
        plot(st.session_state.plotTwo, 'two')
        plot(st.session_state.plotFour, 'four')