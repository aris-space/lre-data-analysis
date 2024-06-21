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

from db_analysis_utilities import *

GLOBAL_PLOT_FILE_PREFIX = "/home/dacs/git/data-management/database_pro/"

#plot sensors of a given test in one plot
def plot_sensors(date, sensor_names, sensors, start, end, title=None, titlex= None, titley= None, events = [], event_names=[]):
    fig = go.Figure()
    for i, sensor in enumerate(sensors):
        sensor_name = sensor_names[i]
        values = sensors[sensor]
        sensor_cut = values[(values['timestamp'] >= start) & (values['timestamp'] <= end)]
        sensor_cut['time_relative'] = (sensor_cut['timestamp'] - start)
        fig.add_trace(go.Scatter(x=sensor_cut['time_relative'],y=sensor_cut['value'], name=sensor_name))
    #fig.update_layout(title = title, xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')
    for i, event in enumerate(events):
        print(event)
        if isinstance(event, list): 
            if len(event) == 0:
                print('empty')
        else:
            if isinstance(event, list):
                event=event[0]
            event_name = event_names[i]
            if event-start>= 0:
                fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
    fig.show()
    filepath = f"{GLOBAL_PLOT_FILE_PREFIX}simpleplot_{str(date)}.html"
    i=0
    while os.path.exists(filepath):
        filepath = f"{GLOBAL_PLOT_FILE_PREFIX}simpleplot_{str(date)}_{str(i)}.html"
        i=i+1
    fig.write_html(filepath)

#plot sensors in multiple subplot. n can be thought of as a matrix that specidies how many sensors should go into each frame
def subplot_sensors(date, sensor_names, sensors, start=0, end=1000000000000000000000, titles=None, titlex=None, titley=None, rows=1, columns=1, n=1000, events=[], event_names=[]):
    fig = make_subplots(rows=rows, cols=columns, subplot_titles=titles)
    i = 0
    j = 1
    row = 1
    col = 1
    for sensor in sensors:
        sensor_name = sensor_names[i]
        values = sensors[sensor]
        sensor_cut = values[(values['timestamp'] >= start) & (values['timestamp'] <= end)]
        sensor_cut['time_relative'] = sensor_cut['timestamp'] - start
        fig.add_trace(go.Scatter(x=sensor_cut['time_relative'],y=sensor_cut['value'], name=sensor_name), row=row, col=col)
        fig.update_yaxes(title_text = titley[row-1][col-1], row = row, col = col)
        fig.update_xaxes(title = titlex, row=row, col = col)
        i=i+1
        if col is columns and j==n[row-1][col-1]:
            col = 1
            row = row + 1
            j = 1
        elif j==n[row-1][col-1]:
            col = col + 1
            j = 1
        else:
            j = j+1
    fig.update_layout(template = 'plotly_dark')
    i=0
    for event in events:
        if isinstance(event, list):
            event=event[0]
        event_name = event_names[i]
        if event-start>= 0:
            fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
        i=i+1
    fig.show()
    filepath = f"{GLOBAL_PLOT_FILE_PREFIX}multiplot_{date}.html"
    i=0
    while os.path.exists(filepath):
        filepath = f"{GLOBAL_PLOT_FILE_PREFIX}multiplot_{date}_{str(i)}.html"
        i= i+1
    fig.write_html(filepath)

