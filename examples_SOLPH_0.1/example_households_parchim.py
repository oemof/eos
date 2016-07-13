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

from oemof import outputlib as tpd

try:
    from docopt import docopt
except ImportError:
    print("Unable to import docopt.\nIs the 'docopt' package installed?")

# Default logger of oemof
from oemof.tools import logger

import oemof.solph as solph
from oemof.solph import OperationalModel
from eos import helper_parchim as hlp


def initialise_energysystem(number_timesteps=8760):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2010', periods=number_timesteps,
                                    freq='H')

    energysystem = solph.EnergySystem(
        groupings=solph.GROUPINGS, time_idx=date_time_index)
    return energysystem


def validate(**arguments):
    valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if arguments["--loglevel"] not in valid:
        exit("Invalid loglevel: " + arguments["--loglevel"])
    return arguments


def optimise_storage_size(energysystem,
                          solvername='cbc'):
    # read load data in kW
    data_load = pd.read_csv(
        "../example/example_data/example_data_load_hourly_mean.csv",
        sep=",") / 1000

    # read household specific pv data
    data_pv = pd.read_csv(
        "../example/example_data/households_pv.csv", sep=";")
    # pv_max = data_pv['hh_2'][0] #TODO in kW????
    # azimuth = data_pv['hh_2'][1]
    # tilt = data_pv['hh_2'][2]
    # albedo = data_pv['hh_2'][3]

    #number_hh = np.shape(data_pv)[1] - 1 #TODO
    number_hh = 2

    loc = {
        'tz': 'Europe/Berlin',
        'latitude': 53.41,
        'longitude': 11.84}    # Parchim

    price_el = 0.30
    max_feedin = 0.5
    fit = 0.01         # -0.123
    sc_tax = 0      # TODO ab 10kWp/10MW: 0.0222
    hh_start = 1    # TODO: softcode

    # Calculate ep_costs from capex to compare with old solph
    #TODO ????
    capex = 1500
    lifetime = 10
    wacc = 0.05

    capex_pv = 1000
    lifetime_pv = 20

    epc = capex * (wacc * (1 + wacc) ** lifetime) / (
        (1 + wacc) ** lifetime - 1)
    epc_pv = capex_pv * (wacc * (1 + wacc) ** lifetime_pv) / (
        (1 + wacc) ** lifetime_pv - 1)

    # create list of household(numbers) to choośe, beginning with hh_start
    hh_to_choose = np.arange(hh_start, hh_start + number_hh)

    #creta dict hh with 'demand_1' = 'hh_start'
    hh = {}
    for n in range(0, number_hh):
        hh['demand_' + str(n+1)] = 'hh_' + str(hh_to_choose[n])

    # create list of households (strings: 'hh_1', ..)
    households = []
    for x in hh_to_choose:
        households.append('hh_' + str(x))
    print(households)

    ##########################################################################
    # Create oemof objects
    ##########################################################################
    logging.info('Create oemof objects')
    # create objects for every hh

    # create electricity bus for grid demand
    bel_grid = solph.Bus(label="bel_grid")
    # create commodity object for import electricity resource
    solph.Source(label='gridsource', outputs={bel_grid: solph.Flow(
        variable_costs=price_el)})

    house_pv = 0

    for house in households:
        house_pv = house_pv + 1
        label_pv = 'hh_' + str(house_pv)
        print(label_pv)
        # label_pv must start with 1

        # create electricity bus for pv
        bel_pv = solph.Bus(label="bel_pv_"+house)

        # create electricity bus for demand
        bel_demand = solph.Bus(label="bel_demand_"+house)

        # create fixed source objects for pv
        solph.Source(label='pv_'+house,
                     outputs={bel_pv: solph.Flow(
                         actual_value=hlp.get_pv_generation(
                             azimuth=data_pv[label_pv][1],
                             tilt=data_pv[label_pv][2],
                             albedo=data_pv[label_pv][3],
                             loc=loc),
                         nominal_value=data_pv[label_pv][0],
                         fixed=True, fixed_costs=50,
                         investment=solph.Investment(ep_costs=epc_pv))})

        # create excess component for bel_pv to allow overproduction
        solph.Sink(label="excess_"+house, inputs={bel_pv: solph.Flow()})
        # create excess component for the pv feedin
        solph.Sink(label='feedin_'+house, inputs={bel_pv: solph.Flow(
            variable_costs=fit,
            nominal_value=data_pv[label_pv][0],
            max=max_feedin)})
        # TODO stimmt das mit nominalvalue und max???

        # TODO: how to make a 2-to-1 transformer?
        solph.LinearTransformer(
            label="sc_Transformer_"+house,
            inputs={bel_pv: solph.Flow(variable_costs=sc_tax)},
            outputs={bel_demand: solph.Flow()},
            conversion_factors={bel_demand: 1})

        solph.LinearTransformer(
            label="gridTransformer_"+house,
            inputs={bel_grid: solph.Flow()},
            outputs={bel_demand: solph.Flow()},
            conversion_factors={bel_demand: 1})

        # create simple sink object for demands
        solph.Sink(
            label="demand_"+house,
            inputs={bel_demand: solph.Flow(
                actual_value=data_load[str(house)],
                fixed=True,
                nominal_value=1)})

        # create storage transformer object for storage
        solph.Storage(
            label='bat_'+house,
            inputs={bel_demand: solph.Flow(variable_costs=0)},
            outputs={bel_demand: solph.Flow(variable_costs=0)},
            capacity_loss=0.01,
            initial_capacity=0,
            nominal_input_capacity_ratio=1/6,
            nominal_output_capacity_ratio=1/6,
            inflow_conversion_factor=0.9, outflow_conversion_factor=0.9,
            fixed_costs=0,
            investment=solph.Investment(ep_costs=epc, maximum=20))

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info('Optimise the energy system')

    om = OperationalModel(energysystem, timeindex=energysystem.time_idx)

    logging.info('Store lp-file')
    om.write('optimization_problem.lp',
             io_options={'symbolic_solver_labels': True})

    for e in energysystem.entities:
        print (e)

    logging.info('Solve the optimization problem')

    om.solve(solver=solvername, solve_kwargs={'tee': True})

    return energysystem, households


