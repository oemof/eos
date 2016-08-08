# -*- coding: utf-8 -*-

''' Example for simulating one node.

Usage: example_one_node.py [options]

Options:

  -o, --solver=SOLVER      The solver to use. Should be one of "glpk", "cbc"
                           or "gurobi".
                           [default: cbc]
  -l, --loglevel=LOGLEVEL  Set the loglevel. Should be one of DEBUG, INFO,
                           WARNING, ERROR or CRITICAL.
                           [default: ERROR]
  -t, --timesteps=TSTEPS   Set number of timesteps. [default: 8760]
  -h, --help               Display this help.
      --lat=LAT            Sets the simulation longitude to choose the right
                           weather data set. [default: 53.41] # Parchim
      --lon=LON            Sets the simulation latitude to choose the right
                           weather data set. [default: 11.84] # Parchim
      --year=YEAR          Weather data year. Choose from 1998, 2003, 2007,
                           2010-2014. [default: 2010]
      --pv-costopt         Cost optimization for pv plants.
      --feedin             Option with different pv plants (will need
                           scenario_pv.csv) and max feedin
      --write-results      write results to data/scenarioname_results.csv
      --ssr=SSR            Self-sufficiency degree.
      --tau=TAU            Time increment of load profile. [default: 1]
      --dry-run            Do nothing. Only print what would be done.

'''

###############################################################################
# imports
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import logging
import csv
import pickle
import pprint as pp

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

# import helper to read coastdat data
from eos import helper_coastdat as hlp


def initialise_energysystem(year, number_timesteps):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/' + year,
                                    periods=number_timesteps,
                                    freq='15Min')

    return solph.EnergySystem(groupings=solph.GROUPINGS,
                              time_idx=date_time_index)


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

    # Tech parameters
    cap_loss = 0
    c_rate = 1/6
    eta_in = 1
    eta_out = 0.8

    # Cost parameters
    price_el = 0.15
    fit = 0
    sc_tax = 0
    opex_fix_bat = 0
    opex_fix_pv = 0

    pv_inst = 200
    max_feedin = 100

    # Calculate ep_costs from capex
    storage_capex = 375
    storage_lifetime = 10
    storage_wacc = 0.07
    storage_epc = storage_capex * (storage_wacc * (1 + storage_wacc) **
                                   storage_lifetime) / ((1 + storage_wacc) **
                                                        storage_lifetime - 1)

    pv_capex = 1000
    pv_lifetime = 20
    pv_wacc = 0.07
    pv_epc = pv_capex * (pv_wacc * (1 + pv_wacc) **
                         pv_lifetime) / ((1 + pv_wacc) ** pv_lifetime - 1)

    # Read load data in kW
    data_load = \
        pd.read_csv(
                 "../example/example_data/load_2015_15min.csv",
                 sep=",")

    data_load = data_load['load']

    # Read standardized feed-in from pv
    # loc = {
    #     'tz': 'Europe/Berlin',
    #     'latitude': float(arguments['--lat']),
    #     'longitude': float(arguments['--lon'])}

    # data_pv = hlp.get_pv_generation(
    #                 year=int(arguments['--year']),
    #                 azimuth=180,
    #                 tilt=30,
    #                 albedo=0.2,
    #                 loc=loc)

    # Or read pv data from file
    data_pv = \
        pd.read_csv(
                 "../example/example_data/osna_pv_15min.csv",
                 sep=",")

    data_pv = data_pv['pv']

    # Calculate grid share
    if arguments['--ssr']:
        grid_share = 1 - float(arguments['--ssr'])

    else:
        grid_share = None

    parameters = {'price_el': price_el,
                  'fit': fit,
                  'sc_tax': sc_tax,
                  'opex_fix_bat': opex_fix_bat,
                  'opex_fix_pv': opex_fix_pv,
                  'cap_loss': cap_loss,
                  'c_rate': c_rate,
                  'eta_in': eta_in,
                  'eta_out': eta_out,
                  'pv_inst': pv_inst,
                  'max_feedin': max_feedin,
                  'storage_epc': storage_epc,
                  'pv_epc': pv_epc,
                  'data_load': data_load,
                  'data_pv': data_pv,
                  'grid_share': grid_share}

    logging.info('Check parameters')

    return parameters


