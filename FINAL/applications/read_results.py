# -*- coding: utf-8 -*-

''' Plots.

Usage: read_results.py [options]

Options:

  -c, --cost=COST          The cost scenario. [default: 1]
  -t, --tech=TECH          The tech scenario. [default: 1]
  -n, --number=NUM         Number of region. [default: 1]
      --num-hh=NUM         Number of households. [default: 84]
      --region=REG         Region.
      --year=YEAR          Weather year. [default: 2005]
      --scenario=SC        Path including the results
      --scenario-year=SY   Scenario year. [default: 2030]
      --ssr=SSR            Self-sufficiency degree. [default: None]
      --profile=PROFILE    Choose between random, summer, winter,
                           day, night, slp_h0, slp and include_g0_l0.
                           [default: random]
      --pv_installed=PV    PV installed.
  -h, --help               Display this help.

'''

###############################################################################
# imports
###############################################################################
import pickle
import pandas as pd
from docopt import docopt
import numpy as np


class System:
    """
    A quartier class.
    """

    def __init__(self, name=None):
        self.name = name

    def get_results(arguments):

        # smb://192.168.10.14/Caros_Daten/quartier_1000/' +



###################################################################
# REGION
        results = pd.read_pickle('../results/1_EIN_SPEICHER/' +
                                   'region_results_dc_' +
                                   str(arguments['--region']) + '_' +
                                   str(arguments['--scenario-year']) + '_' +
                                   str(arguments['--year']) +
                                   '_' +
                                   str(arguments['--ssr']) +
                                   '_1_' +
                                   '.p')

#         results = pd.read_pickle('../results/region_commune/' +
#                                    'region_results_dc_' +
#                                    str(arguments['--region']) +
#                                    '_' +
#                                    str(arguments['--year']) +
#                                    '_' +
#                                    str(arguments['--ssr']) +
#                                    '_' +
#                                    str(arguments['--number']) +
#                                    '_.p')

#         results = pd.read_pickle('../results/REGION_COMMUNE_MULTI/ohne_biogas/' +
#                                     'results_single_regions_0.80.p')
#
        # results = pd.read_pickle('../results/REGION_COMMUNE_MULTI/mit_biogas_unflex/' +
                                    # 'results_single_regions_0.80.p')

        return results
###################################################################

###################################################################
# QUARTIER
        # results = pd.read_pickle('../results/QUARTIER_TUSSENHAUSEN/' +
        #                            'quartier_results_' +
        #                             str(arguments['--num-hh']) +
        #                            '_1_1_' +
        #                             str(arguments['--year']) +
        #                             '_' +
        #                             str(arguments['--ssr']) +
        #                            '_1_' +
        #                             str(arguments['--profile']) +
        #                            '.p')

        # results = pd.read_pickle('../results/HOUSEHOLDS_QUARTIER/' +
        #                            'quartier_results_' +
        #                             str(arguments['--num-hh']) +
        #                            '_1_1_' +
        #                             str(arguments['--year']) +
        #                             '_' +
        #                             str(arguments['--ssr']) +
        #                             '_' +
        #                            '.p')

        # results = pd.read_pickle('../results/QUARTIER_RANDOM/' +
        #                             'quartier_results_10_2_2_' +
        #                             str(arguments['--year']) +
        #                             '_0.5_' +
        #                             '1' +
        #                             '_random' +
        #                             '.p')


        # return results
###################################################################

