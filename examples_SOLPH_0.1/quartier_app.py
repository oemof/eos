# -*- coding: utf-8 -*-

''' Example for simulating pv-battery systems in quarters

Usage: example_quartier_10hh_11_to_20.py [options]

Options:

  -s, --scenario=SCENARIO  The scenario name. [default: scenario_parchim]
  -c, --cost=COST          The cost scenario. [default: 1]
  -o, --solver=SOLVER      The solver to use. Should be one of "glpk", "cbc"
                           or "gurobi".
                           [default: cbc]
  -h, --help               Display this help.
      --timesteps=TSTEPS   Set number of timesteps. [default: 8760]
      --lat=LAT            Sets the simulation longitude to choose the right
                           weather data set. [default: 53.41] # Parchim
      --lon=LON            Sets the simulation latitude to choose the right
                           weather data set. [default: 11.84] # Parchim
      --demand=DEM         Annual electric energy demand in MWh.
      --pv_installed=PV    Installed PV capacity in kWp.
      --profile=PROFILE    Load an own profile.
      --year=YEAR          Weather data year. Choose from 1998, 2003, 2007,
                           2010-2014. [default: 2010]
      --pv-costopt         Cost optimization for pv plants.
      --save               Save results.
      --dry-run            Do nothing. Only print what would be done.

'''

###############################################################################
# imports
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import logging
import pickle
from demandlib import bdew as bdew
from collections import OrderedDict

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
import sys
sys.path.append('/home/caro/rlihome/Git')
# from eos import helper_coastdat as hlp


def initialise_energysystem(year, number_timesteps):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/' + year,
                                    periods=number_timesteps,
                                    freq='H')

    return solph.EnergySystem(groupings=solph.GROUPINGS,
                              timeindex=date_time_index)


