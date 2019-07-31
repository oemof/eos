# -*- coding: utf-8 -*-

''' Example for simulating wind-pv-battery systems in regions.

Usage: example_region.py [options]

Options:

  -s, --scenario=SCENARIO  The scenario name. [default: scenario]
  -c, --cost=COST          The cost scenario. [default: 0]
  -t, --tech=TECH          The tech scenario. [default: 0]
  -o, --solver=SOLVER      The solver to use. Should be one of "glpk", "cbc"
                           or "gurobi".
                           [default: cbc]
  -l, --loglevel=LOGLEVEL  Set the loglevel. Should be one of DEBUG, INFO,
                           WARNING, ERROR or CRITICAL.
                           [default: ERROR]
      --timesteps=TSTEPS   Set number of timesteps. [default: 8760]
  -h, --help               Display this help.
      --year=YEAR          Weather data year. Choose from 1998 to 2014
                           [default: 2005]
      --num-regions=NUM    Number of regions. [default: 24]
      --multi-regions=NUM  Number of regions to combine each. [default: 1]
      --costopt            Cost optimization.
      --biogas             Include biogas potential.
      --biogas-flex        Include biogas as flexible potential.
      --biogas-costopt     Also cost optimize biogas bhkw.
      --lkos               LKOS load profile
      --bdew               BDEW standard load profile h0
      --ssr=SSR            Self-sufficiency degree.
      --write-results      write results to data/scenarioname_results.csv
      --dry-run            Do nothing. Only print what would be done.

'''

###############################################################################
# imports
###############################################################################
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import logging
import csv
import pickle
import pprint as pp
import os
from demandlib import bdew as bdew

try:
    from docopt import docopt
except ImportError:
    print("Unable to import docopt.\nIs the 'docopt' package installed?")

# Outputlib
from oemof import outputlib

# Default logger of oemof
from oemof.tools import logger

# import oemof core and solph classes to create energy system objects
import oemof.solph as solph


def initialise_energysystem(year, number_timesteps):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/' + year,
                                    periods=number_timesteps,
                                    freq='H')

    return solph.EnergySystem(groupings=solph.GROUPINGS,
                              timeindex=date_time_index)


def validate(**arguments):
    valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if arguments["--loglevel"] not in valid:
        exit("Invalid loglevel: " + arguments["--loglevel"])
    return arguments


