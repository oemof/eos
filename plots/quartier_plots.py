# -*- coding: utf-8 -*-

''' Plots.

Usage: quartier_plots.py [options]

Options:

  -c, --cost=COST          The cost scenario. [default: 1]
      --num-hh=NUM    Number of households. [default: 84]
      --year=YEAR          Weather year. [default: 2010]
      --ssr=SSR            Self-sufficiency degree. [default: None]
      --profile=PROFILE    Choose between random, summer, winter, day and night.
                           [default: random]
  -h, --help               Display this help.

'''

###############################################################################
# imports
###############################################################################
import pickle
from docopt import docopt
import numpy as np


def get_results(arguments):
    results = pickle.load(open('../results/quartier_results_' +
                               str(arguments['--num-hh']) + '_' +
                               str(arguments['--cost']) + '_' +
                               str(arguments['--year']) + '_' +
                               str(arguments['--ssr']) + '_' +
                               str(arguments['--profile']) + '.p', 'rb'))

    return results


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    results = get_results(arguments)
    print('check_ssr: ', results['check_ssr'])
    print('storage_cap: ', results['storage_cap'])
    print('objective: ', results['objective'])
    print(np.arange(1, 85))
   #  for house in np.arange(1, 85):
   #      print(house)
   #      print('pv_max_' + str(house) + ':',
   #              results['pv_max_house_' + str(house)])
    # print('hh: ', results['hh'])
    # print('pv_max: ', results['pv_max_house_1' ])