def read_and_calculate_parameters(**arguments):

    ###########################################################################
    # read and calculate parameters
    ###########################################################################

    logging.info('Read and calculate parameters')

    # Read parameter csv files
    cost_parameter = pd.read_csv(
        'data/' + arguments['--scenario'] +
            '_cost_parameter_' + str(arguments['--cost']) + '.csv',
        delimiter=',', index_col=0)

    tech_parameter = pd.read_csv(
        'data/' + arguments['--scenario'] +
            '_tech_parameter.csv',
        delimiter=',', index_col=0)

    # Electricity from grid price
    price_el = cost_parameter.loc['grid']['opex_var']
    fit = cost_parameter.loc['fit']['opex_var']
    sc_tax = cost_parameter.loc['sc']['opex_var']
    opex_pv = cost_parameter.loc['pv']['opex_fix']
    opex_bat = cost_parameter.loc['storage']['opex_fix']

    # Calculate ep_costs from capex
    storage_capex = cost_parameter.loc['storage']['capex']
    storage_lifetime = cost_parameter.loc['storage']['lifetime']
    storage_wacc = cost_parameter.loc['storage']['wacc']
    storage_epc = storage_capex * (storage_wacc * (1 + storage_wacc) **
                                   storage_lifetime) / ((1 + storage_wacc) **
                                                        storage_lifetime - 1)

    pv_capex = cost_parameter.loc['pv']['capex']
    pv_lifetime = cost_parameter.loc['pv']['lifetime']
    pv_wacc = cost_parameter.loc['pv']['wacc']
    pv_epc = pv_capex * (pv_wacc * (1 + pv_wacc) **
                         pv_lifetime) / ((1 + pv_wacc) ** pv_lifetime - 1)

    # Read load data and calculate total demand
    data_load = \
        pd.read_csv(
             "../example/example_data/example_data_load_hourly_mean_74_profiles.csv",
                 sep=",") / 1000

    e_slp = bdew.ElecSlp(int(arguments['--year']))
    h0_slp_15_min = e_slp.get_profile({'h0': 1})
    h0_slp = h0_slp_15_min.resample('H').mean()

    # Read standardized feed-in from pv
    # loc = {
    #     'tz': 'Europe/Berlin',
    #     'latitude': float(arguments['--lat']),
    #     'longitude': float(arguments['--lon'])}

    pv_generation = pd.read_csv(
              '../example/example_data/pv_generation_' + str(arguments['--year']) + '.csv', sep=",")

    pv_generation = pv_generation['pv']

    parameters = {'cost_parameter': cost_parameter,
                  'tech_parameter': tech_parameter,
                  'price_el': price_el,
                  'fit': fit,
                  'sc_tax': sc_tax,
                  'opex_pv': opex_pv,
                  'opex_bat': opex_bat,
                  'storage_epc': storage_epc,
                  'pv_epc': pv_epc,
                  'data_load': data_load,
                  'h0_slp': h0_slp['h0'],
                  # 'loc': loc,
                  'pv_generation': pv_generation}

    logging.info('Check parameters')
    print('cost parameter:\n', parameters['cost_parameter'])
    print('tech parameter:\n', parameters['tech_parameter'])

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
        fixed_costs=parameters['opex_bat'],
        investment=solph.Investment(ep_costs=parameters['storage_epc']))

    # Create commodity object for import electricity resource
    solph.Source(label='gridsource', outputs={
        bel_demand: solph.Flow(
            variable_costs=parameters['price_el'])})

    # Create electricity bus for pv
    bel_pv = solph.Bus(label="bel_pv")

    # Create excess component for bel_pv to allow overproduction
    solph.Sink(label="excess", inputs={bel_pv: solph.Flow()})

    # Create linear transformer to connect pv and demand bus
    solph.LinearTransformer(
        label="sc_Transformer",
        inputs={bel_pv: solph.Flow(variable_costs=parameters['sc_tax'])},
        outputs={bel_demand: solph.Flow()},
        conversion_factors={bel_demand: 1})

    if arguments['--pv-costopt']:
        solph.Source(label='pv', outputs={bel_pv: solph.Flow(
            actual_value=parameters['pv_generation'],
            fixed=True,
            fixed_costs=parameters['opex_pv'],
            investment=solph.Investment(ep_costs=parameters['pv_epc']))})

    else:
        solph.Source(label='pv', outputs={bel_pv: solph.Flow(
            actual_value=parameters['pv_generation'],
            nominal_value=float(arguments['--pv_installed']),
            fixed=True,
            fixed_costs=parameters['opex_pv'])})

    # Create simple sink objects for demands
    solph.Sink(
        label="demand",
        inputs={bel_demand: solph.Flow(
            actual_value=(parameters['h0_slp'] /
                sum(parameters['h0_slp']) *
                    float(arguments['--demand']) * 1e3),
                fixed=True,
                nominal_value=1)})

    return energysystem


def optimize_energysystem(energysystem):

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = solph.OperationalModel(energysystem)

#     logging.info('Store lp-file')
#     om.write('optimization_problem.lp',
#              io_options={'symbolic_solver_labels': True})
#
    logging.info('Solve the optimization problem')
    om.solve(solver=arguments['--solver'], solve_kwargs={'tee': True})

    return energysystem


