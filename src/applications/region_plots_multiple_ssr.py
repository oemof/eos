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
    regions_80 = np.arange(1, 18 + 1)
    i = 1
    combinations_80 = [0, 0, 0]
    for n in itertools.combinations(regions_80, 2):
        combinations_80 = np.vstack((combinations_80, [i, n[0], n[1]]))
        i = i + 1

    # das war mal notwendig, da es mit dem alten Wetterdatensatz (?)
    # mehr Kombinationsmöglichkeiten bei 70 % Autarkie gab
    # regions_70 = np.arange(1, 20 + 1)
    # i = 1
    # combinations_70 = [0, 0, 0]
    # for n in itertools.combinations(regions_70, 2):
    #     combinations_70 = np.vstack((combinations_70, [i, n[0], n[1]]))
    #     i = i + 1

    print('combinations_80: ', combinations_80)
    # print('combinations_70: ', combinations_70)

    # return (combinations_80, combinations_70)
    return combinations_80


# def scatter_plot(combinations_80, combinations_70):
def scatter_plot(combinations_80):

    res_single_regions_80 = pickle.load(open('../results/results_single_regions_80.p', 'rb'))
    res_single_regions_70 = pickle.load(open('../results/results_single_regions_70.p', 'rb'))

    results_70 = [0, 0, 0]
    results_80 = [0, 0, 0]

    for i in np.arange(1, len(combinations_80)):
        res_combinations_80 = pickle.load(open
                ('../results/region_results_dc_region_80_2005_0.80_' + str(i) + '_.p', 'rb'))
        results_80 = np.vstack((results_80,
                [i, (res_single_regions_80['storage_cap' + str(combinations_80[i][1])] +
                     res_single_regions_80['storage_cap' + str(combinations_80[i][2])]),
                     res_combinations_80['storage_cap_' + str(i)]]))
    for i in np.arange(1, len(combinations_80)):
        res_combinations_80 = pickle.load(open
                ('../results/region_results_dc_region_80_2005_0.70_' + str(i) + '_.p', 'rb'))
        results_70 = np.vstack((results_70,
                [i, (res_single_regions_70['storage_cap' + str(combinations_80[i][1])] +
                     res_single_regions_70['storage_cap' + str(combinations_80[i][2])]),
                     res_combinations_80['storage_cap_' + str(i)]]))

    print('results_70: ', results_70)  # results in MWh
    print('results_80: ', results_80)  # results in MWh
    results_70_GWh = results_70/1e3
    results_80_GWh = results_80/1e3

    plt.scatter(results_70_GWh[:, 1], results_70_GWh[:, 2], c='tomato', label='SSR = 70%', edgecolor='none')
    plt.scatter(results_80_GWh[:, 1], results_80_GWh[:, 2], c='blue', label='SSR = 80%', edgecolor='none')
    plt.plot([0, results_80_GWh.max()], [0, results_80_GWh.max()], 'r-')
    plt.axis([-10, results_80_GWh.max()+10, -10, results_80_GWh.max()+10])
    plt.xlabel('Storage capacity (single regions summed) in MWh', size=16)
    plt.ylabel('Storage capacity (both regions connected) in MWh', size=16)
    plt.rcParams.update({'font.size': 18})
    plt.legend(loc='upper left')

    plt.show()

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    combinations_80 = calculate_combinations()
    # [combinations_80, combinations_70] = calculate_combinations()
    scatter_plot(combinations_80)
    # scatter_plot(combinations_80, combinations_70)
