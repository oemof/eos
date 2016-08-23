# -*- coding: utf-8 -*-

''' Plots.

Usage: region_plots.py [options]

Options:

      --num-regions=NUM    Number of regions. [default: 24]
'''

###############################################################################
# imports
###############################################################################
import pickle
import pprint as pp
import itertools
import numpy as np
import matplotlib.pyplot as plt
import pprint as pp
from docopt import docopt

# res = pickle.load(open('../results/households_results_dc_0.7.p', 'rb'))
# pp.pprint(res)


def calculate_combinations(num_regions):
    regions = np.arange(1, num_regions + 1)
    i = 1
    combinations = [0, 0, 0]
    for n in itertools.combinations(regions, 2):
        combinations = np.vstack((combinations, [i, n[0], n[1]]))
        i = i + 1

    print('combinations: ', combinations)

    return combinations


def scatter_plot(combinations):

    res_single_regions = pickle.load(open('../results/results_single_regions_85.p', 'rb'))

    results = [0, 0, 0]

    for i in np.arange(1, len(combinations)):
        res_combinations = pickle.load(open
                ('../results/region_results_dc_0.85_' + str(i) + '_.p', 'rb'))
        results = np.vstack((results,
                [i, (res_single_regions['storage_cap' + str(combinations[i][1])] +
                     res_single_regions['storage_cap' + str(combinations[i][2])]),
                     res_combinations['storage_cap' + str(i)]]))

    print('results: ', results)  # results in MWh
    results_MWh = results/1e3

    plt.scatter(results_MWh[:, 1], results_MWh[:, 2])
    plt.plot([0, results_MWh.max()], [0, results_MWh.max()], 'r-')
    plt.axis([-10, results_MWh.max()+10, -10, results_MWh.max()+10])
    plt.xlabel('Storage capacity (single regions summed) in MWh', size=16)
    plt.ylabel('Storage capacity (both regions connected) in MWh', size=16)
    plt.rcParams.update({'font.size': 18})

    plt.show()

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    combinations = calculate_combinations(int(arguments['--num-regions']))
    scatter_plot(combinations)