def get_result_dict(energysystem, parameters, **arguments):
    logging.info('Check the results')

    year = arguments['--year']

    myresults = outputlib.DataFramePlot(energy_system=energysystem)

    grid = myresults.slice_by(obj_label='gridsource',
                              date_from=year+'-01-01 00:00:00',
                              date_to=year+'-12-31 23:00:00').reset_index(
                                                  ['bus_label', 'type', 'obj_label'],
                                                  drop=True)

    bat_input = myresults.slice_by(obj_label='bat', type='from_bus',
                                   date_from=year+'-01-01 00:00:00',
                                   date_to=year+'-12-31 23:00:00').reset_index(
                                                  ['bus_label', 'type', 'obj_label'],
                                                  drop=True)

    bat_output = myresults.slice_by(obj_label='bat', type='to_bus',
                                    date_from=year+'-01-01 00:00:00',
                                    date_to=year+'-12-31 23:00:00').reset_index(
                                                   ['bus_label', 'type', 'obj_label'],
                                                   drop=True)

    bat_soc = myresults.slice_by(obj_label='bat', type='other',
                                 date_from=year+'-01-01 00:00:00',
                                 date_to=year+'-12-31 23:00:00').reset_index(
                                                 ['bus_label', 'type', 'obj_label'],
                                                 drop=True)

    storage = energysystem.groups['bat']

    results_dc = {}
    demand_total = 0
    ts_demand_list = []
    ts_pv_list = []
    ts_excess_list = []
    ts_sc_list = []

    results_dc['ts_grid'] = grid
    results_dc['ts_bat_input'] = bat_input
    results_dc['ts_bat_output'] = bat_output
    results_dc['ts_bat_soc'] = bat_soc

    demand = myresults.slice_by(obj_label='demand',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00').reset_index(
                                        ['bus_label', 'type', 'obj_label'],
                                        drop=True)

    pv = myresults.slice_by(obj_label='pv',
                            date_from=year+'-01-01 00:00:00',
                            date_to=year+'-12-31 23:00:00').reset_index(
                                        ['bus_label', 'type', 'obj_label'],
                                        drop=True)

    excess = myresults.slice_by(obj_label='excess',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00').reset_index(
                                        ['bus_label', 'type', 'obj_label'],
                                        drop=True)

    sc = myresults.slice_by(obj_label='sc_Transformer', type='to_bus',
                            date_from=year+'-01-01 00:00:00',
                            date_to=year+'-12-31 23:00:00').reset_index(
                                        ['bus_label', 'type', 'obj_label'],
                                        drop=True)

    if arguments['--pv-costopt']:
        pv_i = energysystem.groups['pv']
        pv_bel = energysystem.groups['bel_pv']
        pv_inst = energysystem.results[pv_i][pv_bel].invest
        results_dc['pv_inst'] = pv_inst

    results_dc['demand'] = demand.sum()
    results_dc['ts_demand'] = demand
    demand_total = demand_total + demand.sum()
    results_dc['pv'] = pv.sum()
    results_dc['pv_max'] = pv.max()
    results_dc['ts_pv'] = pv
    results_dc['excess'] = excess.sum()
    results_dc['ts_excess'] = excess
    results_dc['self_con'] = sc.sum()
    # results_dc['check_ssr'] = 1 - (grid.sum() / demand.sum())

    ts_demand_list.append(demand)
    ts_pv_list.append(pv)
    ts_excess_list.append(excess)
    ts_sc_list.append(sc)

    results_dc['grid'] = grid.sum()
    results_dc['check_ssr'] = 1 - (grid.sum() / demand_total)
    results_dc['storage_cap'] = energysystem.results[
        storage][storage].invest
    results_dc['objective'] = energysystem.results.objective

    results_dc['cost_parameter'] = parameters['cost_parameter']
    results_dc['tech_parameter'] = parameters['tech_parameter']

    ts_demand_all = pd.concat(ts_demand_list, axis=1)
    ts_pv_all = pd.concat(ts_pv_list, axis=1)
    ts_excess_all = pd.concat(ts_excess_list, axis=1)
    ts_sc_all = pd.concat(ts_sc_list, axis=1)

    residual = ts_demand_all.sum(axis=1) - ts_pv_all.sum(axis=1)
    positive_residual = residual.where(residual >= 0, 0)
    covered_by_pv = ts_demand_all.sum(axis=1) - positive_residual