# plot the given sensors in a heatmap
def heatmap(date, sensor_names, sensors_values, start=0, end=1000000000000000000000, title=None, titlex= None, titley= None, events = [], event_names=[]):
    z = []
    for i in range(0,len(sensor_names)):
        values = sensors_values[sensor_names[i]]
        cut_values = values[(values['timestamp']<=end) & (values['timestamp'] >= start)]
        z.append(cut_values['value'])
    cut_values['relative time'] = cut_values['timestamp'] - start
    fig = go.Figure(data=go.Heatmap(
                   z= z,
                   x= cut_values['relative time'],
                   y= sensor_names,
                   hoverongaps = False,
                   colorscale='Portland'))
    i = 0
    fig.update_layout(xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')
    for event in events:
        if isinstance(event, list):
            event=event[0]
        event_name = event_names[i]
        if event-start>= 0:
            fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
        i=i+1
    fig.show()
    filepath = f"{GLOBAL_PLOT_FILE_PREFIX}heatmap_{date}.html"
    i=0
    while os.path.exists(filepath):
        filepath = f"{GLOBAL_PLOT_FILE_PREFIX}heatmap_{date}_{str(i)}.html"
        i = i+1
    fig.write_html(filepath)

# compare different tests: all sensors from one test go into one frame. So the number of tests should equal rows * columns
def compare_tests(config_ids, sensor_names, sensors, starts, ends, titles=None, titlex=None, titley=None, rows=1, columns=1, events=None, event_names=None):
    fig = make_subplots(rows=rows, cols=columns, subplot_titles=titles)
    row = 1
    col = 1
    for id in config_ids:
        for i, sensor in enumerate(sensors[id]):
            sensor_name = sensor_names[i]
            values = sensors[id][sensor_name]
            sensor_cut = values[(values['timestamp'] >= starts[id]) & (values['timestamp'] <= ends[id])]
            sensor_cut['time_relative'] = sensor_cut['timestamp'] - starts[id]
            fig.add_trace(go.Scatter(x=sensor_cut['time_relative'],y=sensor_cut['value'], name=sensor_name+ '_test_'+str(id)), row=row, col=col)
        if events is not None:
            for j, event in enumerate(events[id]):
                event_name = event_names[id][j]
                if isinstance(event, list):
                    event=event[0]
                if event - starts[id]>=0:
                    fig.add_vline(x=event-starts[id], line_width=1, line_dash="dash", line_color="white", annotation_text = event_name, row=row, col = col)
        if col is columns:
            col = 1
            row = row + 1
        else:
            col = col + 1
    fig.update_layout(xaxis_title = titlex, yaxis_title = titley, template = 'plotly_dark')
    fig.show()
    filepath = "{GLOBAL_PLOT_FILE_PREFIX}compare_tests.html"
    i=0
    while os.path.exists(filepath):
        filepath = f"{GLOBAL_PLOT_FILE_PREFIX}compare_tests_{str(i)}.html"
        i=i+1
    fig.write_html(filepath)

# plot the relation between three sensor values in a scatter plot (third sensor is color scale)
def three_fold_relation(db, x_sensor, y_sensor, color_sensor, config_ids, title, title_x, title_y, xmin, xmax, ymin, ymax):
    all = db.values_sensors_selected([x_sensor,y_sensor,color_sensor], config_ids)
    x = all[x_sensor]
    y = all[y_sensor]
    c = all[color_sensor]
    x['datetime'] = pd.to_datetime(x['timestamp'], unit='s')
    y['datetime'] = pd.to_datetime(y['timestamp'], unit='s')
    c['datetime'] = pd.to_datetime(c['timestamp'], unit='s')
    y_grouped = y.groupby(pd.Grouper(key='datetime', freq='100ms')).mean()
    c_grouped = c.groupby(pd.Grouper(key='datetime', freq='100ms')).mean()
    x_grouped = x.groupby(pd.Grouper(key='datetime', freq='100ms')).mean()
    joined = x_grouped.merge(y_grouped, left_on='datetime', right_on = 'datetime')
    joined = joined.merge(c_grouped, left_on='datetime', right_on = 'datetime')
    filtered = joined.loc[(joined['value_y']>ymin)&(joined['value_x']>xmin)&(joined['value_y']<ymax)&(joined['value_x']<xmax)]
    filtered.rename(columns = {'value':color_sensor, 'value_x':x_sensor, 'value_y':y_sensor}, inplace = True)
    joined.rename(columns = {'value':color_sensor, 'value_x':x_sensor, 'value_y':y_sensor}, inplace = True)
    p =np.polyfit(filtered[x_sensor],filtered[y_sensor],1)
    p=np.poly1d(p)
    x=np.linspace(xmin-1,xmax+1,1000)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered[x_sensor],y=filtered[y_sensor], mode = 'markers', marker = dict(colorscale = 'Plasma', showscale = True), marker_color= filtered[color_sensor], name='Data Points'))
    fig.add_trace(go.Scatter(x=x, y=p(x), name = 'Linear Curve Fit'))
    fig.update_layout(title = title, xaxis_title = title_x, yaxis_title = title_y)
    fig.update_layout(template = 'plotly_dark')
    fig.show()
    filepath = "{GLOBAL_PLOT_FILE_PREFIX}three_fold.html"
    i=0
    while os.path.exists(filepath):
        filepath = f"{GLOBAL_PLOT_FILE_PREFIX}three_fold_{str(i)}.html"
        i=i+1
    fig.write_html(filepath)

