# -*- coding: utf-8 -*-

''' Example for simulating pv-battery systems in quarters

Usage: example_quartier_10hh_11_to_20.py [options]

Options:

  -s, --scenario=SCENARIO  The scenario name. [default: scenario_parchim]
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
      --start-hh=START     Household to start when choosing from household
                           pool. Counts a chosen number of households up
                           from start-hh, see next option.
                           [default: 1]
      --num-hh=NUM         Number of households to choose. [default: 2]
      --ssr=SSR            Self-sufficiency degree.
      --year=YEAR          Weather data year. Choose from 1998, 2003, 2007,
                           2010-2014. [default: 2010]
      --parchim=PARCHIM    Option with different pv plants (will need
                           scenario_pv.csv) and max feedin [default: True]
      --dry-run            Do nothing. Only print what would be done.

'''

###############################################################################
# imports
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import logging

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
from oemof.solph import OperationalModel

# import helper to read coastdat data
from eos import helper_coastdat as hlp

def initialise_energysystem(year, number_timesteps):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/' + year,
                                    periods=number_timesteps,
                                    freq='H')

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
    print(arguments['--scenario'])

    # Read parameter csv files
    cost_parameter = pd.read_csv(
        'data/' + arguments['--scenario'] + '_cost_parameter.csv',
        delimiter=',', index_col=0)

    tech_parameter = pd.read_csv(
        'data/' + arguments['--scenario'] + '_tech_parameter.csv',
        delimiter=',', index_col=0)

    if arguments['--parchim'] is True:
        pv_parameter = pd.read_csv(
            'data/' + arguments['--scenario'] + '_pv.csv',
            delimiter=';')
    else:
        pv_parameter = 0

    print('pv_parameter:')
    print(pv_parameter)

    # Electricity from grid price
    price_el = cost_parameter.loc['grid']['opex_var']
    fit = cost_parameter.loc['fit']['opex_var']
    sc_tax = cost_parameter.loc['sc']['opex_var']
    opex_pv = cost_parameter.loc['pv']['opex_fix']
    opex_bat = cost_parameter.loc['storage']['opex_fix']

    max_feedin = tech_parameter.loc['pv']['max_feedin']

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

    # Choose households according to simulation options
    hh_start = int(arguments['--start-hh'])
    hh_to_choose = np.arange(hh_start, hh_start+int(arguments['--num-hh']))
    hh = {}
    for i in np.arange(int(arguments['--num-hh'])):
        hh['house_' + str(i+1)] = 'hh_' + str(hh_to_choose[i])

    # Read load data in kW
    data_load = \
        pd.read_csv(
            "../example/example_data/example_data_load_hourly_mean.csv",
            sep=",") / 1000

    consumption_of_chosen_households = {}
    for i in np.arange(int(arguments['--num-hh'])):
        consumption_of_chosen_households['house_' + str(i+1)] = \
            data_load[str(hh['house_' + str(i+1)])].sum()

    # read standardized feed-in from pv
    loc = {
        'tz': 'Europe/Berlin',
        'latitude': float(arguments['--lat']),
        'longitude': float(arguments['--lon'])}

    data_pv = hlp.get_pv_generation(year=int(arguments['--year']),
                                    azimuth=180,
                                    tilt=30,
                                    albedo=0.2,
                                    loc=loc)

    # Calculate grid share
    if arguments['--ssr']:
        grid_share = 1 - float(arguments['--ssr'])

    else:
        grid_share = None

    parameters = {'cost_parameter': cost_parameter,
                  'tech_parameter': tech_parameter,
                  'pv_parameter': pv_parameter,
                  'price_el': price_el,
                  'fit': fit,
                  'sc_tax': sc_tax,
                  'max_feedin': max_feedin,
                  'opex_pv': opex_pv,
                  'opex_bat': opex_bat,
                  'storage_epc': storage_epc,
                  'pv_epc': pv_epc,
                  'data_load': data_load,
                  'data_pv': data_pv,
                  'grid_share': grid_share,
                  'hh': hh,
                  'consumption_households': consumption_of_chosen_households,
                  'loc': loc}

    logging.info('Check parameters')
    print(parameters['cost_parameter'])
    print(parameters['tech_parameter'])

    return parameters