###################################################################
# HOUSEHOLDS
        # results_1_bis_20 = pd.read_pickle('../results/households/' +
        #                                'households_results_' +
        #                                '1_bis_20'+
        #                                '_1_1_' +
        #                                 str(arguments['--year']) +
        #                                '_' +
        #                             str(arguments['--ssr']) +
        #                                '_' +
        #                                '.p')

        # results_21_bis_40 = pd.read_pickle('../results/households/' +
        #                                'households_results_' +
        #                                '21_bis_40'+
        #                                '_1_1_' +
        #                                 str(arguments['--year']) +
        #                                '_' +
        #                                 str(arguments['--ssr']) +
        #                                '_' +
        #                                '.p')

        # results_41_bis_60 = pd.read_pickle('../results/HOUSEHOLDS_QUARTIER/' +
        #                                'households_results_' +
        #                                '41_bis_60'+
        #                                '_1_1_' +
        #                                 str(arguments['--year']) +
        #                                '_' +
        #                                 str(arguments['--ssr']) +
        #                                '_' +
        #                                '.p')

        # results_61_bis_74 = pd.read_pickle('../results/households/' +
        #                                'households_results_' +
        #                                '61_bis_74'+
        #                                '_1_1_' +
        #                                 str(arguments['--year']) +
        #                                '_' +
        #                                 str(arguments['--ssr']) +
        #                                '_' +
        #                                '.p')

        # results_1_bis_20_costopt = pd.read_pickle('../results/households/' +
        #                                        'households_results_' +
        #                                        '1_bis_20'+
        #                                        '_1_1_' +
        #                                         str(arguments['--year']) +
        #                                        '_' +
        #                                        str(arguments['--ssr']) +
        #                                        '_costopt' +
        #                                        '.p')

        # results_21_bis_40_costopt = pd.read_pickle('../results/households/' +
        #                                        'households_results_' +
        #                                        '21_bis_40'+
        #                                        '_1_1_' +
        #                                         str(arguments['--year']) +
        #                                        '_' +
        #                                         str(arguments['--ssr']) +
        #                                        '_costopt' +
        #                                        '.p')

        # results_41_bis_60_costopt = pd.read_pickle('../results/households/' +
        #                                        'households_results_' +
        #                                        '41_bis_60'+
        #                                        '_1_1_' +
        #                                         str(arguments['--year']) +
        #                                        '_' +
        #                                         str(arguments['--ssr']) +
        #                                        '_costopt' +
        #                                        '.p')

        # results_61_bis_74_costopt = pd.read_pickle('../results/households/' +
        #                                        'households_results_' +
        #                                        '61_bis_74'+
        #                                        '_1_1_' +
        #                                         str(arguments['--year']) +
        #                                        '_' +
        #                                         str(arguments['--ssr']) +
        #                                        '_costopt' +
        #                                        '.p')

        # return (results_1_bis_20, results_1_bis_20_costopt,
        #         results_21_bis_40, results_21_bis_40_costopt,
        #         results_41_bis_60, results_41_bis_60_costopt,
        #         results_61_bis_74, results_61_bis_74_costopt)

###################################################################

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    sys = System
    results = sys.get_results(arguments)
    # (results_1_bis_20, results_1_bis_20_costopt,
    # results_21_bis_40, results_21_bis_40_costopt,
    # results_41_bis_60, results_41_bis_60_costopt,
    # results_61_bis_74, results_61_bis_74_costopt) = sys.get_results(arguments)


# REGION (QUARTIER WEITER UNTEN)
# -------------------------------------------------------------------
    number=str(arguments['--number'])
    # print('pv_max: ', results['pv_max_'+str(number)])
    # # print('pv_inst: ', results['pv_inst_1'])
    # print('wind_max: ', results['wind_max_'+str(number)])
    # # print('wind_inst: ', results['wind_inst_1'])
    # print('demand: ', results['demand_'+str(number)])
    # print('check_ssr: ', results['check_ssr_'+str(number)])
    print('storage_cap: ', results['storage_cap_'+str(number)])
    # print('storage_in_max: ', results['storage_in_ts_'+str(number)].max())
    # # print('storage_in_max: ', results['storage_in_max_'+str(number)])
    # print('storage_out_max: ', results['storage_out_ts_'+str(number)].max())
    # # print('storage_out_max: ', results['storage_out_max_'+str(number)])

    # # print('storage_short_cap: ', results['storage_short_cap_0'])
    # # print('storage_short_in_max: ', results['storage_short_in_max_1'])
    # # print('storage_short_out_max: ', results['storage_short_out_max_1'])
    # # print('storage_long_cap: ', results['storage_long_cap_1'])
    # # print('storage_long_in_max: ', results['storage_long_in_max_1'])
    # # print('storage_long_out_max: ', results['storage_long_out_max_1'])

    # print('biogas_used: ', results['biogas_bhkw_ts_1'].sum()/0.38)
    # # print('biogas_bhkw_inst: ', results['biogas_bhkw_inst_1'])
    # print('grid: ', results['grid_'+str(number)])
    # print('grid_max: ', results['grid_ts_'+str(number)].max())
    # # # # print('hours_deficit: ', results['grid_ts_1'].count())
    # # print('hours_deficit: ', 8760-(results['grid_ts_'+str(number)]==0).sum())
    # print('excess: ', results['excess_'+str(number)])
    # print('objective: ', results['objective'])
    # # # print('check_ssr_pv: ', results['check_ssr_pv1'])
    # # print(results['hh'])
    # # excess = results['ts_excess_all'].sum(axis=1)
    # # print(excess.sum())
    # # sc = results['ts_sc_all'].sum(axis=1)
    # # print(sc.sum())
