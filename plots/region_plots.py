# -*- coding: utf-8 -*-

''' Plots.
'''

###############################################################################
# imports
###############################################################################
import pickle
import pprint as pp
import itertools
import numpy as np
import matplotlib.pyplot as plt

# res = pickle.load(open('../results/households_results_dc_0.7.p', 'rb'))
# pp.pprint(res)

regions = np.arange(1, 18 + 1)
i = 1
combinations = [0, 0, 0]
for n in itertools.combinations(regions, 2):
    combinations = np.vstack((combinations, [i, n[0], n[1]]))
    i = i + 1

print(combinations)


def scatter_plot(combinations):

    res_single_regions = pickle.load(open('../results/results_single_regions.p', 'rb'))
    res_combinations = pickle.load(open('../results/results_combinations.p', 'rb'))

    results = [0, 0, 0]

    for i in np.arange(1, 7):
        results = np.vstack((results,
                [i, (res_single_regions['storage_cap' + str(combinations[i][1])] +
                     res_single_regions['storage_cap' + str(combinations[i][2])]),
                     res_combinations['storage_cap' + str(i)]]))

    print(results)

    plt.scatter(results[:, 1], results[:, 2])
    plt.show()


if __name__ == '__main__':
    scatter_plot(combinations)
