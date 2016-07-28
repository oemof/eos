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

    res_single_regions = pickle.load(open('../results/results_single_regions.p', 'rb'))
    res_combinations = pickle.load(open('../results/results_combinations.p', 'rb'))
# --num-regions

    results = [0, 0, 0]

    for i in np.arange(1, len(combinations)):
        results = np.vstack((results,
                [i, (res_single_regions['storage_cap' + str(combinations[i][1])] +
                     res_single_regions['storage_cap' + str(combinations[i][2])]),
                     res_combinations['storage_cap' + str(i)]]))

    print('results: ', results)  # results in MWh

    plt.scatter(results[:, 1]/1e3, results[:, 2]/1e3)
    plt.plot([0, 160], [0, 160], 'r-')
    plt.axis([-10, 170, -10, 170])
    plt.xlabel('Storage capacity (single regions summed) in GWh', size=20)
    plt.ylabel('Storage capacity (two regions connected) in GWh', size=20)
    plt.rcParams.update({'font.size': 18})

    plt.show()

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    combinations = calculate_combinations(int(arguments['--num-regions']))
    scatter_plot(combinations)