#   #   print('excess house: ', results['excess_house_1'])
#   #   print('self_con house: ', results['self_con_house_1'])
#   #   print('pv house: ', results['pv_house_1'])
#   #   print('demand house: ', results['demand_house_1'])
#   #   print('feedin house: ', results['feedin_house_1'])
    # #'] print(np.arange(1, 85))
   ##   for house in np.arange(1, 85):
   ##       print(house)
   ##       print('pv_max_' + str(house) + ':',
   ##               results['pv_max_house_' + str(house)])
    # # print('hh: ', results['hh'])
# pr# int('pv_max: ', results['pv_max_house_1' ])

# QUARTIER
# -------------------------------------------------------------------
    # # print(results)
    # print('storage_cap: ', results['storage_cap'])
    # print('check_ssr: ', results['check_ssr'])
    # print('grid: ', results['grid'])
    # print('grid_max: ', results['ts_grid'].max())
    # print('hours_deficit: ', 8760-(results['ts_grid']==0).sum())
    # # print('excess: ', results['excess_'])
    # print('objective: ', results['objective'])

    # demand_total = 0
    # for house in results['hh']:
    #     demand_total = demand_total + results['demand_' + house]
    # print('demand_total: ', demand_total)

    # excess_total = 0
    # for house in results['hh']:
    #     excess_total = excess_total + results['excess_' + house]
    # print('excess_total: ', excess_total)

    # # nur bei costopt
    # pv_inst_total = 0
    # for house in results['hh']:
    #     pv_inst_total = pv_inst_total + results['pv_inst_' + house]
    # print('pv_inst_total: ', pv_inst_total)

