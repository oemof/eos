# -*- coding: utf-8 -*-

"""
General description:
---------------------

The example models the following energy system:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |


"""

###############################################################################
# imports
###############################################################################
import matplotlib.pyplot as plt
import pandas as pd
import logging

# import solph module to create/process optimization model instance
from oemof.solph import predefined_objectives as predefined_objectives

# Outputlib
from oemof.outputlib import to_pandas as tpd

# Default logger of oemof
from oemof.tools import logger

# import oemof base classes to create energy system objects
from oemof.core import energy_system as es
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer


# Define logger
logger.define_logging()

###############################################################################
# read data from csv file and set time index
###############################################################################

logging.info('Read data from csv file and set time index')

# read load data in W
data_load = pd.read_csv("../example_data/example_data_load_hourly_mean.csv", sep=",")

# read standardized feed-in from wind and pv
data_re = pd.read_csv("../example_data/example_data_re.csv", sep=',')

time_index = pd.date_range('1/1/2012', periods=8760, freq='H')

###############################################################################
# initialize the energy system
###############################################################################

logging.info('Initialize the energy system')
simulation = es.Simulation(
    timesteps=range(len(time_index)), verbose=True, solver='gurobi',
    debug=True,
    objective_options={'function': predefined_objectives.minimize_cost})

energysystem = es.EnergySystem(time_idx=time_index, simulation=simulation)

###############################################################################
# set optimzation options for storage components
###############################################################################

transformer.Storage.optimization_options.update({'investment': True})
# source.FixedSource.optimization_options.update({'investment': True})
# transformer.Simple.optimization_options.update({'investment': True})

###############################################################################
# Create oemof object
###############################################################################

logging.info('Create oemof objects')

# create gas bus
bgas = Bus(uid="bgas",
           type="gas",
           price=0,
           sum_out_limit=45243/0.58*0.0,
           balanced=True,
           excess=False)

# create electricity bus for quartier
bel = Bus(uid="bel",
          type="el",
          excess=True)

# create commodity object for gas resource
rgas = source.Commodity(uid='rgas',
                        outputs=[bgas])
                        # sum_out_limit=12708/0.58*0.2)
                        # sum_out_limit=1467)
                        # sum_out_limit=5869)

# create simple transformer object for gas powerplant
pp_gas = transformer.Simple(uid='pp_gas',
                            inputs=[bgas], outputs=[bel],
                            opex_var=0, out_max=[10e10], eta=[0.58])

# create simple sink object for demand in household 1
demand_1 = sink.Simple(uid="demand_1", inputs=[bel], val=data_load['hh_11']/1000)

# create simple sink object for demand in household 2
demand_2 = sink.Simple(uid="demand_2", inputs=[bel], val=data_load['hh_12']/1000)

# create simple sink object for demand in household 3
demand_3 = sink.Simple(uid="demand_3", inputs=[bel], val=data_load['hh_13']/1000)

# create simple sink object for demand in household 4
demand_4 = sink.Simple(uid="demand_4", inputs=[bel], val=data_load['hh_14']/1000)

# create simple sink object for demand in household 5
demand_5 = sink.Simple(uid="demand_5", inputs=[bel], val=data_load['hh_15']/1000)

# create simple sink object for demand in household 6
demand_6 = sink.Simple(uid="demand_6", inputs=[bel], val=data_load['hh_16']/1000)

# create simple sink object for demand in household 7
demand_7 = sink.Simple(uid="demand_7", inputs=[bel], val=data_load['hh_17']/1000)

# create simple sink object for demand in household 8
demand_8 = sink.Simple(uid="demand_8", inputs=[bel], val=data_load['hh_18']/1000)

# create simple sink object for demand in household 9
demand_9 = sink.Simple(uid="demand_9", inputs=[bel], val=data_load['hh_19']/1000)

# create simple sink object for demand in household 10
demand_10 = sink.Simple(uid="demand_10", inputs=[bel], val=data_load['hh_20']/1000)

##################################################################################

# create fixed source object for pv in quartier
pv = source.FixedSource(uid="pv",
                        outputs=[bel],
                        out_max=[100],
                        val=data_re['pv'],
                        capex=900,
                        opex_fix=15,
                        lifetime=25,
                        wacc=0.07)

