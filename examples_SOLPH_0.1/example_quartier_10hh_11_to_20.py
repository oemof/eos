# -*- coding: utf-8 -*-

"""
General description:
---------------------


"""

###############################################################################
# imports
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import logging

# Outputlib
from oemof.outputlib import to_pandas as tpd

# Default logger of oemof
from oemof.tools import logger

# import oemof core and solph classes to create energy system objects
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import (Bus, Source, Sink, Flow, Storage)
from oemof.solph.network import Investment
from oemof.solph import OperationalModel


def initialise_energysystem(number_timesteps=8760):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2012', periods=number_timesteps,
                                    freq='H')

    return core_es.EnergySystem(groupings=solph.GROUPINGS,
                                time_idx=date_time_index)


def optimise_storage_size(energysystem,
                          solvername='gurobi'):

    hh_start = 11

    hh_to_choose = np.arange(hh_start, hh_start+10)

    hh = {'demand_1': 'hh_' + str(hh_to_choose[0]),
          'demand_2': 'hh_' + str(hh_to_choose[1]),
          'demand_3': 'hh_' + str(hh_to_choose[2]),
          'demand_4': 'hh_' + str(hh_to_choose[3]),
          'demand_5': 'hh_' + str(hh_to_choose[4]),
          'demand_6': 'hh_' + str(hh_to_choose[5]),
          'demand_7': 'hh_' + str(hh_to_choose[6]),
          'demand_8': 'hh_' + str(hh_to_choose[7]),
          'demand_9': 'hh_' + str(hh_to_choose[8]),
          'demand_10': 'hh_' + str(hh_to_choose[9])}

    # read load data in kW
    data_load = \
            pd.read_csv(
                 "../example/example_data/example_data_load_hourly_mean.csv",
                 sep=",") / 1000

    # read standardized feed-in from wind and pv
    data_re = pd.read_csv(
            "../example/example_data/example_data_re.csv", sep=',')

    ##########################################################################
    # Create oemof object
    ##########################################################################

    ssr = 0.7  # noch als Uebergabewert implementieren
    grid_share = 1 - ssr

    logging.info('Create oemof objects')

    # create electricity bus
    bel = Bus(label="electricity")

    # create excess component for the electricity bus to allow overproduction
    Sink(label='excess_bel', inputs={bel: Flow()})

    # create commodity object for import electricity resource
    Source(label='gridsource', outputs={bel: Flow(nominal_value=45243*grid_share,
                                           summed_max=1)})

    # create fixed source object for pv
    Source(label='pv', outputs={bel: Flow(actual_value=data_re['pv'],
                                          nominal_value=100,
                                          fixed=True, fixed_costs=15)})

    # create simple sink objects for demands 1 to 10
    [Sink(
        label=demand,
        inputs={bel: Flow(actual_value=data_load[str(hh[demand])],
                fixed=True, nominal_value=1)})
        for demand in ['demand_1', 'demand_2', 'demand_3', 'demand_4',
                       'demand_5', 'demand_6', 'demand_7', 'demand_8',
                       'demand_9', 'demand_10']]

    # Calculate ep_costs from capex to compare with old solph
    capex = 375
    lifetime = 10
    wacc = 0.07
    epc = capex * (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)

    # create storage transformer object for storage
    Storage(
        label='ces',
        inputs={bel: Flow(variable_costs=0)},
        outputs={bel: Flow(variable_costs=0)},
        capacity_loss=0.00,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        fixed_costs=0,
        investment=Investment(ep_costs=epc),
    )

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = OperationalModel(energysystem, timeindex=energysystem.time_idx)

    logging.info('Solve the optimization problem')
    om.solve(solver=solvername, solve_kwargs={'tee': True})

    logging.info('Store lp-file')
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})

    return energysystem


def get_result_dict(energysystem):
    logging.info('Check the results')
    ces = energysystem.groups['ces']
    myresults = tpd.DataFramePlot(energy_system=energysystem)

    gridsource = myresults.slice_by(obj_label='gridsource', type='input',
                                    date_from='2012-01-01 00:00:00',
                                    date_to='2012-12-31 23:00:00')

    demand_1 = myresults.slice_by(obj_label='demand_1',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_2 = myresults.slice_by(obj_label='demand_2',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_3 = myresults.slice_by(obj_label='demand_3',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_4 = myresults.slice_by(obj_label='demand_4',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_5 = myresults.slice_by(obj_label='demand_5',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_6 = myresults.slice_by(obj_label='demand_6',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_7 = myresults.slice_by(obj_label='demand_7',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_8 = myresults.slice_by(obj_label='demand_8',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_9 = myresults.slice_by(obj_label='demand_9',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')

    demand_10 = myresults.slice_by(obj_label='demand_10',
                                   date_from='2012-01-01 00:00:00',
                                   date_to='2012-12-31 23:00:00')

    pv = myresults.slice_by(obj_label='pv',
                            date_from='2012-01-01 00:00:00',
                            date_to='2012-12-31 23:00:00')

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


def create_plots(energysystem):
    imp = gridsource.sort_values(by='val', ascending=False).reset_index()

    imp.plot(linewidth=1.5)

    plt.show()


if __name__ == "__main__":
    logger.define_logging()
    esys = initialise_energysystem()
    esys = optimise_storage_size(esys)
    # esys.dump()
    # esys.restore()
    import pprint as pp
    pp.pprint(get_result_dict(esys))
    create_plots(esys)