def read_and_calculate_parameters(**arguments):

    ###########################################################################
    # read and calculate parameters
    ###########################################################################

    logging.info('Read and calculate parameters')

    # Read parameter csv files
    region_parameter = pd.read_csv(
        '../../scenarios/region/' + arguments['--scenario'] +
        '_region_parameter.csv',
        delimiter=',', index_col=0)

    cost_parameter = pd.read_csv(
        '../../scenarios/region/' + arguments['--scenario'] +
            '_cost_parameter_' + str(arguments['--cost']) + '.csv',
        delimiter=',', index_col=0)

    tech_parameter = pd.read_csv(
        '../../scenarios/region/' + arguments['--scenario'] +
            '_tech_parameter_' + str(arguments['--tech']) + '.csv',
        delimiter=',', index_col=0)

    data = pd.read_csv("../../data/storage_invest.csv", sep=',')
    data_weather = pd.read_csv('../../data/' + arguments['--year'] + '_feedin_8043_52279.csv', sep=',')
    if arguments['--lkos']:
        data_load = pd.read_csv('../data/Lastprofil_LKOS_MW_1h.csv', sep=',')
        data_load = data_load['demand_el'] * 1e3  # demand in kW
    elif arguments['--bdew']:
        e_slp = bdew.ElecSlp(int(arguments['--year']))
        h0_slp_15_min = e_slp.get_profile({'h0': 1})
        h0_slp = h0_slp_15_min.resample('H').mean()
        data_load = h0_slp['h0'].reset_index(drop=True)
    else:
        data_load = data['demand_el']  # demand in kW

    # data_wind = data['wind']
    # data_pv = data['pv']
    data_wind = data_weather['wind']
    data_pv = data_weather['pv']

    # Calculate ep_costs from capex
    storage_capex = cost_parameter.loc['storage']['capex']
    storage_lifetime = cost_parameter.loc['storage']['lifetime']
    storage_wacc = cost_parameter.loc['storage']['wacc']
    storage_epc = storage_capex * (storage_wacc * (1 + storage_wacc) **
                                   storage_lifetime) / ((1 + storage_wacc) **
                                                        storage_lifetime - 1)

    wind_capex = cost_parameter.loc['wind']['capex']
    wind_lifetime = cost_parameter.loc['wind']['lifetime']
    wind_wacc = cost_parameter.loc['wind']['wacc']
    wind_epc = wind_capex * (wind_wacc * (1 + wind_wacc) **
                        wind_lifetime) / ((1 + wind_wacc) ** wind_lifetime - 1)

    pv_capex = cost_parameter.loc['pv']['capex']
    pv_lifetime = cost_parameter.loc['pv']['lifetime']
    pv_wacc = cost_parameter.loc['pv']['wacc']
    pv_epc = pv_capex * (pv_wacc * (1 + pv_wacc) **
                         pv_lifetime) / ((1 + pv_wacc) ** pv_lifetime - 1)

    biogas_bhkw_capex = cost_parameter.loc['biogas_bhkw']['capex']
    biogas_bhkw_lifetime = cost_parameter.loc['biogas_bhkw']['lifetime']
    biogas_bhkw_wacc = cost_parameter.loc['biogas_bhkw']['wacc']
    biogas_bhkw_epc = biogas_bhkw_capex * (biogas_bhkw_wacc * (1 + biogas_bhkw_wacc) **
                         biogas_bhkw_lifetime) / ((1 + biogas_bhkw_wacc) ** biogas_bhkw_lifetime - 1)

    print(biogas_bhkw_epc)
    # Calculate grid share
    if arguments['--ssr']:
        grid_share = 1 - float(arguments['--ssr'])

    else:
        grid_share = None

    # Define combinations of multi regions
    regions = np.arange(1, int(arguments['--num-regions']) + 1)
    if int(arguments['--multi-regions']) == 2:
        i = 1
        combinations = [0, 0, 0]
        for n in itertools.combinations(regions, int(arguments['--multi-regions'])):
            combinations = np.vstack((combinations, [i, n[0], n[1]]))
            i = i + 1
    else:
        combinations = None

    print('regions: ', regions)
    print('combinations: ', combinations)

    if int(arguments['--multi-regions']) == 2:
        loop = np.arange(1, len(combinations))
    else:
        loop = regions

    parameters = {'region_parameter': region_parameter,
                  'cost_parameter': cost_parameter,
                  'tech_parameter': tech_parameter,
                  'storage_epc': storage_epc,
                  'wind_epc': wind_epc,
                  'pv_epc': pv_epc,
                  'biogas_bhkw_epc': biogas_bhkw_epc,
                  'data': data,
                  'data_load': data_load,
                  'data_wind': data_wind,
                  'data_pv': data_pv,
                  'grid_share': grid_share,
                  'regions': regions,
                  'combinations': combinations,
                  'loop': loop,
                  }

    logging.info('Check parameters')
    print('cost parameter:\n', parameters['cost_parameter'])
    print('tech parameter:\n', parameters['tech_parameter'])

    return parameters


