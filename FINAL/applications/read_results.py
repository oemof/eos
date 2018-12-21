# -*- coding: utf-8 -*-

''' Plots.

Usage: quartier_plots.py [options]

Options:

  -c, --cost=COST          The cost scenario. [default: 1]
  -t, --tech=TECH          The tech scenario. [default: 1]
  -n, --number=NUM         Number of run. [default: 1]
      --num-hh=NUM         Number of households. [default: 84]
      --region=REG         Region.
      --year=YEAR          Weather year. [default: 2010]
      --scenario=SC        Path including the results
      --scenario_year=SY   Scenario year. [default: 2030]
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
        # results = pd.read_pickle('../results/' +
        #                            'region_results_dc_region_westerkappeln_' + str(arguments['--year']) + '_' +
        #                             str(arguments['--ssr']) + '_1_' +
        #                            '.p')

        results = pd.read_pickle('../results/' +
                                   'region_results_dc_total_region_2050_' + str(arguments['--year']) + '_' +
                                    str(arguments['--ssr']) + '_1_' +
                                   '.p')

        # results = pickle.load(open('../results/results/' +
        #                            'region_results_dc_total_region_2030_2005_' +
        #                             str(arguments['--ssr']) + '_1_' +
        #                            '.p', 'rb'))

        # results = pd.read_pickle(open('../../../../Caros_Daten/masterplan_results_mit_biogas_unflex/region_results_dc_' +
        #                            str(arguments['--region']) + '_' +
        #                            str(arguments['--scenario_year']) + '_' +
        #                            str(arguments['--year']) + '_' +
        #                            str(arguments['--ssr']) + '_1_' +
        #                            '.p', 'rb'))

        return results
# smb://192.168.10.14/Caros_Daten/quartier_1000/' +

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    sys = System
    results = sys.get_results(arguments)
    number=1
    print('pv_max: ', results['pv_max_'+str(number)])
    # print('pv_inst: ', results['pv_inst_1'])
    print('wind_max: ', results['wind_max_'+str(number)])
    # print('wind_inst: ', results['wind_inst_1'])
    print('demand: ', results['demand_'+str(number)])
    print('check_ssr: ', results['check_ssr_'+str(number)])
    print('storage_cap: ', results['storage_cap_'+str(number)])
    print('storage_in_max: ', results['storage_in_max_'+str(number)])
    print('storage_out_max: ', results['storage_out_max_'+str(number)])
    # print('storage_short_cap: ', results['storage_short_cap_1'])
    # print('storage_long_cap: ', results['storage_long_cap_1'])
    # print('biogas_bhkw: ', results['biogas_bhkw_inst_1'])
    # print('biogas_bhkw_ts: ', results['biogas_bhkw_ts_1'])
    # print('biogas_bhkw_inst: ', results['biogas_bhkw_inst_1'])
    print('grid: ', results['grid_'+str(number)])
    print('grid_max: ', results['grid_ts_'+str(number)].max())
    # print('hours_deficit: ', results['grid_ts_1'].count())
    print('hours_deficit: ', 8760-(results['grid_ts_'+str(number)]==0).sum())
    print('excess: ', results['excess_'+str(number)])
    print('objective: ', results['objective'])
    # print('check_ssr_pv: ', results['check_ssr_pv1'])
    # print(results['hh'])
    # pv_inst_total = 0
    # for house in results['hh']:
    #     pv_inst_total = pv_inst_total + results['pv_inst_' + house]
    # print('pv_inst_total: ', pv_inst_total)
    # excess = results['ts_excess_all'].sum(axis=1)
    # print(excess.sum())
    # sc = results['ts_sc_all'].sum(axis=1)
    # print(sc.sum())
#     print('excess house: ', results['excess_house_1'])
#     print('self_con house: ', results['self_con_house_1'])
#     print('pv house: ', results['pv_house_1'])
#     print('demand house: ', results['demand_house_1'])
#     print('feedin house: ', results['feedin_house_1'])
    #'] print(np.arange(1, 85))
   #  for house in np.arange(1, 85):
   #      print(house)
   #      print('pv_max_' + str(house) + ':',
   #              results['pv_max_house_' + str(house)])
    # print('hh: ', results['hh'])
# print('pv_max: ', results['pv_max_house_1' ])

