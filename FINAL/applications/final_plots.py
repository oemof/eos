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
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from docopt import docopt

# res = pickle.load(open('../results/households_results_dc_0.7.p', 'rb'))
# pp.pprint(res)


def read_results_storage():

    results_storage_2030 = np.zeros(5).reshape(1, 5)

    results_storage_2030[0][0] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['storage_cap_1']

    results_storage_2030[0][1] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['storage_cap_1']

    results_storage_2030[0][2] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['storage_cap_1']

    results_storage_2030[0][3] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['storage_cap_1']

    results_storage_2030[0][4] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['storage_cap_1']

    results_storage_2050 = np.zeros(5).reshape(1, 5)

    results_storage_2050[0][0] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['storage_cap_1']

    results_storage_2050[0][1] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['storage_cap_1']

    results_storage_2050[0][2] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['storage_cap_1']

    results_storage_2050[0][3] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['storage_cap_1']

    results_storage_2050[0][4] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt = np.zeros(5).reshape(1, 5)

    results_storage_costopt[0][0] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt[0][1] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt[0][2] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt[0][3] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt[0][4] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['storage_cap_1']

    results_storage_2030_GWh = results_storage_2030 / 1e6
    results_storage_2050_GWh = results_storage_2050 / 1e6
    results_storage_costopt_GWh = results_storage_costopt / 1e6

    results_storage_GWh = {'2030': results_storage_2030_GWh,
                           '2050': results_storage_2050_GWh,
                           'costopt': results_storage_costopt_GWh}

    return results_storage_GWh