def create_energysystem(energysystem, parameters, loopi,
                        **arguments):

    ##########################################################################
    # Create oemof object
    ##########################################################################
    logging.info('Create oemof objects')

    # Create electricity bus for demand
    bel = solph.Bus(label='region_'+str(loopi)+'_bel')

    # Create biogas bus for biogas
    bbiogas = solph.Bus(label='region_'+str(loopi)+'_bbiogas')

    # Create storage transformer object for storage
    solph.Storage(
        label='region_'+str(loopi)+'_bat',
        inputs={bel: solph.Flow(variable_costs=0)},
        outputs={bel: solph.Flow(variable_costs=0)},
        capacity_loss=parameters[
            'tech_parameter'].loc['storage']['cap_loss'],
        nominal_input_capacity_ratio=parameters[
            'tech_parameter'].loc['storage']['c_rate'],
        nominal_output_capacity_ratio=parameters[
            'tech_parameter'].loc['storage']['c_rate'],
        inflow_conversion_factor=parameters[
            'tech_parameter'].loc['storage']['eta_in'],
        outflow_conversion_factor=parameters[
            'tech_parameter'].loc['storage']['eta_out'],
        capacity_min=parameters[
            'tech_parameter'].loc['storage']['capacity_min'],
        capacity_max=parameters[
            'tech_parameter'].loc['storage']['capacity_max'],
        fixed_costs=parameters[
            'cost_parameter'].loc['storage']['opex_fix'],
        investment=solph.Investment(ep_costs=parameters['storage_epc']))

    # Create commodity object for import electricity resource
    if arguments['--costopt']:
        if arguments['--ssr']:
            gridsource_nv = (float(parameters
                               ['region_parameter'].loc
                               ['annual_demand_GWh'][str(loopi)]) *
                               1e6 * parameters['grid_share'])

            solph.Source(
                    label='region_'+str(loopi)+'_gridsource',
                    outputs={bel: solph.Flow(
                        nominal_value=gridsource_nv,
                        summed_max=1)})
                        # summed_max=1,
                        # min=0.0)})
        else:
            solph.Source(
                    label='region_'+str(loopi)+'_gridsource',
                    outputs={bel: solph.Flow(
                        variable_costs=parameters[
                            'cost_parameter'].loc['grid']['opex_var'])})
                            # 'cost_parameter'].loc['grid']['opex_var'],
                            # min=0.0)})

    elif arguments['--ssr']:
        if int(arguments['--multi-regions']) == 2:

            gridsource_nv = ((float(parameters
                               ['region_parameter'].loc
                               ['annual_demand_GWh'][str(parameters
                                   ['combinations'][loopi][1])]) *
                               1e6 * parameters['grid_share']) +

                            (float(parameters
                               ['region_parameter'].loc
                               ['annual_demand_GWh'][str(parameters
                                   ['combinations'][loopi][2])]) *
                               1e6 * parameters['grid_share']))
        else:
            gridsource_nv = (float(parameters
                               ['region_parameter'].loc
                               ['annual_demand_GWh'][str(loopi)]) *
                               1e6 * parameters['grid_share'])

        solph.Source(
            label='region_'+str(loopi)+'_gridsource',
            outputs={bel: solph.Flow(
                nominal_value=gridsource_nv,
                summed_max=1)})
                # summed_min=1,
                # max=0.0001)})

    else:
        print('Something is missing')

    # Create excess component to allow overproduction
    solph.Sink(label='region_'+str(loopi)+'_excess',
               inputs={bel: solph.Flow()})

    # Create fixed source object for wind

    if arguments['--costopt']:
        solph.Source(label='region_'+str(loopi)+'_wind',
                     outputs={bel: solph.Flow(
                              actual_value=parameters['data_wind'],
                              fixed=True,
                              fixed_costs=parameters[
                                  'cost_parameter'].loc['wind']['opex_fix'],
                              investment=solph.Investment(
                                  ep_costs=parameters['wind_epc']))})

    else:
        if int(arguments['--multi-regions']) == 2:
            wind_nv = (float(parameters['region_parameter'].
                             loc['wind_MW'][str(parameters
                                                ['combinations']
                                                [loopi][1])]) * 1e3 +

                       float(parameters['region_parameter'].
                             loc['wind_MW'][str(parameters
                                                ['combinations']
                                                [loopi][2])]) * 1e3)

        else:
            wind_nv = float(parameters['region_parameter'].
                            loc['wind_MW'][str(loopi)]) * 1e3

        solph.Source(label='region_'+str(loopi)+'_wind',
                     outputs={bel: solph.Flow(
                              actual_value=parameters['data_wind'],
                              nominal_value=wind_nv,
                              fixed=True)})

    # Create fixed source object for pv
    if arguments['--costopt']:
        solph.Source(label='region_'+str(loopi)+'_pv',
                         outputs={bel: solph.Flow(
                              actual_value=parameters['data_pv'],
                              fixed=True,
                              fixed_costs=parameters[
                                  'cost_parameter'].loc['pv']['opex_fix'],
                              investment=solph.Investment(
                                  ep_costs=parameters['pv_epc']))})

    else:
        if int(arguments['--multi-regions']) == 2:
                pv_nv = (float(parameters['region_parameter'].
                           loc['pv_MW'][str(parameters
                                            ['combinations']
                                            [loopi][1])]) * 1e3 +

                     float(parameters['region_parameter'].
                           loc['pv_MW'][str(parameters
                                            ['combinations']
                                            [loopi][2])]) * 1e3)

        else:
            pv_nv = float(parameters['region_parameter'].
                          loc['pv_MW'][str(loopi)]) * 1e3

        solph.Source(label='region_'+str(loopi)+'_pv',
                     outputs={bel: solph.Flow(
                              actual_value=parameters['data_pv'],
                              nominal_value=pv_nv,
                              fixed=True)})

    # Create source and transformer object for biogas
    if arguments['--biogas']:

        if int(arguments['--multi-regions']) == 2:
            biogas_nv = (float(parameters['region_parameter'].
                           loc['biogas_GWh'][str(parameters
                                            ['combinations']
                                            [loopi][1])]) * 1e6 +

                     float(parameters['region_parameter'].
                           loc['biogas_GWh'][str(parameters
                                            ['combinations']
                                            [loopi][2])]) * 1e6)

        else:

            biogas_nv = float(parameters['region_parameter'].
                                loc['biogas_GWh'][str(loopi)]) * 1e6

        solph.Source(label='region_'+str(loopi)+'_rbiogas',
                outputs={bbiogas: solph.Flow(
                    nominal_value=biogas_nv,
                    summed_max=1)})

        if arguments['--biogas-flex']:

            solph.LinearTransformer(
                    label='region_'+str(loopi)+'_biogas_bhkw',
                    inputs={bbiogas: solph.Flow()},
                    outputs={bel: solph.Flow(
                        nominal_value=biogas_nv*0.38/8760*2)},
                        # nominal_value=biogas_nv*0.38/8760*2)},
                        conversion_factors={bel: 0.38})

        else:
            solph.LinearTransformer(
                    label='region_'+str(loopi)+'_biogas_bhkw',
                    inputs={bbiogas: solph.Flow()},
                    outputs={bel: solph.Flow(
                        nominal_value=biogas_nv*0.38/8760)},
                        # nominal_value=biogas_nv*0.38/8760*2)},
                        conversion_factors={bel: 0.38})

    if arguments['--biogas-costopt']:

        biogas_nv = float(parameters['region_parameter'].
                            loc['biogas_GWh'][str(loopi)]) * 1e6

        solph.Source(label='region_'+str(loopi)+'_rbiogas',
                outputs={bbiogas: solph.Flow(
                    nominal_value=biogas_nv,
                    variable_costs=parameters[
                        'cost_parameter'].loc['biogas_th']['opex_var'],
                    summed_max=1)})

        solph.LinearTransformer(
                label='region_'+str(loopi)+'_biogas_bhkw',
                inputs={bbiogas: solph.Flow()},
                outputs={bel: solph.Flow(
                             fixed_costs=parameters[
                                   'cost_parameter'].loc['biogas_bhkw']['opex_fix'],
                             variable_costs=parameters[
                                   'cost_parameter'].loc['biogas_bhkw']['opex_var'],
                             investment=solph.Investment(
                                   ep_costs=parameters['biogas_bhkw_epc']))},
                             conversion_factors={bel: 0.38})

    # Create simple sink objects for demands
    if int(arguments['--multi-regions']) == 2:
        demand_av = ((parameters['data_load'] /
                      parameters['data_load'].sum() *
                      float(parameters['region_parameter'].
                      loc['annual_demand_GWh'][str(parameters
                                                       ['combinations']
                                                       [loopi][1])]) * 1e6) +

                     (parameters['data_load'] /
                      parameters['data_load'].sum() *
                      float(parameters['region_parameter'].
                      loc['annual_demand_GWh'][str(parameters
                                                       ['combinations']
                                                       [loopi][2])]) * 1e6))

    else:
        demand_av = (parameters['data_load'] /
                     parameters['data_load'].sum() *
                     float(parameters['region_parameter'].
                     loc['annual_demand_GWh'][str(loopi)])*1e6)

    solph.Sink(label='region_'+str(loopi)+'_demand',
               inputs={bel: solph.Flow(
                       actual_value=demand_av,
                       fixed=True,
                       nominal_value=1)})

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = solph.OperationalModel(energysystem)

    logging.info('Store lp-file')
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})

    logging.info('Solve the optimization problem')
    om.solve(solver=arguments['--solver'], solve_kwargs={'tee': True})

    return energysystem


