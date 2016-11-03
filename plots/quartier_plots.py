# -*- coding: utf-8 -*-

''' Plots.

Usage: quartier_plots.py [options]

Options:

  -c, --cost=COST          The cost scenario. [default: 1]
  -t, --tech=TECH          The tech scenario. [default: 1]
      --num-hh=NUM         Number of households. [default: 84]
      --year=YEAR          Weather year. [default: 2010]
      --ssr=SSR            Self-sufficiency degree. [default: None]
      --profile=PROFILE    Choose between random, summer, winter,
                           day, night, slp_h0, slp and include_g0_l0.
                           [default: random]
  -h, --help               Display this help.

'''

###############################################################################
# imports
###############################################################################
import pickle
from docopt import docopt
import numpy as np


class Quartier:
    """
    A quartier class.
    """

    def __init__(self, name=None):
        self.name = name

    def get_results(arguments):
        results = pickle.load(open('../results/quartier_results_' +
                                   str(arguments['--num-hh']) + '_' +
                                   str(arguments['--cost']) + '_' +
                                   str(arguments['--tech']) + '_' +
                                   str(arguments['--year']) + '_' +
                                   str(arguments['--ssr']) + '_' +
                                   str(arguments['--profile']) + '.p', 'rb'))

        return results


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    quar = Quartier
    results = quar.get_results(arguments)
    print('check_ssr: ', results['check_ssr'])
    print('storage_cap: ', results['storage_cap'])
    print('objective: ', results['objective'])
    print('check_ssr_pv: ', results['check_ssr_pv'])
    print(results['hh'])
    # pv_inst_total = 0
    # for house in parameters['hh']:
        # pv_inst_total =
    # excess = results['ts_excess_all'].sum(axis=1)
    # print(excess.sum())
    # sc = results['ts_sc_all'].sum(axis=1)
    # print(sc.sum())
    # print(results['excess_house_7'])
    # print(results['self_con_house_7'])
    # print(results['pv_house_7'])
    # print(results['demand_house_7'])
    # print(results['feedin_house_7'])
    #'] print(np.arange(1, 85))
   #  for house in np.arange(1, 85):
   #      print(house)
   #      print('pv_max_' + str(house) + ':',
   #              results['pv_max_house_' + str(house)])
    # print('hh: ', results['hh'])
# print('pv_max: ', results['pv_max_house_1' ])

