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


def calculate_combinations():
    regions_85 = np.arange(1, 18 + 1)
    i = 1
    combinations_85 = [0, 0, 0]
    for n in itertools.combinations(regions_85, 2):
        combinations_85 = np.vstack((combinations_85, [i, n[0], n[1]]))
        i = i + 1

    regions_70 = np.arange(1, 20 + 1)
    i = 1
    combinations_70 = [0, 0, 0]
    for n in itertools.combinations(regions_70, 2):
        combinations_70 = np.vstack((combinations_70, [i, n[0], n[1]]))
        i = i + 1

    print('combinations_85: ', combinations_85)
    print('combinations_70: ', combinations_70)

    return (combinations_85, combinations_70)


def scatter_plot(combinations_85, combinations_70):

    res_single_regions_85 = pickle.load(open('../results/results_single_regions_85.p', 'rb'))
    res_single_regions_70 = pickle.load(open('../results/results_single_regions_70.p', 'rb'))

    results_70 = [0, 0, 0]
    results_85 = [0, 0, 0]

    for i in np.arange(1, len(combinations_85)):
        res_combinations_85 = pickle.load(open
                ('../results/region_results_dc_0.85_' + str(i) + '_.p', 'rb'))
        results_85 = np.vstack((results_85,
                [i, (res_single_regions_85['storage_cap' + str(combinations_85[i][1])] +
                     res_single_regions_85['storage_cap' + str(combinations_85[i][2])]),
                     res_combinations_85['storage_cap' + str(i)]]))
    for i in np.arange(1, len(combinations_70)):
        res_combinations_70 = pickle.load(open
                ('../results/region_results_dc_0.70_' + str(i) + '_.p', 'rb'))
        results_70 = np.vstack((results_70,
                [i, (res_single_regions_70['storage_cap' + str(combinations_70[i][1])] +
                     res_single_regions_70['storage_cap' + str(combinations_70[i][2])]),
                     res_combinations_70['storage_cap' + str(i)]]))

    print('results_70: ', results_70)  # results in MWh
    print('results_85: ', results_85)  # results in MWh
    results_70_GWh = results_70/1e3
    results_85_GWh = results_85/1e3

    plt.scatter(results_70_GWh[:, 1], results_70_GWh[:, 2], c='tomato', label='SSR = 70%', edgecolor='none')
    plt.scatter(results_85_GWh[:, 1], results_85_GWh[:, 2], c='blue', label='SSR = 85%', edgecolor='none')
    plt.plot([0, results_85_GWh.max()], [0, results_85_GWh.max()], 'r-')
    plt.axis([-10, results_85_GWh.max()+10, -10, results_85_GWh.max()+10])
    plt.xlabel('Storage capacity (single regions summed) in MWh', size=16)
    plt.ylabel('Storage capacity (both regions connected) in MWh', size=16)
    plt.rcParams.update({'font.size': 18})
    plt.legend(loc='upper left')

    plt.show()

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    [combinations_85, combinations_70] = calculate_combinations()
    scatter_plot(combinations_85, combinations_70)
