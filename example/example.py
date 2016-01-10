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

# import solph module to create/process optimization model instance
from oemof.solph import predefined_objectives as predefined_objectives
# import oemof base classes to create energy system objects
from oemof.core import energy_system as es
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer


###############################################################################
# read data from csv file
###############################################################################

data_load = pd.read_csv("example_data/example_data_load_hourly_mean.csv", sep=",")
data_re = pd.read_csv("example_data/example_data_re.csv", sep=',')
timesteps = [t for t in range(8760)]


###############################################################################
# set optimzation options for storage components
###############################################################################

transformer.Storage.optimization_options.update({'investment': True})

###############################################################################
# Create oemof objetc
###############################################################################

# create bus
bgas = Bus(uid="bgas",
           type="gas",
           price=70,
           balanced=True,
           excess=False)

# create electricity bus
bel = Bus(uid="bel",
          type="el",
          excess=True)

# create commodity object for gas resource
rgas = source.Commodity(uid='rgas',
                        outputs=[bgas],
                        sum_out_limit=194397000)

# create fixed source object for wind
wind = source.FixedSource(uid="wind",
                          outputs=[bel],
                          val=data_re['wind'],
                          out_max=[1000000],
                          add_out_limit=0,
                          capex=1000,
                          opex_fix=20,
                          lifetime=25,
                          crf=0.08)

# create fixed source object for pv
pv = source.FixedSource(uid="pv",
                        outputs=[bel],
                        val=data_re['pv'],
                        out_max=[582000],
                        add_out_limit=0,
                        capex=900,
                        opex_fix=15,
                        lifetime=25,
                        crf=0.08)

# create simple sink object for demand
demand = sink.Simple(uid="demand", inputs=[bel], val=data_load['hh_01'])

# create simple transformer object for gas powerplant
pp_gas = transformer.Simple(uid='pp_gas',
                            inputs=[bgas], outputs=[bel],
                            opex_var=50, out_max=[10e10], eta=[0.58])

# create storage transformer object for storage
storage = transformer.Storage(uid='sto_simple',
                              inputs=[bel],
                              outputs=[bel],
                              eta_in=1,
                              eta_out=0.8,
                              cap_loss=0.00,
                              opex_fix=35,
                              opex_var=10e10,
                              capex=1000,
                              cap_max=0,
                              cap_initial=0,
                              c_rate_in=1/6,
                              c_rate_out=1/6)

###############################################################################
# Create, solve and postprocess OptimizationModel instance
###############################################################################

# group busses
buses = [bgas, bel]

# create lists of components
transformers = [pp_gas]
renewable_sources = [pv, wind]
commodities = [rgas]
storages = [storage]
sinks = [demand]

# groupt components
components = transformers + renewable_sources + storages + sinks + commodities

# create list of all entities
entities = components + buses

# TODO: other solver libraries should be passable
simulation = es.Simulation(solver='gurobi', timesteps=timesteps,
                           stream_solver_output=True,
                           objective_options={
                               'function':predefined_objectives.minimize_cost})

energysystem = es.EnergySystem(entities=entities, simulation=simulation)
energysystem.year = 2010

energysystem.optimize()


if __name__ == "__main__":
    import postprocessing as pp

    data = renewable_sources+transformers+storages

    pp.plot_dispatch(bel, energysystem.results,
                     simulation.timesteps, data, storage, demand)

    pp.print_results(bel, data, demand,
                     transformers, storage, energysystem)

    # Alternative plotting variant
    # Setting the time range to plot
    prange = pd.date_range(pd.datetime(energysystem.year, 6, 1, 0, 0),
                           periods=168, freq='H')
    pp.use_devplot(energysystem, bel.uid, prange)