# create storage transformer object for quartier
storage = transformer.Storage(uid='storage',
                              inputs=[bel],
                              outputs=[bel],
                              eta_in=1,
                              eta_out=0.8,
                              cap_loss=0.00,
                              opex_fix=0,
                              opex_var=10,
                              capex=375,
                              c_rate_in=1/6,
                              c_rate_out=1/6,
                              lifetime=10,
                              wacc=0.07)

###############################################################################
# Optimise the energy system and plot the results
###############################################################################

logging.info('Optimise the energy system')

# If you dumped the energysystem once, you can skip the optimisation with '#'
# and use the restore method.
energysystem.optimize()

# energysystem.dump()
# energysystem.restore()

# Creation of a multi-indexed pandas dataframe
es_df = tpd.EnergySystemDataFrame(energy_system=energysystem)

# Example usage of dataframe object
es_df.data_frame.describe
es_df.data_frame.index.get_level_values('bus_uid').unique()
es_df.data_frame.index.get_level_values('bus_type').unique()

# Example slice (see http://pandas.pydata.org/pandas-docs/stable/advanced.html)
idx = pd.IndexSlice
print(es_df.data_frame.loc[idx[:,
                         :,
                         :,
                         :,
                         slice(
                             pd.Timestamp("2012-01-01 00:00:00"),
                             pd.Timestamp("2012-01-01 01:00:00"))], :])

pp_gas = es_df.data_frame.loc[idx[:,
                         'el',
                         :,
                         slice('pp_gas', 'pv'),
                         slice(
                             pd.Timestamp("2012-01-01 00:00:00"),
                             pd.Timestamp("2012-12-31 23:00:00"))], :]

# print(es_df.data_frame.loc[idx[:,
#                                :,
#                                :,
#                                :,
#                          slice(
#                              pd.Timestamp("2012-06-01 00:00:00"),
#                              pd.Timestamp("2012-06-01 09:00:00"))], :])
#
# print(es_df.data_frame.loc[idx[:,
#                                :,
#                                :,
#                                :,
#                          slice(
#                              pd.Timestamp("2012-01-01 00:00:00"),
#                              pd.Timestamp("2012-01-01 01:00:00"))], :])

soc = es_df.data_frame.loc[idx['bel',
                               'el',
                               'other',
                               'storage',
                               slice(
                                   pd.Timestamp("2012-01-01 00:00:00"),
                                   pd.Timestamp("2012-12-31 23:00:00"))], :]