#same as three fold relation only without color scale
def two_fold_relation(db, x_sensor, y_sensor, config_ids, title, title_x, title_y, title_color, xmin, xmax, ymin, ymax):
    all = db.values_sensors_selected([x_sensor,y_sensor], config_ids)
    x = all[x_sensor]
    y = all[y_sensor]
    x['datetime'] = pd.to_datetime(x['timestamp'], unit='s')
    y['datetime'] = pd.to_datetime(y['timestamp'], unit='s')
    y_grouped = y.groupby(pd.Grouper(key='datetime', freq='100ms')).mean()
    x_grouped = x.groupby(pd.Grouper(key='datetime', freq='100ms')).mean()
    joined = x_grouped.merge(y_grouped, left_on='datetime', right_on = 'datetime')
    filtered = joined.loc[(joined['value_y']>ymin)&(joined['value_x']>xmin)&(joined['value_y']<ymax)&(joined['value_x']<xmax)]
    filtered.rename(columns = {'value_x':x_sensor, 'value_y':y_sensor}, inplace = True)
    p =np.polyfit(filtered[x_sensor],filtered[y_sensor],1)
    p=np.poly1d(p)
    x=np.linspace(xmin-1,xmax+1,1000)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered[x_sensor],y=filtered[y_sensor], mode = 'markers', name='Data Points'))
    fig.add_trace(go.Scatter(x=x, y=p(x), name = 'Linear Curve Fit'))
    fig.update_layout(title = title, xaxis_title = title_x, yaxis_title = title_y)
    fig.update_layout(template = 'plotly_dark')
    fig.show()
    filepath = "{GLOBAL_PLOT_FILE_PREFIX}two_fold.html"
    i=0
    while os.path.exists(filepath):
        filepath = f"{GLOBAL_PLOT_FILE_PREFIX}two_fold_{str(i)}.html"
        i=i+1
    fig.write_html(filepath)

