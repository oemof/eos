# -*- coding: utf-8 -*-

'''Calculating and plotting residual loads.

Usage: region_residual_load [options]

Options:

  -o, --region_1=REGONE    The region 1. Choose from stein, lkos, osna and
                           rheine.
  -t, --region_2=REGTWO    The region 2. Choose from stein, lkos, osna and
                           rheine.
      --region_3=REGTHR    The region 3. Choose from stein, lkos, osna and
                           rheine.
      --region_4=REGFOU    The region 4. Choose from stein, lkos, osna and
                           rheine.
      --year_1=YEAR1       The year for region 1.
      --year_2=YEAR2       The year for region 2.
      --year_3=YEAR3       The year for region 3.
      --year_4=YEAR4       The year for region 4.
      --load_1=LOAD1       The load profile for region 1.
      --load_2=LOAD2       The load profile for region 2.
      --load_3=LOAD3       The load profile for region 3.
      --load_4=LOAD4       The load profile for region 4.
      --kombi_1            Region combination: lkos + osna
      --kombi_1_1          Region combination: lkos + osna,
                           osna has a different load profile
      --kombi_2            Region combination: stein + rheine
      --kombi_3            Region combination: stein + lkos + osna
      --kombi_3_1          Region combination: stein + lkos + osna,
                           osna has a different load profile
      --kombi_4            Region combination: stein + lkos + rheine
      --kombi_5            Region combination: stein + lkos
      --kombi_5_1          Region combination: stein + lkos,
                           lkos has a different load profile
      --kombi_6            Region combination: stein + osna
      --year=YEAR          Scenario year. Choose from 2020, 2030, 2040 and
                           2050. [default: 2030]
      --entsoe             ENTSO-E load profile
      --entsoe_1           ENTSO-E load profile, 1 hour shift
      --entsoe_12          ENTSO-E load profile, 12 hour shift
      --lkos               LKOS load profile
      --bdew               BDEW standard load profile h0
      --carpet             Plot carpet.
      --line               Plot line.
      --bar                Plot bar.
      --jdl                Plot sorted annual load duration curve of the
                           residual load.
      --save               Save figure.
      --post-storage       Post storage.
  -h, --help               Display this help.

'''

from shapely import geometry as geopy
import pandas as pd
import numpy as np
import os

# from oemof import db
# from oemof.db import coastdat
# from feedinlib import powerplants as plants
from demandlib import bdew as bdew
from helper import carpet_plot

try:
    from docopt import docopt
except ImportError:
    print("Unable to import docopt.\nIs the 'docopt' package installed?")


