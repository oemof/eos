# -*- coding: utf-8 -*-

''' Plots.

Usage: region_plots.py [options]

Options:

      --region=REG         kreis_steinfurt,
                           landkreis_osnabrueck
                           or total_region. [default: total_region]
      --scenario=SCEN      scenario or path to results
                           [default: 2_szenario_mit_biogas_unflex_ein_speicher]
      --scenario_year=SY   2030, 2050 or both. [default: both]
      --save               Save figure.
'''

###############################################################################
# imports
###############################################################################
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from docopt import docopt

# res = pickle.load(open('../results/households_results_dc_0.7.p', 'rb'))
# pp.pprint(res)


def read_results_storage():

    results_storage_2030 = np.zeros(85).reshape(17, 5)

    for i in np.arange(17):
        results_storage_2030[i][0] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2030' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.70_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_2030[i][1] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2030' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.75_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_2030[i][2] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2030' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.80_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_2030[i][3] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2030' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.85_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_2030[i][4] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2030' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.90_1_.p', 'rb'))['storage_cap_1']

    results_storage_2050 = np.zeros(85).reshape(17, 5)

    for i in np.arange(17):
        results_storage_2050[i][0] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2050' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.70_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_2050[i][1] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2050' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.75_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_2050[i][2] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2050' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.80_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_2050[i][3] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2050' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.85_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_2050[i][4] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                                '2_szenario_mit_biogas_unflex_ein_speicher/' +
                                                'region_results_dc' + '_' +
                                                str(arguments['--region']) + '_' +
                                                '2050' + '_' +
                                                str(i + 1998) + '_' +
                                                '0.90_1_.p', 'rb'))['storage_cap_1']
# costopt

    results_storage_costopt = np.zeros(85).reshape(17, 5)

    for i in np.arange(17):
        results_storage_costopt[i][0] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.70_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_costopt[i][1] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.75_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_costopt[i][2] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.80_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_costopt[i][3] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.85_1_.p', 'rb'))['storage_cap_1']

    for i in np.arange(17):
        results_storage_costopt[i][4] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.90_1_.p', 'rb'))['storage_cap_1']

    results_storage_2030_GWh = results_storage_2030 / 1e6
    results_storage_2050_GWh = results_storage_2050 / 1e6
    results_storage_costopt_GWh = results_storage_costopt / 1e6

    results_storage_GWh = {'2030': results_storage_2030_GWh,
                           '2050': results_storage_2050_GWh,
                           'costopt': results_storage_costopt_GWh}

    return results_storage_GWh


def read_results_wind_pv():

# costopt

    results_wind_costopt = np.zeros(85).reshape(17, 5)
    results_pv_costopt = np.zeros(85).reshape(17, 5)

# wind
    for i in np.arange(17):
        results_wind_costopt[i][0] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.70_1_.p', 'rb'))['wind_inst_1']

    for i in np.arange(17):
        results_wind_costopt[i][1] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.75_1_.p', 'rb'))['wind_inst_1']

    for i in np.arange(17):
        results_wind_costopt[i][2] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.80_1_.p', 'rb'))['wind_inst_1']

    for i in np.arange(17):
        results_wind_costopt[i][3] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.85_1_.p', 'rb'))['wind_inst_1']

    for i in np.arange(17):
        results_wind_costopt[i][4] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.90_1_.p', 'rb'))['wind_inst_1']

# pv
    for i in np.arange(17):
        results_pv_costopt[i][0] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.70_1_.p', 'rb'))['pv_inst_1']

    for i in np.arange(17):
        results_pv_costopt[i][1] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.75_1_.p', 'rb'))['pv_inst_1']

    for i in np.arange(17):
        results_pv_costopt[i][2] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.80_1_.p', 'rb'))['pv_inst_1']

    for i in np.arange(17):
        results_pv_costopt[i][3] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.85_1_.p', 'rb'))['pv_inst_1']

    for i in np.arange(17):
        results_pv_costopt[i][4] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                            '6_v2_costopt_mit_biogas_costopt_ein_speicher/' +
                                            'region_results_dc' + '_' +
                                            str(arguments['--region']) + '_' +
                                            str(arguments['--scenario_year']) + '_' +
                                            str(i + 1998) + '_' +
                                            '0.90_1_.p', 'rb'))['pv_inst_1']

    results_wind_costopt_MW = results_wind_costopt / 1e3
    results_pv_costopt_MW = results_pv_costopt / 1e3

    results_wind_pv_MW = {'wind': results_wind_costopt_MW,
                          'pv': results_pv_costopt_MW}

    return results_wind_pv_MW