def create_energysystem(energysystem, parameters,
                        **arguments):

    ##########################################################################
    # Create oemof object
    ##########################################################################
    logging.info('Create oemof objects')

    house_pv = 0
    for house in parameters['hh']:
        house_pv = house_pv + 1
        label_pv = 'hh_' + str(house_pv)

        # create electricity bus for pv
        bel_pv = solph.Bus(label=house+"_bel_pv")

        # create electricity bus for demand
        bel_demand = solph.Bus(label=house+"_bel_demand")

        # create excess component for bel_pv to allow overproduction
        solph.Sink(label=house+"_excess", inputs={bel_pv: solph.Flow()})

        if arguments['--parchim'] is True:
            # create excess component for the pv feedin
            solph.Sink(label=house+'_feedin', inputs={bel_pv: solph.Flow(
                variable_costs=parameters['fit'],
                nominal_value=parameters['pv_parameter'][label_pv][0],
                max=parameters['max_feedin'])})

        # create commodity object for import electricity resource
        if arguments['--ssr']:
            solph.Source(
                label=house + '_gridsource',
                outputs={bel_demand: solph.Flow(
                    nominal_value=parameters['consumption_households']
                    [house] *
                    parameters['grid_share'],
                    summed_max=1)})

        else:
            solph.Source(label=house+'_gridsource', outputs={
                bel_demand: solph.Flow(
                    variable_costs=parameters['price_el'])})

        # create fixed source object for pv
        if arguments['--parchim'] is True:
            solph.Source(label=house+'_pv', outputs={bel_pv: solph.Flow(
                actual_value=hlp.get_pv_generation(
                    year=int(arguments['--year']),
                    azimuth=parameters['pv_parameter'][label_pv][1],
                    tilt=parameters['pv_parameter'][label_pv][2],
                    albedo=parameters['pv_parameter'][label_pv][3],
                    loc=parameters['loc']),
                nominal_value=parameters['pv_parameter'][label_pv][0],
                fixed=True,
                fixed_costs=parameters['opex_pv'])})
        else:
            solph.Source(label=house + '_pv', outputs={bel_pv: solph.Flow(
                actual_value=parameters['data_pv'],
                nominal_value=10,
                fixed=True, fixed_costs=15)})  # TODO: opex_pv???

        # create simple sink objects for demands
        solph.Sink(
            label=house+"_demand",
            inputs={bel_demand: solph.Flow(
                actual_value=parameters['data_load']
                    [str(parameters['hh'][house])],
                    fixed=True,
                    nominal_value=1)})

        # create storage transformer object for storage
        tech_parameter = parameters['tech_parameter']
        solph.Storage(
            label=house + '_bat',
            inputs={bel_demand: solph.Flow(variable_costs=0)},
            outputs={bel_demand: solph.Flow(variable_costs=0)},
            capacity_loss=tech_parameter.loc['storage']['cap_loss'],
            nominal_input_capacity_ratio=tech_parameter.loc['storage'][
                'c_rate'],
            nominal_output_capacity_ratio=tech_parameter.loc['storage'][
                'c_rate'],
            inflow_conversion_factor=tech_parameter.loc['storage']['eta_in'],
            outflow_conversion_factor=tech_parameter.loc['storage']['eta_out'],
            fixed_costs=parameters['opex_bat'],
            investment=solph.Investment(ep_costs=parameters['storage_epc']))

        # create linear transformer to connect pv and demand bus
        solph.LinearTransformer(
            label=house+"_sc_Transformer",
            inputs={bel_pv: solph.Flow(variable_costs=parameters['sc_tax'])},
            outputs={bel_demand: solph.Flow()},
            conversion_factors={bel_demand: 1})

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = OperationalModel(energysystem, timeindex=energysystem.time_idx)

    logging.info('Store lp-file')
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})

    logging.info('Solve the optimization problem')
    om.solve(solver=arguments['--solver'], solve_kwargs={'tee': True})

    return energysystem


