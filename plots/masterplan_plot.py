# -*- coding: utf-8 -*-

''' Plots.

Usage: region_plots.py [options]

Options:

      --region=REG         kreis_steinfurt,
                           landkreis_osnabrueck
                           or total_region. [default: total_region]
      --scenario=SCEN      scenario or path to results
                           [default: masterplan_results_mit_biogas_unflex]
      --scenario_year=SY   2030, 2050 or both. [default: both]
      --save               Save figure.
'''

###############################################################################
# imports
###############################################################################
import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
from docopt import docopt

# res = pickle.load(open('../results/households_results_dc_0.7.p', 'rb'))
# pp.pprint(res)


def read_results_storage():

    if arguments['--scenario_year'] == 'both':

        results_storage_2030 = np.zeros(85).reshape(17, 5)

        for i in np.arange(17):
            results_storage_2030[i][0] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.70_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage_2030[i][1] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.75_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage_2030[i][2] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.80_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage_2030[i][3] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.85_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage_2030[i][4] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.90_1_.p', 'rb'))['storage_cap_1']

        results_storage_2050 = np.zeros(85).reshape(17, 5)

        for i in np.arange(17):
            results_storage_2050[i][0] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.70_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage_2050[i][1] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.75_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage_2050[i][2] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.80_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage_2050[i][3] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.85_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage_2050[i][4] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.90_1_.p', 'rb'))['storage_cap_1']

        results_storage_2030_GWh = results_storage_2030 / 1e6
        results_storage_2050_GWh = results_storage_2050 / 1e6

        results_storage_GWh = {'2030': results_storage_2030_GWh,
                              '2050': results_storage_2050_GWh}

    else:
        results_storage = np.zeros(85).reshape(17, 5)
        for i in np.arange(17):
            results_storage[i][0] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.70_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage[i][1] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.75_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage[i][2] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.80_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage[i][3] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.85_1_.p', 'rb'))['storage_cap_1']

        for i in np.arange(17):
            results_storage[i][4] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.90_1_.p', 'rb'))['storage_cap_1']

        results_storage_GWh = results_storage / 1e6

    return results_storage_GWh


def read_results_excess_grid():

    if arguments['--scenario_year']:

        results_excess = np.zeros(85).reshape(17, 5)
        results_grid = np.zeros(85).reshape(17, 5)
        results_grid_max = np.zeros(85).reshape(17, 5)

        for i in np.arange(17):
            results_excess[i][0] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.70_1_.p', 'rb'))['excess_1']

            results_grid[i][0] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.70_1_.p', 'rb'))['grid_1']

            results_grid_max[i][0] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.70_1_.p', 'rb'))['grid_ts_1'].max()

        for i in np.arange(17):
            results_excess[i][1] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.75_1_.p', 'rb'))['excess_1']

            results_grid[i][1] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.75_1_.p', 'rb'))['grid_1']

            results_grid_max[i][1] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.75_1_.p', 'rb'))['grid_ts_1'].max()

        for i in np.arange(17):
            results_excess[i][2] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.80_1_.p', 'rb'))['excess_1']

            results_grid[i][2] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.80_1_.p', 'rb'))['grid_1']

            results_grid_max[i][2] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.80_1_.p', 'rb'))['grid_ts_1'].max()

        for i in np.arange(17):
            results_excess[i][3] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.85_1_.p', 'rb'))['excess_1']

            results_grid[i][3] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.85_1_.p', 'rb'))['grid_1']

            results_grid_max[i][3] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.85_1_.p', 'rb'))['grid_ts_1'].max()

        for i in np.arange(17):
            results_excess[i][4] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.90_1_.p', 'rb'))['excess_1']

            results_grid[i][4] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.90_1_.p', 'rb'))['grid_1']

            results_grid_max[i][4] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.90_1_.p', 'rb'))['grid_ts_1'].max()

        results_excess_GWh = results_excess / 1e6
        results_grid_GWh = results_grid / 1e6
        results_grid_max_MW = results_grid_max / 1e3

    # print(results_excess_GWh)
    # print(results_grid_GWh)

    return (results_excess_GWh, results_grid_GWh, results_grid_max_MW)


def dot_plot_storage(results_storage):

    if arguments['--scenario_year'] == 'both':

        for i in np.arange(17):
            fig = plt.figure(1)
            plt.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                    results_storage['2030'][i][:], 'ro')
            plt.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                    results_storage['2050'][i][:], 'bo')
        plt.axis([0.68, 0.92,
            results_storage['2030'].min(), results_storage['2030'].max() + 1])
        plt.legend(['2030', '2050'], loc='upper left', prop={'size': 18})

    else:
        for i in np.arange(17):
            fig = plt.figure(1)
            plt.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                    results_storage[i][:], 'ro')
        plt.axis([0.68, 0.92, results_storage.min(), results_storage.max() + 1])

    plt.yticks([0, 10, 20, 30, 40])
    plt.xlabel('Self-sufficiency degree', size=18)
    plt.ylabel('Storage capacity in GWh', size=18)
    plt.rcParams.update({'font.size': 18})
    plt.tight_layout()

    plt.show()

    return fig


def dot_plot_excess_and_grid_energy(results_excess, results_grid):

    for i in np.arange(17):
        fig = plt.figure(1)
        plt.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                results_excess[i][:], 'bo')
        plt.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                results_grid[i][:], 'ro')
    # plt.axis([0.68, 0.92,
        # results_excess.min(), results_excess.max() + 1])
    plt.legend(['Excess', 'Import'], loc='upper left', prop={'size': 18})

    plt.yticks([0, 2000, 4000, 6000, 8000, 10000])
    plt.xlabel('Self-sufficiency degree', size=18)
    plt.ylabel('Excess and import energy in GWh', size=18)
    plt.rcParams.update({'font.size': 18})
    plt.tight_layout()

    plt.show()

    return fig


def dot_plot_grid_power(results_grid_max):

    for i in np.arange(17):
        fig = plt.figure(1)
        plt.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                results_grid_max[i][:], 'ro')
    # plt.axis([0.68, 0.92,
        # results_excess.min(), results_excess.max() + 1])
    # plt.legend(['Importleistung'], loc='upper left', prop={'size': 18})

    # plt.ylim([500, 850])
    # plt.yticks([500, 600, 700, 800])
    plt.ylim([0, 38000])
    plt.yticks([0, 10000, 20000, 30000])
    plt.xlabel('Self-sufficiency degree', size=18)
    plt.ylabel('Max. Importleistung in MW', size=18)
    plt.rcParams.update({'font.size': 18})
    plt.tight_layout()

    plt.show()

    return fig


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    results_storage = read_results_storage()
    (results_excess, results_grid, results_grid_max) = read_results_excess_grid()
    fig_1 = dot_plot_storage(results_storage)
    fig_2 = dot_plot_excess_and_grid_energy(results_excess, results_grid)
    fig_3 = dot_plot_grid_power(results_grid_max)

    if arguments['--save']:
        fig_3.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures') +
                '/' + 'current_figure' +
                '.png')