pp_gas = es_df.data_frame.loc[idx['bel',
                                  'el',
                                  'input',
                                  'pp_gas',
                                  slice(
                                      pd.Timestamp("2012-01-01 00:00:00"),
                                      pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_1 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_1',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_2 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_2',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_3 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_3',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_4 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_4',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_5 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_5',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_6 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_6',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_7 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_7',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_8 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_8',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_9 = es_df.data_frame.loc[idx['bel',
                                    'el',
                                    'output',
                                    'demand_9',
                                    slice(
                                        pd.Timestamp("2012-01-01 00:00:00"),
                                        pd.Timestamp("2012-12-31 23:00:00"))], :]

demand_10 = es_df.data_frame.loc[idx['bel',
                                     'el',
                                     'output',
                                     'demand_10',
                                     slice(
                                         pd.Timestamp("2012-01-01 00:00:00"),
                                         pd.Timestamp("2012-12-31 23:00:00"))], :]

pv = es_df.data_frame.loc[idx['bel',
                              'el',
                              'input',
                              'pv',
                              slice(
                                  pd.Timestamp("2012-01-01 00:00:00"),
                                  pd.Timestamp("2012-12-31 23:00:00"))], :]

print('soc_max: ', soc.max())

print('storage_cap: ', energysystem.results[storage].add_cap)

print('pp_gas_sum: ', pp_gas.sum())

print('demand_sum_1: ', demand_1.sum())
print('demand_sum_2: ', demand_2.sum())
print('demand_sum_3: ', demand_3.sum())
print('demand_sum_4: ', demand_4.sum())
print('demand_sum_5: ', demand_5.sum())
print('demand_sum_6: ', demand_6.sum())
print('demand_sum_7: ', demand_7.sum())
print('demand_sum_8: ', demand_8.sum())
print('demand_sum_9: ', demand_9.sum())
print('demand_sum_10: ', demand_10.sum())

print('pv_max: ', pv.max()/0.76474)

print('pv_sum: ', pv.sum())

print('objective: ', energysystem.results.objective())


# print(pp_gas)
# pp_gas.to_csv('/home/caro/temp/pp_gas.csv')

# logging.info('Plot the results')
#
cdict_1 = {'pv_1': '#ffde32',
           'storage_1': '#42c77a',
           'pp_gas_1': '#636f6b',
           'demand_1': '#ce4aff'}


cdict_2 = {'pv_2': '#ffde32',
           'storage_2': '#42c77a',
           'pp_gas_2': '#636f6b',
           'demand_2': '#ce4aff'}

cdict_3 = {'pv_3': '#ffde32',
           'storage_3': '#42c77a',
           'pp_gas_3': '#636f6b',
           'demand_3': '#ce4aff'}

cdict_4 = {'pv_4': '#ffde32',
           'storage_4': '#42c77a',
           'pp_gas_4': '#636f6b',
           'demand_4': '#ce4aff'}

# Plotting line plots
es_df.plot_bus(bus_uid="bel", bus_type="el", type="input",
               title="January 2016", xlabel="Power in MW",
               ylabel="Date", tick_distance=24*7,
               colordict=cdict_1)
               # date_from="2012-06-01 00:00:00",
               # date_to="2012-06-08 00:00:00")

# # Minimal parameter
es_df.plot_bus(bus_uid="bel", type="output", title="Year 2016")
#
# plt.show()
#
# Plotting a combined stacked plot

es_df.stackplot("bel",
                colordict=cdict_1,
                date_from="2012-06-01 00:00:00",
                date_to="2012-06-08 00:00:00",
                title="Electricity bus",
                ylabel="Power in MW", xlabel="Date",
                linewidth=4,
                tick_distance=24, save=True)

# es_df.stackplot("bel_2",
#                 colordict=cdict_2,
#                 date_from="2012-06-01 00:00:00",
#                 date_to="2012-06-8 00:00:00",
#                 title="Electricity bus",
#                 ylabel="Power in MW", xlabel="Date",
#                 linewidth=4,
#                 tick_distance=24, save=True)
#
# es_df.stackplot("bel_3",
#                 colordict=cdict_3,
#                 date_from="2012-06-01 00:00:00",
#                 date_to="2012-06-8 00:00:00",
#                 title="Electricity bus",
#                 ylabel="Power in MW", xlabel="Date",
#                 linewidth=4,
#                 tick_distance=24, save=True)
#
# es_df.stackplot("bel_4",
#                 colordict=cdict_4,
#                 date_from="2012-06-01 00:00:00",
#                 date_to="2012-06-8 00:00:00",
#                 title="Electricity bus",
#                 ylabel="Power in MW", xlabel="Date",
#                 linewidth=4,
#                 tick_distance=24, save=True)
# plt.show()

# ###############################################################################
# # Create, solve and postprocess OptimizationModel instance
# ###############################################################################
#
# # group busses
# # buses = [bgas, bel]
# buses = [bel, bel_hh]
#
# # create lists of components
# # transformers = [pp_gas]
# renewable_sources = [pv_hh, pv, wind]
# commodities = []
# storages = [storage]
# sinks = [demand]
#
# # groupt components
# components = renewable_sources + storages + sinks + commodities
#
# # create list of all entities
# entities = components + buses
#
# # TODO: other solver libraries should be passable
# simulation = es.Simulation(solver='gurobi', timesteps=timesteps,
#                            stream_solver_output=True,debug=True,
#                            objective_options={
#                                'function':predefined_objectives.minimize_cost})
#
# energysystem = es.EnergySystem(entities=entities, simulation=simulation)
# energysystem.year = 2010
#
# energysystem.optimize()
#
#
# if __name__ == "__main__":
#     import postprocessing as pp
#
#     data = renewable_sources+transformers+storages
#
# #     pp.plot_dispatch(bel, energysystem.results,
# #                      simulation.timesteps, data, storage, demand)
# #
# #     pp.print_results(bel, data, demand,
# #                      transformers, storage, energysystem)
#
#     # Alternative plotting variant
#     # Setting the time range to plot
#     prange = pd.date_range(pd.datetime(energysystem.year, 6, 1, 0, 0),
#                            periods=168, freq='H')
#     pp.use_devplot(energysystem, bel.uid, prange)
