#!/usr/bin/python3
# -*- coding: utf-8

try:
    from matplotlib import pyplot as plt
    plot_fkt = True
except:
    plot_fkt = False

import logging
from shapely import geometry as geopy

from oemof import db
from oemof.db import coastdat

from feedinlib import powerplants as plants
from feedinlib import models

# Feel free to remove or change these lines
import warnings
warnings.simplefilter(action="ignore", category=RuntimeWarning)
logging.getLogger().setLevel(logging.INFO)

# Specification of the pv model
required_parameter_pv = {
    'azimuth': 'Azimuth angle of the pv module',
    'tilt': 'Tilt angle of the pv module',
    'module_name': 'According to the sandia module library.',
    'albedo': 'Albedo value'}

# Specification of the weather data set CoastDat2
coastDat2 = {
    'dhi': 0,
    'dirhi': 0,
    'pressure': 0,
    'temp_air': 2,
    'v_wind': 10,
    'Z0': 0}

azimuth_dc = {}
#todo: füllen!
# Specification of the pv module
for ind in (1,2,3,4,5,6):
	pv_plant = {
		'module_name': 'Advent_Solar_Ventura_210___2008_',
		'azimuth': azimuth_dc[str(ind)],
		'tilt': tilt_dc[str(ind)],
		'albedo': albedo_dc[str(ind)]}

# Specification of the pv module
yingli210 = {
    'module_name': 'Yingli_YL210__2008__E__',
    'azimuth': 180,
    'tilt': 30,
    'albedo': 0.2}

loc_parchim = {
    'tz': 'Europe/Berlin',
    'latitude': 53.41,
    'longitude': 11.84
    }


year = 2010

conn = db.connection()
my_weather = coastdat.get_weather(
    conn, geopy.Point(loc_parchim['longitude'], loc_parchim['latitude']), year)

##geo = geopy.Polygon([(12.2, 52.2), (12.2, 51.6), (13.2, 51.6), (13.2, 52.2)])
#multi_weather = coastdat.get_weather(conn, geo, year)
#my_weather = multi_weather[0]


# Create a feedin series for a specific powerplant under specific weather
# conditions. One can define the number of turbines or the over all capacity.
# If no multiplier is set, the time series will be for one turbine.


# Apply the model
yingli_module = plants.Photovoltaic(**yingli210)
advent_module = plants.Photovoltaic(**advent210)

# Apply the pv plant
pv_feedin1 = yingli_module.feedin(weather=my_weather, number=30000) 
# müsste egal sein, wenn man eine normierte zeitreihe verwendet und die maximal installierbare leistung pro hausdach als limit nimmt
pv_feedin2 = yingli_module.feedin(weather=my_weather, area=15000)
pv_feedin3 = yingli_module.feedin(weather=my_weather, peak_power=15000)
pv_feedin4 = yingli_module.feedin(weather=my_weather)
pv_feedin5 = advent_module.feedin(weather=my_weather)

pv_feedin4.name = 'Yingli'
pv_feedin5.name = 'Advent'

# Output
if plot_fkt:
    pv_feedin4.plot(legend=True)
    pv_feedin5.plot(legend=True)
    plt.show()
else:
    print(pv_feedin5)

# Use directly methods of the model
w_model = models.SimpleWindTurbine()
w_model.get_wind_pp_types()
cp_values = models.SimpleWindTurbine().fetch_cp_values(
    wind_conv_type='ENERCON E 126 7500')
if plot_fkt:
    plt.plot(cp_values.loc[0, :][2:55].index,
             cp_values.loc[0, :][2:55].values, '*')
    plt.show()
else:
    print(cp_values.loc[0, :][2:55].values)

logging.info('Done!')
