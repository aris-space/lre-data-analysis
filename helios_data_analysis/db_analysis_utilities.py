import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import math
import matplotlib.pyplot as plt
pd.options.plotting.backend = "plotly"
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import mysql.connector as con
import os.path


class DatabaseInstance():

    ## Basic connection methods
    def __init__(self):
        self.connection = None
        self.hostip = '127.0.0.1'
        self.cursor = None
        self.tables = None

    def __enter__(self):
        self.connection, self.cursor = self.establishConnection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
         self.cursor.close()
         self.connection.close()

    def establishConnection(self):
        dbConnection = con.connect(
            host=self.hostip,
            user="root",
            password="aris",
            database="dacs"        
        )
        dbCursor = dbConnection.cursor(buffered=True, dictionary=True)
        return dbConnection, dbCursor
    
    def getTables(self):
        self.cursor.execute('SHOW tables')
        table_rows = self.cursor.fetchall()
        self.tables = pd.DataFrame(table_rows)
    
    def get_test_date(self, config_id):
        query = "SELECT date FROM tests WHERE config_id = %s" %(config_id)
        self.cursor.execute(query)
        return self.cursor.fetchone()['date'].strftime("%m-%d-%Y")

    def get_unc(self, sensor, config_id):
        query = "SELECT unc FROM sensors_meta INNER JOIN sensors ON sensor_id = sensors.id WHERE config_id = %s AND name LIKE '%s'" %(config_id, sensor)
        self.cursor.execute(query)
        unc = self.cursor.fetchone()
        return unc['unc']

    def get_unc_type(self, sensor, config_id):
        query = "SELECT unc_type FROM sensors_meta INNER JOIN sensors ON sensor_id = sensors.id WHERE config_id = %s AND name LIKE '%s'" %(config_id, sensor)
        self.cursor.execute(query)
        unc = self.cursor.fetchone()
        return unc['unc_type']

    def dfs_from_tables(self, tables):
        dfs = {}
        for table in tables:
            query = 'SELECT * FROM %s' %(table)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows)
            dfs[table] = df
        return dfs

    def values_sensors(self, sensors, config_id):
        values= {}
        for sensor in sensors:
            print(sensor)
            query = "SELECT * FROM sensor_values INNER JOIN sensors ON sensor_id = sensors.id WHERE config_id = %s AND name LIKE '%s'" %(config_id, sensor)
            self.cursor.execute(query)
            print('queried')
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows)
            df = df.sort_values(by= ['timestamp'])
            values[sensor] = df
        return values

    def values_sensors_all(self, sensors):
        values= {}
        for sensor in sensors:
            query = "SELECT * FROM sensor_values INNER JOIN sensors ON sensor_id = sensors.id WHERE name LIKE '%s'" %(sensor)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows)
            df = df.sort_values(by= ['timestamp'])
            values[sensor] = df
        return values

    def values_sensors_selected(self, sensors, ids):
        string = 'AND ('
        for j, id in enumerate(ids):
            string = string + 'sensors.config_id = %s' %(id)
            if j is not len(ids)-1:
                string = string + ' OR '
        string = string + ')'
        values= {}
        for sensor in sensors:
            query = "SELECT * FROM sensor_values INNER JOIN sensors ON sensor_id = sensors.id WHERE name LIKE '%s' %s" %(sensor, string)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows)
            df = df.sort_values(by= ['timestamp'])
            values[sensor] = df
        return values

    def values_actuators(self, actuators, config_id):
        values= {}
        for actuator in actuators:
            print("query: actuator")
            query = "SELECT * FROM actuator_values INNER JOIN actuators ON actuator_id = actuators.id WHERE config_id = %s AND name LIKE '%s'" %(config_id, actuator)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            df = pd.DataFrame(rows)
            df = df.sort_values(by= ['timestamp'])
            values[actuator] = df
        return values

    def values_circuits(self, config_id):
        query = "SELECT * FROM circuit_values INNER JOIN actuators ON actuator_id = actuators.id WHERE config_id = %s" %(config_id)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows)
        return df

    def values_states(self, config_id):
        query = "SELECT * FROM states WHERE config_id = %s" %(config_id)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows)
        return df

    def get_firing_times(self, config_id):
        query = "SELECT timestamp FROM states WHERE config_id = %s AND state LIKE 'firing confirmation'" %(config_id)
        self.cursor.execute(query)
        firing_start = self.cursor.fetchall()
        firing_starts = []
        for element in firing_start:
            firing_starts.append(element['timestamp'])
        query = "SELECT timestamp FROM states WHERE config_id = %s AND state LIKE 'POST_FIRING'" %(config_id)
        self.cursor.execute(query)
        firing_end = self.cursor.fetchall()
        firing_ends = []
        for element in firing_end:
            firing_ends.append(element['timestamp'])
        return firing_starts, firing_ends
    
    def get_actuation_values(self, config_id, actuator_name):
        query = "SELECT timestamp FROM actuator_values INNER JOIN actuators ON actuator_id = actuators.id WHERE config_id = %s AND value = 1 AND name = '%s' ORDER BY timestamp ASC" %(config_id, actuator_name)
        self.cursor.execute(query)
        on = self.cursor.fetchall()
        ons = []
        for element in on:
            ons.append(element['timestamp'])
        query = "SELECT timestamp FROM actuator_values INNER JOIN actuators ON actuator_id = actuators.id WHERE config_id = %s AND value = 0 AND name = '%s' ORDER BY timestamp ASC" %(config_id, actuator_name)
        self.cursor.execute(query)
        off = self.cursor.fetchall()
        offs = []
        for element in off:
            offs.append(element['timestamp'])
        return ons, offs