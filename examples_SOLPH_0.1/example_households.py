# -*- coding: utf-8 -*-

''' Example for simulating pv-battery systems in quarters

Usage: example_quartier_10hh_11_to_20.py [options]

Options:

  -o, --solver=SOLVER      The solver to use. Should be one of "glpk", "cbc"
                           or "gurobi".
                           [default: gurobi]
  -l, --loglevel=LOGLEVEL  Set the loglevel. Should be one of DEBUG, INFO,
                           WARNING, ERROR or CRITICAL.
                           [default: ERROR]
  -h, --help               Display this help.
      --start-hh=START     Household to start when choosing from household
                           pool. Counts a chosen number of households up
                           from start-hh, see next option.
                           [default: 1]
      --num-hh=NUM         Number of households to choose. [default: 10]
      --ssr=SSR            Self-sufficiency degree. [default: 0.7]
      --year=YEAR          Weather data year. Choose from 1998, 2003, 2007,
                           2010-2014. [default: 2010]
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
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph.network import Investment
from oemof.solph import OperationalModel

# import helper to read coastdat data
from eos import helper_coastdat as hlp


def initialise_energysystem(year, number_timesteps=8760):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/' + year,
                                    periods=number_timesteps,
                                    freq='H')

    return core_es.EnergySystem(groupings=solph.GROUPINGS,
                                time_idx=date_time_index)


def validate(**arguments):
    valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if arguments["--loglevel"] not in valid:
        exit("Invalid loglevel: " + arguments["--loglevel"])
    return arguments


def optimise_storage_size(energysystem,
                          **arguments):

    hh_start = int(arguments['--start-hh'])
    hh_to_choose = np.arange(hh_start, hh_start+int(arguments['--num-hh']))
    hh = {}
    for i in np.arange(int(arguments['--num-hh'])):
        hh['house_' + str(i+1)] = 'hh_' + str(hh_to_choose[i])

    # read load data in kW
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
        'latitude': 53.41,
        'longitude': 11.84}    # Parchim

    data_pv = hlp.get_pv_generation(year=int(arguments['--year']),
                                    azimuth=180,
                                    tilt=30,
                                    albedo=0.2,
                                    loc=loc)

    ##########################################################################
    # Create oemof object
    ##########################################################################

    ssr = float(arguments['--ssr'])
    grid_share = 1 - ssr

    logging.info('Create oemof objects')

    # create electricity bus
    bel = {bustype: solph.Bus(
              uid=bustype,
              type=bustype,
              balanced=True,
              excess=False)
           for bustype in hh}

    # create excess component for the electricity bus to allow overproduction
    [solph.Sink(
        label=label + 'excess_bel',
        inputs={bel[label]: solph.Flow()})
        for label in hh]

    # create commodity object for import electricity resource
    [solph.Source(
        label=label + '_gridsource',
        outputs={bel[label]: solph.Flow(
            nominal_value=consumption_of_chosen_households
            [label] *
            grid_share,
            summed_max=1)})
        for label in hh]

    # create fixed source object for pv
    [solph.Source(
        label=label + '_pv',
        outputs={bel[label]: solph.Flow(actual_value=data_pv,
                                        nominal_value=10,
                                        fixed=True, fixed_costs=15)})
        for label in hh]

    # create simple sink objects for demands 1 to 10
    [solph.Sink(
        label=label + '_demand',
        inputs={bel[label]: solph.Flow(actual_value=data_load[str(hh[label])],
                fixed=True, nominal_value=1)})
        for label in hh]

    # Calculate ep_costs from capex to compare with old solph
    capex = 375
    lifetime = 10
    wacc = 0.07
    epc = capex * (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1
                                                     )

    # create storage transformer object for storage
    [solph.Storage(
        label=label + 'ces',
        inputs={bel[label]: solph.Flow(variable_costs=0)},
        outputs={bel[label]: solph.Flow(variable_costs=0)},
        capacity_loss=0.00,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        fixed_costs=0,
        investment=Investment(ep_costs=epc),
    )
        for label in hh]

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


def get_result_dict(energysystem, year):
    logging.info('Check the results')
    ces = energysystem.groups['ces']
    myresults = outputlib.DataFramePlot(energy_system=energysystem)

    gridsource = myresults.slice_by(obj_label='house_1_gridsource',
                                    type='input',
                                    date_from=year + '-01-01 00:00:00',
                                    date_to=year + '-12-31 23:00:00')

    demand_1 = myresults.slice_by(obj_label='house_1_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_2 = myresults.slice_by(obj_label='house_2_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_3 = myresults.slice_by(obj_label='house_3_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_4 = myresults.slice_by(obj_label='house_4_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_5 = myresults.slice_by(obj_label='house_5_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_6 = myresults.slice_by(obj_label='house_6_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_7 = myresults.slice_by(obj_label='house_7_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_8 = myresults.slice_by(obj_label='house_8_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_9 = myresults.slice_by(obj_label='house_9_demand',
                                  date_from=year + '-01-01 00:00:00',
                                  date_to=year + '-12-31 23:00:00')

    demand_10 = myresults.slice_by(obj_label='house_10_demand',
                                   date_from=year + '-01-01 00:00:00',
                                   date_to=year + '-12-31 23:00:00')

    pv = myresults.slice_by(obj_label='house_1_pv',
                            date_from=year + '-01-01 00:00:00',
                            date_to=year + '-12-31 23:00:00')

    return {'gridsource_sum': gridsource.sum(),
            'demand_sum_1': demand_1.sum(),
            'demand_sum_2': demand_2.sum(),
            'demand_sum_3': demand_3.sum(),
            'demand_sum_4': demand_4.sum(),
            'demand_sum_5': demand_5.sum(),
            'demand_sum_6': demand_6.sum(),
            'demand_sum_7': demand_7.sum(),
            'demand_sum_8': demand_8.sum(),
            'demand_sum_9': demand_9.sum(),
            'demand_sum_10': demand_10.sum(),
            'pv_sum': pv.sum(),
            'pv_inst': pv.max()/0.76474,
            'storage_cap': energysystem.results[ces][ces].invest,
            'objective': energysystem.results.objective
            }


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
    logger.define_logging()
    esys = initialise_energysystem(year=arguments['--year'])
    esys = optimise_storage_size(esys, **arguments)
    esys.dump()
    # esys.restore()
    import pprint as pp
    pp.pprint(get_result_dict(esys, year=arguments['--year']))
    create_plots(esys, year=arguments['--year'])


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    if arguments["--dry-run"]:
        print("This is a dry run. Exiting before doing anything.")
        exit(0)
    arguments = validate(**arguments)
    main(**arguments)