def read_results_storage_biogas_options():

    results_storage_biogas_flex_2030 = np.zeros(5).reshape(1, 5)

    results_storage_biogas_flex_2030[0][0] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2030[0][1] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2030[0][2] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2030[0][3] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2030[0][4] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2050 = np.zeros(5).reshape(1, 5)

    results_storage_biogas_flex_2050[0][0] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2050[0][1] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2050[0][2] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2050[0][3] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2050[0][4] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'masterplan_results_mit_biogas_flex' + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt_auch_biogas = np.zeros(5).reshape(1, 5)

    results_storage_costopt_auch_biogas[0][0] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt_auch_biogas/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt_auch_biogas[0][1] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt_auch_biogas/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt_auch_biogas[0][2] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt_auch_biogas/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt_auch_biogas[0][3] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt_auch_biogas/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['storage_cap_1']

    results_storage_costopt_auch_biogas[0][4] = pd.read_pickle(open('../../../../Caros_Daten/' +
                                        'costopt_auch_biogas/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['storage_cap_1']

    results_storage_biogas_flex_2030_GWh = results_storage_biogas_flex_2030 / 1e6
    results_storage_biogas_flex_2050_GWh = results_storage_biogas_flex_2050 / 1e6
    results_storage_costopt_auch_biogas_GWh = results_storage_costopt_auch_biogas / 1e6

    results_storage_biogas_options_GWh = {'flex_2030': results_storage_biogas_flex_2030_GWh,
                                          'flex_2050': results_storage_biogas_flex_2050_GWh,
                                          'biogas_costopt': results_storage_costopt_auch_biogas_GWh}

    return results_storage_biogas_options_GWh


def read_results_deficit_excess():

    results_deficit_2030 = np.zeros(5).reshape(1, 5)
    results_excess_2030 = np.zeros(5).reshape(1, 5)

    # Read deficit 2030

    results_deficit_2030[0][0] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['grid_1']

    results_deficit_2030[0][1] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['grid_1']

    results_deficit_2030[0][2] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['grid_1']

    results_deficit_2030[0][3] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['grid_1']

    results_deficit_2030[0][4] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['grid_1']

    # Read excess 2030

    results_excess_2030[0][0] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['excess_1']

    results_excess_2030[0][1] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['excess_1']

    results_excess_2030[0][2] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['excess_1']

    results_excess_2030[0][3] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['excess_1']

    results_excess_2030[0][4] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['excess_1']

    results_deficit_2050 = np.zeros(5).reshape(1, 5)
    results_excess_2050 = np.zeros(5).reshape(1, 5)

    # Read deficit 2050

    results_deficit_2050[0][0] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['grid_1']

    results_deficit_2050[0][1] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['grid_1']

    results_deficit_2050[0][2] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['grid_1']

    results_deficit_2050[0][3] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['grid_1']

    results_deficit_2050[0][4] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['grid_1']

    # Read excess 2050

    results_excess_2050[0][0] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['excess_1']

    results_excess_2050[0][1] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['excess_1']

    results_excess_2050[0][2] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['excess_1']

    results_excess_2050[0][3] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['excess_1']

    results_excess_2050[0][4] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2050' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['excess_1']

    results_deficit_costopt = np.zeros(5).reshape(1, 5)
    results_excess_costopt = np.zeros(5).reshape(1, 5)

    # Read deficit costopt

    results_deficit_costopt[0][0] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['grid_1']

    results_deficit_costopt[0][1] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['grid_1']

    results_deficit_costopt[0][2] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['grid_1']

    results_deficit_costopt[0][3] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['grid_1']

    results_deficit_costopt[0][4] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['grid_1']

    # Read excess costopt

    results_excess_costopt[0][0] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['grid_1']

    results_excess_costopt[0][1] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['grid_1']

    results_excess_costopt[0][2] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['grid_1']

    results_excess_costopt[0][3] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['grid_1']

    results_excess_costopt[0][4] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['grid_1']

    # Read demand
    results_demand = np.zeros(5).reshape(1, 5)

    results_demand[0][0] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['demand_1']

    results_demand[0][1] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['demand_1']

    results_demand[0][2] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['demand_1']

    results_demand[0][3] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['demand_1']

    results_demand[0][4] = pickle.load(open('../results/' +
                                        str(arguments['--scenario']) + '/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['demand_1']

    results_deficit_2030_GWh = results_deficit_2030 / 1e6
    results_deficit_2050_GWh = results_deficit_2050 / 1e6
    results_deficit_costopt = results_deficit_costopt / 1e6

    results_deficit_GWh = {'2030': results_deficit_2030_GWh,
                           '2050': results_deficit_2050_GWh,
                           'costopt': results_deficit_costopt}

    results_excess_2030_GWh = results_excess_2030 / 1e6
    results_excess_2050_GWh = results_excess_2050 / 1e6
    results_excess_costopt = results_excess_costopt / 1e6

    results_excess_GWh = {'2030': results_excess_2030_GWh,
                           '2050': results_excess_2050_GWh,
                           'costopt': results_excess_costopt}

    results_demand_GWh = results_demand / 1e6

    return (results_deficit_GWh, results_excess_GWh, results_demand_GWh)


def read_results_capacities():

    masterplan_stein = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                  'stein' + '.csv', sep=',',
                                  index_col=0)

    masterplan_lkos = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                                  'lkos' + '.csv', sep=',',
                                  index_col=0)

    masterplan_osna = pd.read_csv('../examples_SOLPH_0.1/scenarios/masterplan_' +
                              'osna' + '.csv', sep=',',
                              index_col=0)

    results_wind_2030_MW = (masterplan_stein.loc['wind']['2030']
                            + masterplan_lkos.loc['wind']['2030']
                            + masterplan_osna.loc['wind']['2030'])

    results_wind_2050_MW = (masterplan_stein.loc['wind']['2050']
                            + masterplan_lkos.loc['wind']['2050']
                            + masterplan_osna.loc['wind']['2050'])

    results_pv_2030_MW = (masterplan_stein.loc['pv']['2030']
                          + masterplan_lkos.loc['pv']['2030']
                          + masterplan_osna.loc['pv']['2030'])

    results_pv_2050_MW = (masterplan_stein.loc['pv']['2050']
                          + masterplan_lkos.loc['pv']['2050']
                          + masterplan_osna.loc['pv']['2050'])

    results_wind_costopt = np.zeros(5).reshape(1, 5)

    results_wind_costopt[0][0] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['wind_inst_1']

    results_wind_costopt[0][1] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['wind_inst_1']

    results_wind_costopt[0][2] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['wind_inst_1']

    results_wind_costopt[0][3] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['wind_inst_1']

    results_wind_costopt[0][4] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['wind_inst_1']

    results_pv_costopt = np.zeros(5).reshape(1, 5)

    results_pv_costopt[0][0] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.70_1_.p', 'rb'))['pv_inst_1']

    results_pv_costopt[0][1] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.75_1_.p', 'rb'))['pv_inst_1']

    results_pv_costopt[0][2] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.80_1_.p', 'rb'))['pv_inst_1']

    results_pv_costopt[0][3] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.85_1_.p', 'rb'))['pv_inst_1']

    results_pv_costopt[0][4] = pickle.load(open('../results/' +
                                        'costopt/' +
                                        'region_results_dc' + '_' +
                                        str(arguments['--region']) + '_' +
                                        '2030' + '_' +
                                        str(2005) + '_' +
                                        '0.90_1_.p', 'rb'))['pv_inst_1']

    results_wind_costopt_MW = results_wind_costopt / 1e3
    results_pv_costopt_MW = results_pv_costopt / 1e3

    results_costopt_MW = {'wind': results_wind_costopt_MW,
                       'pv': results_pv_costopt_MW,
                       'wind_2030': results_wind_2030_MW,
                       'wind_2050': results_wind_2050_MW,
                       'pv_2030': results_pv_2030_MW,
                       'pv_2050': results_pv_2050_MW}

    print(results_costopt_MW['wind_2030'])
    print(results_costopt_MW['wind_2050'])
    print(results_costopt_MW['pv_2030'])
    print(results_costopt_MW['pv_2050'])

    return results_costopt_MW


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
                     markeredgecolor='orange',
                     markeredgewidth=3,
                     markerfacecolor='None',
                     label='2030')
    colors.append(plt.getp(line,'markeredgecolor'))

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                     results_storage['2050'][0][:],
                     linestyle='',
                     marker='o',
                     markersize=16,
                     markeredgecolor='b',
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
                     label='kostenoptimiert')
    colors.append(plt.getp(line,'markeredgecolor'))

    # plt.axis([0.68, 0.92,
        # results_storage['2030'].min(), results_storage['2030'].max() + 1])

    plt.xlim([0.68, 0.92])
    plt.ylim([0, 11])

    plt.xticks([0.70, 0.75, 0.80, 0.85, 0.90], fontsize=28, color=diagram_color)
    plt.yticks([0, 5, 10], fontsize=28, color=diagram_color)
    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    plt.ylabel('Speicherkapazität in GWh', fontsize=28, color=diagram_color)

    leg = plt.legend(loc='upper left', frameon=False, prop={'size': 28})
    leg._legend_box.align = 'left'
    leg.set_title('Kreis Steinfurt', prop={'size': 28})
    for color,text in zip(colors,leg.get_texts()):
        # for text in leg.get_texts():
            text.set_color(color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.show()

    return fig


def dot_plot_storage_biogas_options(results_storage,
        results_storage_biogas_options):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    darker_grey = '#595959'
    colors = []

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                     results_storage['2050'][0][:],
                     linestyle='',
                     marker='o',
                     markersize=16,
                     markeredgecolor='b',
                     markeredgewidth=3,
                     markerfacecolor='None',
                     label='Biogas-BHKW konstant 2050')
    colors.append(plt.getp(line,'markeredgecolor'))

    line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
                     results_storage_biogas_options['flex_2050'][0][:],
                     linestyle='',
                     marker='o',
                     markersize=16,
                     markeredgecolor='g',
                     markeredgewidth=3,
                     markerfacecolor='None',
                     label='Biogas-BHKW flexibel 2050')
    colors.append(plt.getp(line,'markeredgecolor'))

    # line, = ax.plot([0.70, 0.75, 0.80, 0.85, 0.90],
    #                  results_storage_biogas_options['biogas_costopt'][0][:],
    #                  linestyle='',
    #                  marker='o',
    #                  markersize=16,
    #                  markeredgecolor=darker_grey,
    #                  markeredgewidth=3,
    #                  markerfacecolor='None',
    #                  label='Biogas-BHKW kostenoptimiert')
    # colors.append(plt.getp(line,'markeredgecolor'))

    # plt.axis([0.68, 0.92,
        # results_storage['2030'].min(), results_storage['2030'].max() + 1])

    plt.xlim([0.68, 0.92])
    plt.ylim([0, 5])

    plt.xticks([0.70, 0.75, 0.80, 0.85, 0.90], fontsize=28, color=diagram_color)
    plt.yticks([0, 1, 2, 3, 4], fontsize=28, color=diagram_color)
    # plt.yticks([0, 5, 10], fontsize=28, color=diagram_color)
    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    plt.ylabel('Speicherkapazität in GWh', fontsize=28, color=diagram_color)

    leg = plt.legend(loc='upper left', frameon=False, prop={'size': 28})
    leg._legend_box.align = 'left'
    leg.set_title('Landkreis Osnabrück', prop={'size': 28})
    for color,text in zip(colors,leg.get_texts()):
        # for text in leg.get_texts():
            text.set_color(color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.show()

    return fig


def bar_plot_capacities(results_capacities):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    bar_width = 0.35
    diagram_color = 'black'
    main_color = '#7f7f7f'
    grey_color = '#a6a6a6'
    colors = []

    X = np.arange(5)

    # ax.bar(X, results_capacities['wind'][0][:],
    #        bar_width,
    #        facecolor=main_color,
    #        edgecolor='white',
    #        label='kostenoptimiert')
    # line = ax.axhline(results_capacities['wind_2030'],
    #         linewidth=2,
    #         color='slateblue',
    #         label='2030')
    # # colors.append(plt.getp(line,'markeredgecolor'))
    # line = ax.axhline(results_capacities['wind_2050'],
    #         linewidth=2,
    #         color='midnightblue',
    #         label='2050')
    # # colors.append(plt.getp(line,'markeredgecolor'))

    ax.bar(X, results_capacities['wind'][0][:],
           bar_width,
           facecolor='slateblue',
           edgecolor='white',
           label='Windenergie')
    ax.bar(X+bar_width, results_capacities['pv'][0][:],
           bar_width,
           facecolor='gold',
           edgecolor='white',
           label='PV')

    plt.ylim([0, 3600])
    # plt.xticks(X, ('0.70', '0.75', '0.80', '0.85', '0.90'), fontsize=28, color=diagram_color)
    plt.xticks(X + bar_width / 2, ('0.70', '0.75', '0.80', '0.85', '0.90'), fontsize=28, color=diagram_color)
    plt.yticks([1000, 2000, 3000], fontsize=28, color=diagram_color)
    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    plt.ylabel('Installierte Leistung in MW', fontsize=28, color=diagram_color)

    leg = ax.legend(loc='upper left', frameon=False, prop={'size': 28})
    # leg = ax.legend(loc=(0.03, 0.42), frameon=False, prop={'size': 28}) # für PV-Grafik
    leg.set_title('Masterplanregion', prop={'size': 28})
    leg._legend_box.align = 'left'

    for bar,text in zip(leg.get_patches(), leg.get_texts()):
        text.set_color(bar.get_facecolor())
    # for color,text in zip(['slateblue', 'midnightblue', main_color], leg.get_texts()):
        # text.set_color(color)
    # for color,text in zip(['gold', 'goldenrod', main_color], leg.get_texts()):
    #     text.set_color(color)
    # for color,text in zip(colors,leg.get_texts()):
    # # for text in l.get_texts():
    #     text.set_color(color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    # plt.ylim([0, 5100])
    # plt.xlabel('Weather year', size=18)
    # plt.ylabel('Installed capacities in MW', size=18)
    # plt.xticks(ind, ['1998', '1999', '2000', '2001', '2002', '2003', '2004',
    #                  '2005', '2006', '2007', '2008', '2009', '2010', '2011',
    #                  '2012', '2013', '2014'])
    # plt.legend((p1[0], p2[0], p3[0]), ('Windenergie', 'Photovoltaik', 'Biogas-BHKW'),
    #             loc='upper left', prop={'size': 18})
    # plt.rcParams.update({'font.size': 18})
    # plt.tight_layout()

    plt.show()

    return fig


def bar_plot_deficit_excess(results_deficit, results_excess, results_demand):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

    n = 5
    X = np.arange(n)

    Y1 = results_demand[0][:] - results_deficit['2050'][0][:]  # covered demand
    Y2 = (-1) * results_excess['2050'][0][:]
    Y3 = results_demand[0][:]

    ax.bar(X, Y3, facecolor='orangered', edgecolor='white',
        label='Deficit')
    ax.bar(X, Y1, facecolor='#a6a6a6', edgecolor='white',
        label='Covered demand')
    ax.bar(X, Y2, facecolor='darkcyan', edgecolor='white',
        label='Excess')

    plt.axhline(0, linewidth=0.5, color=main_color)

    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    plt.ylabel('Strombedarf in GWh', fontsize=28, color=diagram_color)
    plt.xticks(X, ['0.70', '0.75', '0.80', '0.85', '0.90'], fontsize=28, color=diagram_color)

    plt.ylim(-5000, 7500)
    plt.yticks([-4000, -2000, 0, 2000, 4000, 6000], fontsize=28, color=diagram_color)

    leg = ax.legend(loc='upper center', ncol=3, frameon=False, prop={'size': 24})
    leg.set_title('Masterplanregion', prop={'size': 28})
    leg._legend_box.align = 'left'

    for bar,text in zip(leg.get_patches(), leg.get_texts()):
        text.set_color(bar.get_facecolor())
    # for color,text in zip(colors,leg.get_texts()):
    # for text in l.get_texts():
    # text.set_color(color)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    plt.tight_layout()

    plt.show()

    return fig


def bar_plot_excess(results_excess):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    bar_width = 0.2
    diagram_color = 'black'
    main_color = '#7f7f7f'
    grey_color = '#a6a6a6'
    colors = []

    X = np.arange(5)

    ax.bar(X, results_excess['2030'][0][:],
           bar_width,
           facecolor='darkcyan',
           edgecolor='white',
           label='2030')
    ax.bar(X+bar_width, results_excess['2050'][0][:],
           bar_width,
           facecolor='#00468c',
           edgecolor='white',
           label='2050')
    ax.bar(X+2*bar_width, results_excess['costopt'][0][:],
           bar_width,
           facecolor=main_color,
           edgecolor='white',
           label='kostenoptimiert')

    plt.ylim([0, 6200])
    # plt.xticks(X, ('0.70', '0.75', '0.80', '0.85', '0.90'), fontsize=28, color=diagram_color)
    plt.xticks(X + bar_width / 3, ('0.70', '0.75', '0.80', '0.85', '0.90'), fontsize=28, color=diagram_color)
    plt.yticks([2000, 4000, 6000], fontsize=28, color=diagram_color)
    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    plt.ylabel('Überschussenergie in GWh', fontsize=28, color=diagram_color)

    leg = ax.legend(loc='upper left', ncol=3,  frameon=False, prop={'size': 28})
    # leg = ax.legend(loc=(0.03, 0.42), frameon=False, prop={'size': 28}) # für PV-Grafik
    leg.set_title('Masterplanregion', prop={'size': 28})
    leg._legend_box.align = 'left'

    for bar,text in zip(leg.get_patches(), leg.get_texts()):
        text.set_color(bar.get_facecolor())
    # for color,text in zip(['slateblue', 'midnightblue', main_color], leg.get_texts()):
        # text.set_color(color)
    # for color,text in zip(['gold', 'goldenrod', main_color], leg.get_texts()):
    #     text.set_color(color)
    # for color,text in zip(colors,leg.get_texts()):
    # # for text in l.get_texts():
    #     text.set_color(color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    # plt.ylim([0, 5100])
    # plt.xlabel('Weather year', size=18)
    # plt.ylabel('Installed capacities in MW', size=18)
    # plt.xticks(ind, ['1998', '1999', '2000', '2001', '2002', '2003', '2004',
    #                  '2005', '2006', '2007', '2008', '2009', '2010', '2011',
    #                  '2012', '2013', '2014'])
    # plt.legend((p1[0], p2[0], p3[0]), ('Windenergie', 'Photovoltaik', 'Biogas-BHKW'),
    #             loc='upper left', prop={'size': 18})
    # plt.rcParams.update({'font.size': 18})
    # plt.tight_layout()

    plt.show()

    return fig


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    results_storage = read_results_storage()
    ig = dot_plot_storage(results_storage)
    # results_capacities = read_results_capacities()
    # fig = bar_plot_capacities(results_capacities)
    # (results_deficit, results_excess, results_demand) = read_results_deficit_excess()
    # fig = bar_plot_deficit_excess(results_deficit, results_excess, results_demand)
    # fig = bar_plot_excess(results_excess)
    # results_storage_biogas_options = read_results_storage_biogas_options()
    # fig = dot_plot_storage_biogas_options(results_storage, results_storage_biogas_options)

    if arguments['--save']:
        fig.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures') +
                '/' + 'current_figure' +
                '.png')