def get_result_dict(energysystem, households):
    logging.info('Check the results')

    myresults = tpd.DataFramePlot(energy_system=energysystem)

    gridsource = myresults.slice_by(obj_label='gridsource',
                                    date_from='2012-01-01 00:00:00',
                                    date_to='2012-12-31 23:00:00')
    results_dc = {}

    for house in households:
        storage = energysystem.groups['bat_'+house]
        demand = myresults.slice_by(obj_label='demand_'+house,
                                    date_from='2012-01-01 00:00:00',
                                    date_to='2012-12-31 23:00:00')
        pv = myresults.slice_by(obj_label='pv_'+house,
                                date_from='2012-01-01 00:00:00',
                                date_to='2012-12-31 23:00:00')

        results_dc['demand_'+house] = demand.sum()
        results_dc['pv_'+house] = demand.sum()
        results_dc['pv_inst_'+house] = pv.max()
        results_dc['gridsource'] = gridsource.sum()
        results_dc['objective'] = energysystem.results.objective
        results_dc['storage_cap_'+house] = energysystem.results[
            storage][storage].invest
    return(results_dc)


def create_plots(energysystem):
    logging.info('Plot results')
    myresults = tpd.DataFramePlot(energy_system=energysystem)
    gridsource = myresults.slice_by(obj_label='gridsource', type='input',
                                    date_from='2012-01-01 00:00:00',
                                    date_to='2012-12-31 23:00:00')

    imp = gridsource.sort_values(by='val', ascending=False).reset_index()

    imp.plot(linewidth=1.5)

    plt.show()

if __name__ == "__main__":
#    arguments = docopt(__doc__)
#    print(arguments)
#    if arguments["--dry-run"]:
#        print("This is a dry run. Exiting before doing anything.")
#        exit(0)
#    arguments = validate(**arguments)

    logger.define_logging()
    esys = initialise_energysystem()
    esys, households = optimise_storage_size(esys)
    esys.dump()
    # esys.restore()
    import pprint as pp
    pp.pprint(get_result_dict(esys, households))
    create_plots(esys)