# HOUSEHOLDS
# -------------------------------------------------------------------
 #    df = pd.DataFrame(columns=['storage_cap'])
 #    for house in np.arange(20):
 #        df = df.append({'storage_cap': results_1_bis_20['storage_cap_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(20):
 #        df = df.append({'storage_cap': results_21_bis_40['storage_cap_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(20):
 #        df = df.append({'storage_cap': results_41_bis_60['storage_cap_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(14):
 #        df = df.append({'storage_cap': results_61_bis_74['storage_cap_house_' + str(house+1)]}, ignore_index=True)

 #    # -----------------------------------------------------------

 #    df_costopt = pd.DataFrame(columns=['storage_cap'])
 #    for house in np.arange(20):
 #        df_costopt = df_costopt.append({'storage_cap': results_1_bis_20_costopt['storage_cap_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(20):
 #        df_costopt = df_costopt.append({'storage_cap': results_21_bis_40_costopt['storage_cap_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(20):
 #        df_costopt = df_costopt.append({'storage_cap': results_41_bis_60_costopt['storage_cap_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(14):
 #        df_costopt = df_costopt.append({'storage_cap': results_61_bis_74_costopt['storage_cap_house_' + str(house+1)]}, ignore_index=True)

 #    # -----------------------------------------------------------

 #    df_pv = pd.DataFrame(columns=['pv'])
 #    for house in np.arange(20):
 #        df_pv = df_pv.append({'pv': results_1_bis_20['pv_inst_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(20):
 #        df_pv = df_pv.append({'pv': results_21_bis_40['pv_inst_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(20):
 #        df_pv = df_pv.append({'pv': results_41_bis_60['pv_inst_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(14):
 #        df_pv = df_pv.append({'pv': results_61_bis_74['pv_inst_house_' + str(house+1)]}, ignore_index=True)

 #    # -----------------------------------------------------------

 #    df_pv_costopt = pd.DataFrame(columns=['pv'])
 #    for house in np.arange(20):
 #        df_pv_costopt = df_pv_costopt.append({'pv': results_1_bis_20_costopt['pv_inst_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(20):
 #        df_pv_costopt = df_pv_costopt.append({'pv': results_21_bis_40_costopt['pv_inst_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(20):
 #        df_pv_costopt = df_pv_costopt.append({'pv': results_41_bis_60_costopt['pv_inst_house_' + str(house+1)]}, ignore_index=True)

 #    for house in np.arange(14):
 #        df_pv_costopt = df_pv_costopt.append({'pv': results_61_bis_74_costopt['pv_inst_house_' + str(house+1)]}, ignore_index=True)

 #    with pd.option_context('display.max_rows', 999):
 #        print(df)
 #    # print(results_1_bis_20_costopt['pv_inst_house_1'])
 #    # print('mean', df.mean(0))
 #    # print('std', df.std(0))
 #    # print('min', df.min(0))
 #    # print('quantile_25', df.quantile(0.25))
 #    # print('median', df.median(0))
 #    # print('quantile_75', df.quantile(0.75))
 #    # print('max', df.max(0))

 #    # print('mean costopt', df_costopt.mean(0))
 #    # print('std costopt', df_costopt.std(0))
 #    # print('min costopt', df_costopt.min(0))
 #    # print('quantile_25 costopt', df_costopt.quantile(0.25))
 #    # print('median costopt', df_costopt.median(0))
 #    # print('quantile_75 costopt', df_costopt.quantile(0.75))
 #    # print('max costopt', df_costopt.max(0))

 #    # print('mean costopt', df_pv_costopt.mean(0))
 #    # print('std costopt', df_pv_costopt.std(0))
 #    # print('min costopt', df_pv_costopt.min(0))
 #    # print('quantile_25 costopt', df_pv_costopt.quantile(0.25))
 #    # print('median costopt', df_pv_costopt.median(0))
 #    # print('quantile_75 costopt', df_pv_costopt.quantile(0.75))
 #    # print('max costopt', df_pv_costopt.max(0))

##          print('storage_cap_' + str(house+1) +':', results['storage_cap_house_' + str(house+1)])
##
##      for house in np.arange(20):
##          print('demand_' + str(house+1) + ':', results['demand_house_' + str(house+1)])
##
##      for house in np.arange(20):
##          print('check_ssr_' + str(house+1) + ':', results['check_ssr_house_' + str(house+1)])
##
##      for house in np.arange(20):
##          print('grid_' + str(house+1) + ':', results['grid_house_' + str(house+1)])
##
##      # for house in np.arange(20):
##          # print('grid_max_' + str(house+1) + ':', results['ts_grid_house_' + str(house+1)].max())
##
##      # for house in np.arange(20):
##          # print('hours_deficit_' + str(house+1) + ':', 8760-(results['ts_grid_house_' + str(house+1)]==0).sum())
##
##      # for house in np.arange(20):
##          # print('objective_' + str(house+1) + ':', results['objective_house_' + str(house+1)])
##
##      for house in np.arange(20):
##          print('excess_' + str(house+1) + ':', results['excess_house_' + str(house+1)])
##
##      for house in np.arange(20):
##          print('pv_inst_' + str(house+1) + ':', results['pv_inst_house_' + str(house+1)])
##
