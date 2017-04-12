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


def read_results():

    # weather_years = np.array(np.mat('1 1998; 2 1999; 3 2000; 4 2001; 5 2002;
    #                                  6 2003; 7 2004; 8 2005; 9 2006; 10 2007;
    #                                  11 2008; 12 2009; 13 2010; 14 2011;
    #                                  15 2012; 16 2013; 17 2014'))

    if arguments['--scenario_year'] == 'both':

        results_region_2030 = np.zeros(85).reshape(17, 5)

        for i in np.arange(17):
            results_region_2030[i][0] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.70_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region_2030[i][1] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.75_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region_2030[i][2] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.80_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region_2030[i][3] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.85_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region_2030[i][4] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2030' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.90_1_.p', 'rb'))['storage_cap1']

        results_region_2050 = np.zeros(85).reshape(17, 5)

        for i in np.arange(17):
            results_region_2050[i][0] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.70_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region_2050[i][1] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.75_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region_2050[i][2] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.80_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region_2050[i][3] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.85_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region_2050[i][4] = pickle.load(open('../results/' +
                                                    str(arguments['--scenario']) + '/' +
                                                    'region_results_dc' + '_' +
                                                    str(arguments['--region']) + '_' +
                                                    '2050' + '_' +
                                                    str(i + 1998) + '_' +
                                                    '0.90_1_.p', 'rb'))['storage_cap1']

        results_region_2030_GWh = results_region_2030 / 1e6
        results_region_2050_GWh = results_region_2050 / 1e6

        results_region_GWh = {'2030': results_region_2030_GWh,
                              '2050': results_region_2050_GWh}

    else:
        results_region = np.zeros(85).reshape(17, 5)
        for i in np.arange(17):
            results_region[i][0] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.70_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region[i][1] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.75_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region[i][2] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.80_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region[i][3] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.85_1_.p', 'rb'))['storage_cap1']

        for i in np.arange(17):
            results_region[i][4] = pickle.load(open('../results/' +
                                               str(arguments['--scenario']) + '/' +
                                               'region_results_dc' + '_' +
                                               str(arguments['--region']) + '_' +
                                               str(arguments['--scenario_year']) + '_' +
                                               str(i + 1998) + '_' +
                                               '0.90_1_.p', 'rb'))['storage_cap1']

        results_region_GWh = results_region / 1e6

    print(results_region_GWh)

    return results_region_GWh

def dot_plot(results):

    if arguments['--scenario_year'] == 'both':

        for i in np.arange(17):
            fig = plt.figure(1)
            plt.plot([0.70, 0.75, 0.80, 0.85, 0.90], results['2030'][i][:], 'ro')
            plt.plot([0.70, 0.75, 0.80, 0.85, 0.90], results['2050'][i][:], 'bo')
        plt.axis([0.68, 0.92, results['2030'].min(), results['2030'].max() + 1])
        plt.legend(['2030', '2050'], loc='upper left', prop={'size': 18})

    else:
        for i in np.arange(17):
            fig = plt.figure(1)
            plt.plot([0.70, 0.75, 0.80, 0.85, 0.90], results[i][:], 'ro')
        plt.axis([0.68, 0.92, results.min(), results.max() + 1])

    plt.yticks([0, 10, 20, 30, 40])
    plt.xlabel('Self-sufficiency degree', size=18)
    plt.ylabel('Storage capacity in GWh', size=18)
    plt.rcParams.update({'font.size': 18})
    plt.tight_layout()

    plt.show()

    return fig

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    results = read_results()
    fig = dot_plot(results)

    if arguments['--save']:
        fig.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures') +
                '/' + 'current_figure' +
                '.png')
