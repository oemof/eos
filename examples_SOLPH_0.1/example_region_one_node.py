# -*- coding: utf-8 -*-

''' Example for simulating pv-battery systems in quarters

Usage: example_quartier_10hh_11_to_20.py [options]

Options:

  -s, --scenario=SCENARIO  The scenario name. [default: scenario]
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
      --num-regions=NUM    Number of regions. [default: 24]
      --costopt            Cost optimization.
      --ssr=SSR            Self-sufficiency degree.
      --dry-run            Do nothing. Only print what would be done.

'''

###############################################################################
# imports
###############################################################################
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

    # Read parameter csv files
    region_parameter = pd.read_csv(
        'scenarios_region/' + arguments['--scenario'] +
        '_region_parameter.csv',
        delimiter=',', index_col=0)

    cost_parameter = pd.read_csv(
        'scenarios_region/' + arguments['--scenario'] + '_cost_parameter.csv',
        delimiter=',', index_col=0)

    tech_parameter = pd.read_csv(
        'scenarios_region/' + arguments['--scenario'] + '_tech_parameter.csv',
        delimiter=',', index_col=0)

    data = pd.read_csv("../example/example_data/storage_invest.csv", sep=',')
    data_load = data['demand_el']  # demand in kW
    data_wind = data['wind']
    data_pv = data['pv']

    # residual = data_load - (data['wind']*wind_installed*1e3
    #                                 + data['pv']*pv_installed*1e3)
    # positive = residual.where(residual > 0, 0)
    # negative = residual.where(residual < 0, 0)
    # print(positive.sum())
    # print(negative.sum())
    # print('len',len(negative.nonzero()[0]))

    # Calculate ep_costs from capex
    storage_capex = cost_parameter.loc['storage']['capex']
    storage_lifetime = cost_parameter.loc['storage']['lifetime']
    storage_wacc = cost_parameter.loc['storage']['wacc']
    storage_epc = storage_capex * (storage_wacc * (1 + storage_wacc) **
                                   storage_lifetime) / ((1 + storage_wacc) **
                                                        storage_lifetime - 1)

    # Calculate grid share
    if arguments['--ssr']:
        grid_share = 1 - float(arguments['--ssr'])

    else:
        grid_share = None

    parameters = {'region_parameter': region_parameter,
                  'cost_parameter': cost_parameter,
                  'tech_parameter': tech_parameter,
                  'data': data,
                  'data_load': data_load,
                  'data_wind': data_wind,
                  'data_pv': data_pv,
                  'storage_epc': storage_epc,
                  'grid_share': grid_share,
                  }

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

    for region in range(int(arguments['--num-regions'])):

        # Create electricity bus for demand
        bel = solph.Bus(label='region_'+str(region)+'_bel')

        # Create storage transformer object for storage
        solph.Storage(
            label='region_'+str(region)+'_bat',
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
            fixed_costs=parameters[
                'cost_parameter'].loc['storage']['opex_fix'],
            investment=solph.Investment(ep_costs=parameters['storage_epc']))

        # Create commodity object for import electricity resource
        if arguments['--ssr']:
            solph.Source(
                label='region_'+str(region)+'_gridsource',
                outputs={bel: solph.Flow(
                    nominal_value=(float(parameters
                                   ['region_parameter'].loc
                                   ['annual_demand_GWh'][region]) *
                                   1e6 * parameters['grid_share']),
                    summed_max=1)})

        else:
            print('Cost optimization is not implemented yet')
            # solph.Source(label='region_'+str(region)+'_gridsource', outputs={
            #     bel: solph.Flow(
            #         variable_costs=parameters['price_el'])})

        # Create excess component to allow overproduction
        solph.Sink(label='region_'+str(region)+'__excess',
                   inputs={bel: solph.Flow()})

        # Create fixed source object for wind

        if arguments['--costopt']:
            print('Cost optimization is not implemented yet')
            # solph.Source(label='region_'+str(region)+'_wind',
            #              outputs={bel: solph.Flow(
            #                       actual_value=parameters['data_wind'],
            #                       fixed=True,
            #                       fixed_costs=parameters['opex_wind'],
            #                       investment=solph.Investment(
            #                           ep_costs=parameters['wind_epc']))})

        else:
            test=solph.Source(label='region_'+str(region)+'_wind',
                         outputs={bel: solph.Flow(
                                  actual_value=parameters['data_wind'],
                                  nominal_value=float(parameters['region_parameter'].
                                  loc['wind_MW'][region])*1e3,
                                  fixed=True)})

        # Create fixed source object for pv
        if arguments['--costopt']:
            print('Cost optimization is not implemented yet')
            # solph.Source(label='region_'+str(region)+'_pv',
            #              outputs={bel: solph.Flow(
            #                       actual_value=parameters['data_pv'],
            #                       fixed=True,
            #                       fixed_costs=parameters['opex_pv'],
            #                       investment=solph.Investment(
            #                           ep_costs=parameters['pv_epc']))})

        else:
            test2=solph.Source(label='region_'+str(region)+'_pv',
                         outputs={bel: solph.Flow(
                                  actual_value=parameters['data_pv'],
                                  nominal_value=float(parameters['region_parameter'].
                                  loc['pv_MW'][region])*1e3,
                                  fixed=True)})

        # Create simple sink objects for demands
        solph.Sink(label='region_'+str(region)+'_demand',
                   inputs={bel: solph.Flow(
                           actual_value=(parameters['data_load'] /
                                         parameters['data_load'].sum() *
                                         float(parameters['region_parameter'].
                                         loc['annual_demand_GWh'][region])*1e6),

                           fixed=True,
                           nominal_value=1)})


    print(test)
    # print(test).nominal_value
    # print(test2).nominal_value
    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = solph.OperationalModel(energysystem, timeindex=energysystem.time_idx)

    logging.info('Store lp-file')
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})

    logging.info('Solve the optimization problem')
    om.solve(solver=arguments['--solver'], solve_kwargs={'tee': True})

    return energysystem


