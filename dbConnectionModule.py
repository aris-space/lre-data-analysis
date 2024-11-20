import streamlit as st
import pandas as pd
from mysql.connector import connect, Error
from io import StringIO
from datetime import timedelta

connection_config = {
    "host": st.secrets["DB_HOST"],
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
    "database": st.secrets["DB_NAME"],
}

def test():
    st.write('test')

# Function to Fetch Data from the Database in general
@st.cache_data(hash_funcs={connect: id}, show_spinner=False)
def fetch_data(query):
    """Fetch data from the database based on the SQL query."""
    try:
        with connect(**connection_config) as connection:
            return pd.read_sql(query, connection)
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return pd.DataFrame()

# Function to Fetch Config IDs to show them in the dropdown menu
def get_config_ids_with_dates():
    """Fetch distinct config IDs with dates."""
    query = "SELECT date, config_id, description FROM tests ORDER BY date DESC;"
    df = fetch_data(query)
    if not df.empty:
        # Combine config_id and date in a string for the dropdown
        df["config_id_date"] = df.apply(
            lambda row: f"{row['config_id']} - {row['date'].strftime('%Y-%m-%d')}",
            axis=1,
        )
    return df.set_index('config_id')

# Function to Fetch Sensor Names for a specific test
def get_sensors_with_data(config_id):
    query = f"""
    SELECT id, name
    FROM sensors
    WHERE config_id = '{config_id}';
    """
    return fetch_data(query)

# get the data for a sensor ID
def get_sensor_data(id):
    name = get_sensor_name(id)
    unit = get_sensor_unit(id)
    df = moving_average(get_sensor_values(id))

    return {'name': name, 'unit': unit, 'data': df}

# get the name of the sensor from id
def get_sensor_name(sensor_id):
    query = f"""
    SELECT name
    FROM sensors
    WHERE id = '{sensor_id}'
    """
    return fetch_data(query)['name'][0]

# Function to fetch all sensor values for a specific sensor_id
def get_sensor_values(sensor_id):
    query = f"""
    SELECT value, timestamp
    FROM sensor_values
    WHERE sensor_id = '{sensor_id}
    ORDER BY timestamp ASC;'
    """
    df = fetch_data(query)

    if not df.empty:
        # Normalize timestamps and convert to seconds
        df["timestamp"] = (pd.to_datetime(df["timestamp"], unit="s") - pd.to_datetime(df["timestamp"].min(), unit="s")) / timedelta(seconds=1)
    return df.set_index('timestamp').sort_index()

# Function to fetch sensor units for a specific sensor_id as a string
def get_sensor_unit(sensor_id):
    query = f"""
    SELECT unit
    FROM sensors_meta
    WHERE sensor_id = '{sensor_id}'
    """
    return fetch_data(query)['unit'][0]

# Function to Calculate Moving Average, change window if  you want to adapt how many values should be taken in the moving average
@st.cache_data
def moving_average(df, column="value", window=30):
    df["value_ma"] = df[column].rolling(window=window, center=True, win_type='gaussian').mean(std=window)
    # df["value_ma_std"] = df["value"].rolling(window=window).mean()
    df["value_ma"] = df["value_ma"].fillna(df[column])
    return df.drop(columns=column)

def update_available_sensors():
    st.session_state.selected_config_id = st.session_state["config_select"].split(" - ")[0]

    # get all sensors that were connected at this test
    st.session_state.available_sensors = get_sensors_with_data(st.session_state.selected_config_id)

    for sensor in st.session_state.selected_plot:
        st.session_state[sensor] = True

def update_selected_plot(key):

    for sensor in st.session_state.selected_plot:
        st.session_state[sensor] = False

    match st.session_state[key]:
        case "Plot 1":
            st.session_state.selected_plot = st.session_state.plotOne
        case "Plot 2":
            st.session_state.selected_plot = st.session_state.plotTwo
        case "Plot 3":
            st.session_state.selected_plot = st.session_state.plotThree
        case "Plot 4":
            st.session_state.selected_plot = st.session_state.plotFour
    
    for sensor in st.session_state.selected_plot:
        st.session_state[sensor] = True

def update_selected_sensor(**kwargs):
    sensor_id = kwargs['id']

    if not st.session_state[sensor_id]:
        if f"{sensor_id}" in st.session_state.selected_plot: 
            del st.session_state.selected_plot[f"{sensor_id}"]
        return
    
    st.session_state.selected_plot[f"{sensor_id}"] = get_sensor_data(sensor_id)

def update_selected_sensor_csv(**kwargs):
    sensor_id = kwargs['id']

    if not st.session_state[sensor_id]:
        if f"{sensor_id}" in st.session_state.selected_plot: 
            del st.session_state.selected_plot[f"{sensor_id}"]
        return
    df = st.session_state["csv_data"]
    sensor_data = moving_average(df[df['id'] == sensor_id], column="_value")[["_time", "value_ma"]]

    if not df.empty:
        # Normalize timestamps and convert to seconds (format="%Y-%m-%dT%H:%M:%SZ")

        sensor_data["_time"] = (pd.to_datetime(sensor_data["_time"], format='mixed') - pd.to_datetime(sensor_data["_time"].min(), format='mixed')) / timedelta(seconds=1)
    
    sensor_data.rename(columns={"_time": "timestamp"}, inplace=True)
    sensor_data.set_index("timestamp", inplace=True)
    sensor_data.sort_index(inplace=True)

    st.session_state.selected_plot[f"{sensor_id}"] = {'name': sensor_id, 'unit': '-', 'data': sensor_data}

# Function to convert dataframe into csv file so that data can be downloaded
# ATTENTION: atm we don't really use this option yet, we don't have the option implemented to download stuff, but i'm planning to implement this again
def convert_df_to_csv(df):
    csv = StringIO()
    df.to_csv(csv, index=False)
    csv.seek(0)
    return csv.getvalue()

# this here doesnt work yet, I'm not sure how to implement so that we eventually actually have the actuator names in there. but i'll keep trying
def fetch_actuator_times(config_id, actuator_name="DefaultActuator"):
    """Fetch activation and deactivation times for a given actuator and configuration."""
    query_on = f"""
    SELECT timestamp FROM actuator_values
    JOIN actuators ON actuator_values.actuator_id = actuators.id
    WHERE config_id = '{config_id}' AND actuators.name = '{actuator_name}' AND value = 1
    ORDER BY timestamp;
    """
    df_on = fetch_data(query_on)

    query_off = f"""
    SELECT timestamp FROM actuator_values
    JOIN actuators ON actuator_values.actuator_id = actuators.id
    WHERE config_id = '{config_id}' AND actuators.name = '{actuator_name}' AND value = 0
    ORDER BY timestamp;
    """
    df_off = fetch_data(query_off)

    # Convert timestamps from UNIX time to datetime
    if not df_on.empty:
        df_on["timestamp"] = pd.to_datetime(df_on["timestamp"], unit="s")
    if not df_off.empty:
        df_off["timestamp"] = pd.to_datetime(df_off["timestamp"], unit="s")

    return df_on["timestamp"].tolist(), df_off["timestamp"].tolist()