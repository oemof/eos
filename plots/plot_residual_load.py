# -*- coding: utf-8 -*-

'''Calculating and plotting residual loads.

Usage: plot_residual_load [options]

Options:

  -o, --region_1=REGONE    The region 1. Choose from stein, lkos, osna and
                           rheine.
  -t, --region_2=REGTWO    The region 2. Choose from stein, lkos, osna and
      --region_3=REGTHR    The region 3. Choose from stein, lkos, osna and
                           rheine.
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
      --kombi_2            Region combination: stein + rheine
      --kombi_3            Region combination: stein + lkos + osna
      --kombi_4            Region combination: stein + lkos + rheine
      --kombi_5            Region combination: stein + lkos
      --year=YEAR          Scenario year. Choose from 2020, 2030, 2040 and
                           2050. [default: 2030]
      --entsoe             ENTSO-E load profile
      --lkos               LKOS load profile
      --bdew               BDEW standard load profile h0
      --carpet             Plot carpet.
      --line               Plot line.
      --jdl                Plot sorted annual load duration curve of the
                           residual load.
      --save               Save figure.
  -h, --help               Display this help.

'''

import pandas as pd
import os
from demandlib import bdew as bdew
import carpet_plot

try:
    from docopt import docopt
except ImportError:
    print("Unable to import docopt.\nIs the 'docopt' package installed?")