def main(**arguments):

    results = {}

    # Read weather data from file
    # data_weather = pd.read_csv("../example/example_data/storage_invest.csv", sep=',')
    data_weather = pd.read_csv('../data/2005_feedin_8043_52279.csv', sep=',')

    # # Read weather data from coastdat
    # data_weather = {}

    # conn = db.connection()
    # my_weather = coastdat.get_weather(
    #     conn, geopy.Point(8.043, 52.279), 2013)
    #     # conn, geopy.Point(9, 54), 2014)

    # coastDat2 = {
    #     'dhi': 0,
    #     'dirhi': 0,
    #     'pressure': 0,
    #     'temp_air': 2,
    #     'v_wind': 100,
    #     'Z0': 0}

    # yingli210 = {
    #     'module_name': 'Yingli_YL210__2008__E__',
    #     'azimuth': 180,
    #     'tilt': 60,
    #     'albedo': 0.2}

    # enerconE126 = {
    #     'h_hub': 135,
    #     'd_rotor': 127,
    #     'wind_conv_type': 'ENERCON E 126 7500',
    #     'data_height': coastDat2}

    # E126_power_plant = plants.WindPowerPlant(**enerconE126)
    # yingli_module = plants.Photovoltaic(**yingli210)

    # wind_feedin = E126_power_plant.feedin(weather=my_weather, installed_capacity=1)
    # pv_feedin = yingli_module.feedin(weather=my_weather, peak_power=1)

    # # print(pv_feedin.sum())
    # # print(wind_feedin.sum())

    # wind_feedin.to_csv('wind_feedin.csv')
    # pv_feedin.to_csv('pv_feedin.csv')

    # Get load profile data
    if arguments['--entsoe']:
        data = pd.read_csv("../../example/example_data/storage_invest.csv", sep=',')
        data_load = data['demand_el']  # demand in kW

    if arguments['--entsoe_1']:
        data = pd.read_csv("../example/example_data/storage_invest_load_1h_verschoben.csv", sep=',')
        data_load = data['demand_el']  # demand in kW

    if arguments['--entsoe_12']:
        data = pd.read_csv("../example/example_data/storage_invest_load_12h_verschoben.csv", sep=',')
        data_load = data['demand_el']  # demand in kW

    if arguments['--lkos']:
        data_load = pd.read_csv('../data/Lastprofil_LKOS_MW_1h.csv', sep=',')
        # data_load_df = pd.read_csv('../data/Lastprofil_LKOS_MW_15min.csv', sep=',')
        # index = pd.date_range(
        #             pd.datetime(int(arguments['--year']), 1, 1, 0),
        #             periods=35040,
        #             freq='15min')
        # data_load_df.set_index(index, inplace=True)
        # data_load_df = data_load_df.resample('H').mean()
        # data_load_df.to_csv('../data/Lastprofil_LKOS_MW_1h.csv')
        data_load = data_load['demand_el'] * 1e3  # demand in kW

    if arguments['--bdew']:
        e_slp = bdew.ElecSlp(int(arguments['--year']))
        h0_slp_15_min = e_slp.get_profile({'h0': 1})
        h0_slp = h0_slp_15_min.resample('H').mean()
        data_load = h0_slp['h0'].reset_index(drop=True)

    if arguments['--kombi_1']:

        masterplan_lkos = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'lkos' + '.csv', sep=',',
                                      index_col=0)

        masterplan_osna = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                                  'osna' + '.csv', sep=',',
                                  index_col=0)

        print(masterplan_lkos)
        print(masterplan_osna)

        demand = (masterplan_lkos.loc['demand'][str(arguments['--year'])]
                  + masterplan_osna.loc['demand'][str(arguments['--year'])])  # demand in GWh
        wind = (masterplan_lkos.loc['wind'][str(arguments['--year'])]
                + masterplan_osna.loc['wind'][str(arguments['--year'])])  # installed wind in MW
        pv = (masterplan_lkos.loc['pv'][str(arguments['--year'])]
          + masterplan_osna.loc['pv'][str(arguments['--year'])])  # installed pv in MW
        bio = (masterplan_lkos.loc['bio_MW'][str(arguments['--year'])]
          + masterplan_osna.loc['bio_MW'][str(arguments['--year'])])  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        bio_ts_MW = np.ones(8760)*bio
        # bio_ts_MW = np.ones(8785)*bio
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)

        print(max(demand_ts_MW))
        print(min(demand_ts_MW))
        print(demand_ts_MW.mean())

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)

        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_positive = positive[1:744]
        feb_positive = positive[745:1416]
        mar_positive = positive[1417:2160]
        apr_positive = positive[2161:2880]
        mai_positive = positive[2881:3624]
        jun_positive = positive[3625:4344]
        jul_positive = positive[4345:5088]
        aug_positive = positive[5089:5832]
        sep_positive = positive[5833:6552]
        okt_positive = positive[6553:7296]
        nov_positive = positive[7297:8016]
        dez_positive = positive[8017:8760]

        jan_negative = negative[1:744]
        feb_negative = negative[745:1416]
        mar_negative = negative[1417:2160]
        apr_negative = negative[2161:2880]
        mai_negative = negative[2881:3624]
        jun_negative = negative[3625:4344]
        jul_negative = negative[4345:5088]
        aug_negative = negative[5089:5832]
        sep_negative = negative[5833:6552]
        okt_negative = negative[6553:7296]
        nov_negative = negative[7297:8016]
        dez_negative = negative[8017:8760]

        jan_demand = demand_ts_MW[1:744]
        feb_demand = demand_ts_MW[745:1416]
        mar_demand = demand_ts_MW[1417:2160]
        apr_demand = demand_ts_MW[2161:2880]
        mai_demand = demand_ts_MW[2881:3624]
        jun_demand = demand_ts_MW[3625:4344]
        jul_demand = demand_ts_MW[4345:5088]
        aug_demand = demand_ts_MW[5089:5832]
        sep_demand = demand_ts_MW[5833:6552]
        okt_demand = demand_ts_MW[6553:7296]
        nov_demand = demand_ts_MW[7297:8016]
        dez_demand = demand_ts_MW[8017:8760]

        jan_covered_demand = demand_ts_MW[1:744] + positive[1:744] * (-1)
        feb_covered_demand = demand_ts_MW[745:1416] + positive[745:1416] * (-1)
        mar_covered_demand = demand_ts_MW[1417:2160] + positive[1417:2160] * (-1)
        apr_covered_demand = demand_ts_MW[2161:2880] + positive[2161:2880] * (-1)
        mai_covered_demand = demand_ts_MW[2881:3624] + positive[2881:3624] * (-1)
        jun_covered_demand = demand_ts_MW[3625:4344] + positive[3625:4344] * (-1)
        jul_covered_demand = demand_ts_MW[4345:5088] + positive[4345:5088] * (-1)
        aug_covered_demand = demand_ts_MW[5089:5832] + positive[5089:5832] * (-1)
        sep_covered_demand = demand_ts_MW[5833:6552] + positive[5833:6552] * (-1)
        okt_covered_demand = demand_ts_MW[6553:7296] + positive[6553:7296] * (-1)
        nov_covered_demand = demand_ts_MW[7297:8016] + positive[7297:8016] * (-1)
        dez_covered_demand = demand_ts_MW[8017:8760] + positive[8017:8760] * (-1)

        jan_wind = wind_ts_MW[1:744]
        feb_wind = wind_ts_MW[745:1416]
        mar_wind = wind_ts_MW[1417:2160]
        apr_wind = wind_ts_MW[2161:2880]
        mai_wind = wind_ts_MW[2881:3624]
        jun_wind = wind_ts_MW[3625:4344]
        jul_wind = wind_ts_MW[4345:5088]
        aug_wind = wind_ts_MW[5089:5832]
        sep_wind = wind_ts_MW[5833:6552]
        okt_wind = wind_ts_MW[6553:7296]
        nov_wind = wind_ts_MW[7297:8016]
        dez_wind = wind_ts_MW[8017:8760]

        jan_pv = pv_ts_MW[1:744]
        feb_pv = pv_ts_MW[745:1416]
        mar_pv = pv_ts_MW[1417:2160]
        apr_pv = pv_ts_MW[2161:2880]
        mai_pv = pv_ts_MW[2881:3624]
        jun_pv = pv_ts_MW[3625:4344]
        jul_pv = pv_ts_MW[4345:5088]
        aug_pv = pv_ts_MW[5089:5832]
        sep_pv = pv_ts_MW[5833:6552]
        okt_pv = pv_ts_MW[6553:7296]
        nov_pv = pv_ts_MW[7297:8016]
        dez_pv = pv_ts_MW[8017:8760]

        positive_monthly_MWh = np.array([jan_positive.sum(), feb_positive.sum(),
                mar_positive.sum(), apr_positive.sum(), mai_positive.sum(),
                jun_positive.sum(), jul_positive.sum(), aug_positive.sum(),
                sep_positive.sum(), okt_positive.sum(), nov_positive.sum(),
                dez_positive.sum()])

        negative_monthly_MWh = np.array([jan_negative.sum(), feb_negative.sum(),
                mar_negative.sum(), apr_negative.sum(), mai_negative.sum(),
                jun_negative.sum(), jul_negative.sum(), aug_negative.sum(),
                sep_negative.sum(), okt_negative.sum(), nov_negative.sum(),
                dez_negative.sum()])

        demand_monthly_MWh = np.array([jan_demand.sum(),
            feb_demand.sum(), mar_demand.sum(),
            apr_demand.sum(), mai_demand.sum(),
            jun_demand.sum(), jul_demand.sum(),
            aug_demand.sum(), sep_demand.sum(),
            okt_demand.sum(), nov_demand.sum(),
            dez_demand.sum()])

        covered_demand_monthly_MWh = np.array([jan_covered_demand.sum(),
            feb_covered_demand.sum(), mar_covered_demand.sum(),
            apr_covered_demand.sum(), mai_covered_demand.sum(),
            jun_covered_demand.sum(), jul_covered_demand.sum(),
            aug_covered_demand.sum(), sep_covered_demand.sum(),
            okt_covered_demand.sum(), nov_covered_demand.sum(),
            dez_covered_demand.sum()])

        print('kombi_1' + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        print('kombi_1' + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        print('kombi_1' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_1' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_1' + '_max_positive_MW: ', positive.max())
        print('kombi_1' + '_min_negative_MW: ', negative.min())
        print('kombi_1' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_1' + '_hours_negative: ', len(negative.nonzero()[0]))

        print('kombi_1' + '_jan_negative: ', jan_negative.sum())
        print('kombi_1' + '_feb_negative: ', feb_negative.sum())
        print('kombi_1' + '_mar_negative: ', mar_negative.sum())
        print('kombi_1' + '_apr_negative: ', apr_negative.sum())
        print('kombi_1' + '_mai_negative: ', mai_negative.sum())
        print('kombi_1' + '_jun_negative: ', jun_negative.sum())
        print('kombi_1' + '_jul_negative: ', jul_negative.sum())
        print('kombi_1' + '_aug_negative: ', aug_negative.sum())
        print('kombi_1' + '_sep_negative: ', sep_negative.sum())
        print('kombi_1' + '_okt_negative: ', okt_negative.sum())
        print('kombi_1' + '_nov_negative: ', nov_negative.sum())
        print('kombi_1' + '_dez_negative: ', dez_negative.sum())

        print('kombi_1' + '_jan_cov: ', jan_covered_demand.sum())
        print('kombi_1' + '_feb_cov: ', feb_covered_demand.sum())
        print('kombi_1' + '_mar_cov: ', mar_covered_demand.sum())
        print('kombi_1' + '_apr_cov: ', apr_covered_demand.sum())
        print('kombi_1' + '_mai_cov: ', mai_covered_demand.sum())
        print('kombi_1' + '_jun_cov: ', jun_covered_demand.sum())
        print('kombi_1' + '_jul_cov: ', jul_covered_demand.sum())
        print('kombi_1' + '_aug_cov: ', aug_covered_demand.sum())
        print('kombi_1' + '_sep_cov: ', sep_covered_demand.sum())
        print('kombi_1' + '_okt_cov: ', okt_covered_demand.sum())
        print('kombi_1' + '_nov_cov: ', nov_covered_demand.sum())
        print('kombi_1' + '_dez_cov: ', dez_covered_demand.sum())

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_1'] = residual_MW
        results['positive_monthly_kombi_1'] = positive_monthly_MWh
        results['negative_monthly_kombi_1'] = negative_monthly_MWh
        results['demand_monthly_kombi_1'] = demand_monthly_MWh
        results['covered_demand_monthly_kombi_1'] = covered_demand_monthly_MWh
        results['jan_demand'] = jan_demand
        results['jan_wind'] = jan_wind
        results['jan_pv'] = jan_pv


    if arguments['--kombi_3']:

        masterplan_stein = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'stein' + '.csv', sep=',',
                                      index_col=0)

        masterplan_lkos = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'lkos' + '.csv', sep=',',
                                      index_col=0)

        masterplan_osna = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'osna' + '.csv', sep=',',
                                      index_col=0)

        print(masterplan_stein)
        print(masterplan_lkos)
        print(masterplan_osna)

        demand = (masterplan_stein.loc['demand'][str(arguments['--year'])]
                  + masterplan_lkos.loc['demand'][str(arguments['--year'])]
                  + masterplan_osna.loc['demand'][str(arguments['--year'])])  # demand in GWh
        wind = (masterplan_stein.loc['wind'][str(arguments['--year'])]
                + masterplan_lkos.loc['wind'][str(arguments['--year'])]
                + masterplan_osna.loc['wind'][str(arguments['--year'])])  # installed wind in MW
        pv = (masterplan_stein.loc['pv'][str(arguments['--year'])]
              + masterplan_lkos.loc['pv'][str(arguments['--year'])]
              + masterplan_osna.loc['pv'][str(arguments['--year'])])  # installed pv in MW
        bio = (masterplan_stein.loc['bio_MW'][str(arguments['--year'])]
              + masterplan_lkos.loc['bio_MW'][str(arguments['--year'])]
              + masterplan_osna.loc['bio_MW'][str(arguments['--year'])])  # installed pv in MW


        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        bio_ts_MW = np.ones(8760)*bio
        # bio_ts_MW = np.ones(8785)*bio
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)

        print(max(demand_ts_MW))
        print(min(demand_ts_MW))
        print(demand_ts_MW.mean())

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)

        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_positive = positive[1:744]
        feb_positive = positive[745:1416]
        mar_positive = positive[1417:2160]
        apr_positive = positive[2161:2880]
        mai_positive = positive[2881:3624]
        jun_positive = positive[3625:4344]
        jul_positive = positive[4345:5088]
        aug_positive = positive[5089:5832]
        sep_positive = positive[5833:6552]
        okt_positive = positive[6553:7296]
        nov_positive = positive[7297:8016]
        dez_positive = positive[8017:8760]

        jan_negative = negative[1:744]
        feb_negative = negative[745:1416]
        mar_negative = negative[1417:2160]
        apr_negative = negative[2161:2880]
        mai_negative = negative[2881:3624]
        jun_negative = negative[3625:4344]
        jul_negative = negative[4345:5088]
        aug_negative = negative[5089:5832]
        sep_negative = negative[5833:6552]
        okt_negative = negative[6553:7296]
        nov_negative = negative[7297:8016]
        dez_negative = negative[8017:8760]

        jan_demand = demand_ts_MW[1:744]
        feb_demand = demand_ts_MW[745:1416]
        mar_demand = demand_ts_MW[1417:2160]
        apr_demand = demand_ts_MW[2161:2880]
        mai_demand = demand_ts_MW[2881:3624]
        jun_demand = demand_ts_MW[3625:4344]
        jul_demand = demand_ts_MW[4345:5088]
        aug_demand = demand_ts_MW[5089:5832]
        sep_demand = demand_ts_MW[5833:6552]
        okt_demand = demand_ts_MW[6553:7296]
        nov_demand = demand_ts_MW[7297:8016]
        dez_demand = demand_ts_MW[8017:8760]

        jan_covered_demand = demand_ts_MW[1:744] + positive[1:744] * (-1)
        feb_covered_demand = demand_ts_MW[745:1416] + positive[745:1416] * (-1)
        mar_covered_demand = demand_ts_MW[1417:2160] + positive[1417:2160] * (-1)
        apr_covered_demand = demand_ts_MW[2161:2880] + positive[2161:2880] * (-1)
        mai_covered_demand = demand_ts_MW[2881:3624] + positive[2881:3624] * (-1)
        jun_covered_demand = demand_ts_MW[3625:4344] + positive[3625:4344] * (-1)
        jul_covered_demand = demand_ts_MW[4345:5088] + positive[4345:5088] * (-1)
        aug_covered_demand = demand_ts_MW[5089:5832] + positive[5089:5832] * (-1)
        sep_covered_demand = demand_ts_MW[5833:6552] + positive[5833:6552] * (-1)
        okt_covered_demand = demand_ts_MW[6553:7296] + positive[6553:7296] * (-1)
        nov_covered_demand = demand_ts_MW[7297:8016] + positive[7297:8016] * (-1)
        dez_covered_demand = demand_ts_MW[8017:8760] + positive[8017:8760] * (-1)

        jan_wind = wind_ts_MW[1:744]
        feb_wind = wind_ts_MW[745:1416]
        mar_wind = wind_ts_MW[1417:2160]
        apr_wind = wind_ts_MW[2161:2880]
        mai_wind = wind_ts_MW[2881:3624]
        jun_wind = wind_ts_MW[3625:4344]
        jul_wind = wind_ts_MW[4345:5088]
        aug_wind = wind_ts_MW[5089:5832]
        sep_wind = wind_ts_MW[5833:6552]
        okt_wind = wind_ts_MW[6553:7296]
        nov_wind = wind_ts_MW[7297:8016]
        dez_wind = wind_ts_MW[8017:8760]

        jan_pv = pv_ts_MW[1:744]
        feb_pv = pv_ts_MW[745:1416]
        mar_pv = pv_ts_MW[1417:2160]
        apr_pv = pv_ts_MW[2161:2880]
        mai_pv = pv_ts_MW[2881:3624]
        jun_pv = pv_ts_MW[3625:4344]
        jul_pv = pv_ts_MW[4345:5088]
        aug_pv = pv_ts_MW[5089:5832]
        sep_pv = pv_ts_MW[5833:6552]
        okt_pv = pv_ts_MW[6553:7296]
        nov_pv = pv_ts_MW[7297:8016]
        dez_pv = pv_ts_MW[8017:8760]

        positive_monthly_MWh = np.array([jan_positive.sum(), feb_positive.sum(),
                mar_positive.sum(), apr_positive.sum(), mai_positive.sum(),
                jun_positive.sum(), jul_positive.sum(), aug_positive.sum(),
                sep_positive.sum(), okt_positive.sum(), nov_positive.sum(),
                dez_positive.sum()])

        negative_monthly_MWh = np.array([jan_negative.sum(), feb_negative.sum(),
                mar_negative.sum(), apr_negative.sum(), mai_negative.sum(),
                jun_negative.sum(), jul_negative.sum(), aug_negative.sum(),
                sep_negative.sum(), okt_negative.sum(), nov_negative.sum(),
                dez_negative.sum()])

        demand_monthly_MWh = np.array([jan_demand.sum(),
            feb_demand.sum(), mar_demand.sum(),
            apr_demand.sum(), mai_demand.sum(),
            jun_demand.sum(), jul_demand.sum(),
            aug_demand.sum(), sep_demand.sum(),
            okt_demand.sum(), nov_demand.sum(),
            dez_demand.sum()])

        covered_demand_monthly_MWh = np.array([jan_covered_demand.sum(),
            feb_covered_demand.sum(), mar_covered_demand.sum(),
            apr_covered_demand.sum(), mai_covered_demand.sum(),
            jun_covered_demand.sum(), jul_covered_demand.sum(),
            aug_covered_demand.sum(), sep_covered_demand.sum(),
            okt_covered_demand.sum(), nov_covered_demand.sum(),
            dez_covered_demand.sum()])

        print('kombi_3' + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        print('kombi_3' + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        print('kombi_3' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_3' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_3' + '_max_positive_MW: ', positive.max())
        print('kombi_3' + '_min_negative_MW: ', negative.min())
        print('kombi_3' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_3' + '_hours_negative: ', len(negative.nonzero()[0]))

        # print('kombi_5' + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        # print('kombi_5' + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        # print('kombi_5' + '_positive_GWh: ', positive.sum()/1e3)
        # print('kombi_5' + '_negative_GWh: ', negative.sum()/1e3)
        # print('kombi_5' + '_max_positive_MW: ', positive.max())
        # print('kombi_5' + '_min_negative_MW: ', negative.min())
        # print('kombi_5' + '_hours_positive: ', len(positive.nonzero()[0]))
        # print('kombi_5' + '_hours_negative: ', len(negative.nonzero()[0]))
        # print('kombi_5' + '_jan_residual: ', jan_residual.sum())
        # print('kombi_5' + '_feb_residual: ', feb_residual.sum())
        # print('kombi_5' + '_mar_residual: ', mar_residual.sum())
        # print('kombi_5' + '_apr_residual: ', apr_residual.sum())
        # print('kombi_5' + '_mai_residual: ', mai_residual.sum())
        # print('kombi_5' + '_jun_residual: ', jun_residual.sum())
        # print('kombi_5' + '_jul_residual: ', jul_residual.sum())
        # print('kombi_5' + '_aug_residual: ', aug_residual.sum())
        # print('kombi_5' + '_sep_residual: ', sep_residual.sum())
        # print('kombi_5' + '_okt_residual: ', okt_residual.sum())
        # print('kombi_5' + '_nov_residual: ', nov_residual.sum())
        # print('kombi_5' + '_dez_residual: ', dez_residual.sum())
        # print('kombi_5' + '_jan_positive: ', jan_positive.sum())
        # print('kombi_5' + '_feb_positive: ', feb_positive.sum())
        # print('kombi_5' + '_mar_positive: ', mar_positive.sum())
        # print('kombi_5' + '_apr_positive: ', apr_positive.sum())
        # print('kombi_5' + '_mai_positive: ', mai_positive.sum())
        # print('kombi_5' + '_jun_positive: ', jun_positive.sum())
        # print('kombi_5' + '_jul_positive: ', jul_positive.sum())
        # print('kombi_5' + '_aug_positive: ', aug_positive.sum())
        # print('kombi_5' + '_sep_positive: ', sep_positive.sum())
        # print('kombi_5' + '_okt_positive: ', okt_positive.sum())
        # print('kombi_5' + '_nov_positive: ', nov_positive.sum())
        # print('kombi_5' + '_dez_positive: ', dez_positive.sum())
        # print('kombi_5' + '_jan_negative: ', jan_negative.sum())
        # print('kombi_5' + '_feb_negative: ', feb_negative.sum())
        # print('kombi_5' + '_mar_negative: ', mar_negative.sum())
        # print('kombi_5' + '_apr_negative: ', apr_negative.sum())
        # print('kombi_5' + '_mai_negative: ', mai_negative.sum())
        # print('kombi_5' + '_jun_negative: ', jun_negative.sum())
        # print('kombi_5' + '_jul_negative: ', jul_negative.sum())
        # print('kombi_5' + '_aug_negative: ', aug_negative.sum())
        # print('kombi_5' + '_sep_negative: ', sep_negative.sum())
        # print('kombi_5' + '_okt_negative: ', okt_negative.sum())
        # print('kombi_5' + '_nov_negative: ', nov_negative.sum())
        # print('kombi_5' + '_dez_negative: ', dez_negative.sum())
        # print('kombi_5' + '_jan_demand: ', jan_demand.sum())
        # print('kombi_5' + '_feb_demand: ', feb_demand.sum())
        # print('kombi_5' + '_mar_demand: ', mar_demand.sum())
        # print('kombi_5' + '_apr_demand: ', apr_demand.sum())
        # print('kombi_5' + '_mai_demand: ', mai_demand.sum())
        # print('kombi_5' + '_jun_demand: ', jun_demand.sum())
        # print('kombi_5' + '_jul_demand: ', jul_demand.sum())
        # print('kombi_5' + '_aug_demand: ', aug_demand.sum())
        # print('kombi_5' + '_sep_demand: ', sep_demand.sum())
        # print('kombi_5' + '_okt_demand: ', okt_demand.sum())
        # print('kombi_5' + '_nov_demand: ', nov_demand.sum())
        # print('kombi_5' + '_dez_demand: ', dez_demand.sum())
        # print('kombi_5' + '_jan_wind: ', jan_wind.sum())
        # print('kombi_5' + '_feb_wind: ', feb_wind.sum())
        # print('kombi_5' + '_mar_wind: ', mar_wind.sum())
        # print('kombi_5' + '_apr_wind: ', apr_wind.sum())
        # print('kombi_5' + '_mai_wind: ', mai_wind.sum())
        # print('kombi_5' + '_jun_wind: ', jun_wind.sum())
        # print('kombi_5' + '_jul_wind: ', jul_wind.sum())
        # print('kombi_5' + '_aug_wind: ', aug_wind.sum())
        # print('kombi_5' + '_sep_wind: ', sep_wind.sum())
        # print('kombi_5' + '_okt_wind: ', okt_wind.sum())
        # print('kombi_5' + '_nov_wind: ', nov_wind.sum())
        # print('kombi_5' + '_dez_wind: ', dez_wind.sum())
        # print('kombi_5' + '_jan_pv: ', jan_pv.sum())
        # print('kombi_5' + '_feb_pv: ', feb_pv.sum())
        # print('kombi_5' + '_mar_pv: ', mar_pv.sum())
        # print('kombi_5' + '_apr_pv: ', apr_pv.sum())
        # print('kombi_5' + '_mai_pv: ', mai_pv.sum())
        # print('kombi_5' + '_jun_pv: ', jun_pv.sum())
        # print('kombi_5' + '_jul_pv: ', jul_pv.sum())
        # print('kombi_5' + '_aug_pv: ', aug_pv.sum())
        # print('kombi_5' + '_sep_pv: ', sep_pv.sum())
        # print('kombi_5' + '_okt_pv: ', okt_pv.sum())
        # print('kombi_5' + '_nov_pv: ', nov_pv.sum())
        # print('kombi_5' + '_dez_pv: ', dez_pv.sum())

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_3'] = residual_MW
        results['positive_monthly_kombi_3'] = positive_monthly_MWh
        results['negative_monthly_kombi_3'] = negative_monthly_MWh
        results['demand_monthly_kombi_3'] = demand_monthly_MWh
        results['covered_demand_monthly_kombi_3'] = covered_demand_monthly_MWh
        results['jan_demand'] = jan_demand
        results['jan_wind'] = jan_wind
        results['jan_pv'] = jan_pv

    if arguments['--kombi_3_1']:

        masterplan_stein = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'stein' + '.csv', sep=',',
                                      index_col=0)

        masterplan_lkos = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'lkos' + '.csv', sep=',',
                                      index_col=0)

        masterplan_osna = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'osna' + '.csv', sep=',',
                                      index_col=0)

        print(masterplan_stein)
        print(masterplan_lkos)
        print(masterplan_osna)

        data_stein_lkos = pd.read_csv("../example/example_data/storage_invest.csv", sep=',')
        data_load_stein_lkos = data_stein_lkos['demand_el']  # demand in kW

        data_osna = pd.read_csv("../example/example_data/storage_invest_load_12h_verschoben.csv", sep=',')
        # data_osna = pd.read_csv('../data/Lastprofil_LKOS_MW_1h.csv', sep=',')
        # e_slp = bdew.ElecSlp(int(arguments['--year']))
        # h0_slp_15_min = e_slp.get_profile({'h0': 1})
        # h0_slp = h0_slp_15_min.resample('H').mean()
        # data_load_osna = h0_slp['h0'].reset_index(drop=True)

        data_load_osna = data_osna['demand_el']  # demand in kW

        demand_stein_lkos = (masterplan_stein.loc['demand'][str(arguments['--year'])]
                  + masterplan_lkos.loc['demand'][str(arguments['--year'])])
        demand_osna = masterplan_osna.loc['demand'][str(arguments['--year'])]  # demand in GWh
        wind = (masterplan_stein.loc['wind'][str(arguments['--year'])]
                + masterplan_lkos.loc['wind'][str(arguments['--year'])]
                + masterplan_osna.loc['wind'][str(arguments['--year'])])  # installed wind in MW
        pv = (masterplan_stein.loc['pv'][str(arguments['--year'])]
              + masterplan_lkos.loc['pv'][str(arguments['--year'])]
              + masterplan_osna.loc['pv'][str(arguments['--year'])])  # installed pv in MW
        bio = (masterplan_stein.loc['bio_MW'][str(arguments['--year'])]
              + masterplan_lkos.loc['bio_MW'][str(arguments['--year'])]
              + masterplan_osna.loc['bio_MW'][str(arguments['--year'])])  # installed pv in MW

        demand_ts_stein_lkos_MW = (data_load_stein_lkos/data_load_stein_lkos.sum()
            * demand_stein_lkos * 1e3)
        demand_ts_osna_MW = (data_load_osna/data_load_osna.sum()
            * demand_osna * 1e3)
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        residual_MW = (demand_ts_stein_lkos_MW + demand_ts_osna_MW
            - (wind_ts_MW + pv_ts_MW))

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)

        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_positive = positive[1:744]
        feb_positive = positive[745:1416]
        mar_positive = positive[1417:2160]
        apr_positive = positive[2161:2880]
        mai_positive = positive[2881:3624]
        jun_positive = positive[3625:4344]
        jul_positive = positive[4345:5088]
        aug_positive = positive[5089:5832]
        sep_positive = positive[5833:6552]
        okt_positive = positive[6553:7296]
        nov_positive = positive[7297:8016]
        dez_positive = positive[8017:8760]

        jan_negative = negative[1:744]
        feb_negative = negative[745:1416]
        mar_negative = negative[1417:2160]
        apr_negative = negative[2161:2880]
        mai_negative = negative[2881:3624]
        jun_negative = negative[3625:4344]
        jul_negative = negative[4345:5088]
        aug_negative = negative[5089:5832]
        sep_negative = negative[5833:6552]
        okt_negative = negative[6553:7296]
        nov_negative = negative[7297:8016]
        dez_negative = negative[8017:8760]

        jan_demand = demand_ts_stein_lkos_MW[1:744] + demand_ts_osna_MW[1:744]
        feb_demand = demand_ts_stein_lkos_MW[745:1416] + demand_ts_osna_MW[745:1416]
        mar_demand = demand_ts_stein_lkos_MW[1417:2160] + demand_ts_osna_MW[1417:2160]
        apr_demand = demand_ts_stein_lkos_MW[2161:2880] + demand_ts_osna_MW[2161:2880]
        mai_demand = demand_ts_stein_lkos_MW[2881:3624] + demand_ts_osna_MW[2881:3624]
        jun_demand = demand_ts_stein_lkos_MW[3625:4344] + demand_ts_osna_MW[3625:4344]
        jul_demand = demand_ts_stein_lkos_MW[4345:5088] + demand_ts_osna_MW[4345:5088]
        aug_demand = demand_ts_stein_lkos_MW[5089:5832] + demand_ts_osna_MW[5089:5832]
        sep_demand = demand_ts_stein_lkos_MW[5833:6552] + demand_ts_osna_MW[5833:6552]
        okt_demand = demand_ts_stein_lkos_MW[6553:7296] + demand_ts_osna_MW[6553:7296]
        nov_demand = demand_ts_stein_lkos_MW[7297:8016] + demand_ts_osna_MW[7297:8016]
        dez_demand = demand_ts_stein_lkos_MW[8017:8760] + demand_ts_osna_MW[8017:8760]

        jan_covered_demand = (demand_ts_stein_lkos_MW[1:744] +
                demand_ts_osna_MW[1:744] +
                positive[1:744] * (-1))
        feb_covered_demand = (demand_ts_stein_lkos_MW[745:1416] +
            demand_ts_osna_MW[745:1416] +
            positive[745:1416] * (-1))
        mar_covered_demand = (demand_ts_stein_lkos_MW[1417:2160] +
            demand_ts_osna_MW[1417:2160] +
            positive[1417:2160] * (-1))
        apr_covered_demand = (demand_ts_stein_lkos_MW[2161:2880] +
            demand_ts_osna_MW[2161:2880] +
            positive[2161:2880] * (-1))
        mai_covered_demand = (demand_ts_stein_lkos_MW[2881:3624] +
            demand_ts_osna_MW[2881:3624] +
            positive[2881:3624] * (-1))
        jun_covered_demand = (demand_ts_stein_lkos_MW[3625:4344] +
            demand_ts_osna_MW[3625:4344] +
            positive[3625:4344] * (-1))
        jul_covered_demand = (demand_ts_stein_lkos_MW[4345:5088] +
            demand_ts_osna_MW[4345:5088] +
            positive[4345:5088] * (-1))
        aug_covered_demand = (demand_ts_stein_lkos_MW[5089:5832] +
            demand_ts_osna_MW[5089:5832] +
            positive[5089:5832] * (-1))
        sep_covered_demand = (demand_ts_stein_lkos_MW[5833:6552] +
            demand_ts_osna_MW[5833:6552] +
            positive[5833:6552] * (-1))
        okt_covered_demand = (demand_ts_stein_lkos_MW[6553:7296] +
            demand_ts_osna_MW[6553:7296] +
            positive[6553:7296] * (-1))
        nov_covered_demand = (demand_ts_stein_lkos_MW[7297:8016] +
            demand_ts_osna_MW[7297:8016] +
            positive[7297:8016] * (-1))
        dez_covered_demand = (demand_ts_stein_lkos_MW[8017:8760] +
            demand_ts_osna_MW[8017:8760] +
            positive[8017:8760] * (-1))

        jan_wind = wind_ts_MW[1:744]
        feb_wind = wind_ts_MW[745:1416]
        mar_wind = wind_ts_MW[1417:2160]
        apr_wind = wind_ts_MW[2161:2880]
        mai_wind = wind_ts_MW[2881:3624]
        jun_wind = wind_ts_MW[3625:4344]
        jul_wind = wind_ts_MW[4345:5088]
        aug_wind = wind_ts_MW[5089:5832]
        sep_wind = wind_ts_MW[5833:6552]
        okt_wind = wind_ts_MW[6553:7296]
        nov_wind = wind_ts_MW[7297:8016]
        dez_wind = wind_ts_MW[8017:8760]

        jan_pv = pv_ts_MW[1:744]
        feb_pv = pv_ts_MW[745:1416]
        mar_pv = pv_ts_MW[1417:2160]
        apr_pv = pv_ts_MW[2161:2880]
        mai_pv = pv_ts_MW[2881:3624]
        jun_pv = pv_ts_MW[3625:4344]
        jul_pv = pv_ts_MW[4345:5088]
        aug_pv = pv_ts_MW[5089:5832]
        sep_pv = pv_ts_MW[5833:6552]
        okt_pv = pv_ts_MW[6553:7296]
        nov_pv = pv_ts_MW[7297:8016]
        dez_pv = pv_ts_MW[8017:8760]

        positive_monthly_MWh = np.array([jan_positive.sum(), feb_positive.sum(),
                mar_positive.sum(), apr_positive.sum(), mai_positive.sum(),
                jun_positive.sum(), jul_positive.sum(), aug_positive.sum(),
                sep_positive.sum(), okt_positive.sum(), nov_positive.sum(),
                dez_positive.sum()])

        negative_monthly_MWh = np.array([jan_negative.sum(), feb_negative.sum(),
                mar_negative.sum(), apr_negative.sum(), mai_negative.sum(),
                jun_negative.sum(), jul_negative.sum(), aug_negative.sum(),
                sep_negative.sum(), okt_negative.sum(), nov_negative.sum(),
                dez_negative.sum()])

        demand_monthly_MWh = np.array([jan_demand.sum(),
            feb_demand.sum(), mar_demand.sum(),
            apr_demand.sum(), mai_demand.sum(),
            jun_demand.sum(), jul_demand.sum(),
            aug_demand.sum(), sep_demand.sum(),
            okt_demand.sum(), nov_demand.sum(),
            dez_demand.sum()])

        covered_demand_monthly_MWh = np.array([jan_covered_demand.sum(),
            feb_covered_demand.sum(), mar_covered_demand.sum(),
            apr_covered_demand.sum(), mai_covered_demand.sum(),
            jun_covered_demand.sum(), jul_covered_demand.sum(),
            aug_covered_demand.sum(), sep_covered_demand.sum(),
            okt_covered_demand.sum(), nov_covered_demand.sum(),
            dez_covered_demand.sum()])

        print('kombi_3_1' + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        print('kombi_3_1' + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        print('kombi_3_1' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_3_1' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_3_1' + '_max_positive_MW: ', positive.max())
        print('kombi_3_1' + '_min_negative_MW: ', negative.min())
        print('kombi_3_1' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_3_1' + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_stein_lkos_MW + demand_ts_osna_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_3_1'] = residual_MW
        results['positive_monthly_kombi_3_1'] = positive_monthly_MWh
        results['negative_monthly_kombi_3_1'] = negative_monthly_MWh
        results['demand_monthly_kombi_3_1'] = demand_monthly_MWh
        results['covered_demand_monthly_kombi_3_1'] = covered_demand_monthly_MWh
        results['jan_demand'] = jan_demand
        results['jan_wind'] = jan_wind
        results['jan_pv'] = jan_pv

    if arguments['--kombi_5']:

        masterplan_stein = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'stein' + '.csv', sep=',',
                                      index_col=0)

        masterplan_lkos = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'lkos' + '.csv', sep=',',
                                      index_col=0)

        print(masterplan_stein)
        print(masterplan_lkos)

        demand = (masterplan_stein.loc['demand'][str(arguments['--year'])]
                  + masterplan_lkos.loc['demand'][str(arguments['--year'])])  # demand in GWh
        wind = (masterplan_stein.loc['wind'][str(arguments['--year'])]
                + masterplan_lkos.loc['wind'][str(arguments['--year'])])  # installed wind in MW
        pv = (masterplan_stein.loc['pv'][str(arguments['--year'])]
              + masterplan_lkos.loc['pv'][str(arguments['--year'])])  # installed pv in MW
        bio = (masterplan_stein.loc['bio_MW'][str(arguments['--year'])]
              + masterplan_lkos.loc['bio_MW'][str(arguments['--year'])])  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        bio_ts_MW = np.ones(8760)*bio
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)

        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_positive = positive[1:744]
        feb_positive = positive[745:1416]
        mar_positive = positive[1417:2160]
        apr_positive = positive[2161:2880]
        mai_positive = positive[2881:3624]
        jun_positive = positive[3625:4344]
        jul_positive = positive[4345:5088]
        aug_positive = positive[5089:5832]
        sep_positive = positive[5833:6552]
        okt_positive = positive[6553:7296]
        nov_positive = positive[7297:8016]
        dez_positive = positive[8017:8760]

        jan_negative = negative[1:744]
        feb_negative = negative[745:1416]
        mar_negative = negative[1417:2160]
        apr_negative = negative[2161:2880]
        mai_negative = negative[2881:3624]
        jun_negative = negative[3625:4344]
        jul_negative = negative[4345:5088]
        aug_negative = negative[5089:5832]
        sep_negative = negative[5833:6552]
        okt_negative = negative[6553:7296]
        nov_negative = negative[7297:8016]
        dez_negative = negative[8017:8760]

        jan_demand = demand_ts_MW[1:744]
        feb_demand = demand_ts_MW[745:1416]
        mar_demand = demand_ts_MW[1417:2160]
        apr_demand = demand_ts_MW[2161:2880]
        mai_demand = demand_ts_MW[2881:3624]
        jun_demand = demand_ts_MW[3625:4344]
        jul_demand = demand_ts_MW[4345:5088]
        aug_demand = demand_ts_MW[5089:5832]
        sep_demand = demand_ts_MW[5833:6552]
        okt_demand = demand_ts_MW[6553:7296]
        nov_demand = demand_ts_MW[7297:8016]
        dez_demand = demand_ts_MW[8017:8760]

        jan_covered_demand = demand_ts_MW[1:744] + positive[1:744] * (-1)
        feb_covered_demand = demand_ts_MW[745:1416] + positive[745:1416] * (-1)
        mar_covered_demand = demand_ts_MW[1417:2160] + positive[1417:2160] * (-1)
        apr_covered_demand = demand_ts_MW[2161:2880] + positive[2161:2880] * (-1)
        mai_covered_demand = demand_ts_MW[2881:3624] + positive[2881:3624] * (-1)
        jun_covered_demand = demand_ts_MW[3625:4344] + positive[3625:4344] * (-1)
        jul_covered_demand = demand_ts_MW[4345:5088] + positive[4345:5088] * (-1)
        aug_covered_demand = demand_ts_MW[5089:5832] + positive[5089:5832] * (-1)
        sep_covered_demand = demand_ts_MW[5833:6552] + positive[5833:6552] * (-1)
        okt_covered_demand = demand_ts_MW[6553:7296] + positive[6553:7296] * (-1)
        nov_covered_demand = demand_ts_MW[7297:8016] + positive[7297:8016] * (-1)
        dez_covered_demand = demand_ts_MW[8017:8760] + positive[8017:8760] * (-1)

        jan_wind = wind_ts_MW[1:744]
        feb_wind = wind_ts_MW[745:1416]
        mar_wind = wind_ts_MW[1417:2160]
        apr_wind = wind_ts_MW[2161:2880]
        mai_wind = wind_ts_MW[2881:3624]
        jun_wind = wind_ts_MW[3625:4344]
        jul_wind = wind_ts_MW[4345:5088]
        aug_wind = wind_ts_MW[5089:5832]
        sep_wind = wind_ts_MW[5833:6552]
        okt_wind = wind_ts_MW[6553:7296]
        nov_wind = wind_ts_MW[7297:8016]
        dez_wind = wind_ts_MW[8017:8760]

        jan_pv = pv_ts_MW[1:744]
        feb_pv = pv_ts_MW[745:1416]
        mar_pv = pv_ts_MW[1417:2160]
        apr_pv = pv_ts_MW[2161:2880]
        mai_pv = pv_ts_MW[2881:3624]
        jun_pv = pv_ts_MW[3625:4344]
        jul_pv = pv_ts_MW[4345:5088]
        aug_pv = pv_ts_MW[5089:5832]
        sep_pv = pv_ts_MW[5833:6552]
        okt_pv = pv_ts_MW[6553:7296]
        nov_pv = pv_ts_MW[7297:8016]
        dez_pv = pv_ts_MW[8017:8760]

        positive_monthly_MWh = np.array([jan_positive.sum(), feb_positive.sum(),
                mar_positive.sum(), apr_positive.sum(), mai_positive.sum(),
                jun_positive.sum(), jul_positive.sum(), aug_positive.sum(),
                sep_positive.sum(), okt_positive.sum(), nov_positive.sum(),
                dez_positive.sum()])

        negative_monthly_MWh = np.array([jan_negative.sum(), feb_negative.sum(),
                mar_negative.sum(), apr_negative.sum(), mai_negative.sum(),
                jun_negative.sum(), jul_negative.sum(), aug_negative.sum(),
                sep_negative.sum(), okt_negative.sum(), nov_negative.sum(),
                dez_negative.sum()])

        demand_monthly_MWh = np.array([jan_demand.sum(),
            feb_demand.sum(), mar_demand.sum(),
            apr_demand.sum(), mai_demand.sum(),
            jun_demand.sum(), jul_demand.sum(),
            aug_demand.sum(), sep_demand.sum(),
            okt_demand.sum(), nov_demand.sum(),
            dez_demand.sum()])

        covered_demand_monthly_MWh = np.array([jan_covered_demand.sum(),
            feb_covered_demand.sum(), mar_covered_demand.sum(),
            apr_covered_demand.sum(), mai_covered_demand.sum(),
            jun_covered_demand.sum(), jul_covered_demand.sum(),
            aug_covered_demand.sum(), sep_covered_demand.sum(),
            okt_covered_demand.sum(), nov_covered_demand.sum(),
            dez_covered_demand.sum()])

        print('kombi_5' + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        print('kombi_5' + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        print('kombi_5' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_5' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_5' + '_max_positive_MW: ', positive.max())
        print('kombi_5' + '_min_negative_MW: ', negative.min())
        print('kombi_5' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_5' + '_hours_negative: ', len(negative.nonzero()[0]))
        print('kombi_5' + '_jan_residual: ', jan_residual.sum())
        print('kombi_5' + '_feb_residual: ', feb_residual.sum())
        print('kombi_5' + '_mar_residual: ', mar_residual.sum())
        print('kombi_5' + '_apr_residual: ', apr_residual.sum())
        print('kombi_5' + '_mai_residual: ', mai_residual.sum())
        print('kombi_5' + '_jun_residual: ', jun_residual.sum())
        print('kombi_5' + '_jul_residual: ', jul_residual.sum())
        print('kombi_5' + '_aug_residual: ', aug_residual.sum())
        print('kombi_5' + '_sep_residual: ', sep_residual.sum())
        print('kombi_5' + '_okt_residual: ', okt_residual.sum())
        print('kombi_5' + '_nov_residual: ', nov_residual.sum())
        print('kombi_5' + '_dez_residual: ', dez_residual.sum())
        print('kombi_5' + '_jan_positive: ', jan_positive.sum())
        print('kombi_5' + '_feb_positive: ', feb_positive.sum())
        print('kombi_5' + '_mar_positive: ', mar_positive.sum())
        print('kombi_5' + '_apr_positive: ', apr_positive.sum())
        print('kombi_5' + '_mai_positive: ', mai_positive.sum())
        print('kombi_5' + '_jun_positive: ', jun_positive.sum())
        print('kombi_5' + '_jul_positive: ', jul_positive.sum())
        print('kombi_5' + '_aug_positive: ', aug_positive.sum())
        print('kombi_5' + '_sep_positive: ', sep_positive.sum())
        print('kombi_5' + '_okt_positive: ', okt_positive.sum())
        print('kombi_5' + '_nov_positive: ', nov_positive.sum())
        print('kombi_5' + '_dez_positive: ', dez_positive.sum())
        print('kombi_5' + '_jan_negative: ', jan_negative.sum())
        print('kombi_5' + '_feb_negative: ', feb_negative.sum())
        print('kombi_5' + '_mar_negative: ', mar_negative.sum())
        print('kombi_5' + '_apr_negative: ', apr_negative.sum())
        print('kombi_5' + '_mai_negative: ', mai_negative.sum())
        print('kombi_5' + '_jun_negative: ', jun_negative.sum())
        print('kombi_5' + '_jul_negative: ', jul_negative.sum())
        print('kombi_5' + '_aug_negative: ', aug_negative.sum())
        print('kombi_5' + '_sep_negative: ', sep_negative.sum())
        print('kombi_5' + '_okt_negative: ', okt_negative.sum())
        print('kombi_5' + '_nov_negative: ', nov_negative.sum())
        print('kombi_5' + '_dez_negative: ', dez_negative.sum())
        print('kombi_5' + '_jan_demand: ', jan_demand.sum())
        print('kombi_5' + '_feb_demand: ', feb_demand.sum())
        print('kombi_5' + '_mar_demand: ', mar_demand.sum())
        print('kombi_5' + '_apr_demand: ', apr_demand.sum())
        print('kombi_5' + '_mai_demand: ', mai_demand.sum())
        print('kombi_5' + '_jun_demand: ', jun_demand.sum())
        print('kombi_5' + '_jul_demand: ', jul_demand.sum())
        print('kombi_5' + '_aug_demand: ', aug_demand.sum())
        print('kombi_5' + '_sep_demand: ', sep_demand.sum())
        print('kombi_5' + '_okt_demand: ', okt_demand.sum())
        print('kombi_5' + '_nov_demand: ', nov_demand.sum())
        print('kombi_5' + '_dez_demand: ', dez_demand.sum())
        print('kombi_5' + '_jan_wind: ', jan_wind.sum())
        print('kombi_5' + '_feb_wind: ', feb_wind.sum())
        print('kombi_5' + '_mar_wind: ', mar_wind.sum())
        print('kombi_5' + '_apr_wind: ', apr_wind.sum())
        print('kombi_5' + '_mai_wind: ', mai_wind.sum())
        print('kombi_5' + '_jun_wind: ', jun_wind.sum())
        print('kombi_5' + '_jul_wind: ', jul_wind.sum())
        print('kombi_5' + '_aug_wind: ', aug_wind.sum())
        print('kombi_5' + '_sep_wind: ', sep_wind.sum())
        print('kombi_5' + '_okt_wind: ', okt_wind.sum())
        print('kombi_5' + '_nov_wind: ', nov_wind.sum())
        print('kombi_5' + '_dez_wind: ', dez_wind.sum())
        print('kombi_5' + '_jan_pv: ', jan_pv.sum())
        print('kombi_5' + '_feb_pv: ', feb_pv.sum())
        print('kombi_5' + '_mar_pv: ', mar_pv.sum())
        print('kombi_5' + '_apr_pv: ', apr_pv.sum())
        print('kombi_5' + '_mai_pv: ', mai_pv.sum())
        print('kombi_5' + '_jun_pv: ', jun_pv.sum())
        print('kombi_5' + '_jul_pv: ', jul_pv.sum())
        print('kombi_5' + '_aug_pv: ', aug_pv.sum())
        print('kombi_5' + '_sep_pv: ', sep_pv.sum())
        print('kombi_5' + '_okt_pv: ', okt_pv.sum())
        print('kombi_5' + '_nov_pv: ', nov_pv.sum())
        print('kombi_5' + '_dez_pv: ', dez_pv.sum())

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_5'] = residual_MW
        results['positive_monthly_kombi_5'] = positive_monthly_MWh
        results['negative_monthly_kombi_5'] = negative_monthly_MWh
        results['demand_monthly_kombi_5'] = demand_monthly_MWh
        results['covered_demand_monthly_kombi_5'] = covered_demand_monthly_MWh
        results['jan_demand'] = jan_demand
        results['jan_wind'] = jan_wind
        results['jan_pv'] = jan_pv

    if arguments['--kombi_5_1']:

        masterplan_stein = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'stein' + '.csv', sep=',',
                                      index_col=0)

        masterplan_lkos = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'lkos' + '.csv', sep=',',
                                      index_col=0)

        print(masterplan_stein)
        print(masterplan_lkos)

        data_stein = pd.read_csv("../example/example_data/storage_invest.csv", sep=',')
        data_load_stein = data_stein['demand_el']  # demand in kW

        data_lkos = pd.read_csv("../example/example_data/storage_invest_load_1h_verschoben.csv", sep=',')
        data_load_lkos = data_lkos['demand_el']  # demand in kW

        demand_stein = masterplan_stein.loc['demand'][str(arguments['--year'])]
        demand_lkos = masterplan_lkos.loc['demand'][str(arguments['--year'])]  # demand in GWh
        wind = (masterplan_stein.loc['wind'][str(arguments['--year'])]
                + masterplan_lkos.loc['wind'][str(arguments['--year'])])  # installed wind in MW
        pv = (masterplan_stein.loc['pv'][str(arguments['--year'])]
              + masterplan_lkos.loc['pv'][str(arguments['--year'])])  # installed pv in MW
        bio = (masterplan_stein.loc['bio_MW'][str(arguments['--year'])]
              + masterplan_lkos.loc['bio_MW'][str(arguments['--year'])])  # installed pv in MW

        demand_ts_stein_MW = (data_load_stein/data_load_stein.sum()
            * demand_stein * 1e3)
        demand_ts_lkos_MW = (data_load_lkos/data_load_lkos.sum()
            * demand_lkos * 1e3)
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        residual_MW = (demand_ts_stein_MW + demand_ts_lkos_MW
            - (wind_ts_MW + pv_ts_MW))

        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_demand = demand_ts_stein_MW[1:744] + demand_ts_lkos_MW[1:744]
        feb_demand = demand_ts_stein_MW[745:1416] + demand_ts_lkos_MW[745:1416]
        mar_demand = demand_ts_stein_MW[1417:2160] + demand_ts_lkos_MW[1417:2160]
        apr_demand = demand_ts_stein_MW[2161:2880] + demand_ts_lkos_MW[2161:2880]
        mai_demand = demand_ts_stein_MW[2881:3624] + demand_ts_lkos_MW[2881:3624]
        jun_demand = demand_ts_stein_MW[3625:4344] + demand_ts_lkos_MW[3625:4344]
        jul_demand = demand_ts_stein_MW[4345:5088] + demand_ts_lkos_MW[4345:5088]
        aug_demand = demand_ts_stein_MW[5089:5832] + demand_ts_lkos_MW[5089:5832]
        sep_demand = demand_ts_stein_MW[5833:6552] + demand_ts_lkos_MW[5833:6552]
        okt_demand = demand_ts_stein_MW[6553:7296] + demand_ts_lkos_MW[6553:7296]
        nov_demand = demand_ts_stein_MW[7297:8016] + demand_ts_lkos_MW[7297:8016]
        dez_demand = demand_ts_stein_MW[8017:8760] + demand_ts_lkos_MW[8017:8760]

        jan_wind = wind_ts_MW[1:744]
        feb_wind = wind_ts_MW[745:1416]
        mar_wind = wind_ts_MW[1417:2160]
        apr_wind = wind_ts_MW[2161:2880]
        mai_wind = wind_ts_MW[2881:3624]
        jun_wind = wind_ts_MW[3625:4344]
        jul_wind = wind_ts_MW[4345:5088]
        aug_wind = wind_ts_MW[5089:5832]
        sep_wind = wind_ts_MW[5833:6552]
        okt_wind = wind_ts_MW[6553:7296]
        nov_wind = wind_ts_MW[7297:8016]
        dez_wind = wind_ts_MW[8017:8760]

        jan_pv = pv_ts_MW[1:744]
        feb_pv = pv_ts_MW[745:1416]
        mar_pv = pv_ts_MW[1417:2160]
        apr_pv = pv_ts_MW[2161:2880]
        mai_pv = pv_ts_MW[2881:3624]
        jun_pv = pv_ts_MW[3625:4344]
        jul_pv = pv_ts_MW[4345:5088]
        aug_pv = pv_ts_MW[5089:5832]
        sep_pv = pv_ts_MW[5833:6552]
        okt_pv = pv_ts_MW[6553:7296]
        nov_pv = pv_ts_MW[7297:8016]
        dez_pv = pv_ts_MW[8017:8760]

        demand_monthly_MWh = np.array([jan_demand.sum(), feb_demand.sum(),
                mar_demand.sum(), apr_demand.sum(), mai_demand.sum(),
                jun_demand.sum(), jul_demand.sum(), aug_demand.sum(),
                sep_demand.sum(), okt_demand.sum(), nov_demand.sum(),
                dez_demand.sum()])

        residual_monthly_MWh = np.array([jan_residual.sum(), feb_residual.sum(),
                mar_residual.sum(), apr_residual.sum(), mai_residual.sum(),
                jun_residual.sum(), jul_residual.sum(), aug_residual.sum(),
                sep_residual.sum(), okt_residual.sum(), nov_residual.sum(),
                dez_residual.sum()])

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print('kombi_5_1' + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        print('kombi_5_1' + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        print('kombi_5_1' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_5_1' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_5_1' + '_max_positive_MW: ', positive.max())
        print('kombi_5_1' + '_min_negative_MW: ', negative.min())
        print('kombi_5_1' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_5_1' + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_stein_MW + demand_ts_lkos_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_5_1'] = residual_MW
        results['residual_monthly_kombi_5_1'] = residual_monthly_MWh
        results['demand_monthly_kombi_5_1'] = demand_monthly_MWh

    if arguments['--kombi_6']:

        masterplan_stein = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'stein' + '.csv', sep=',',
                                      index_col=0)

        masterplan_osna = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'osna' + '.csv', sep=',',
                                      index_col=0)

        print(masterplan_stein)
        print(masterplan_osna)

        demand = (masterplan_stein.loc['demand'][str(arguments['--year'])]
                  + masterplan_osna.loc['demand'][str(arguments['--year'])])  # demand in GWh
        wind = (masterplan_stein.loc['wind'][str(arguments['--year'])]
                + masterplan_osna.loc['wind'][str(arguments['--year'])])  # installed wind in MW
        pv = (masterplan_stein.loc['pv'][str(arguments['--year'])]
              + masterplan_osna.loc['pv'][str(arguments['--year'])])  # installed pv in MW
        bio = (masterplan_stein.loc['bio_MW'][str(arguments['--year'])]
              + masterplan_osna.loc['bio_MW'][str(arguments['--year'])])  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        bio_ts_MW = np.ones(8760)*bio
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)

        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_positive = positive[1:744]
        feb_positive = positive[745:1416]
        mar_positive = positive[1417:2160]
        apr_positive = positive[2161:2880]
        mai_positive = positive[2881:3624]
        jun_positive = positive[3625:4344]
        jul_positive = positive[4345:5088]
        aug_positive = positive[5089:5832]
        sep_positive = positive[5833:6552]
        okt_positive = positive[6553:7296]
        nov_positive = positive[7297:8016]
        dez_positive = positive[8017:8760]

        jan_negative = negative[1:744]
        feb_negative = negative[745:1416]
        mar_negative = negative[1417:2160]
        apr_negative = negative[2161:2880]
        mai_negative = negative[2881:3624]
        jun_negative = negative[3625:4344]
        jul_negative = negative[4345:5088]
        aug_negative = negative[5089:5832]
        sep_negative = negative[5833:6552]
        okt_negative = negative[6553:7296]
        nov_negative = negative[7297:8016]
        dez_negative = negative[8017:8760]

        jan_demand = demand_ts_MW[1:744]
        feb_demand = demand_ts_MW[745:1416]
        mar_demand = demand_ts_MW[1417:2160]
        apr_demand = demand_ts_MW[2161:2880]
        mai_demand = demand_ts_MW[2881:3624]
        jun_demand = demand_ts_MW[3625:4344]
        jul_demand = demand_ts_MW[4345:5088]
        aug_demand = demand_ts_MW[5089:5832]
        sep_demand = demand_ts_MW[5833:6552]
        okt_demand = demand_ts_MW[6553:7296]
        nov_demand = demand_ts_MW[7297:8016]
        dez_demand = demand_ts_MW[8017:8760]

        jan_covered_demand = demand_ts_MW[1:744] + positive[1:744] * (-1)
        feb_covered_demand = demand_ts_MW[745:1416] + positive[745:1416] * (-1)
        mar_covered_demand = demand_ts_MW[1417:2160] + positive[1417:2160] * (-1)
        apr_covered_demand = demand_ts_MW[2161:2880] + positive[2161:2880] * (-1)
        mai_covered_demand = demand_ts_MW[2881:3624] + positive[2881:3624] * (-1)
        jun_covered_demand = demand_ts_MW[3625:4344] + positive[3625:4344] * (-1)
        jul_covered_demand = demand_ts_MW[4345:5088] + positive[4345:5088] * (-1)
        aug_covered_demand = demand_ts_MW[5089:5832] + positive[5089:5832] * (-1)
        sep_covered_demand = demand_ts_MW[5833:6552] + positive[5833:6552] * (-1)
        okt_covered_demand = demand_ts_MW[6553:7296] + positive[6553:7296] * (-1)
        nov_covered_demand = demand_ts_MW[7297:8016] + positive[7297:8016] * (-1)
        dez_covered_demand = demand_ts_MW[8017:8760] + positive[8017:8760] * (-1)

        jan_wind = wind_ts_MW[1:744]
        feb_wind = wind_ts_MW[745:1416]
        mar_wind = wind_ts_MW[1417:2160]
        apr_wind = wind_ts_MW[2161:2880]
        mai_wind = wind_ts_MW[2881:3624]
        jun_wind = wind_ts_MW[3625:4344]
        jul_wind = wind_ts_MW[4345:5088]
        aug_wind = wind_ts_MW[5089:5832]
        sep_wind = wind_ts_MW[5833:6552]
        okt_wind = wind_ts_MW[6553:7296]
        nov_wind = wind_ts_MW[7297:8016]
        dez_wind = wind_ts_MW[8017:8760]

        jan_pv = pv_ts_MW[1:744]
        feb_pv = pv_ts_MW[745:1416]
        mar_pv = pv_ts_MW[1417:2160]
        apr_pv = pv_ts_MW[2161:2880]
        mai_pv = pv_ts_MW[2881:3624]
        jun_pv = pv_ts_MW[3625:4344]
        jul_pv = pv_ts_MW[4345:5088]
        aug_pv = pv_ts_MW[5089:5832]
        sep_pv = pv_ts_MW[5833:6552]
        okt_pv = pv_ts_MW[6553:7296]
        nov_pv = pv_ts_MW[7297:8016]
        dez_pv = pv_ts_MW[8017:8760]

        positive_monthly_MWh = np.array([jan_positive.sum(), feb_positive.sum(),
                mar_positive.sum(), apr_positive.sum(), mai_positive.sum(),
                jun_positive.sum(), jul_positive.sum(), aug_positive.sum(),
                sep_positive.sum(), okt_positive.sum(), nov_positive.sum(),
                dez_positive.sum()])

        negative_monthly_MWh = np.array([jan_negative.sum(), feb_negative.sum(),
                mar_negative.sum(), apr_negative.sum(), mai_negative.sum(),
                jun_negative.sum(), jul_negative.sum(), aug_negative.sum(),
                sep_negative.sum(), okt_negative.sum(), nov_negative.sum(),
                dez_negative.sum()])

        demand_monthly_MWh = np.array([jan_demand.sum(),
            feb_demand.sum(), mar_demand.sum(),
            apr_demand.sum(), mai_demand.sum(),
            jun_demand.sum(), jul_demand.sum(),
            aug_demand.sum(), sep_demand.sum(),
            okt_demand.sum(), nov_demand.sum(),
            dez_demand.sum()])

        covered_demand_monthly_MWh = np.array([jan_covered_demand.sum(),
            feb_covered_demand.sum(), mar_covered_demand.sum(),
            apr_covered_demand.sum(), mai_covered_demand.sum(),
            jun_covered_demand.sum(), jul_covered_demand.sum(),
            aug_covered_demand.sum(), sep_covered_demand.sum(),
            okt_covered_demand.sum(), nov_covered_demand.sum(),
            dez_covered_demand.sum()])

        print('kombi_6' + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        print('kombi_6' + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        print('kombi_6' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_6' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_6' + '_max_positive_MW: ', positive.max())
        print('kombi_6' + '_min_negative_MW: ', negative.min())
        print('kombi_6' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_6' + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_6'] = residual_MW
        results['positive_monthly_kombi_6'] = positive_monthly_MWh
        results['negative_monthly_kombi_6'] = negative_monthly_MWh
        results['demand_monthly_kombi_6'] = demand_monthly_MWh
        results['covered_demand_monthly_kombi_6'] = covered_demand_monthly_MWh
        results['jan_demand'] = jan_demand
        results['jan_wind'] = jan_wind
        results['jan_pv'] = jan_pv

    if arguments['--region_1']:

        if arguments['--load_1'] == 'entsoe':
            data = pd.read_csv("../data/storage_invest.csv", sep=',')
            data_load = data['demand_el']  # demand in kW

        if arguments['--load_1'] == 'lkos':
            data_load = pd.read_csv('../data/Lastprofil_LKOS_MW_1h.csv', sep=',')
            # data_load_df = pd.read_csv('../data/Lastprofil_LKOS_MW_15min.csv', sep=',')
            # index = pd.date_range(
            #             pd.datetime(int(arguments['--year']), 1, 1, 0),
            #             periods=35040,
            #             freq='15min')
            # data_load_df.set_index(index, inplace=True)
            # data_load_df = data_load_df.resample('H').mean()
            # data_load_df.to_csv('../data/Lastprofil_LKOS_MW_1h.csv')
            data_load = data_load['demand_el'] * 1e3  # demand in kW

        if arguments['--load_1'] == 'bdew':
            e_slp = bdew.ElecSlp(int(arguments['--year']))
            h0_slp_15_min = e_slp.get_profile({'h0': 1})
            h0_slp = h0_slp_15_min.resample('H').mean()
            data_load = h0_slp['h0'].reset_index(drop=True)

        e_slp = bdew.ElecSlp(int(arguments['--year']))
        h0_slp_15_min = e_slp.get_profile({'h0': 1})
        h0_slp = h0_slp_15_min.resample('H').mean()
        data_load_2 = h0_slp['h0'].reset_index(drop=True)

        # masterplan = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 # str(arguments['--region_1']) + '.csv', sep=',',
                                 # index_col=0)

        masterplan = pd.read_csv('../scenarios/region/region_' +
                                 str(arguments['--region_1']) +
                                 '_region_parameter' +
                                 '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['annual_demand_GWh'][str(arguments['--year_1'])]  # demand in GWh
        wind = masterplan.loc['wind_MW'][str(arguments['--year_1'])]  # installed wind in MW
        pv = masterplan.loc['pv_MW'][str(arguments['--year_1'])]  # installed pv in MW
        # bio = masterplan.loc['bio_MW'][str(arguments['--year_1'])]  # installed pv in MW
        bio = 2

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        demand_ts_MW_2 = data_load_2/data_load_2.sum() * demand * 1e3
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        bio_ts_MW = np.ones(8760)*bio
        # bio_ts_MW = np.ones(8785)*bio
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)
        # residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW)

        print(max(demand_ts_MW))
        print(min(demand_ts_MW))
        print(demand_ts_MW.mean())

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)

        print(positive.sum())
        print('autarkie: ', 100*(1-positive.sum()/(demand.sum()*1e3)))

        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_positive = positive[1:744]
        feb_positive = positive[745:1416]
        mar_positive = positive[1417:2160]
        apr_positive = positive[2161:2880]
        mai_positive = positive[2881:3624]
        jun_positive = positive[3625:4344]
        jul_positive = positive[4345:5088]
        aug_positive = positive[5089:5832]
        sep_positive = positive[5833:6552]
        okt_positive = positive[6553:7296]
        nov_positive = positive[7297:8016]
        dez_positive = positive[8017:8760]

        jan_negative = negative[1:744]
        feb_negative = negative[745:1416]
        mar_negative = negative[1417:2160]
        apr_negative = negative[2161:2880]
        mai_negative = negative[2881:3624]
        jun_negative = negative[3625:4344]
        jul_negative = negative[4345:5088]
        aug_negative = negative[5089:5832]
        sep_negative = negative[5833:6552]
        okt_negative = negative[6553:7296]
        nov_negative = negative[7297:8016]
        dez_negative = negative[8017:8760]

        woche_demand = demand_ts_MW[200:536]
        woche_demand_2 = demand_ts_MW_2[200:536]
        jan_demand = demand_ts_MW[1:744]
        # jan_demand_2 = demand_ts_MW_2[1:744]
        feb_demand = demand_ts_MW[745:1416]
        mar_demand = demand_ts_MW[1417:2160]
        apr_demand = demand_ts_MW[2161:2880]
        mai_demand = demand_ts_MW[2881:3624]
        jun_demand = demand_ts_MW[3625:4344]
        jul_demand = demand_ts_MW[4345:5088]
        aug_demand = demand_ts_MW[5089:5832]
        sep_demand = demand_ts_MW[5833:6552]
        okt_demand = demand_ts_MW[6553:7296]
        nov_demand = demand_ts_MW[7297:8016]
        dez_demand = demand_ts_MW[8017:8760]

        jan_covered_demand = demand_ts_MW[1:744] + positive[1:744] * (-1)
        feb_covered_demand = demand_ts_MW[745:1416] + positive[745:1416] * (-1)
        mar_covered_demand = demand_ts_MW[1417:2160] + positive[1417:2160] * (-1)
        apr_covered_demand = demand_ts_MW[2161:2880] + positive[2161:2880] * (-1)
        mai_covered_demand = demand_ts_MW[2881:3624] + positive[2881:3624] * (-1)
        jun_covered_demand = demand_ts_MW[3625:4344] + positive[3625:4344] * (-1)
        jul_covered_demand = demand_ts_MW[4345:5088] + positive[4345:5088] * (-1)
        aug_covered_demand = demand_ts_MW[5089:5832] + positive[5089:5832] * (-1)
        sep_covered_demand = demand_ts_MW[5833:6552] + positive[5833:6552] * (-1)
        okt_covered_demand = demand_ts_MW[6553:7296] + positive[6553:7296] * (-1)
        nov_covered_demand = demand_ts_MW[7297:8016] + positive[7297:8016] * (-1)
        dez_covered_demand = demand_ts_MW[8017:8760] + positive[8017:8760] * (-1)

        woche_wind = wind_ts_MW[200:536]
        jan_wind = wind_ts_MW[1:744]
        feb_wind = wind_ts_MW[745:1416]
        mar_wind = wind_ts_MW[1417:2160]
        apr_wind = wind_ts_MW[2161:2880]
        mai_wind = wind_ts_MW[2881:3624]
        jun_wind = wind_ts_MW[3625:4344]
        jul_wind = wind_ts_MW[4345:5088]
        aug_wind = wind_ts_MW[5089:5832]
        sep_wind = wind_ts_MW[5833:6552]
        okt_wind = wind_ts_MW[6553:7296]
        nov_wind = wind_ts_MW[7297:8016]
        dez_wind = wind_ts_MW[8017:8760]

        woche_pv = pv_ts_MW[200:536]
        jan_pv = pv_ts_MW[1:744]
        feb_pv = pv_ts_MW[745:1416]
        mar_pv = pv_ts_MW[1417:2160]
        apr_pv = pv_ts_MW[2161:2880]
        mai_pv = pv_ts_MW[2881:3624]
        jun_pv = pv_ts_MW[3625:4344]
        jul_pv = pv_ts_MW[4345:5088]
        aug_pv = pv_ts_MW[5089:5832]
        sep_pv = pv_ts_MW[5833:6552]
        okt_pv = pv_ts_MW[6553:7296]
        nov_pv = pv_ts_MW[7297:8016]
        dez_pv = pv_ts_MW[8017:8760]

        woche_bio = bio_ts_MW[200:536]

        positive_monthly_MWh = np.array([jan_positive.sum(), feb_positive.sum(),
                mar_positive.sum(), apr_positive.sum(), mai_positive.sum(),
                jun_positive.sum(), jul_positive.sum(), aug_positive.sum(),
                sep_positive.sum(), okt_positive.sum(), nov_positive.sum(),
                dez_positive.sum()])

        negative_monthly_MWh = np.array([jan_negative.sum(), feb_negative.sum(),
                mar_negative.sum(), apr_negative.sum(), mai_negative.sum(),
                jun_negative.sum(), jul_negative.sum(), aug_negative.sum(),
                sep_negative.sum(), okt_negative.sum(), nov_negative.sum(),
                dez_negative.sum()])

        demand_monthly_MWh = np.array([jan_demand.sum(),
            feb_demand.sum(), mar_demand.sum(),
            apr_demand.sum(), mai_demand.sum(),
            jun_demand.sum(), jul_demand.sum(),
            aug_demand.sum(), sep_demand.sum(),
            okt_demand.sum(), nov_demand.sum(),
            dez_demand.sum()])

        covered_demand_monthly_MWh = np.array([jan_covered_demand.sum(),
            feb_covered_demand.sum(), mar_covered_demand.sum(),
            apr_covered_demand.sum(), mai_covered_demand.sum(),
            jun_covered_demand.sum(), jul_covered_demand.sum(),
            aug_covered_demand.sum(), sep_covered_demand.sum(),
            okt_covered_demand.sum(), nov_covered_demand.sum(),
            dez_covered_demand.sum()])

        # print(str(arguments['--region_1']) + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        # print(str(arguments['--region_1']) + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        # print(str(arguments['--region_1']) + '_positive_GWh: ', positive.sum()/1e3)
        # print(str(arguments['--region_1']) + '_negative_GWh: ', negative.sum()/1e3)
        # print(str(arguments['--region_1']) + '_max_positive_MW: ', positive.max())
        # print(str(arguments['--region_1']) + '_min_negative_MW: ', negative.min())
        # print(str(arguments['--region_1']) + '_hours_positive: ', len(positive.nonzero()[0]))
        # print(str(arguments['--region_1']) + '_hours_negative: ', len(negative.nonzero()[0]))
        # print(str(arguments['--region_1']) + '_jan_residual: ', jan_residual.sum())
        # print(str(arguments['--region_1']) + '_feb_residual: ', feb_residual.sum())
        # print(str(arguments['--region_1']) + '_mar_residual: ', mar_residual.sum())
        # print(str(arguments['--region_1']) + '_apr_residual: ', apr_residual.sum())
        # print(str(arguments['--region_1']) + '_mai_residual: ', mai_residual.sum())
        # print(str(arguments['--region_1']) + '_jun_residual: ', jun_residual.sum())
        # print(str(arguments['--region_1']) + '_jul_residual: ', jul_residual.sum())
        # print(str(arguments['--region_1']) + '_aug_residual: ', aug_residual.sum())
        # print(str(arguments['--region_1']) + '_sep_residual: ', sep_residual.sum())
        # print(str(arguments['--region_1']) + '_okt_residual: ', okt_residual.sum())
        # print(str(arguments['--region_1']) + '_nov_residual: ', nov_residual.sum())
        # print(str(arguments['--region_1']) + '_dez_residual: ', dez_residual.sum())
        # print(str(arguments['--region_1']) + '_jan_positive: ', jan_positive.sum())
        # print(str(arguments['--region_1']) + '_feb_positive: ', feb_positive.sum())
        # print(str(arguments['--region_1']) + '_mar_positive: ', mar_positive.sum())
        # print(str(arguments['--region_1']) + '_apr_positive: ', apr_positive.sum())
        # print(str(arguments['--region_1']) + '_mai_positive: ', mai_positive.sum())
        # print(str(arguments['--region_1']) + '_jun_positive: ', jun_positive.sum())
        # print(str(arguments['--region_1']) + '_jul_positive: ', jul_positive.sum())
        # print(str(arguments['--region_1']) + '_aug_positive: ', aug_positive.sum())
        # print(str(arguments['--region_1']) + '_sep_positive: ', sep_positive.sum())
        # print(str(arguments['--region_1']) + '_okt_positive: ', okt_positive.sum())
        # print(str(arguments['--region_1']) + '_nov_positive: ', nov_positive.sum())
        # print(str(arguments['--region_1']) + '_dez_positive: ', dez_positive.sum())
        # print(str(arguments['--region_1']) + '_jan_negative: ', jan_negative.sum())
        # print(str(arguments['--region_1']) + '_feb_negative: ', feb_negative.sum())
        # print(str(arguments['--region_1']) + '_mar_negative: ', mar_negative.sum())
        # print(str(arguments['--region_1']) + '_apr_negative: ', apr_negative.sum())
        # print(str(arguments['--region_1']) + '_mai_negative: ', mai_negative.sum())
        # print(str(arguments['--region_1']) + '_jun_negative: ', jun_negative.sum())
        # print(str(arguments['--region_1']) + '_jul_negative: ', jul_negative.sum())
        # print(str(arguments['--region_1']) + '_aug_negative: ', aug_negative.sum())
        # print(str(arguments['--region_1']) + '_sep_negative: ', sep_negative.sum())
        # print(str(arguments['--region_1']) + '_okt_negative: ', okt_negative.sum())
        # print(str(arguments['--region_1']) + '_nov_negative: ', nov_negative.sum())
        # print(str(arguments['--region_1']) + '_dez_negative: ', dez_negative.sum())
        # print(str(arguments['--region_1']) + '_jan_demand: ', jan_demand.sum())
        # print(str(arguments['--region_1']) + '_feb_demand: ', feb_demand.sum())
        # print(str(arguments['--region_1']) + '_mar_demand: ', mar_demand.sum())
        # print(str(arguments['--region_1']) + '_apr_demand: ', apr_demand.sum())
        # print(str(arguments['--region_1']) + '_mai_demand: ', mai_demand.sum())
        # print(str(arguments['--region_1']) + '_jun_demand: ', jun_demand.sum())
        # print(str(arguments['--region_1']) + '_jul_demand: ', jul_demand.sum())
        # print(str(arguments['--region_1']) + '_aug_demand: ', aug_demand.sum())
        # print(str(arguments['--region_1']) + '_sep_demand: ', sep_demand.sum())
        # print(str(arguments['--region_1']) + '_okt_demand: ', okt_demand.sum())
        # print(str(arguments['--region_1']) + '_nov_demand: ', nov_demand.sum())
        # print(str(arguments['--region_1']) + '_dez_demand: ', dez_demand.sum())
        # print(str(arguments['--region_1']) + '_jan_wind: ', jan_wind.sum())
        # print(str(arguments['--region_1']) + '_feb_wind: ', feb_wind.sum())
        # print(str(arguments['--region_1']) + '_mar_wind: ', mar_wind.sum())
        # print(str(arguments['--region_1']) + '_apr_wind: ', apr_wind.sum())
        # print(str(arguments['--region_1']) + '_mai_wind: ', mai_wind.sum())
        # print(str(arguments['--region_1']) + '_jun_wind: ', jun_wind.sum())
        # print(str(arguments['--region_1']) + '_jul_wind: ', jul_wind.sum())
        # print(str(arguments['--region_1']) + '_aug_wind: ', aug_wind.sum())
        # print(str(arguments['--region_1']) + '_sep_wind: ', sep_wind.sum())
        # print(str(arguments['--region_1']) + '_okt_wind: ', okt_wind.sum())
        # print(str(arguments['--region_1']) + '_nov_wind: ', nov_wind.sum())
        # print(str(arguments['--region_1']) + '_dez_wind: ', dez_wind.sum())
        # print(str(arguments['--region_1']) + '_jan_pv: ', jan_pv.sum())
        # print(str(arguments['--region_1']) + '_feb_pv: ', feb_pv.sum())
        # print(str(arguments['--region_1']) + '_mar_pv: ', mar_pv.sum())
        # print(str(arguments['--region_1']) + '_apr_pv: ', apr_pv.sum())
        # print(str(arguments['--region_1']) + '_mai_pv: ', mai_pv.sum())
        # print(str(arguments['--region_1']) + '_jun_pv: ', jun_pv.sum())
        # print(str(arguments['--region_1']) + '_jul_pv: ', jul_pv.sum())
        # print(str(arguments['--region_1']) + '_aug_pv: ', aug_pv.sum())
        # print(str(arguments['--region_1']) + '_sep_pv: ', sep_pv.sum())
        # print(str(arguments['--region_1']) + '_okt_pv: ', okt_pv.sum())
        # print(str(arguments['--region_1']) + '_nov_pv: ', nov_pv.sum())
        # print(str(arguments['--region_1']) + '_dez_pv: ', dez_pv.sum())
# #
#         print(str(arguments['--region_1']) + '_jan_cov: ', jan_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_feb_cov: ', feb_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_mar_cov: ', mar_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_apr_cov: ', apr_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_mai_cov: ', mai_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_jun_cov: ', jun_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_jul_cov: ', jul_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_aug_cov: ', aug_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_sep_cov: ', sep_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_okt_cov: ', okt_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_nov_cov: ', nov_covered_demand.sum())
#         print(str(arguments['--region_1']) + '_dez_cov: ', dez_covered_demand.sum())
#
        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_region_1'] = residual_MW
        results['positive_monthly_region_1'] = positive_monthly_MWh
        results['negative_monthly_region_1'] = negative_monthly_MWh
        results['demand_monthly_region_1'] = demand_monthly_MWh
        results['covered_demand_monthly_region_1'] = covered_demand_monthly_MWh
        results['jan_demand'] = jan_demand
        # results['jan_demand_2'] = jan_demand_2
        results['jan_wind'] = jan_wind
        results['jan_pv'] = jan_pv
        results['woche_demand'] = woche_demand
        results['woche_demand_2'] = woche_demand_2
        results['woche_wind'] = woche_wind
        results['woche_pv'] = woche_pv
        results['woche_bio'] = woche_bio


    if arguments['--region_2']:

        if arguments['--post-storage']:
            results = pd.read_pickle(open('../../../../Caros_Daten/masterplan_results_mit_biogas_unflex/region_results_dc_' +
                                   'landkreis_osnabrueck_' +
                                   '2030_' +
                                   '2005_' +
                                   '0.80_1_' +
                                   '.p', 'rb'))

            residual_MW = results['grid_ts_1']/1000

        if arguments['--load_2'] == 'entsoe':
            data = pd.read_csv("../data/storage_invest.csv", sep=',')
            data_load = data['demand_el']  # demand in kW

        if arguments['--load_2'] == 'lkos':
            data_load = pd.read_csv('../data/Lastprofil_LKOS_MW_1h.csv', sep=',')
            # data_load_df = pd.read_csv('../data/Lastprofil_LKOS_MW_15min.csv', sep=',')
            # index = pd.date_range(
            #             pd.datetime(int(arguments['--year']), 1, 1, 0),
            #             periods=35040,
            #             freq='15min')
            # data_load_df.set_index(index, inplace=True)
            # data_load_df = data_load_df.resample('H').mean()
            # data_load_df.to_csv('../data/Lastprofil_LKOS_MW_1h.csv')
            data_load = data_load['demand_el'] * 1e3  # demand in kW

        if arguments['--load_2'] == 'bdew':
            e_slp = bdew.ElecSlp(int(arguments['--year']))
            h0_slp_15_min = e_slp.get_profile({'h0': 1})
            h0_slp = h0_slp_15_min.resample('H').mean()
            data_load = h0_slp['h0'].reset_index(drop=True)

        masterplan = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                               str(arguments['--region_2']) + '.csv', sep=',',
                               index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year_2'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year_2'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year_2'])]  # installed pv in MW
        bio = masterplan.loc['bio_MW'][str(arguments['--year_2'])]  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        bio_ts_MW = np.ones(8760)*bio
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_positive = positive[1:744]
        feb_positive = positive[745:1416]
        mar_positive = positive[1417:2160]
        apr_positive = positive[2161:2880]
        mai_positive = positive[2881:3624]
        jun_positive = positive[3625:4344]
        jul_positive = positive[4345:5088]
        aug_positive = positive[5089:5832]
        sep_positive = positive[5833:6552]
        okt_positive = positive[6553:7296]
        nov_positive = positive[7297:8016]
        dez_positive = positive[8017:8760]

        jan_negative = negative[1:744]
        feb_negative = negative[745:1416]
        mar_negative = negative[1417:2160]
        apr_negative = negative[2161:2880]
        mai_negative = negative[2881:3624]
        jun_negative = negative[3625:4344]
        jul_negative = negative[4345:5088]
        aug_negative = negative[5089:5832]
        sep_negative = negative[5833:6552]
        okt_negative = negative[6553:7296]
        nov_negative = negative[7297:8016]
        dez_negative = negative[8017:8760]

        # jan_demand = demand_ts_MW[1:744]
        # feb_demand = demand_ts_MW[745:1416]
        # mar_demand = demand_ts_MW[1417:2160]
        # apr_demand = demand_ts_MW[2161:2880]
        # mai_demand = demand_ts_MW[2881:3624]
        # jun_demand = demand_ts_MW[3625:4344]
        # jul_demand = demand_ts_MW[4345:5088]
        # aug_demand = demand_ts_MW[5089:5832]
        # sep_demand = demand_ts_MW[5833:6552]
        # okt_demand = demand_ts_MW[6553:7296]
        # nov_demand = demand_ts_MW[7297:8016]
        # dez_demand = demand_ts_MW[8017:8760]

        # jan_covered_demand = demand_ts_MW[1:744] + positive[1:744] * (-1)
        # feb_covered_demand = demand_ts_MW[745:1416] + positive[745:1416] * (-1)
        # mar_covered_demand = demand_ts_MW[1417:2160] + positive[1417:2160] * (-1)
        # apr_covered_demand = demand_ts_MW[2161:2880] + positive[2161:2880] * (-1)
        # mai_covered_demand = demand_ts_MW[2881:3624] + positive[2881:3624] * (-1)
        # jun_covered_demand = demand_ts_MW[3625:4344] + positive[3625:4344] * (-1)
        # jul_covered_demand = demand_ts_MW[4345:5088] + positive[4345:5088] * (-1)
        # aug_covered_demand = demand_ts_MW[5089:5832] + positive[5089:5832] * (-1)
        # sep_covered_demand = demand_ts_MW[5833:6552] + positive[5833:6552] * (-1)
        # okt_covered_demand = demand_ts_MW[6553:7296] + positive[6553:7296] * (-1)
        # nov_covered_demand = demand_ts_MW[7297:8016] + positive[7297:8016] * (-1)
        # dez_covered_demand = demand_ts_MW[8017:8760] + positive[8017:8760] * (-1)

        # jan_wind = wind_ts_MW[1:744]
        # feb_wind = wind_ts_MW[745:1416]
        # mar_wind = wind_ts_MW[1417:2160]
        # apr_wind = wind_ts_MW[2161:2880]
        # mai_wind = wind_ts_MW[2881:3624]
        # jun_wind = wind_ts_MW[3625:4344]
        # jul_wind = wind_ts_MW[4345:5088]
        # aug_wind = wind_ts_MW[5089:5832]
        # sep_wind = wind_ts_MW[5833:6552]
        # okt_wind = wind_ts_MW[6553:7296]
        # nov_wind = wind_ts_MW[7297:8016]
        # dez_wind = wind_ts_MW[8017:8760]

        # jan_pv = pv_ts_MW[1:744]
        # feb_pv = pv_ts_MW[745:1416]
        # mar_pv = pv_ts_MW[1417:2160]
        # apr_pv = pv_ts_MW[2161:2880]
        # mai_pv = pv_ts_MW[2881:3624]
        # jun_pv = pv_ts_MW[3625:4344]
        # jul_pv = pv_ts_MW[4345:5088]
        # aug_pv = pv_ts_MW[5089:5832]
        # sep_pv = pv_ts_MW[5833:6552]
        # okt_pv = pv_ts_MW[6553:7296]
        # nov_pv = pv_ts_MW[7297:8016]
        # dez_pv = pv_ts_MW[8017:8760]

        # positive_monthly_MWh = np.array([jan_positive.sum(), feb_positive.sum(),
        #         mar_positive.sum(), apr_positive.sum(), mai_positive.sum(),
        #         jun_positive.sum(), jul_positive.sum(), aug_positive.sum(),
        #         sep_positive.sum(), okt_positive.sum(), nov_positive.sum(),
        #         dez_positive.sum()])

        # negative_monthly_MWh = np.array([jan_negative.sum(), feb_negative.sum(),
        #         mar_negative.sum(), apr_negative.sum(), mai_negative.sum(),
        #         jun_negative.sum(), jul_negative.sum(), aug_negative.sum(),
        #         sep_negative.sum(), okt_negative.sum(), nov_negative.sum(),
        #         dez_negative.sum()])

        # demand_monthly_MWh = np.array([jan_demand.sum(),
        #     feb_demand.sum(), mar_demand.sum(),
        #     apr_demand.sum(), mai_demand.sum(),
        #     jun_demand.sum(), jul_demand.sum(),
        #     aug_demand.sum(), sep_demand.sum(),
        #     okt_demand.sum(), nov_demand.sum(),
        #     dez_demand.sum()])

        # covered_demand_monthly_MWh = np.array([jan_covered_demand.sum(),
        #     feb_covered_demand.sum(), mar_covered_demand.sum(),
        #     apr_covered_demand.sum(), mai_covered_demand.sum(),
        #     jun_covered_demand.sum(), jul_covered_demand.sum(),
        #     aug_covered_demand.sum(), sep_covered_demand.sum(),
        #     okt_covered_demand.sum(), nov_covered_demand.sum(),
        #     dez_covered_demand.sum()])

        # print(str(arguments['--region_2']) + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        # print(str(arguments['--region_2']) + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        # print(str(arguments['--region_2']) + '_positive_GWh: ', positive.sum()/1e3)
        # print(str(arguments['--region_2']) + '_negative_GWh: ', negative.sum()/1e3)
        # print(str(arguments['--region_2']) + '_max_positive_MW: ', positive.max())
        # print(str(arguments['--region_2']) + '_min_negative_MW: ', negative.min())
        # print(str(arguments['--region_2']) + '_hours_positive: ', len(positive.nonzero()[0]))
        # print(str(arguments['--region_2']) + '_hours_negative: ', len(negative.nonzero()[0]))

        # results['demand_ts'] = demand_ts_MW
        # results['wind_ts'] = wind_ts_MW
        # results['pv_ts'] = pv_ts_MW
        results['residual_region_2'] = residual_MW
        # results['positive_monthly_region_2'] = positive_monthly_MWh
        # results['negative_monthly_region_2'] = negative_monthly_MWh
        # results['demand_monthly_region_2'] = demand_monthly_MWh
        # results['covered_demand_monthly_region_2'] = covered_demand_monthly_MWh

    if arguments['--region_3']:

        if arguments['--load_3'] == 'entsoe':
            data = pd.read_csv("../data/storage_invest.csv", sep=',')
            data_load = data['demand_el']  # demand in kW

        if arguments['--load_3'] == 'lkos':
            data_load = pd.read_csv('../data/Lastprofil_LKOS_MW_1h.csv', sep=',')
            # data_load_df = pd.read_csv('../data/Lastprofil_LKOS_MW_15min.csv', sep=',')
            # index = pd.date_range(
            #             pd.datetime(int(arguments['--year']), 1, 1, 0),
            #             periods=35040,
            #             freq='15min')
            # data_load_df.set_index(index, inplace=True)
            # data_load_df = data_load_df.resample('H').mean()
            # data_load_df.to_csv('../data/Lastprofil_LKOS_MW_1h.csv')
            data_load = data_load['demand_el'] * 1e3  # demand in kW

        if arguments['--load_3'] == 'bdew':
            e_slp = bdew.ElecSlp(int(arguments['--year']))
            h0_slp_15_min = e_slp.get_profile({'h0': 1})
            h0_slp = h0_slp_15_min.resample('H').mean()
            data_load = h0_slp['h0'].reset_index(drop=True)

        masterplan = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 str(arguments['--region_3']) + '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year_3'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year_3'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year_3'])]  # installed pv in MW
        bio = masterplan.loc['bio_MW'][str(arguments['--year_3'])]  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        bio_ts_MW = np.ones(8760)*bio
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)

        jan_residual = residual_MW[1:744]
        feb_residual = residual_MW[745:1416]
        mar_residual = residual_MW[1417:2160]
        apr_residual = residual_MW[2161:2880]
        mai_residual = residual_MW[2881:3624]
        jun_residual = residual_MW[3625:4344]
        jul_residual = residual_MW[4345:5088]
        aug_residual = residual_MW[5089:5832]
        sep_residual = residual_MW[5833:6552]
        okt_residual = residual_MW[6553:7296]
        nov_residual = residual_MW[7297:8016]
        dez_residual = residual_MW[8017:8760]

        jan_positive = positive[1:744]
        feb_positive = positive[745:1416]
        mar_positive = positive[1417:2160]
        apr_positive = positive[2161:2880]
        mai_positive = positive[2881:3624]
        jun_positive = positive[3625:4344]
        jul_positive = positive[4345:5088]
        aug_positive = positive[5089:5832]
        sep_positive = positive[5833:6552]
        okt_positive = positive[6553:7296]
        nov_positive = positive[7297:8016]
        dez_positive = positive[8017:8760]

        jan_negative = negative[1:744]
        feb_negative = negative[745:1416]
        mar_negative = negative[1417:2160]
        apr_negative = negative[2161:2880]
        mai_negative = negative[2881:3624]
        jun_negative = negative[3625:4344]
        jul_negative = negative[4345:5088]
        aug_negative = negative[5089:5832]
        sep_negative = negative[5833:6552]
        okt_negative = negative[6553:7296]
        nov_negative = negative[7297:8016]
        dez_negative = negative[8017:8760]

        jan_demand = demand_ts_MW[1:744]
        feb_demand = demand_ts_MW[745:1416]
        mar_demand = demand_ts_MW[1417:2160]
        apr_demand = demand_ts_MW[2161:2880]
        mai_demand = demand_ts_MW[2881:3624]
        jun_demand = demand_ts_MW[3625:4344]
        jul_demand = demand_ts_MW[4345:5088]
        aug_demand = demand_ts_MW[5089:5832]
        sep_demand = demand_ts_MW[5833:6552]
        okt_demand = demand_ts_MW[6553:7296]
        nov_demand = demand_ts_MW[7297:8016]
        dez_demand = demand_ts_MW[8017:8760]

        jan_covered_demand = demand_ts_MW[1:744] + positive[1:744] * (-1)
        feb_covered_demand = demand_ts_MW[745:1416] + positive[745:1416] * (-1)
        mar_covered_demand = demand_ts_MW[1417:2160] + positive[1417:2160] * (-1)
        apr_covered_demand = demand_ts_MW[2161:2880] + positive[2161:2880] * (-1)
        mai_covered_demand = demand_ts_MW[2881:3624] + positive[2881:3624] * (-1)
        jun_covered_demand = demand_ts_MW[3625:4344] + positive[3625:4344] * (-1)
        jul_covered_demand = demand_ts_MW[4345:5088] + positive[4345:5088] * (-1)
        aug_covered_demand = demand_ts_MW[5089:5832] + positive[5089:5832] * (-1)
        sep_covered_demand = demand_ts_MW[5833:6552] + positive[5833:6552] * (-1)
        okt_covered_demand = demand_ts_MW[6553:7296] + positive[6553:7296] * (-1)
        nov_covered_demand = demand_ts_MW[7297:8016] + positive[7297:8016] * (-1)
        dez_covered_demand = demand_ts_MW[8017:8760] + positive[8017:8760] * (-1)

        jan_wind = wind_ts_MW[1:744]
        feb_wind = wind_ts_MW[745:1416]
        mar_wind = wind_ts_MW[1417:2160]
        apr_wind = wind_ts_MW[2161:2880]
        mai_wind = wind_ts_MW[2881:3624]
        jun_wind = wind_ts_MW[3625:4344]
        jul_wind = wind_ts_MW[4345:5088]
        aug_wind = wind_ts_MW[5089:5832]
        sep_wind = wind_ts_MW[5833:6552]
        okt_wind = wind_ts_MW[6553:7296]
        nov_wind = wind_ts_MW[7297:8016]
        dez_wind = wind_ts_MW[8017:8760]

        jan_pv = pv_ts_MW[1:744]
        feb_pv = pv_ts_MW[745:1416]
        mar_pv = pv_ts_MW[1417:2160]
        apr_pv = pv_ts_MW[2161:2880]
        mai_pv = pv_ts_MW[2881:3624]
        jun_pv = pv_ts_MW[3625:4344]
        jul_pv = pv_ts_MW[4345:5088]
        aug_pv = pv_ts_MW[5089:5832]
        sep_pv = pv_ts_MW[5833:6552]
        okt_pv = pv_ts_MW[6553:7296]
        nov_pv = pv_ts_MW[7297:8016]
        dez_pv = pv_ts_MW[8017:8760]

        positive_monthly_MWh = np.array([jan_positive.sum(), feb_positive.sum(),
                mar_positive.sum(), apr_positive.sum(), mai_positive.sum(),
                jun_positive.sum(), jul_positive.sum(), aug_positive.sum(),
                sep_positive.sum(), okt_positive.sum(), nov_positive.sum(),
                dez_positive.sum()])

        negative_monthly_MWh = np.array([jan_negative.sum(), feb_negative.sum(),
                mar_negative.sum(), apr_negative.sum(), mai_negative.sum(),
                jun_negative.sum(), jul_negative.sum(), aug_negative.sum(),
                sep_negative.sum(), okt_negative.sum(), nov_negative.sum(),
                dez_negative.sum()])

        demand_monthly_MWh = np.array([jan_demand.sum(),
            feb_demand.sum(), mar_demand.sum(),
            apr_demand.sum(), mai_demand.sum(),
            jun_demand.sum(), jul_demand.sum(),
            aug_demand.sum(), sep_demand.sum(),
            okt_demand.sum(), nov_demand.sum(),
            dez_demand.sum()])

        covered_demand_monthly_MWh = np.array([jan_covered_demand.sum(),
            feb_covered_demand.sum(), mar_covered_demand.sum(),
            apr_covered_demand.sum(), mai_covered_demand.sum(),
            jun_covered_demand.sum(), jul_covered_demand.sum(),
            aug_covered_demand.sum(), sep_covered_demand.sum(),
            okt_covered_demand.sum(), nov_covered_demand.sum(),
            dez_covered_demand.sum()])

        print(str(arguments['--region_3']) + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        print(str(arguments['--region_3']) + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        print(str(arguments['--region_3']) + '_positive_GWh: ', positive.sum()/1e3)
        print(str(arguments['--region_3']) + '_negative_GWh: ', negative.sum()/1e3)
        print(str(arguments['--region_3']) + '_max_positive_MW: ', positive.max())
        print(str(arguments['--region_3']) + '_min_negative_MW: ', negative.min())
        print(str(arguments['--region_3']) + '_hours_positive: ', len(positive.nonzero()[0]))
        print(str(arguments['--region_3']) + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_region_3'] = residual_MW
        results['positive_monthly_region_3'] = positive_monthly_MWh
        results['negative_monthly_region_3'] = negative_monthly_MWh
        results['demand_monthly_region_3'] = demand_monthly_MWh
        results['covered_demand_monthly_region_3'] = covered_demand_monthly_MWh

    if arguments['--region_4']:

        if arguments['--load_4'] == 'entsoe':
            data = pd.read_csv("../../example/example_data/storage_invest.csv", sep=',')
            data_load = data['demand_el']  # demand in kW

        if arguments['--load_4'] == 'lkos':
            data_load = pd.read_csv('../data/Lastprofil_LKOS_MW_1h.csv', sep=',')
            # data_load_df = pd.read_csv('../data/Lastprofil_LKOS_MW_15min.csv', sep=',')
            # index = pd.date_range(
            #             pd.datetime(int(arguments['--year']), 1, 1, 0),
            #             periods=35040,
            #             freq='15min')
            # data_load_df.set_index(index, inplace=True)
            # data_load_df = data_load_df.resample('H').mean()
            # data_load_df.to_csv('../data/Lastprofil_LKOS_MW_1h.csv')
            data_load = data_load['demand_el'] * 1e3  # demand in kW

        if arguments['--load_4'] == 'bdew':
            e_slp = bdew.ElecSlp(int(arguments['--year']))
            h0_slp_15_min = e_slp.get_profile({'h0': 1})
            h0_slp = h0_slp_15_min.resample('H').mean()
            data_load = h0_slp['h0'].reset_index(drop=True)

        masterplan = pd.read_csv('../../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 str(arguments['--region_4']) + '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year_4'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year_4'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year_4'])]  # installed pv in MW
        bio = masterplan.loc['bio_MW'][str(arguments['--year_4'])]  # installed bio in MW
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data_weather['wind']*wind
        pv_ts_MW = data_weather['pv']*pv
        bio_ts_MW = np.ones(8760)*bio

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print(str(arguments['--region_4']) + '_wind_GWh: ', ((data_weather['wind']*wind).sum())/1e3)
        print(str(arguments['--region_4']) + '_pv_GWh: ', ((data_weather['pv']*pv).sum())/1e3)
        print(str(arguments['--region_4']) + '_positive_GWh: ', positive.sum()/1e3)
        print(str(arguments['--region_4']) + '_negative_GWh: ', negative.sum()/1e3)
        print(str(arguments['--region_4']) + '_max_positive_MW: ', positive.max())
        print(str(arguments['--region_4']) + '_min_negative_MW: ', negative.min())
        print(str(arguments['--region_4']) + '_hours_positive: ', len(positive.nonzero()[0]))
        print(str(arguments['--region_4']) + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        bio_ts_MW = np.ones(8760)*bio
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW + bio_ts_MW)
        results['residual_region_4'] = residual_MW

    return results

    # residual = ts_demand_all.sum() - ts_pv_all.sum()
    # positive_residual = residual.where(residual >= 0, 0)
    # covered_by_pv = ts_demand_all.sum() - positive_residual
    # print(covered_by_pv.sum())
    # print(demand_total)
    # sum_demand = ts_demand_all.sum()
    # print(sum_demand.sum())
    # results_dc['check_ssr_pv'] = covered_by_pv.sum() / demand_total

if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    # arguments = validate(**arguments)
    results = main(**arguments)
    if arguments['--carpet']:
        carpet = carpet_plot.Carpet
        fig = carpet.carpet_plot(results['residual'],
                                 res_name=('residual_' +
                                           str(arguments['--region']) + '_' +
                                           str(arguments['--year'])),
                                 show=True)
    if arguments['--line']:
        line = carpet_plot.Line
        # fig = line.line_plot(wind=results['wind_ts'], pv=results['pv_ts'],
        #                      demand=results['demand_ts'],
        #                      residual_1=results['residual_region_1'],
        #                      residual_2=results['residual_region_2'],
        #                      residual_3=results['residual_kombi_1'],
        #                      residual_4=results['residual_kombi_3'],
        #                      res_name=('power' +
        #                                str(arguments['--region_1']) + '_' +
        #                                str(arguments['--year'])),
        #                      show=True)

        fig = line.line_plot(pv=results['woche_demand'],
                             demand=results['woche_demand_2'],
                             wind=(results['woche_pv'] +
                                   results['woche_wind'] +
                                   results['woche_bio']),
                             res_name=('Power [MW]'),
                             show=True)

        # fig = line.line_plot(pv=results['demand_ts'],
        #                      wind=results['pv_ts'] + results['wind_ts'],
        #                      res_name=('Power in MW'),
        #                      show=True)
    if arguments['--jdl']:
        line = carpet_plot.Line
        if arguments['--kombi_1']:
            results['residual_kombi_1'].sort_values(ascending=False,inplace=True)
        if arguments['--kombi_3']:
            results['residual_kombi_3'].sort_values(ascending=False,inplace=True)
        if arguments['--kombi_3_1']:
            results['residual_kombi_3_1'].sort_values(ascending=False,inplace=True)
        if arguments['--kombi_5']:
            results['residual_kombi_5'].sort_values(ascending=False,inplace=True)
        if arguments['--kombi_5_1']:
            results['residual_kombi_5_1'].sort_values(ascending=False,inplace=True)
        if arguments['--kombi_6']:
            results['residual_kombi_6'].sort_values(ascending=False,inplace=True)
        if arguments['--region_1']:
            results['residual_region_1'].sort_values(ascending=False, inplace=True)
            results['wind_ts'].sort_values(ascending=False, inplace=True)
            results['pv_ts'].sort_values(ascending=False, inplace=True)
            results['demand_ts'].sort_values(ascending=False, inplace=True)
            xxx = results['residual_region_1']
        if arguments['--region_2']:
            results['residual_region_2'].sort_values(ascending=False, inplace=True)
            results['wind_ts'].sort_values(ascending=False, inplace=True)
            results['pv_ts'].sort_values(ascending=False, inplace=True)
            results['demand_ts'].sort_values(ascending=False, inplace=True)
            yyy = results['residual_region_2']
        if arguments['--region_3']:
            results['residual_region_3'].sort_values(ascending=False, inplace=True)
            results['wind_ts'].sort_values(ascending=False, inplace=True)
            results['pv_ts'].sort_values(ascending=False, inplace=True)
            results['demand_ts'].sort_values(ascending=False, inplace=True)
            zzz = results['residual_region_3']
        if arguments['--region_4']:
            results['residual_region_4'].sort_values(ascending=False,inplace=True)
            results['wind_ts'].sort_values(ascending=False, inplace=True)
            results['pv_ts'].sort_values(ascending=False, inplace=True)
            results['demand_ts'].sort_values(ascending=False, inplace=True)

        # xxx = xxx.to_frame().reset_index()
        # yyy = yyy.to_frame().reset_index()
        # zzz = zzz.to_frame().reset_index()
        # xxx.columns = ['id', 'val']
        # yyy.columns = ['id', 'val']
        # zzz.columns = ['id', 'val']
        # residual = xxx.merge(yyy, how='outer', left_index=True, right_index=True)
        # residual = residual.merge(zzz, how='outer', left_index=True, right_index=True)
        # residual['sum'] = residual['val_x'] + residual['val_y'] + residual['val']
        # print(residual)

        # fig = line.line_plot(residual_1=residual['sum'],
        #                      residual_2=results['residual_kombi_3'],
        #                      # residual_4=results['residual_region_4'],
        #                      res_name='Residual load in MW',
        #                      # res_name=('Residual demand ' +
        #                      # str(arguments['--year']) + ' in MW'),
        #                      show=True)

        # fig = line.line_plot(residual_1=results['residual_region_1']/144.38,
        #                      residual_2=results['residual_kombi_1']/422.51,
        #                      residual_3=results['residual_kombi_3']/712.45,
        #                      res_name='Residual load in MW',
        #                      # res_name=('Residual demand ' +
        #                      # str(arguments['--year']) + ' in MW'),
        #                      show=True)

        fig = line.line_plot(residual_1=results['residual_region_1'],
                             residual_2=results['residual_region_2'],
                             residual_3=results['residual_region_3'],
                             residual_4=results['residual_region_4'],
                             # residual_2=results['residual_kombi_1'],
                             # residual_3=results['residual_kombi_3'],
                             res_name='Residuallast in MW',
                             # res_name='Residual load [MW]',
                             # res_name=('Residual demand ' +
                             # str(arguments['--year']) + ' in MW'),
                             show=True)

        # fig = line.line_plot(residual_1=results['demand_ts'],
        #                      # residual_2=results['pv_ts'],
        #                      res_name='Erzeugungsleistung in MW',
        #                      show=True)

    # print(results['demand_monthly_kombi_3_1'].sum())
    # print(results['covered_demand_monthly_kombi_3_1'].sum())
    # print(results['negative_monthly_kombi_3_1'].sum())

    # print(results['demand_monthly_region_1'].sum() +
    #       results['demand_monthly_region_2'].sum() +
    #       results['demand_monthly_region_3'].sum())
    # print(results['covered_demand_monthly_region_1'].sum() +
    #       results['covered_demand_monthly_region_2'].sum() +
    #       results['covered_demand_monthly_region_3'].sum())
    # print(results['negative_monthly_region_1'].sum() +
    #       results['negative_monthly_region_2'].sum() +
    #       results['negative_monthly_region_3'].sum())

    if arguments['--bar']:
        bar = carpet_plot.Bar

        fig = bar.bar_plot(Y1=results['covered_demand_monthly_region_1'],
                           Y2=results['negative_monthly_region_1'],
                           Y3=results['demand_monthly_region_1'],
                           res_name='Demand [GWh]',
                           show=True)

        # fig = bar.bar_plot(Y1=(results['covered_demand_monthly_region_1'] +
        #                        results['covered_demand_monthly_region_2']),
        #                    Y2=(results['negative_monthly_region_1'] +
        #                        results['negative_monthly_region_2']),
        #                    Y3=(results['demand_monthly_region_1'] +
        #                        results['demand_monthly_region_2']),
        #                    res_name='Demand in GWh',
        #                    show=True)

    if arguments['--save']:
        fig.savefig(os.path.join(os.path.dirname(__file__)) +
                'current_figure' +
                '.pdf')