def get_result_dict(energysystem, parameters, **arguments):
    logging.info('Check the results')

    year = arguments['--year']

    myresults = outputlib.DataFramePlot(energy_system=energysystem)

    grid = myresults.slice_by(obj_label='gridsource',
                              date_from=year+'-01-01 00:00:00',
                              date_to=year+'-12-31 23:00:00')

    bat = myresults.slice_by(obj_label='bat',
                             date_from=year+'-01-01 00:00:00',
                             date_to=year+'-12-31 23:00:00')

    storage = energysystem.groups['bat']

    demand = myresults.slice_by(obj_label=house+'_demand',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00')

    pv = myresults.slice_by(obj_label=house+'_pv',
                            date_from=year+'-01-01 00:00:00',
                            date_to=year+'-12-31 23:00:00')

    excess = myresults.slice_by(obj_label=house+'_excess',
                                date_from=year+'-01-01 00:00:00',
                                date_to=year+'-12-31 23:00:00')

    # if arguments['--pv-costopt']:
        # pv_inst = energysystem.results[pv][pv].invest
        # results_dc['pv_inst'+house] = pv_inst

    results_dc['demand_'+house] = demand.sum()
    results_dc['pv_'+house] = pv.sum()
    results_dc['pv_max_'+house] = pv.max()
    results_dc['excess_'+house] = excess.sum()
    results_dc['self_con_'+house] = sc.sum() / 2
    # TODO get in or oputflow of transformer
    results_dc['check_ssr'+house] = 1 - (grid.sum() / demand.sum())
    results_dc['bat_'+house] = bat.sum()

    results_dc['grid'] = grid.sum()
    results_dc['storage_cap'] = energysystem.results[
        storage][storage].invest
    results_dc['objective'] = energysystem.results.objective
# print('pp_gas_sum: ', pp_gas.sum())
# print('demand_sum: ', demand.sum())
# print('demand_max: ', demand.max())
# print('wind_sum: ', wind.sum())
# print('wind_max: ', wind.max())
# print('pv_sum: ', pv.sum())
# print('pv_max: ', pv.max()/0.7647)
# print('biogas_pot: ', bhkw.sum()/0.38)

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
    pp.pprint(get_result_dict(esys, parameters, **arguments))
#    create_plots(esys, year=arguments['--year'])


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    if arguments["--dry-run"]:
        print("This is a dry run. Exiting before doing anything.")
        exit(0)
    arguments = validate(**arguments)
    main(**arguments)