def create_energysystem(energysystem, parameters,
                        **arguments):

    ##########################################################################
    # Create oemof object
    ##########################################################################
    logging.info('Create oemof objects')

    # Create electricity bus for demand
    bel_demand = solph.Bus(label="bel_demand")

    # Create storage transformer object for storage
    solph.Storage(
        label='bat',
        inputs={bel_demand: solph.Flow(variable_costs=0)},
        outputs={bel_demand: solph.Flow(variable_costs=0)},
        capacity_loss=parameters['cap_loss'],
        nominal_input_capacity_ratio=parameters['c_rate'],
        nominal_output_capacity_ratio=parameters['c_rate'],
        inflow_conversion_factor=parameters['eta_in'],
        outflow_conversion_factor=parameters['eta_out'],
        fixed_costs=parameters['opex_fix_bat'],
        investment=solph.Investment(ep_costs=parameters['storage_epc']))

    # Create commodity object for import electricity resource
    if arguments['--ssr']:
        solph.Source(
            label='gridsource',
            outputs={bel_demand: solph.Flow(
                nominal_value=sum(parameters['data_load']) *
                parameters['grid_share'],
                summed_max=1)})

    else:
        solph.Source(label='gridsource', outputs={
            bel_demand: solph.Flow(
                variable_costs=parameters['price_el'])})

    # Create electricity bus for pv
    bel_pv = solph.Bus(label="bel_pv")

    # Create excess component for bel_pv to allow overproduction
    solph.Sink(label="excess", inputs={bel_pv: solph.Flow()})

    # Create sink component for the pv feedin
    if arguments['--feedin']:
        solph.Sink(label='feedin', inputs={bel_pv: solph.Flow(
            variable_costs=parameters['fit'],
            nominal_value=100,  # TODO: abhängig von PV!
            max=parameters['max_feedin'])})

    # Create linear transformer to connect pv and demand bus
    solph.LinearTransformer(
        label="sc_Transformer",
        inputs={bel_pv: solph.Flow(variable_costs=parameters['sc_tax'])},
        outputs={bel_demand: solph.Flow()},
        conversion_factors={bel_demand: 1})

    # Create fixed source object for pv
    if arguments['--pv-costopt']:
        solph.Source(label='pv', outputs={bel_pv: solph.Flow(
            actual_value=parameters['data_pv'],
            fixed=True,
            fixed_costs=parameters['opex_fix_pv'],
            investment=solph.Investment(ep_costs=parameters['pv_epc']))})

    else:
        solph.Source(label='pv', outputs={bel_pv: solph.Flow(
            actual_value=parameters['data_pv'],
            nominal_value=parameters['pv_inst'],
            fixed=True,
            fixed_costs=parameters['opex_fix_pv'])})

    # Create simple sink objects for demands
    solph.Sink(
        label="demand",
        inputs={bel_demand: solph.Flow(
            actual_value=parameters['data_load'],
                fixed=True,
                nominal_value=1)})

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')
    print(energysystem.time_idx)

    om = solph.OperationalModel(energysystem, timeindex=energysystem.time_idx,
                                timeincrement=float(arguments['--tau']))

    logging.info('Store lp-file')
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})

    logging.info('Solve the optimization problem')
    om.solve(solver=arguments['--solver'], solve_kwargs={'tee': True})

    return energysystem