#     fig = plt.figure()
#     plt.plot(residual)
#     plt.plot(positive_residual)
#     plt.plot(ts_demand_all.sum(axis=1))
#     plt.plot(ts_pv_all.sum(axis=1))
#     plt.plot(covered_by_pv)
#     plt.legend(['residual', 'positive_residual', 'demand', 'pv', 'covered_by_pv'])
#     plt.show()

    results_dc['check_ssr_pv'] = covered_by_pv.sum() / demand_total

    # results_dc['mwh_to_kwp'] = results_dc['demand'] /1e3 / float(arguments['--pv_installed'])

    results_dc['ts_demand_all'] = ts_demand_all
    results_dc['ts_pv_all'] = ts_pv_all
    results_dc['ts_excess_all'] = ts_excess_all
    results_dc['ts_sc_all'] = ts_sc_all

    if arguments['--save']:
        pickle.dump(results_dc, open('../results/quartier_results_' +
                    str(arguments['--cost']) + '_' +
                    str(arguments['--year']) + '_' +
                    str(arguments['--pv_installed']) + '_' +
                    'slp_h0' + '.p', 'wb'))

    return(results_dc)


def create_plots(energysystem, year):

    logging.info('Plot results')

    cdict = {'wind': '#5b5bae',
             'pv': '#ffde32',
             'storage': '#42c77a',
             'demand': '#ce4aff',
             'excess_bel': '#555555'}

    # Plotting the input flows of the electricity bus for January
    myplot = outputlib.DataFramePlot(energy_system=energysystem)
    myplot.slice_unstacked(bus_label="bel_demand", type="from_bus",
                           date_from=year + "-01-01 00:00:00",
                           date_to=year + "-01-31 00:00:00")
    colorlist = myplot.color_from_dict(cdict)
    myplot.plot(color=colorlist, linewidth=2, title="January 2012")
    myplot.ax.legend(loc='upper right')
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.set_datetime_ticks(date_format='%d-%m-%Y', tick_distance=24*7)

    # Plotting the output flows of the electricity bus for January
    myplot.slice_unstacked(bus_label="bel_demand", type="output")
    myplot.plot(title="Year 2016", colormap='Spectral', linewidth=2)
    myplot.ax.legend(loc='upper right')
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.set_datetime_ticks()

    plt.show()

    # Plotting a combined stacked plot
    fig = plt.figure(figsize=(24, 14))
    plt.rc('legend', **{'fontsize': 19})
    plt.rcParams.update({'font.size': 19})
    plt.style.use('grayscale')

    handles, labels = myplot.io_plot(
        bus_label='bel_demand', cdict=cdict,
        barorder=['pv', 'wind', 'storage'],
        lineorder=['demand', 'storage', 'excess_bel'],
        line_kwa={'linewidth': 4},
        ax=fig.add_subplot(1, 1, 1),
        date_from=year + "-06-01 00:00:00",
        date_to=year + "-06-8 00:00:00",
        )
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.ax.set_title("Electricity bus")
    myplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    myplot.outside_legend(handles=handles, labels=labels)

    plt.show()

#     gridsource = myresults.slice_by(obj_label='gridsource', type='input',
#                                     date_from=year + '-01-01 00:00:00',
#                                     date_to=year + '-12-31 23:00:00')
#
#     imp = gridsource.sort_values(by='val', ascending=False).reset_index()
#
#     imp.plot(linewidth=1.5)
#
#     plt.show()
#

def main(**arguments):
    logger.define_logging()
    esys = initialise_energysystem(year=arguments['--year'],
                                   number_timesteps=int(
                                       arguments['--timesteps']))
    parameters = read_and_calculate_parameters(**arguments)
    esys = create_energysystem(esys,
                               parameters,
                               **arguments)
    esys = optimize_energysystem(esys)
    # esys.dump()
    # esys.restore()
    import pprint as pp
    results = get_result_dict(esys, parameters, **arguments)
    print('grid: ', results['grid'])
    print('check_ssr: ', results['check_ssr'])
    print('storage_cap: ', results['storage_cap'])
    print('objective: ', results['objective'])
    # print('mwh_to_kwp: ', results['mwh_to_kwp'])
    print('check_ssr_pv: ', results['check_ssr_pv'])
    # create_plots(esys, year=arguments['--year'])


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    if arguments["--dry-run"]:
        print("This is a dry run. Exiting before doing anything.")
        exit(0)
    main(**arguments)
