# -*- coding: utf-8 -*-

''' Plots.

Usage: quartier_plots.py [options]

Options:

  -c, --cost=COST          The cost scenario. [default: 1]
      --num-regions=NUM    Number of regions. [default: 84]
      --profile=PROFILE    Choose between summer, winter, day and night.

'''

###############################################################################
# imports
###############################################################################
import pickle
from docopt import docopt


def get_results(arguments):
    results = pickle.load(open('../results/quartier_results_' +
                               str(arguments['--num-regions']) + '_' +
                               str(arguments['--cost']) + '_' +
                               str(arguments['--profile']) + '.p', 'rb'))

    return results


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    results = get_results(arguments)
    print('check_ssr: ', results['check_ssr'])
    print('storage_cap: ', results['storage_cap'])
    print('objective: ', results['objective'])
