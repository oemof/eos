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
data_load = pd.read_csv("example_data/example_data_load_hourly_mean.csv", sep=",")
data_re = pd.read_csv("example_data/example_data_re.csv", sep=',')
time_index = pd.date_range('1/1/2012', periods=3, freq='H')

###############################################################################
# initialize the energy system
###############################################################################

logging.info('Initialize the energy system')
simulation = es.Simulation(
    timesteps=range(len(time_index)), stream_solver_output=True, solver='glpk',
    debug=True,
    objective_options={'function': predefined_objectives.minimize_cost})

energysystem = es.EnergySystem(time_idx=time_index, simulation=simulation)

###############################################################################
# set optimzation options for storage components
###############################################################################

transformer.Storage.optimization_options.update({'investment': True})
source.FixedSource.optimization_options.update({'investment': True})

###############################################################################
# Create oemof object
###############################################################################

logging.info('Create oemof objects')
# create gas bus
# bgas = Bus(uid="bgas",
#            type="gas",
#            price=70,
#            balanced=True,
#            excess=False)

# create electricity bus
bel = Bus(uid="bel",
          type="el",
          excess=True)

# create household electricity bus
bel_hh = Bus(uid="bel_hh",
             type="el",
             excess=True)

# create commodity object for gas resource
# rgas = source.Commodity(uid='rgas',
#                         outputs=[bgas],
#                         sum_out_limit=0)
#                         # sum_out_limit=194397000)

# create fixed source object for wind
wind = source.FixedSource(uid="wind",
                          outputs=[bel],
                          val=data_re['wind'],
                          out_max=[0],
                          capex=1000,
                          opex_fix=20,
                          opex_var=200,
                          lifetime=25,
                          crf=0.08)

# create fixed source object for pv
pv = source.FixedSource(uid="pv",
                        outputs=[bel],
                        out_max=[0],
                        val=data_re['pv'],
                        capex=900,
                        opex_fix=15,
                        lifetime=25,
                        crf=0.08)

print(pv.val)
# create fixed source object for household pv
pv_hh = source.FixedSource(uid="pv_hh",
                        outputs=[bel_hh],
                        out_max=[0],
                        val=data_re['pv'],
                        capex=900,
                        opex_fix=15,
                        lifetime=25,
                        crf=0.08)

# create simple sink object for demand
demand = sink.Simple(uid="demand", inputs=[bel, bel_hh], val=data_load['hh_01']/1000)

# create simple transformer object for gas powerplant
# pp_gas = transformer.Simple(uid='pp_gas',
#                             inputs=[bgas], outputs=[bel],
#                             opex_var=50, out_max=[10e10], eta=[0.58])

# create storage transformer object for storage
# storage = transformer.Storage(uid='sto_simple',
#                               inputs=[bel],
#                               outputs=[bel],
#                               eta_in=1,
#                               eta_out=0.8,
#                               cap_loss=0.00,
#                               opex_fix=35,
#                               opex_var=10e10,
#                               capex=1000,
#                               cap_max=0,
#                               cap_initial=0,
#                               c_rate_in=1/6,
#                               c_rate_out=1/6)

# create storage transformer object for household storage
storage = transformer.Storage(uid='sto_simple',
                              inputs=[bel_hh],
                              outputs=[bel_hh],
                              eta_in=1,
                              eta_out=0.8,
                              cap_loss=0.00,
                              opex_fix=35,
                              opex_var=10e10,
                              capex=1000,
                              cap_initial=0,
                              c_rate_in=1/6,
                              c_rate_out=1/6)

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
es_df.data_frame.loc[idx[:,
                         'el',
                         :,
                         slice('pp_gas', 'pv'),
                         slice(
                             pd.Timestamp("2012-01-01 00:00:00"),
                             pd.Timestamp("2012-01-01 01:00:00"))], :]

logging.info('Plot the results')

cdict = {'wind': '#5b5bae',
         'pv': '#ffde32',
         'sto_simple': '#42c77a',
         'pp_gas': '#636f6b',
         'demand': '#ce4aff'}

# Plotting line plots
es_df.plot_bus(bus_uid="bel", bus_type="el", type="input",
               date_from="2012-01-01 00:00:00", colordict=cdict,
               date_to="2012-01-31 00:00:00",
               title="January 2016", xlabel="Power in MW",
               ylabel="Date", tick_distance=24*7)

# Minimal parameter
es_df.plot_bus(bus_uid="bel", bus_type="gas", type="output", title="Year 2016")

plt.show()

# Plotting a combined stacked plot

es_df.stackplot("bel",
                colordict=cdict,
                date_from="2012-06-01 00:00:00",
                date_to="2012-06-8 00:00:00",
                title="Electricity bus",
                ylabel="Power in MW", xlabel="Date",
                linewidth=4,
                tick_distance=24, save=True)

plt.show()

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
