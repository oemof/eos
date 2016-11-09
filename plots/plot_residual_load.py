# -*- coding: utf-8 -*-

'''Calculating and plotting residual loads.

Usage: plot_residual_load [options]

Options:

  -o, --region_1=REGONE    The region 1. Choose from stein, lkos, osna and
                           rheine.
  -t, --region_2=REGTWO    The region 2. Choose from stein, lkos, osna and
                           rheine.
  -k, --kombi=KOMBI        Region combination. Choose from:
                           1: lkos + osna,
                           2: stein + rheine,
                           3: stein + lkos + osna,
                           4: stein + lkos + rheine.
      --year=YEAR          Scenario year. Choose from 2020, 2030, 2040 and
                           2050. [default: 2030]
      --carpet             Plot carpet.
      --line               Plot line.
      --jdl                Plot sorted annual load duration curve of the
                           residual load.
      --save               Save figure.
  -h, --help               Display this help.

'''

import pandas as pd
import os
import carpet_plot

try:
    from docopt import docopt
except ImportError:
    print("Unable to import docopt.\nIs the 'docopt' package installed?")


def main(**arguments):

    results = {}

    data = pd.read_csv("../example/example_data/storage_invest.csv", sep=',')
    data_load = data['demand_el']  # demand in kW
    # data_wind = data['wind']
    # data_pv = data['pv']

    if int(arguments['--kombi']):

        if int(arguments['--kombi']) is 1:

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
            print(str(arguments['--kombi']) + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
            print(str(arguments['--kombi']) + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
            print(str(arguments['--kombi']) + '_positive_GWh: ', positive.sum()/1e3)
            print(str(arguments['--kombi']) + '_negative_GWh: ', negative.sum()/1e3)
            print(str(arguments['--kombi']) + '_hours_positive: ', len(positive.nonzero()[0]))
            print(str(arguments['--kombi']) + '_hours_negative: ', len(negative.nonzero()[0]))

            results['demand_ts'] = demand_ts_MW
            results['wind_ts'] = wind_ts_MW
            results['pv_ts'] = pv_ts_MW
            results['residual_kombi_1'] = residual_MW


        elif int(arguments['--kombi']) is 3:

            masterplan_stein = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                          'stein' + '.csv', sep=',',
                                          index_col=0)

            masterplan_lkos = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                          'lkos' + '.csv', sep=',',
                                          index_col=0)

            masterplan_osna = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                          'osna' + '.csv', sep=',',
                                          index_col=0)

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
            print(str(arguments['--kombi']) + '_wind_GWh: ', ((data['wind']*wind).sum())/1e3)
            print(str(arguments['--kombi']) + '_pv_GWh: ', ((data['pv']*pv).sum())/1e3)
            print(str(arguments['--kombi']) + '_positive_GWh: ', positive.sum()/1e3)
            print(str(arguments['--kombi']) + '_negative_GWh: ', negative.sum()/1e3)
            print(str(arguments['--kombi']) + '_hours_positive: ', len(positive.nonzero()[0]))
            print(str(arguments['--kombi']) + '_hours_negative: ', len(negative.nonzero()[0]))

            results['demand_ts'] = demand_ts_MW
            results['wind_ts'] = wind_ts_MW
            results['pv_ts'] = pv_ts_MW
            results['residual_kombi_3'] = residual_MW

    if arguments['--region_1']:

        masterplan = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 str(arguments['--region_1']) + '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year'])]  # installed pv in MW

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
        print(str(arguments['--region_1']) + '_hours_positive: ', len(positive.nonzero()[0]))
        print(str(arguments['--region_1']) + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_region_1'] = residual_MW

    if arguments['--region_2']:

        masterplan = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                 str(arguments['--region_2']) + '.csv', sep=',',
                                 index_col=0)

        print(masterplan)

        demand = masterplan.loc['demand'][str(arguments['--year'])]  # demand in GWh
        wind = masterplan.loc['wind'][str(arguments['--year'])]  # installed wind in MW
        pv = masterplan.loc['pv'][str(arguments['--year'])]  # installed pv in MW

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
        print(str(arguments['--region_2']) + '_hours_positive: ', len(positive.nonzero()[0]))
        print(str(arguments['--region_2']) + '_hours_negative: ', len(negative.nonzero()[0]))

        results['demand_ts'] = demand_ts_MW
        results['wind_ts'] = wind_ts_MW
        results['pv_ts'] = pv_ts_MW
        results['residual_region_2'] = residual_MW

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
        if int(arguments['--kombi']) is 1:
            results['residual_kombi_1'].sort(ascending=False)
        if int(arguments['--kombi']) is 3:
            results['residual_kombi_3'].sort(ascending=False)
        if arguments['--region_1']:
            results['residual_region_1'].sort(ascending=False)
        if arguments['--region_2']:
            results['residual_region_2'].sort(ascending=False)
        # print(results['residual'])
        fig = line.line_plot(residual_1=results['residual_region_1'],
                             label_res_1=str(arguments['--region_1']),
                             residual_2=results['residual_region_2'],
                             label_res_2=str(arguments['--region_2']),
                             residual_3=results['residual_kombi_3'],
                             label_res_3=str(arguments['--kombi']),
                             res_name=('Residual demand ' +
                             str(arguments['--year']) + ' in MW'),
                             show=True)

    if arguments['--save']:
        fig.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures/jdl') +
                '/' + 'jdl_' +
                'region_1_' + str(arguments['--region_1']) + '_' +
                'region_2_' + str(arguments['--region_2']) + '_' +
                'kombi_' + str(arguments['--kombi']) + '_' +
                str(arguments['--year']) + '.png')
