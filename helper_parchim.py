#!/usr/bin/python3
# -*- coding: utf-8

import logging
from shapely import geometry as geopy

from oemof import db
from oemof.db import coastdat

from feedinlib import powerplants as plants

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


def get_pv_generation(year=2010, module_name='Yingli_YL210__2008__E__',
                      **kwargs):

    # Specification of the pv module
    module = {
            'module_name': module_name,
            'azimuth': kwargs.get('azimuth'),
            'tilt': kwargs.get('tilt'),
            'albedo': kwargs.get('albedo')}

    loc = kwargs.get('loc')

    conn = db.connection()
    my_weather = coastdat.get_weather(
        conn, geopy.Point(loc['longitude'], loc['latitude']), year)

    # Apply the model
    yingli_module = plants.Photovoltaic(**module)

    pv_feedin = yingli_module.feedin(weather=my_weather, peak_power=1)

    return(pv_feedin)

