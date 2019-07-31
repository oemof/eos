# -*- coding: utf-8 -*-

''' Plots.

Usage: region_plots.py [options]

Options:

      --num-regions=NUM    Number of regions. [default: 24]
      --save               Save figure.
'''

###############################################################################
# imports
###############################################################################
import pickle
import pprint as pp
import itertools
import numpy as np
import matplotlib.pyplot as plt
import os
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

    # print('combinations: ', combinations)

    return combinations


def scatter_plot(combinations):

    res_single_regions = pickle.load(open('../results/REGION_COMMUNE_MULTI/mit_biogas_unflex/results_single_regions_0.80.p', 'rb'))
    print(res_single_regions['storage_cap_18'])

    results = [0, 0, 0]

    for i in np.arange(1, len(combinations)):
        res_combinations = pickle.load(open
                ('../results/REGION_COMMUNE_MULTI/mit_biogas_unflex/region_results_dc_region_80_2005_0.80_' + str(i) + '_.p', 'rb'))
        results = np.vstack((results,
                [i, (res_single_regions['storage_cap_' + str(combinations[i][1])] +
                     res_single_regions['storage_cap_' + str(combinations[i][2])]),
                     res_combinations['storage_cap_' + str(i)]]))

    print('results: ', results)  # results in MWh
    results_MWh = results/1e3

#################################################################
    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

    plt.scatter(results_MWh[:, 1], results_MWh[:, 2])
    plt.plot([0, results_MWh.max()], [0, results_MWh.max()], 'r-')
    plt.axis([-10, results_MWh.max()+10, -10, results_MWh.max()+10])
    plt.xlabel('Speicherkapazität in MWh \n (Summe 2 Teilregionen)', size=28, color=diagram_color)
    plt.ylabel('Speicherkapazität in MWh \n (Vernetzung 2 Teilregionen)', size=28, color=diagram_color)
    plt.rcParams.update({'font.size': 18})

    plt.xticks([0, 20, 40, 60, 80, 100, 120], fontsize=28, color=diagram_color)
    plt.yticks([0, 20, 40, 60, 80, 100, 120], fontsize=28, color=diagram_color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.show()

    return fig

#################################################################


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    combinations = calculate_combinations(int(arguments['--num-regions']))
    fig = scatter_plot(combinations)

    if arguments['--save']:
        fig.savefig(os.path.join(os.path.dirname(__file__)) +
                'current_figure' +
                '.pdf')