# for each group of sensors and group of tests a new analysis_instance should be created. the instance saves the data in pandas dataframes so it doesn't have to access the database all the time.
# also the events only need to be initialized once and can then be used for all plots
class Analysis_Instance():
    def __init__(self, db, config_ids, sensors, yaxis):
        self.config_ids = config_ids
        self.sensors = sensors
        self.yaxis = yaxis
        self.sensors_values = {}
        self.firing_starts = {}
        self.firing_ends = {}
        self.ends = {}
        self.starts = {}
        self.fss_throttle = {}
        self.actuations_fss_on = {}
        self.actuations_oss_on = {}
        self.actuations_fss_off = {}
        self.actuations_oss_off = {}
        self.actuations_fss_prz_on = {}
        self.actuations_oss_prz_on = {}
        self.actuations_fss_prz_off = {}
        self.actuations_oss_prz_off = {}
        self.actuations_fss_vnt_on = {}
        self.actuations_oss_vnt_on = {}
        self.actuations_fss_vnt_off = {}
        self.actuations_oss_vnt_off = {}
        self.actuations_oss_fil_on = {}
        self.actuations_oss_fil_off = {}
        self.actuations_ign_fue_on = {}
        self.actuations_ign_fue_off = {}
        self.actuations_ign_oxd_on = {}
        self.actuations_ign_oxd_off = {}
        self.igns_on = {}
        self.igns_off = {}
        self.thr_sl_on = {}
        self.thr_sl_off = {}
        self.dates = {}
        self.event_list = {}
        self.event_names = {}
        self.fill_dicts(db)
        self.initialize_events()
        
        #self.uncs = self.uncertainties(db, sensors, config_ids)
        #self.unctypes = self.uncertainty_types(db, sensors, config_ids)

    def uncertainties(self, db, sensors, config_ids):
        unc_dict = {}
        for config in config_ids:
            for sensor in sensors:
                unc_dict[config].append(db.get_unc(sensor, config))
        return unc_dict

    def uncertainty_types(self, db, sensors, config_ids):
        unc_dict = {}
        for config in config_ids:
            for sensor in sensors:
                unc_dict[config].append(db.get_unc_type(sensor, config))
        return unc_dict

    # this is the function that is called at initialization to fill all the dictionaries with values
    def fill_dicts(self, db):
        for config_id in self.config_ids:
            values = db.values_sensors(self.sensors, config_id)
            self.sensors_values[config_id] = values

            # values_thr = db.values_actuators(["at_fss_thr"], config_id)
            # self.fss_throttle[config_id] = values_thr
            # timestamps of firing detection
            firing_start, firing_end = db.get_firing_times(config_id)
            self.firing_starts[config_id] = firing_start
            self.firing_ends[config_id] = firing_end
            #timestamps for actuators, add actuator if needed1 get_actuation_values returns two list of timestamps: the first where the value is 1 (usually on), the second where the value is 0
            actuation_oss_on, actuation_oss_off = db.get_actuation_values(config_id, 'at_oss_mnv')
            self.actuations_oss_on[config_id] = actuation_oss_on
            self.actuations_oss_off[config_id] = actuation_oss_off
            actuation_fss_on, actuation_fss_off = db.get_actuation_values(config_id, 'at_fss_mnv')
            self.actuations_fss_on[config_id] = actuation_fss_on
            self.actuations_fss_off[config_id] = actuation_fss_off

            actuation_oss_prz_on, actuation_oss_prz_off = db.get_actuation_values(config_id, 'at_oss_prz')
            self.actuations_oss_prz_on[config_id] = actuation_oss_prz_on
            self.actuations_oss_prz_off[config_id] = actuation_oss_prz_off
            actuation_fss_prz_on, actuation_fss_prz_off = db.get_actuation_values(config_id, 'at_fss_prz')
            self.actuations_fss_prz_on[config_id] = actuation_fss_prz_on
            self.actuations_fss_prz_off[config_id] = actuation_fss_prz_off

            actuation_oss_vnt_on, actuation_oss_vnt_off = db.get_actuation_values(config_id, 'at_oss_vnt')
            self.actuations_oss_vnt_on[config_id] = actuation_oss_vnt_on
            self.actuations_oss_vnt_off[config_id] = actuation_oss_vnt_off
            actuation_fss_vnt_on, actuation_fss_vnt_off = db.get_actuation_values(config_id, 'at_fss_vnt')
            self.actuations_fss_vnt_on[config_id] = actuation_fss_vnt_on
            self.actuations_fss_vnt_off[config_id] = actuation_fss_vnt_off

            actuation_oss_fil_on, actuation_oss_fil_off = db.get_actuation_values(config_id, 'at_oss_fil')
            self.actuations_oss_fil_on[config_id] = actuation_oss_fil_on
            self.actuations_oss_fil_off[config_id] = actuation_oss_fil_off

            actuation_ign_fue_on, actuation_ign_fue_off = db.get_actuation_values(config_id, 'at_ign_fue')
            self.actuations_ign_fue_on[config_id] = actuation_ign_fue_on
            self.actuations_ign_fue_off[config_id] = actuation_ign_fue_off

            actuation_ign_oxd_on, actuation_ign_oxd_off = db.get_actuation_values(config_id, 'at_ign_oxd')
            self.actuations_ign_oxd_on[config_id] = actuation_ign_oxd_on
            self.actuations_ign_oxd_off[config_id] = actuation_ign_oxd_off

            ign_on, ign_off= db.get_actuation_values(config_id, 'at_ign_spk')
            self.igns_on[config_id] = ign_on
            self.igns_off[config_id] = ign_off

            thr_sl_on, thr_sl_off= db.get_actuation_values(config_id, 'at_eng_led')
            self.thr_sl_on[config_id] = thr_sl_on
            self.thr_sl_off[config_id] = thr_sl_off
            # set start and end values according to needs. The values here are just the start and end of the data acquisition, you can just add/substract time in seconds
            sensor_df = values[self.sensors[0]]
            self.ends[config_id] = sensor_df['timestamp'].max()
            self.starts[config_id] = sensor_df['timestamp'].min()
            self.dates[config_id] = db.get_test_date(config_id)
    
    # this is the function that is used at initialization to fill all the event dictionaries for later use in plots (to create the vertical lines)
    def initialize_events(self):
        for i in self.config_ids:
            self.event_list[i] = []
            self.event_names[i] = []
            for element in self.firing_starts[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('firing sequence start')
            for element in self.firing_ends[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('firing_end')
            for element in self.actuations_oss_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('oxidizer main valve open')
            for element in self.actuations_fss_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('fuel main valve open')
            for element in self.actuations_oss_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('oxidizer main valve close')
            for element in self.actuations_fss_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('fuel main valve close')

            for element in self.actuations_oss_prz_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('oss pressurization open')
            for element in self.actuations_fss_prz_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('fss pressurization open')
            for element in self.actuations_oss_prz_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('oss pressurization close')
            for element in self.actuations_fss_prz_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('fss pressurization close')

            for element in self.actuations_oss_vnt_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('oss vent close')
            for element in self.actuations_fss_vnt_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('fss vent close')
            for element in self.actuations_oss_vnt_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('oss vent open')
            for element in self.actuations_fss_vnt_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('fss vent open')
            for element in self.actuations_oss_fil_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('oss fill open')
            for element in self.actuations_oss_fil_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('oss fill close')

            for element in self.actuations_ign_fue_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('igniter fuel valve open')
            for element in self.actuations_ign_fue_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('igniter fuel valve close')

            for element in self.actuations_ign_oxd_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('igniter oxidizer valve open')
            for element in self.actuations_ign_oxd_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('igniter oxidizer valve close')

            for element in self.igns_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('spark plug on')
            for element in self.igns_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('spark plug off')

            for element in self.thr_sl_on[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('led on')
            for element in self.thr_sl_off[i]:
                self.event_list[i].append(element)
                self.event_names[i].append('led off')

    # this in principle only uses plot_sensors to create one plot per test
    def one_graph_per_test(self, title):
        for i in self.config_ids: 
            print('plotting test')
            plot_title = title + ' ' +str(self.dates[i])
            #plot_sensors(sensors, sensors_values[i], firing_starts[i][0]-5, firing_ends[i][len(firing_ends[i])-1]+5, title, 'time in s', 'Pressure in Bar', event_list, event_names)
            plot_sensors(self.dates[i], self.sensors, self.sensors_values[i], self.starts[i], self.ends[i], plot_title, 'Time in s', self.yaxis[0], self.event_list[i], self.event_names[i])

    # this plots all sensors in separate plots and for each sensor also plots the moving average with all the window sizes given in windows (list of integers > 0)
    def moving_average(self, config_id, windows):
        i = config_id
        for k,sensor in enumerate(self.sensors):
            df = self.sensors_values[i][sensor]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp']-self.starts[i],y=df['value'], name='Data points'))
            for n in windows:
                string = 'value_avg_' + str(n)
                df[string] = df['value'].rolling(n).mean()
                name = 'Window size '  + str(n)
                fig.add_trace(go.Scatter(x=df['timestamp']-self.starts[i],y=df[string], name=name))
            fig.update_layout(title = sensor, xaxis_title = 'time in s', yaxis_title = self.yaxis[k])
            for j, event in enumerate(self.event_list[i]):
                event_name = self.event_names[i][j]
                if isinstance(event, list):
                    event=event[0]
                if event-self.starts[i]>= 0:
                     fig.add_vline(x=event-self.starts[i], line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
            fig.update_layout(template = 'plotly_dark')
            fig.show()
            filepath = f"{GLOBAL_PLOT_FILE_PREFIX}moving_average_{sensor}_{self.date[config_id]}.html"
            i=0
            while os.path.exists(filepath):
                filepath = f"{GLOBAL_PLOT_FILE_PREFIX}moving_average_{sensor}_{self.date[config_id]}_{str(i)}.html"
                i=i+1
            fig.write_html(filepath)

    # plot the sensors in subplots see subplot_sensors
    def multiplot_sensors(self, config_id, titles, yaxis, rows, columns, n_matrix):
        subplot_sensors(self.dates[config_id], self.sensors, self.sensors_values[config_id], self.starts[config_id], self.ends[config_id], titles, 'Time in s', yaxis, rows, columns, n_matrix, self.event_list[config_id], self.event_names[config_id])
    
    # plots heatmap of given tests, see heatmap
    def make_heatmap(self, config_id, title):
        i = config_id
        heatmap(self.dates[i], self.sensors, self.sensors_values[i], start = self.starts[i], end = self.ends[i], events=self.event_list[i], event_names=self.event_names[i], title = title, titlex='Time in s', titley='Sensor')

    # this compares all the tests in subplots see compare_plots
    def test_comparison(self, config_ids, title):
        title = []
        for id in config_ids:
            title.append(f'Temperatures test {self.dates[id]}')
        title = tuple(title)
        compare_tests(config_ids, self.sensors, self.sensors_values, self.starts, self.ends, title, 'Time in s', 'temperature in °C', 1, len(config_ids), self.event_list, self.event_names)

    # this compares all tests directly in a single plot (beware: it's best to plot few sensors here or it gets really confusing)
    # the sync parameter is central here as it gives you the event to sync all tests about, this should be one of the event dictionaries in the class definition
    def overlay_tests(self, sync_parameter):
        fig = go.Figure()
        for id in self.config_ids:
            for sensor in self.sensors:
                df = self.sensors_values[id][sensor]
                fig.add_trace(go.Scatter(x = df['timestamp']-sync_parameter[id][0], y = df['value'].rolling(30).mean(), name = sensor + ' test '+ str(id)))

            # for i, event in enumerate(self.event_list[id]):
    
            #     if isinstance(event, list): 
            #         if len(event) == 0:
            #             print('empty')
            #     else:
            #         if isinstance(event, list):
            #             event=event[0]
            #         event_name = self.event_names[id][i]
            
            #         x = pd.to_datetime(event, unit = 's')
            #         x = event * 1000
            #     # fig.add_vline(x=event-start, line_width=1, line_dash="dash", line_color="white", annotation_text = event_name)
            #         fig.add_vline(x=x, line_width=1, line_dash="dash", line_color="white",annotation_text = event_name+ ' test ' + str(id))
            #     #fig.add_annotation(yref= 'y domain',x=x, y=0.95-(i%15)*0.05, text=event_name)
    
            # y=[]
            # for i, a in enumerate(fig.to_dict()["layout"]["annotations"]):
            #     y.append([a, 0.95-(i%15)*0.05])

            # fig.update_layout(annotations=[{**element[0], **{"y":element[1]}}  for element in y])
            for j, event in enumerate(self.event_list[id]):
                if isinstance(event, list):
                    event=event[0]
                event_name = self.event_names[id][j]
                fig.add_vline(x=event-sync_parameter[id][0], line_width=1, line_dash="dash", line_color="white", annotation_text = event_name+ ' test ' + str(id))
        fig.update_layout(title = sensor, xaxis_title = 'Time in s', yaxis_title = self.yaxis[0])
        #fig.update_layout(template = 'plotly_dark')
        fig.show()
        filepath = "{GLOBAL_PLOT_FILE_PREFIX}overlay_tests.html"
        i=0
        while os.path.exists(filepath):
            filepath = f"{GLOBAL_PLOT_FILE_PREFIX}overlay_tests_{str(i)}.html"
            i=i+1
        fig.write_html(filepath)