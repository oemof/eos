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
      --ssr=SSR            Self-sufficiency degree for capacities plot.
      --biogas-costopt     Plot also biogas installed capacity.
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

    # weather_years = np.array(np.mat('1 1998; 2 1999; 3 2000; 4 2001; 5 2002;
    #                                  6 2003; 7 2004; 8 2005; 9 2006; 10 2007;
    #                                  11 2008; 12 2009; 13 2010; 14 2011;
    #                                  15 2012; 16 2013; 17 2014'))

    if arguments['--scenario_year']:

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

            print(pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.90_1_.p', 'rb'))['storage_cap_1'])

        results_storage_GWh = results_storage / 1e6

    return results_storage_GWh

def read_results_capacities():

    if arguments['--biogas-costopt']:

        results_capacities = np.zeros(51).reshape(3, 17)

        for i in np.arange(17):
            results_capacities[0][i] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               # str(arguments['--ssr']) +
                                               # '_1_.p', 'rb'))['wind_inst_1']
                                               '1_.p', 'rb'))['wind_inst_1']
        for i in np.arange(17):
            results_capacities[1][i] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               # str(arguments['--ssr']) +
                                               # '_1_.p', 'rb'))['pv_inst_1']
                                               '1_.p', 'rb'))['pv_inst_1']
        for i in np.arange(17):
            results_capacities[2][i] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               #str(arguments['--ssr']) +
                                               #'_1_.p', 'rb'))['biogas_bhkw_inst_1']
                                               '1_.p', 'rb'))['biogas_bhkw_inst_1']

        results_capacities_MW = results_capacities / 1e3

    else:

        results_capacities = np.zeros(34).reshape(2, 17)

        for i in np.arange(17):
            results_capacities[0][i] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               # str(arguments['--ssr']) +
                                               # '_1_.p', 'rb'))['wind_inst_1']
                                               '1_.p', 'rb'))['wind_inst_1']
        for i in np.arange(17):
            results_capacities[1][i] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               # str(arguments['--ssr']) +
                                               # '_1_.p', 'rb'))['pv_inst_1']
                                               '1_.p', 'rb'))['pv_inst_1']

        results_capacities_MW = results_capacities / 1e3

    return results_capacities_MW

def read_results_storage_and_capacities():
    return results_storage_GWh_and_capacities_MW


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


def dot_plot(results_storage):

    for i in np.arange(17):
        fig = plt.figure(1)
        plt.plot([0.70, 0.75, 0.80, 0.85, 0.90], results_storage[i][:], 'ro')
    plt.axis([0.68, 0.92, results_storage.min(), results_storage.max() + 1])
    # plt.yticks([0, 10, 20, 30, 40])
    plt.xticks([0.70, 0.75, 0.80, 0.85, 0.90])
    plt.xlabel('Self-sufficiency degree', size=18)
    plt.ylabel('Storage capacity in GWh', size=18)
    plt.rcParams.update({'font.size': 18})
    plt.tight_layout()

    plt.show()

    return fig

def bar_plot(results_capacities):

    fig = plt.figure(1)

    if arguments['--biogas-costopt']:

        ind = np.arange(17)
        p1 = plt.bar(ind, results_capacities[0,:],
                color='blue')
        p2 = plt.bar(ind, results_capacities[1,:],
                bottom=results_capacities[0,:],
                color='yellow')
        p3 = plt.bar(ind, results_capacities[2,:],
                bottom=results_capacities[0,:] + results_capacities[1,:],
                color='green')
        plt.ylim([0, 5100])
        plt.xlabel('Weather year', size=18)
        plt.ylabel('Installed capacities in MW', size=18)
        plt.xticks(ind, ['1998', '1999', '2000', '2001', '2002', '2003', '2004',
                         '2005', '2006', '2007', '2008', '2009', '2010', '2011',
                         '2012', '2013', '2014'])
        plt.legend((p1[0], p2[0], p3[0]), ('Windenergie', 'Photovoltaik', 'Biogas-BHKW'),
                    loc='upper left', prop={'size': 18})
        plt.rcParams.update({'font.size': 18})
        plt.tight_layout()

    else:

        ind = np.arange(17)
        p1 = plt.bar(ind, results_capacities[0,:], color='blue')
        p2 = plt.bar(ind, results_capacities[1,:], bottom=results_capacities[0,:], color='yellow')
        plt.ylim([0, 5100])
        plt.xlabel('Weather year', size=18)
        plt.ylabel('Installed capacities in MW', size=18)
        plt.xticks(ind, ['1998', '1999', '2000', '2001', '2002', '2003', '2004',
                         '2005', '2006', '2007', '2008', '2009', '2010', '2011',
                         '2012', '2013', '2014'])
        plt.legend((p1[0], p2[0]), ('Windenergie', 'Photovoltaik'),
                    loc='upper left', prop={'size': 18})
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

    plt.ylim([500, 850])
    plt.yticks([500, 600, 700, 800])
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
    results_capacities = read_results_capacities()
    (results_excess, results_grid, results_grid_max) = read_results_excess_grid()
    # fig_1 = dot_plot(results_storage)
    fig_2 = bar_plot(results_capacities)
    # fig_3 = dot_plot_excess_and_grid_energy(results_excess, results_grid)
    # fig_4 = dot_plot_grid_power(results_grid_max)

    if arguments['--save']:
        fig_2.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures') +
                '/' + 'current_figure' +
                '.png')