def get_result_dict(energysystem, parameters, year):
    logging.info('Check the results')

    results_dc = {}
#    ces = energysystem.groups['ces']
    myresults = outputlib.DataFramePlot(energy_system=energysystem)

    for house in parameters['hh']:
        storage = energysystem.groups[house+'_bat']
        demand = myresults.slice_by(obj_label=house+'_demand',
                                    date_from=year+'-01-01 00:00:00',
                                    date_to=year+'-12-31 23:00:00')

        pv = myresults.slice_by(obj_label=house+'_pv',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00')

        excess = myresults.slice_by(obj_label=house+'_excess',
                                    date_from=year+'-01-01 00:00:00',
                                    date_to=year+'-12-31 23:00:00')

        sc = myresults.slice_by(obj_label=house+'_sc_Transformer',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00')

        grid = myresults.slice_by(obj_label=house+'_gridsource',
                                  date_from=year+'-01-01 00:00:00',
                                  date_to=year+'-12-31 23:00:00')

        bat = myresults.slice_by(obj_label=house+'_bat',
                                 date_from=year+'-01-01 00:00:00',
                                 date_to=year+'-12-31 23:00:00')
        if arguments['--parchim'] is True:
            feedin = myresults.slice_by(obj_label=house+'_feedin',
                                        date_from=year+'-01-01 00:00:00',
                                        date_to=year+'-12-31 23:00:00')
        else:
            feedin = [0,0]

        results_dc['demand_'+house] = demand.sum()
        results_dc['pv_'+house] = pv.sum()
        results_dc['pv_inst_'+house] = pv.max()
        results_dc['excess_'+house] = excess.sum()
        results_dc['feedin_'+house] = sum(feedin)
        results_dc['self_con_'+house] = sc.sum() / 2
        # TODO get in or oputflow of transformer
        results_dc['grid_'+house] = grid.sum()
        results_dc['objective'] = energysystem.results.objective
        results_dc['bat_'+house] = bat.sum()
        results_dc['storage_cap_'+house] = energysystem.results[
            storage][storage].invest
    return(results_dc)



def create_plots(energysystem, year):
    import_1 = gridsource_1.sort_values(by='val', ascending=False).reset_index()
    import_2 = gridsource_2.sort_values(by='val', ascending=False).reset_index()
    import_3 = gridsource_3.sort_values(by='val', ascending=False).reset_index()
    import_4 = gridsource_4.sort_values(by='val', ascending=False).reset_index()
    import_5 = gridsource_5.sort_values(by='val', ascending=False).reset_index()
    import_6 = gridsource_6.sort_values(by='val', ascending=False).reset_index()
    import_7 = gridsource_7.sort_values(by='val', ascending=False).reset_index()
    import_8 = gridsource_8.sort_values(by='val', ascending=False).reset_index()
    import_9 = gridsource_9.sort_values(by='val', ascending=False).reset_index()
    import_10 = gridsource_10.sort_values(by='val', ascending=False).reset_index()

    imp = pd.DataFrame(dict(hh_1=import_1.val, hh_2=import_2.val,
                            hh_3=import_3.val, hh_4=import_4.val,
                            hh_5=import_5.val, hh_6=import_6.val,
                            hh_7=import_7.val, hh_8=import_8.val,
                            hh_9=import_9.val, hh_10=import_10.val),
                            index=import_1.index)

    imp.plot(linewidth=1.5)

    plt.show()


def main(**arguments):
#    arguments['--parchim'] = True
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
    pp.pprint(get_result_dict(esys, parameters, year=arguments['--year']))
#    create_plots(esys, year=arguments['--year'])


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    if arguments["--dry-run"]:
        print("This is a dry run. Exiting before doing anything.")
        exit(0)
    arguments = validate(**arguments)
    main(**arguments)