def read_results_excess_grid():

    if arguments['--scenario_year']:

        results_excess = np.zeros(85).reshape(17, 5)
        results_grid = np.zeros(85).reshape(17, 5)
        results_grid_max = np.zeros(85).reshape(17, 5)

        for i in np.arange(17):
            results_excess[i][0] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.70_1_.p', 'rb'))['excess_1']

            results_grid[i][0] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.70_1_.p', 'rb'))['grid_1']

            results_grid_max[i][0] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.70_1_.p', 'rb'))['grid_ts_1'].max()

        for i in np.arange(17):
            results_excess[i][1] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.75_1_.p', 'rb'))['excess_1']

            results_grid[i][1] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.75_1_.p', 'rb'))['grid_1']

            results_grid_max[i][1] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.75_1_.p', 'rb'))['grid_ts_1'].max()

        for i in np.arange(17):
            results_excess[i][2] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.80_1_.p', 'rb'))['excess_1']

            results_grid[i][2] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.80_1_.p', 'rb'))['grid_1']

            results_grid_max[i][2] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.80_1_.p', 'rb'))['grid_ts_1'].max()

        for i in np.arange(17):
            results_excess[i][3] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.85_1_.p', 'rb'))['excess_1']

            results_grid[i][3] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.85_1_.p', 'rb'))['grid_1']

            results_grid_max[i][3] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.85_1_.p', 'rb'))['grid_ts_1'].max()

        for i in np.arange(17):
            results_excess[i][4] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.90_1_.p', 'rb'))['excess_1']

            results_grid[i][4] = pickle.load(open('../results/1_EIN_SPEICHER/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.90_1_.p', 'rb'))['grid_1']

            results_grid_max[i][4] = pickle.load(open('../results/1_EIN_SPEICHER/' +
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

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                      results_storage['2030'][0][:],
                      linestyle='',
                      marker='o',
                      markersize=16,
                      markeredgecolor='goldenrod',
                      markeredgewidth=3,
                      markerfacecolor='None',
                      label='2030')
    colors.append(plt.getp(line,'markeredgecolor'))

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                      results_storage['2050'][0][:],
                      linestyle='',
                      marker='o',
                      markersize=16,
                      markeredgecolor='darkblue',
                      markeredgewidth=3,
                      markerfacecolor='None',
                      label='2050')
    colors.append(plt.getp(line,'markeredgecolor'))

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                      results_storage['costopt'][0][:],
                      linestyle='',
                      marker='o',
                      markersize=16,
                      markeredgecolor=main_color,
                      markeredgewidth=3,
                      markerfacecolor='None',
                      label='Kostenoptimum')
    colors.append(plt.getp(line,'markeredgecolor'))

    leg = plt.legend(loc='upper left', frameon=False, prop={'size': 28})
    leg._legend_box.align = 'left'
    # leg.set_title('Masterplanregion', prop={'size': 28})
    for color,text in zip(colors,leg.get_texts()):
      # for text in leg.get_texts():
            text.set_color(color)

    for i in np.arange(16):
        line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                         results_storage['2030'][i+1][:],
                         linestyle='',
                         marker='o',
                         markersize=16,
                         markeredgecolor='goldenrod',
                         markeredgewidth=3,
                         markerfacecolor='None')

        line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                         results_storage['2050'][i+1][:],
                         linestyle='',
                         marker='o',
                         markersize=16,
                         markeredgecolor='darkblue',
                         markeredgewidth=3,
                         markerfacecolor='None')

        line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                         results_storage['costopt'][i+1][:],
                         linestyle='',
                         marker='o',
                         markersize=16,
                         markeredgecolor=main_color,
                         markeredgewidth=3,
                         markerfacecolor='None')

    plt.xlim([0.68, 0.92])
    # plt.ylim([0, 11])
    # plt.ylim([0, 21])

    plt.xticks([0.70, 0.75, 0.80, 0.85, 0.90])
    ax.set_xticklabels(['0,70', '0,75', '0,80', '0,85', '0,90'], fontsize=28, color=diagram_color)
    plt.yticks([0, 10, 20, 30, 40], fontsize=28, color=diagram_color)
    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    plt.ylabel('Speicherkapazität in GWh', fontsize=28, color=diagram_color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.show()

    return fig


def dot_plot_wind_pv(results_wind_pv):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                      results_wind_pv['wind'][0][:],
                      linestyle='',
                      marker='o',
                      markersize=16,
                      markeredgecolor='#558ed5',
                      markeredgewidth=3,
                      markerfacecolor='None',
                      label='Windenergie')
    colors.append(plt.getp(line,'markeredgecolor'))

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                      results_wind_pv['pv'][0][:],
                      linestyle='',
                      marker='o',
                      markersize=16,
                      markeredgecolor='#ffc000',
                      markeredgewidth=3,
                      markerfacecolor='None',
                      label='Photovoltaik')
    colors.append(plt.getp(line,'markeredgecolor'))

    leg = plt.legend(loc='upper left', frameon=False, prop={'size': 28})
    leg._legend_box.align = 'left'
    # leg.set_title('Masterplanregion', prop={'size': 28})
    for color,text in zip(colors,leg.get_texts()):
      # for text in leg.get_texts():
            text.set_color(color)

    for i in np.arange(16):
        line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                         results_wind_pv['wind'][i+1][:],
                         linestyle='',
                         marker='o',
                         markersize=16,
                         markeredgecolor='#558ed5',
                         markeredgewidth=3,
                         markerfacecolor='None')

        line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                         results_wind_pv['pv'][i+1][:],
                         linestyle='',
                         marker='o',
                         markersize=16,
                         markeredgecolor='#ffc000',
                         markeredgewidth=3,
                         markerfacecolor='None')

    plt.xlim([0.68, 0.92])
    # plt.ylim([0, 11])
    # plt.ylim([0, 21])

    plt.xticks([0.70, 0.75, 0.80, 0.85, 0.90])
    ax.set_xticklabels(['0,70', '0,75', '0,80', '0,85', '0,90'], fontsize=28, color=diagram_color)
    # plt.yticks([0, 10, 20, 30, 40], fontsize=28, color=diagram_color)
    plt.yticks([0, 1000, 2000, 3000, 4000, 5000], fontsize=28, color=diagram_color)
    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    # plt.ylabel('Speicherkapazität in GWh', fontsize=28, color=diagram_color)
    plt.ylabel('Installierte Leistung in MW', fontsize=28, color=diagram_color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.show()

    return fig


def hist_plot_wind_pv(results_wind_pv):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

    df_wind_80 = pd.DataFrame(columns=['wind_80'])
    df_wind_90 = pd.DataFrame(columns=['wind_90'])
    df_pv_80 = pd.DataFrame(columns=['pv_80'])
    df_pv_90 = pd.DataFrame(columns=['pv_90'])

    for i in np.arange(17):
        df_wind_80 = df_wind_80.append({'wind_80': results_wind_pv['wind'][i][2]}, ignore_index=True)

    for i in np.arange(17):
        df_wind_90 = df_wind_90.append({'wind_90': results_wind_pv['wind'][i][4]}, ignore_index=True)

    for i in np.arange(17):
        df_pv_80 = df_pv_80.append({'pv_80': results_wind_pv['pv'][i][2]}, ignore_index=True)

    for i in np.arange(17):
        df_pv_90 = df_pv_90.append({'pv_90': results_wind_pv['pv'][i][4]}, ignore_index=True)

    df_wind_80.hist(bins=[0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000])
    df_wind_90.hist(bins=[0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000])
    df_pv_80.hist(bins=[0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000])
    df_pv_90.hist(bins=[0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000])

#########################################################
    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.show()
#########################################################

    return fig

def dot_plot_excess_and_grid_energy(results_excess, results_grid):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                      results_excess[0][:],
                      linestyle='',
                      marker='o',
                      markersize=16,
                      markeredgecolor=main_color,
                      markeredgewidth=3,
                      markerfacecolor='None',
                      label='Überschuss')
    colors.append(plt.getp(line,'markeredgecolor'))

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                      results_grid[0][:],
                      linestyle='',
                      marker='o',
                      markersize=16,
                      markeredgecolor='#FF5050',
                      markeredgewidth=3,
                      markerfacecolor='None',
                      label='Import')
    colors.append(plt.getp(line,'markeredgecolor'))

    leg = plt.legend(loc='upper left', frameon=False, prop={'size': 28})
    leg._legend_box.align = 'left'
    # leg.set_title('Masterplanregion', prop={'size': 28})
    for color,text in zip(colors,leg.get_texts()):
      # for text in leg.get_texts():
            text.set_color(color)

    for i in np.arange(16):
        line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                         results_excess[i+1][:],
                         linestyle='',
                         marker='o',
                         markersize=16,
                         markeredgecolor=main_color,
                         markeredgewidth=3,
                         markerfacecolor='None')

        line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                         results_grid[i+1][:],
                         linestyle='',
                         marker='o',
                         markersize=16,
                         markeredgecolor='#FF5050',
                         markeredgewidth=3,
                         markerfacecolor='None')

    plt.xlim([0.68, 0.92])
    # plt.ylim([0, 11])
    # plt.ylim([0, 21])

    plt.xticks([0.70, 0.75, 0.80, 0.85, 0.90])
    ax.set_xticklabels(['0,70', '0,75', '0,80', '0,85', '0,90'], fontsize=28, color=diagram_color)
    # plt.yticks([0, 10, 20, 30, 40], fontsize=28, color=diagram_color)
    plt.yticks([0, 2000, 4000, 6000, 8000, 10000], fontsize=28, color=diagram_color)
    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    # plt.ylabel('Speicherkapazität in GWh', fontsize=28, color=diagram_color)
    plt.ylabel('Überschuss- und Importenergie in GWh', fontsize=28, color=diagram_color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.show()

    return fig


def dot_plot_grid_power(results_grid_max):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                      results_grid_max[0][:],
                      linestyle='',
                      marker='o',
                      markersize=16,
                      markeredgecolor='#FF5050',
                      markeredgewidth=3,
                      markerfacecolor='None',
                      label='Max. Importleistung')
    colors.append(plt.getp(line,'markeredgecolor'))

    # leg = plt.legend(loc='upper left', frameon=False, prop={'size': 28})
    # leg._legend_box.align = 'left'
    # # leg.set_title('Masterplanregion', prop={'size': 28})
    # for color,text in zip(colors,leg.get_texts()):
    #   # for text in leg.get_texts():
    #         text.set_color(color)

    for i in np.arange(16):
        line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                         results_grid_max[i+1][:],
                         linestyle='',
                         marker='o',
                         markersize=16,
                         markeredgecolor='#FF5050',
                         markeredgewidth=3,
                         markerfacecolor='None')

    plt.xlim([0.68, 0.92])
    plt.ylim([500, 850])

    plt.xticks([0.70, 0.75, 0.80, 0.85, 0.90])
    ax.set_xticklabels(['0,70', '0,75', '0,80', '0,85', '0,90'], fontsize=28, color=diagram_color)
    plt.yticks([500, 600, 700, 800], fontsize=28, color=diagram_color)
    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    # plt.ylabel('Speicherkapazität in GWh', fontsize=28, color=diagram_color)
    plt.ylabel('Max. Importleistung in MW', fontsize=28, color=diagram_color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.show()

    return fig


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    # results_storage = read_results_storage()
    (results_excess, results_grid, results_grid_max) = read_results_excess_grid()
    # results_wind_pv = read_results_wind_pv()
    # fig = dot_plot_storage(results_storage)
    # fig = dot_plot_excess_and_grid_energy(results_excess, results_grid)
    fig = dot_plot_grid_power(results_grid_max)
    # fig = dot_plot_wind_pv(results_wind_pv)
    # fig = hist_plot_wind_pv(results_wind_pv)

    # df_storage_2030_80 = pd.DataFrame(columns=['storage_2030_80'])
    # df_storage_2030_90 = pd.DataFrame(columns=['storage_2030_90'])

    # df_storage_2050_80 = pd.DataFrame(columns=['storage_2050_80'])
    # df_storage_2050_90 = pd.DataFrame(columns=['storage_2050_90'])

    # df_storage_ko_80 = pd.DataFrame(columns=['storage_ko_80'])
    # df_storage_ko_90 = pd.DataFrame(columns=['storage_ko_90'])

    # for i in np.arange(17):
    #     df_storage_2030_80 = df_storage_2030_80.append({'storage_2030_80': results_storage['2030'][i][2]}, ignore_index=True)

    # for i in np.arange(17):
    #     df_storage_2030_90 = df_storage_2030_90.append({'storage_2030_90': results_storage['2030'][i][4]}, ignore_index=True)

    # for i in np.arange(17):
    #     df_storage_2050_80 = df_storage_2050_80.append({'storage_2050_80': results_storage['2050'][i][2]}, ignore_index=True)

    # for i in np.arange(17):
    #     df_storage_2050_90 = df_storage_2050_90.append({'storage_2050_90': results_storage['2050'][i][4]}, ignore_index=True)

    # for i in np.arange(17):
    #     df_storage_ko_80 = df_storage_ko_80.append({'storage_ko_80': results_storage['costopt'][i][2]}, ignore_index=True)

    # for i in np.arange(17):
    #     df_storage_ko_90 = df_storage_ko_90.append({'storage_ko_90': results_storage['costopt'][i][4]}, ignore_index=True)

    # dataframe = df_storage_2050_90

    # print(dataframe)
    # print('mean', dataframe.mean(0))
    # # print('std', dataframe.std(0))
    # print('min', dataframe.min(0))
    # # print('quantile_25', dataframe.quantile(0.25))
    # print('median', dataframe.median(0))
    # # print('quantile_75', dataframe.quantile(0.75))
    # print('max', dataframe.max(0))

    if arguments['--save']:
        fig.savefig(os.path.join(os.path.dirname(__file__)) +
                'current_figure' +
                '.pdf')