def get_result_dict(energysystem, parameters, loopi, **arguments):
    logging.info('Check the results')

    year = arguments['--year']

    results_dc = {}
    myresults = outputlib.DataFramePlot(energy_system=energysystem)

    bel = energysystem.groups['region_'+str(loopi)+'_bel']

    storage = energysystem.groups['region_'+str(loopi)+'_bat']

    wind_inst = energysystem.groups['region_'+str(loopi)+'_wind']

    pv_inst = energysystem.groups['region_'+str(loopi)+'_pv']

    if arguments['--biogas-costopt']:
        biogas_bhkw_inst = energysystem.groups['region_'+str(loopi)+'_biogas_bhkw']

    demand = myresults.slice_by(obj_label='region_'+str(loopi)+'_demand',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00')

    wind = myresults.slice_by(obj_label='region_'+str(loopi)+'_wind',
                              date_from=year+'-01-01 00:00:00',
                              date_to=year+'-12-31 23:00:00')

    pv = myresults.slice_by(obj_label='region_'+str(loopi)+'_pv',
                            date_from=year+'-01-01 00:00:00',
                            date_to=year+'-12-31 23:00:00')

    storage_in = myresults.slice_by(type='from_bus',
                            obj_label='region_'+str(loopi)+'_bat',
                            date_from=year+'-01-01 00:00:00',
                            date_to=year+'-12-31 23:00:00')

    storage_out = myresults.slice_by(type='to_bus',
                            obj_label='region_'+str(loopi)+'_bat',
                            date_from=year+'-01-01 00:00:00',
                            date_to=year+'-12-31 23:00:00')

    if (arguments['--biogas']) or (arguments['--biogas-costopt']) or (arguments['--biogas-flex']):
        biogas_bhkw = myresults.slice_by(obj_label='region_'+str(loopi)+'_biogas_bhkw',
                                         date_from=year+'-01-01 00:00:00',
                                         date_to=year+'-12-31 23:00:00')

    excess = myresults.slice_by(obj_label='region_'+str(loopi)+'_excess',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00')

    grid = myresults.slice_by(obj_label='region_'+str(loopi)+'_gridsource',
                                  date_from=year+'-01-01 00:00:00',
                                  date_to=year+'-12-31 23:00:00')

    if (arguments['--biogas']) or (arguments['--biogas-costopt']) or (arguments['--biogas-flex']):
        results_dc['biogas_bhkw_ts_'+str(loopi)] = biogas_bhkw

    results_dc['demand_'+str(loopi)] = float(demand.sum())
    results_dc['demand_ts_'+str(loopi)] = demand
    results_dc['grid_'+str(loopi)] = float(grid.sum())
    results_dc['grid_ts_'+str(loopi)] = grid
    results_dc['excess_'+str(loopi)] = float(excess.sum())
    results_dc['excess_ts_'+str(loopi)] = excess
    results_dc['wind_ts_'+str(loopi)] = wind
    results_dc['pv_ts_'+str(loopi)] = pv
    results_dc['check_ssr_'+str(loopi)] = 1 - (grid.sum() / demand.sum())
    results_dc['wind_max_'+str(loopi)] = float(wind.max())
    results_dc['pv_max_'+str(loopi)] = float(pv.max())
    results_dc['storage_cap_'+str(loopi)] = energysystem.results[
        storage][storage].invest
    results_dc['storage_in_ts_'+str(loopi)] = storage_in # ist das der richtige Wert?
    results_dc['storage_out_ts_'+str(loopi)] = storage_out
    results_dc['objective'] = energysystem.results.objective

    if arguments['--costopt']:
        results_dc['wind_inst_'+str(loopi)] = energysystem.results[wind_inst][bel].invest
        results_dc['pv_inst_'+str(loopi)] = energysystem.results[pv_inst][bel].invest

    if arguments['--biogas-costopt']:
        results_dc['biogas_bhkw_inst_'+str(loopi)] = energysystem.results[biogas_bhkw_inst][bel].invest

    if arguments['--write-results']:
        # x = list(results_dc.keys())
        # y = list(results_dc.values())
        # f = open(
        #     'data/'+arguments['--scenario']+'_results.csv',
        #     'w', newline='')
        # w = csv.writer(f, delimiter=';')
        # w.writerow(x)
        # w.writerow(y)
        # f.close

        if arguments['--ssr']:
            pickle.dump(results_dc, open('../../results/region_results_dc_' +
                arguments['--scenario'] + '_' +
                arguments['--year'] + '_' +
                arguments['--ssr'] + '_' +
                str(loopi) + '_' +
                '.p', "wb"))
        else:
            pickle.dump(results_dc, open('../../results/region_results_dc_' +
                arguments['--scenario'] + '_' +
                arguments['--year'] + '_' +
                str(loopi) + '_' +
                '.p', "wb"))
    # pickle.dump(myresults, open("save_myresults.p", "wb"))

    return (results_dc)


def create_plots(energysystem, year):
    logging.info('Plot results')
    myresults = outputlib.DataFramePlot(energy_system=energysystem)
    gridsource = myresults.slice_by(obj_label='gridsource', type='input',
                                    date_from=year + '-01-01 00:00:00',
                                    date_to=year + '-12-31 23:00:00')

    imp = gridsource.sort_values(by='val', ascending=False).reset_index()

    imp.plot(linewidth=1.5)

    plt.show()


def create_subplot(energysystem, results, year):

    esplot = outputlib.DataFramePlot(energy_system=energysystem)
    idx = pd.IndexSlice

    fig, axes = plt.subplots(nrows=3, ncols=1)  # figsize=(6,60)
    tick_distance = 4 * 24

    print(esplot)

    # Electricity generation
    subset_wind = esplot.slice_by(type='to_bus',
                                  obj_label='region_1_wind',
                                  date_from=year + '-06-01 00:00:00',
                                  date_to=year + '-06-08 00:00:00') / 1000

    dates = subset_wind.index.get_level_values('datetime').unique()

    subset_pv = esplot.slice_by(type='to_bus',
                                obj_label='region_1_pv',
                                date_from=year + '-06-01 00:00:00',
                                date_to=year + '-06-08 00:00:00') / 1000

    subset_gridsource = esplot.slice_by(type='to_bus',
                                        obj_label='region_1_gridsource',
                                        date_from=year + '-06-01 00:00:00',
                                        date_to=year + '-06-08 00:00:00') / 1000

    subset_bat = esplot.slice_by(type='to_bus',
                                 obj_label='region_1_bat',
                                 date_from=year + '-06-01 00:00:00',
                                 date_to=year + '-06-08 00:00:00') / 1000

    # subset_bio = esplot.slice_by(type='to_bus',
    #                               obj_label='region_1_biogas_bhkw',
    #                               date_from=year + '-06-01 00:00:00',
    #                               date_to=year + '-06-08 00:00:00') / 1000

    subset_wind.plot(ax=axes[0], kind="bar", stacked='True',
                                    color='#5b5bae',
                                    align='center', width=1)

    subset_pv.plot(ax=axes[0], kind="bar", stacked='True',
                                    color='#ffde32',
                                     align='center', width=1)

    subset_gridsource.plot(ax=axes[0], kind="bar", stacked='True',
                                    color='#636f6b',
                                     align='center', width=1)

    subset_bat.plot(ax=axes[0], kind="bar", stacked='True',
                                    color='#42c77a',
                                     align='center', width=1)

    # subset_bio.plot(ax=axes[0], kind="bar", stacked='True',
    #                                 color='#006400',
    #                                 align='center', width=1)

    axes[0].set_title('Electric energy generation', fontsize=24)
    axes[0].set_xlabel("")
    axes[0].set_xticks(range(0, len(dates), tick_distance), minor=False)
    axes[0].set_xticklabels("")
    axes[0].set_ylabel("MW", fontsize=22)
    # axes[0].set_ylim(0, 201)
    axes[0].set_yticks(range(0, 700, 200), minor=False)
    axes[0].tick_params(axis='x', labelsize=20)
    axes[0].tick_params(axis='y', labelsize=20)
    axes[0].legend(['Wind power', 'PV', 'Import', 'Storage'], loc='upper left', fontsize=18,
                   ncol=4)

    # SOC
    subset_soc = esplot.slice_by(type='other',
                                 obj_label='region_1_bat',
                                 date_from=year + '-06-01 00:00:00',
                                 date_to=year + '-06-08 00:00:00') / results['storage_cap_1']

    subset_soc.plot(ax=axes[1], drawstyle='steps',
                                    color='#42c77a',
                                    linewidth=2)

    axes[1].set_title('Storage state of charge', fontsize=24)
    axes[1].set_xlabel("")
    axes[1].set_xticks(range(0, len(dates), tick_distance), minor=False)
    axes[1].set_xticklabels("")
    axes[1].set_ylabel("%", fontsize=22)
    axes[1].set_ylim(0, 1.1)
    axes[1].set_yticks([0, 0.5, 1], minor=False)
    axes[1].tick_params(axis='x', labelsize=20)
    axes[1].tick_params(axis='y', labelsize=20)
    axes[1].legend(['Storage state of charge'], loc='upper left', fontsize=18)

    # Excess
    subset_excess = esplot.slice_by(type='from_bus',
                                    obj_label='region_1_excess',
                                    date_from=year + '-06-01 00:00:00',
                                    date_to=year + '-06-08 00:00:00') / 1000

    subset_demand = esplot.slice_by(type='from_bus',
                                    obj_label='region_1_demand',
                                    date_from=year + '-06-01 00:00:00',
                                    date_to=year + '-06-08 00:00:00') / 1000

    subset_demand.plot(ax=axes[2], drawstyle='steps',
                                    color='indigo',
                                    linewidth=2)

    subset_excess.plot(ax=axes[2], drawstyle='steps',
                                    color='#830000',
                                    linewidth=2)

    axes[2].set_title('Demand and excess', fontsize=24)
    axes[2].set_xlabel("")
    axes[2].set_xticks(range(0, len(dates), tick_distance), minor=False)
    axes[2].set_xticklabels("")
    axes[2].set_ylabel("MW", fontsize=22)
    # axes[2].set_ylim(0, 1.1)
    axes[2].set_yticks(range(0, 700, 200), minor=False)
    axes[2].tick_params(axis='x', labelsize=20)
    axes[2].tick_params(axis='y', labelsize=20)
    axes[2].legend(['Demand', 'Excess'], loc='upper left', fontsize=18)

    # cdict = {'region_1_wind': '#5b5bae',
    #      'region_1_pv': '#ffde32',
    #      'region_1_bat': '#42c77a',
    #      'region_1_gridsource': '#636f6b',
    #      'region_1_demand': '#830000',
    #      }

    # fig = plt.figure(figsize=(24, 14))
    # plt.rc('legend', **{'fontsize': 14})
    # plt.rcParams.update({'font.size': 24})
    # plt.style.use('ggplot')

    # plt.subplots_adjust(hspace=0.1, left=0.07, right=0.9)

    # handles, labels = esplot.io_plot(
    #     "region_1_bel", cdict, ax=fig.add_subplot(3, 1, 1),
    #     date_from=year+"-06-01 00:00:00", date_to=year+"-06-8 00:00:00",
    #     line_kwa={'linewidth': 4})

    # labels = fix_labels(labels)
    # esplot.outside_legend(handles=handles, labels=labels)
    # esplot.ax.set_ylabel('Power in MW')
    # esplot.ax.set_xlabel('')
    # esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    # esplot.ax.set_xticklabels([])

    # handles, labels = esplot.io_plot(
    #     "region_1_bel", cdict, ax=fig.add_subplot(3, 1, 2),
    #     date_from=year+"-06-01 00:00:00", date_to=year+"-06-8 00:00:00",
    #     line_kwa={'linewidth': 4})

    # labels = fix_labels(labels)
    # esplot.outside_legend(handles=handles, labels=labels)
    # esplot.ax.set_ylabel('Power in MW')
    # esplot.ax.set_xlabel('')
    # esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    # esplot.ax.set_xticklabels([])

    # handles, labels = esplot.io_plot(
    #     "region_1_bel", cdict, ax=fig.add_subplot(3, 1, 3),
    #     date_from=year+"-06-01 00:00:00", date_to=year+"-06-8 00:00:00",
    #     line_kwa={'linewidth': 4})

    # labels = fix_labels(labels)
    # esplot.outside_legend(handles=handles, labels=labels)
    # esplot.ax.set_ylabel('Power in MW')
    # esplot.ax.set_xlabel('Date')
    # esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')

    fig.savefig(os.path.join(os.path.dirname(__file__), 'current_figure.pdf'))
    plt.tight_layout()
    plt.show(fig)

def main(**arguments):

    logger.define_logging()
    parameters = read_and_calculate_parameters(**arguments)

    for loopi in parameters['loop']:
        esys = initialise_energysystem(year=arguments['--year'],
                                   number_timesteps=int(
                                       arguments['--timesteps']))
        esys = create_energysystem(esys,
                                   parameters,
                                   loopi,
                                   **arguments)
        # esys.dump()
        # esys.restore()
        pp.pprint(get_result_dict(esys, parameters, loopi, **arguments))
        # create_plots(esys, year=arguments['--year'])
        results = get_result_dict(esys, parameters, loopi, **arguments)
        create_subplot(esys, results, year=arguments['--year'])

        del esys


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    if arguments["--dry-run"]:
        print("This is a dry run. Exiting before doing anything.")
        exit(0)
    arguments = validate(**arguments)
    main(**arguments)