def main(**arguments):

    results = {}

    data = pd.read_csv("../example/example_data/storage_invest.csv", sep=',')

    if arguments['--entsoe']:
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

        masterplan_lkos = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                      'lkos' + '.csv', sep=',',
                                      index_col=0)

        masterplan_osna = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
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

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data['wind']*wind
        pv_ts_MW = data['pv']*pv
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print('kombi_1' + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
        print('kombi_1' + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
        print('kombi_1' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_1' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_1' + '_max_positive_MW: ', positive.max())
        print('kombi_1' + '_min_negative_MW: ', negative.min())
        print('kombi_1' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_1' + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_1'] = residual_MW


    if arguments['--kombi_3']:

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

        demand = (masterplan_stein.loc['demand'][str(arguments['--year'])]
                  + masterplan_lkos.loc['demand'][str(arguments['--year'])]
                  + masterplan_osna.loc['demand'][str(arguments['--year'])])  # demand in GWh
        wind = (masterplan_stein.loc['wind'][str(arguments['--year'])]
                + masterplan_lkos.loc['wind'][str(arguments['--year'])]
                + masterplan_osna.loc['wind'][str(arguments['--year'])])  # installed wind in MW
        pv = (masterplan_stein.loc['pv'][str(arguments['--year'])]
              + masterplan_lkos.loc['pv'][str(arguments['--year'])]
              + masterplan_osna.loc['pv'][str(arguments['--year'])])  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data['wind']*wind
        pv_ts_MW = data['pv']*pv
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print('kombi_3' + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
        print('kombi_3' + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
        print('kombi_3' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_3' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_3' + '_max_positive_MW: ', positive.max())
        print('kombi_3' + '_min_negative_MW: ', negative.min())
        print('kombi_3' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_3' + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_3'] = residual_MW

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

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data['wind']*wind
        pv_ts_MW = data['pv']*pv
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print('kombi_5' + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
        print('kombi_5' + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
        print('kombi_5' + '_positive_GWh: ', positive.sum()/1e3)
        print('kombi_5' + '_negative_GWh: ', negative.sum()/1e3)
        print('kombi_5' + '_max_positive_MW: ', positive.max())
        print('kombi_5' + '_min_negative_MW: ', negative.min())
        print('kombi_5' + '_hours_positive: ', len(positive.nonzero()[0]))
        print('kombi_5' + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_kombi_5'] = residual_MW

    if arguments['--region_1']:

        if arguments['--load_1'] == 'entsoe':
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

        masterplan = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 str(arguments['--region_1']) + '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year_1'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year_1'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year_1'])]  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data['wind']*wind
        pv_ts_MW = data['pv']*pv
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print(str(arguments['--region_1']) + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
        print(str(arguments['--region_1']) + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
        print(str(arguments['--region_1']) + '_positive_GWh: ', positive.sum()/1e3)
        print(str(arguments['--region_1']) + '_negative_GWh: ', negative.sum()/1e3)
        print(str(arguments['--region_1']) + '_max_positive_MW: ', positive.max())
        print(str(arguments['--region_1']) + '_min_negative_MW: ', negative.min())
        print(str(arguments['--region_1']) + '_hours_positive: ', len(positive.nonzero()[0]))
        print(str(arguments['--region_1']) + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_region_1'] = residual_MW

    if arguments['--region_2']:

        if arguments['--load_2'] == 'entsoe':
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

        masterplan = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 str(arguments['--region_2']) + '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year_2'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year_2'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year_2'])]  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data['wind']*wind
        pv_ts_MW = data['pv']*pv
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print(str(arguments['--region_2']) + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
        print(str(arguments['--region_2']) + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
        print(str(arguments['--region_2']) + '_positive_GWh: ', positive.sum()/1e3)
        print(str(arguments['--region_2']) + '_negative_GWh: ', negative.sum()/1e3)
        print(str(arguments['--region_2']) + '_max_positive_MW: ', positive.max())
        print(str(arguments['--region_2']) + '_min_negative_MW: ', negative.min())
        print(str(arguments['--region_2']) + '_hours_positive: ', len(positive.nonzero()[0]))
        print(str(arguments['--region_2']) + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_region_2'] = residual_MW

    if arguments['--region_3']:

        if arguments['--load_3'] == 'entsoe':
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

        masterplan = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 str(arguments['--region_3']) + '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year_3'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year_3'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year_3'])]  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data['wind']*wind
        pv_ts_MW = data['pv']*pv
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print(str(arguments['--region_3']) + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
        print(str(arguments['--region_3']) + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
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

    if arguments['--region_4']:

        if arguments['--load_4'] == 'entsoe':
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

        masterplan = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 str(arguments['--region_4']) + '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year_4'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year_4'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year_4'])]  # installed pv in MW

        demand_ts_MW = data_load/data_load.sum() * demand * 1e3
        wind_ts_MW = data['wind']*wind
        pv_ts_MW = data['pv']*pv
        residual_MW = demand_ts_MW - (wind_ts_MW + pv_ts_MW)

        positive = residual_MW.where(residual_MW > 0, 0)
        negative = residual_MW.where(residual_MW < 0, 0)
        print(str(arguments['--region_4']) + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
        print(str(arguments['--region_4']) + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
        print(str(arguments['--region_4']) + '_positive_GWh: ', positive.sum()/1e3)
        print(str(arguments['--region_4']) + '_negative_GWh: ', negative.sum()/1e3)
        print(str(arguments['--region_4']) + '_max_positive_MW: ', positive.max())
        print(str(arguments['--region_4']) + '_min_negative_MW: ', negative.min())
        print(str(arguments['--region_4']) + '_hours_positive: ', len(positive.nonzero()[0]))
        print(str(arguments['--region_4']) + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
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
        fig = line.line_plot(wind=results['wind_ts'], pv=results['pv_ts'],
                             demand=results['demand_ts'],
                             residual_1=results['residual_region_1'],
                             residual_2=results['residual_region_2'],
                             residual_3=results['residual_kombi_1'],
                             residual_4=results['residual_kombi_3'],
                             res_name=('power' +
                                       str(arguments['--region_1']) + '_' +
                                       str(arguments['--year'])),
                             show=True)
    if arguments['--jdl']:
        line = carpet_plot.Line
        if arguments['--kombi_1']:
            results['residual_kombi_1'].sort(ascending=False)
        if arguments['--kombi_3']:
            results['residual_kombi_3'].sort(ascending=False)
        if arguments['--kombi_5']:
            results['residual_kombi_5'].sort(ascending=False)
        if arguments['--region_1']:
            results['residual_region_1'].sort(ascending=False)
        if arguments['--region_2']:
            results['residual_region_2'].sort(ascending=False)
        if arguments['--region_3']:
            results['residual_region_3'].sort(ascending=False)
        if arguments['--region_4']:
            results['residual_region_4'].sort(ascending=False)
        # print(results['residual'])

        print(results['residual_region_1'])

        fig = line.line_plot(residual_1=results['residual_region_1'],
                             residual_2=results['residual_region_2'],
                             residual_3=results['residual_region_3'],
                             # residual_3=results['residual_region_3'],
                             # residual_4=results['residual_region_4'],
                             res_name='Residual load in MW',
                             # res_name=('Residual demand ' +
                             # str(arguments['--year']) + ' in MW'),
                             show=True)

        # fig = line.line_plot(residual_1=results['residual_kombi_5'],
        #                      residual_2=results['residual_kombi_3'],
        #                      residual_3=results['residual_kombi_1'],
        #                      res_name='Residual load in MW',
        #                      # res_name=('Residual demand ' +
        #                      # str(arguments['--year']) + ' in MW'),
        #                      show=True)

    if arguments['--save']:
        fig.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures/jdl') +
                '/' + 'jdl_' +
                'region_1_' + str(arguments['--region_1']) + '_' +
                'region_2_' + str(arguments['--region_2']) + '_' +
                'kombi_1_'+ str(arguments['--kombi_1']) + '_' +
                'kombi_3_'+ str(arguments['--kombi_3']) + '_' +
                'kombi_5_'+ str(arguments['--kombi_5']) + '_' +
                '.png')