def get_result_dict(energysystem, parameters, **arguments):
    logging.info('Check the results')

    year = arguments['--year']

    results_dc = {}
    myresults = outputlib.DataFramePlot(energy_system=energysystem)
    print(myresults)

    storage = energysystem.groups['bat']
    pv_i = energysystem.groups['pv']
    pv_bel = energysystem.groups['bel_pv']

    demand = myresults.slice_by(obj_label='demand',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00')

    pv = myresults.slice_by(obj_label='pv',
                            date_from=year+'-01-01 00:00:00',
                            date_to=year+'-12-31 23:00:00')

    excess = myresults.slice_by(obj_label='excess',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00')

    sc = myresults.slice_by(obj_label='sc_Transformer',
                            date_from=year+'-01-01 00:00:00',
                            date_to=year+'-12-31 23:00:00')

    grid = myresults.slice_by(obj_label='gridsource',
                              date_from=year+'-01-01 00:00:00',
                              date_to=year+'-12-31 23:00:00')

    bat = myresults.slice_by(obj_label='bat',
                             date_from=year+'-01-01 00:00:00',
                             date_to=year+'-12-31 23:00:00')


    if arguments['--feedin']:
        feedin = myresults.slice_by(obj_label='_feedin',
                                    date_from=year+'-01-01 00:00:00',
                                    date_to=year+'-12-31 23:00:00')
        results_dc['feedin'] = float(feedin.sum())
    else:
        results_dc['feedin'] = 0

    if arguments['--pv-costopt']:
        pv_inst = energysystem.results[pv_i][pv_bel].invest
        results_dc['pv_inst'] = pv_inst
    else:
        results_dc['pv_inst'] = parameters['pv_inst']

    #  cost_calculation:
    pv_cost = (parameters['pv_epc'] + parameters['opex_fix_pv']) * \
        results_dc['pv_inst']
    storage_cost = (
        parameters['storage_epc'] + parameters['opex_fix_bat']) * \
        energysystem.results[storage][storage].invest
    sc_cost = float(sc.sum()) * parameters['sc_tax']
    grid_cost = float(grid.sum()) * parameters['price_el']
    fit_cost = results_dc['feedin'] * parameters['fit']
    whole_cost = storage_cost + sc_cost + grid_cost + fit_cost + pv_cost
    price_el_mix = whole_cost / float(demand.sum())

    results_dc['demand'] = demand.sum()
    results_dc['pv'] = pv.sum()
    results_dc['pv_max'] = pv.max()
    results_dc['excess'] = excess.sum()
    results_dc['self_con'] = sc.sum() / 2
    results_dc['grid'] = grid.sum()
    results_dc['check_ssr'] = 1 - (grid.sum() / demand.sum())
    results_dc['bat'] = bat.sum()
    results_dc['storage_cap'] = energysystem.results[
        storage][storage].invest
    results_dc['price_el_mix_'] = price_el_mix
    results_dc['cost_pv_'] = pv_cost
    results_dc['cost_storage_'] = storage_cost
    results_dc['cost_sc_'] = sc_cost
    results_dc['cost_grid_'] = grid_cost
    results_dc['cost_fit_'] = fit_cost
    results_dc['objective'] = energysystem.results.objective

    return(results_dc)


def create_plots(energysystem, year):
    logging.info('Plot results')
    myresults = outputlib.DataFramePlot(energy_system=energysystem)
    gridsource = myresults.slice_by(obj_label='gridsource', type='input',
                                    date_from=year + '-01-01 00:00:00',
                                    date_to=year + '-12-31 23:00:00')

    imp = gridsource.sort_values(by='val', ascending=False).reset_index()

    imp.plot(linewidth=1.5)

    plt.show()


def main(**arguments):
    logger.define_logging()
    esys = initialise_energysystem(year=arguments['--year'],
                                   number_timesteps=int(
                                       arguments['--timesteps']))
    parameters = read_and_calculate_parameters(**arguments)
    esys = create_energysystem(esys,
                               parameters,
                               **arguments)
    esys.dump()
    # esys.restore()
    import pprint as pp
    results = get_result_dict(esys, parameters, **arguments)
    pp.pprint(results)
#    create_plots(esys, year=arguments['--year'])


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    if arguments["--dry-run"]:
        print("This is a dry run. Exiting before doing anything.")
        exit(0)
    arguments = validate(**arguments)
    main(**arguments)
