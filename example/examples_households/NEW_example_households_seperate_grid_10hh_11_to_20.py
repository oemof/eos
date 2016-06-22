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
import numpy as np
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

pv_data = data_re['pv']
print(pv_data.max())

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

###############################################################################
# Create oemof object
###############################################################################

logging.info('Create oemof objects')

grid_share = 0.4

# create gas bus
bgas_1 = Bus(uid="bgas_1",
             type="gas",
             price=0,
             sum_out_limit=3887/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_2 = Bus(uid="bgas_2",
             type="gas",
             price=0,
             sum_out_limit=4508/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_3 = Bus(uid="bgas_3",
             type="gas",
             price=0,
             sum_out_limit=4892/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_4 = Bus(uid="bgas_4",
             type="gas",
             price=0,
             sum_out_limit=3259/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_5 = Bus(uid="bgas_5",
             type="gas",
             price=0,
             sum_out_limit=3402/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_6 = Bus(uid="bgas_6",
             type="gas",
             price=0,
             sum_out_limit=3196/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_7 = Bus(uid="bgas_7",
             type="gas",
             price=0,
             sum_out_limit=5924/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_8 = Bus(uid="bgas_8",
             type="gas",
             price=0,
             sum_out_limit=5739/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_9 = Bus(uid="bgas_9",
             type="gas",
             price=0,
             sum_out_limit=5489/0.58*grid_share,
             balanced=True,
             excess=False)

bgas_10 = Bus(uid="bgas_10",
              type="gas",
              price=0,
              sum_out_limit=4946/0.58*grid_share,
              balanced=True,
              excess=False)

##################################################################################

# create electricity bus for household 1
bel_1 = Bus(uid="bel_1",
            type="el",
            excess=True)

# create electricity bus for household 2
bel_2 = Bus(uid="bel_2",
            type="el",
            excess=True)

# create electricity bus for household 3
bel_3 = Bus(uid="bel_3",
            type="el",
            excess=True)

# create electricity bus for household 4
bel_4 = Bus(uid="bel_4",
            type="el",
            excess=True)

# create electricity bus for household 5
bel_5 = Bus(uid="bel_5",
            type="el",
            excess=True)

# create electricity bus for household 6
bel_6 = Bus(uid="bel_6",
            type="el",
            excess=True)

# create electricity bus for household 7
bel_7 = Bus(uid="bel_7",
            type="el",
            excess=True)

# create electricity bus for household 8
bel_8 = Bus(uid="bel_8",
            type="el",
            excess=True)

# create electricity bus for household 9
bel_9 = Bus(uid="bel_9",
            type="el",
            excess=True)

# create electricity bus for household 10
bel_10 = Bus(uid="bel_10",
             type="el",
             excess=True)

##################################################################################

# create commodity object for gas resource
rgas = source.Commodity(uid='rgas',
                        outputs=[bgas_1, bgas_2, bgas_3, bgas_4, bgas_5,
                                 bgas_6, bgas_7, bgas_8, bgas_9, bgas_10])
                        # sum_out_limit=1467)
                        # sum_out_limit=5869)

# create simple transformer object for gas powerplant
pp_gas_1 = transformer.Simple(uid='pp_gas_1',
                              inputs=[bgas_1], outputs=[bel_1],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_2 = transformer.Simple(uid='pp_gas_2',
                              inputs=[bgas_2], outputs=[bel_2],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_3 = transformer.Simple(uid='pp_gas_3',
                              inputs=[bgas_3], outputs=[bel_3],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_4 = transformer.Simple(uid='pp_gas_4',
                              inputs=[bgas_4], outputs=[bel_4],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_5 = transformer.Simple(uid='pp_gas_5',
                              inputs=[bgas_5], outputs=[bel_5],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_6 = transformer.Simple(uid='pp_gas_6',
                              inputs=[bgas_6], outputs=[bel_6],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_7 = transformer.Simple(uid='pp_gas_7',
                              inputs=[bgas_7], outputs=[bel_7],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_8 = transformer.Simple(uid='pp_gas_8',
                              inputs=[bgas_8], outputs=[bel_8],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_9 = transformer.Simple(uid='pp_gas_9',
                              inputs=[bgas_9], outputs=[bel_9],
                              opex_var=0, out_max=[10e10], eta=[0.58])

# create simple transformer object for gas powerplant
pp_gas_10 = transformer.Simple(uid='pp_gas_10',
                               inputs=[bgas_10], outputs=[bel_10],
                               opex_var=0, out_max=[10e10], eta=[0.58])

##################################################################################

# create simple sink object for demand in household 1
demand_1 = sink.Simple(uid="demand_1", inputs=[bel_1], val=data_load['hh_11']/1000)

# create simple sink object for demand in household 2
demand_2 = sink.Simple(uid="demand_2", inputs=[bel_2], val=data_load['hh_12']/1000)

# create simple sink object for demand in household 3
demand_3 = sink.Simple(uid="demand_3", inputs=[bel_3], val=data_load['hh_13']/1000)

# create simple sink object for demand in household 4
demand_4 = sink.Simple(uid="demand_4", inputs=[bel_4], val=data_load['hh_14']/1000)

# create simple sink object for demand in household 4
demand_5 = sink.Simple(uid="demand_5", inputs=[bel_5], val=data_load['hh_15']/1000)

# create simple sink object for demand in household 4
demand_6 = sink.Simple(uid="demand_6", inputs=[bel_6], val=data_load['hh_16']/1000)

# create simple sink object for demand in household 4
demand_7 = sink.Simple(uid="demand_7", inputs=[bel_7], val=data_load['hh_17']/1000)

# create simple sink object for demand in household 4
demand_8 = sink.Simple(uid="demand_8", inputs=[bel_8], val=data_load['hh_18']/1000)

# create simple sink object for demand in household 4
demand_9 = sink.Simple(uid="demand_9", inputs=[bel_9], val=data_load['hh_19']/1000)

# create simple sink object for demand in household 4
demand_10 = sink.Simple(uid="demand_10", inputs=[bel_10], val=data_load['hh_20']/1000)

######################################################################################

# create fixed source object for pv in household 1
pv_1 = source.FixedSource(uid="pv_1",
                          outputs=[bel_1],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 2
pv_2 = source.FixedSource(uid="pv_2",
                          outputs=[bel_2],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 3
pv_3 = source.FixedSource(uid="pv_3",
                          outputs=[bel_3],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 4
pv_4 = source.FixedSource(uid="pv_4",
                          outputs=[bel_4],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 5
pv_5 = source.FixedSource(uid="pv_5",
                          outputs=[bel_5],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 6
pv_6 = source.FixedSource(uid="pv_6",
                          outputs=[bel_6],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 7
pv_7 = source.FixedSource(uid="pv_7",
                          outputs=[bel_7],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 8
pv_8 = source.FixedSource(uid="pv_8",
                          outputs=[bel_8],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 9
pv_9 = source.FixedSource(uid="pv_9",
                          outputs=[bel_9],
                          out_max=[10],
                          val=data_re['pv'],
                          capex=900,
                          opex_fix=15,
                          lifetime=25,
                          wacc=0.07)

# create fixed source object for pv in household 10
pv_10 = source.FixedSource(uid="pv_10",
                           outputs=[bel_10],
                           out_max=[10],
                           val=data_re['pv'],
                           capex=900,
                           opex_fix=15,
                           lifetime=25,
                           wacc=0.07)

#######################################################################

# create storage transformer object for household 1
storage_1 = transformer.Storage(uid='storage_1',
                                inputs=[bel_1],
                                outputs=[bel_1],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)

# create storage transformer object for household 2
storage_2 = transformer.Storage(uid='storage_2',
                                inputs=[bel_2],
                                outputs=[bel_2],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)

# create storage transformer object for household 3
storage_3 = transformer.Storage(uid='storage_3',
                                inputs=[bel_3],
                                outputs=[bel_3],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)

# create storage transformer object for household 4
storage_4 = transformer.Storage(uid='storage_4',
                                inputs=[bel_4],
                                outputs=[bel_4],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)

# create storage transformer object for household 5
storage_5 = transformer.Storage(uid='storage_5',
                                inputs=[bel_5],
                                outputs=[bel_5],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)

# create storage transformer object for household 6
storage_6 = transformer.Storage(uid='storage_6',
                                inputs=[bel_6],
                                outputs=[bel_6],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)

# create storage transformer object for household 7
storage_7 = transformer.Storage(uid='storage_7',
                                inputs=[bel_7],
                                outputs=[bel_7],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)
# create storage transformer object for household 8
storage_8 = transformer.Storage(uid='storage_8',
                                inputs=[bel_8],
                                outputs=[bel_8],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)
# create storage transformer object for household 9
storage_9 = transformer.Storage(uid='storage_9',
                                inputs=[bel_9],
                                outputs=[bel_9],
                                eta_in=1,
                                eta_out=0.8,
                                cap_loss=0.00,
                                opex_fix=0,
                                opex_var=0,
                                capex=375,
                                c_rate_in=1/6,
                                c_rate_out=1/6,
                                lifetime=10,
                                wacc=0.07)
# create storage transformer object for household 10
storage_10 = transformer.Storage(uid='storage_10',
                                 inputs=[bel_10],
                                 outputs=[bel_10],
                                 eta_in=1,
                                 eta_out=0.8,
                                 cap_loss=0.00,
                                 opex_fix=0,
                                 opex_var=0,
                                 capex=375,
                                 c_rate_in=1/6,
                                 c_rate_out=1/6,
                                 lifetime=10,
                                 wacc=0.07)

#######################################################################

excess_1 = sink.Simple(uid="excess_1", inputs=[bel_1], val=np.zeros(8760), bound_type='min')
excess_2 = sink.Simple(uid="excess_2", inputs=[bel_2], val=np.zeros(8760), bound_type='min')
excess_3 = sink.Simple(uid="excess_3", inputs=[bel_3], val=np.zeros(8760), bound_type='min')
excess_4 = sink.Simple(uid="excess_4", inputs=[bel_4], val=np.zeros(8760), bound_type='min')
excess_5 = sink.Simple(uid="excess_5", inputs=[bel_5], val=np.zeros(8760), bound_type='min')
excess_6 = sink.Simple(uid="excess_6", inputs=[bel_6], val=np.zeros(8760), bound_type='min')
excess_7 = sink.Simple(uid="excess_7", inputs=[bel_7], val=np.zeros(8760), bound_type='min')
excess_8 = sink.Simple(uid="excess_8", inputs=[bel_8], val=np.zeros(8760), bound_type='min')
excess_9 = sink.Simple(uid="excess_9", inputs=[bel_9], val=np.zeros(8760), bound_type='min')
excess_10 = sink.Simple(uid="excess_10", inputs=[bel_10], val=np.zeros(8760), bound_type='min')

###############################################################################
# Optimise the energy system and plot the results
###############################################################################

logging.info('Optimise the energy system')

# If you dumped the energysystem once, you can skip the optimisation with '#'
# and use the restore method.
energysystem.optimize()

energysystem.dump()
# energysystem.restore()

# Creation of a multi-indexed pandas dataframe
my_results = tpd.DataFramePlot(energy_system=energysystem)
#print(my_results)

########################################################################

pp_gas_1 = my_results.slice_by(bus_uid="bel_1", bus_type='el',
                               type='input', obj_uid='pp_gas_1',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_2 = my_results.slice_by(bus_uid="bel_2", bus_type='el',
                               type='input', obj_uid='pp_gas_2',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_3 = my_results.slice_by(bus_uid="bel_3", bus_type='el',
                               type='input', obj_uid='pp_gas_3',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_4 = my_results.slice_by(bus_uid="bel_4", bus_type='el',
                               type='input', obj_uid='pp_gas_4',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_5 = my_results.slice_by(bus_uid="bel_5", bus_type='el',
                               type='input', obj_uid='pp_gas_5',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_6 = my_results.slice_by(bus_uid="bel_6", bus_type='el',
                               type='input', obj_uid='pp_gas_6',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_7 = my_results.slice_by(bus_uid="bel_7", bus_type='el',
                               type='input', obj_uid='pp_gas_7',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_8 = my_results.slice_by(bus_uid="bel_8", bus_type='el',
                               type='input', obj_uid='pp_gas_8',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_9 = my_results.slice_by(bus_uid="bel_9", bus_type='el',
                               type='input', obj_uid='pp_gas_9',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

pp_gas_10 = my_results.slice_by(bus_uid="bel_10", bus_type='el',
                                type='input', obj_uid='pp_gas_10',
                                date_from="2012-01-01 00:00:00",
                                date_to="2012-12-31 23:00:00")

##########################################################################

demand_1 = my_results.slice_by(bus_uid="bel_1", bus_type='el',
                               type='output', obj_uid='demand_1',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_2 = my_results.slice_by(bus_uid="bel_2", bus_type='el',
                               type='output', obj_uid='demand_2',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_3 = my_results.slice_by(bus_uid="bel_3", bus_type='el',
                               type='output', obj_uid='demand_3',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_4 = my_results.slice_by(bus_uid="bel_4", bus_type='el',
                               type='output', obj_uid='demand_4',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_5 = my_results.slice_by(bus_uid="bel_5", bus_type='el',
                               type='output', obj_uid='demand_5',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_6 = my_results.slice_by(bus_uid="bel_6", bus_type='el',
                               type='output', obj_uid='demand_6',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_7 = my_results.slice_by(bus_uid="bel_7", bus_type='el',
                               type='output', obj_uid='demand_7',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_8 = my_results.slice_by(bus_uid="bel_8", bus_type='el',
                               type='output', obj_uid='demand_8',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_9 = my_results.slice_by(bus_uid="bel_9", bus_type='el',
                               type='output', obj_uid='demand_9',
                               date_from="2012-01-01 00:00:00",
                               date_to="2012-12-31 23:00:00")

demand_10 = my_results.slice_by(bus_uid="bel_10", bus_type='el',
                                type='output', obj_uid='demand_10',
                                date_from="2012-01-01 00:00:00",
                                date_to="2012-12-31 23:00:00")

##########################################################################

pv_1 = my_results.slice_by(bus_uid="bel_1", bus_type='el',
                           type='input', obj_uid='pv_1',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_2 = my_results.slice_by(bus_uid="bel_2", bus_type='el',
                           type='input', obj_uid='pv_2',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_3 = my_results.slice_by(bus_uid="bel_3", bus_type='el',
                           type='input', obj_uid='pv_3',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_4 = my_results.slice_by(bus_uid="bel_4", bus_type='el',
                           type='input', obj_uid='pv_4',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_5 = my_results.slice_by(bus_uid="bel_5", bus_type='el',
                           type='input', obj_uid='pv_5',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_6 = my_results.slice_by(bus_uid="bel_6", bus_type='el',
                           type='input', obj_uid='pv_6',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_7 = my_results.slice_by(bus_uid="bel_7", bus_type='el',
                           type='input', obj_uid='pv_7',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_8 = my_results.slice_by(bus_uid="bel_8", bus_type='el',
                           type='input', obj_uid='pv_8',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_9 = my_results.slice_by(bus_uid="bel_9", bus_type='el',
                           type='input', obj_uid='pv_9',
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-12-31 23:00:00")

pv_10 = my_results.slice_by(bus_uid="bel_10", bus_type='el',
                            type='input', obj_uid='pv_10',
                            date_from="2012-01-01 00:00:00",
                            date_to="2012-12-31 23:00:00")

#print('soc_max_1: ', soc_1.max())
#print('soc_max_2: ', soc_2.max())
#print('soc_max_3: ', soc_3.max())
#print('soc_max_4: ', soc_4.max())
#
print('storage_cap_1: ', energysystem.results[storage_1].add_cap)
print('storage_cap_2: ', energysystem.results[storage_2].add_cap)
print('storage_cap_3: ', energysystem.results[storage_3].add_cap)
print('storage_cap_4: ', energysystem.results[storage_4].add_cap)
print('storage_cap_5: ', energysystem.results[storage_5].add_cap)
print('storage_cap_6: ', energysystem.results[storage_6].add_cap)
print('storage_cap_7: ', energysystem.results[storage_7].add_cap)
print('storage_cap_8: ', energysystem.results[storage_8].add_cap)
print('storage_cap_9: ', energysystem.results[storage_9].add_cap)
print('storage_cap_10: ', energysystem.results[storage_10].add_cap)

#print(energysystem.results[storage_1].add_out)
#print(energysystem.results[storage_2].add_out)
#print(energysystem.results[storage_3].add_out)
#print(energysystem.results[storage_4].add_out)

print('pp_gas_sum_1: ', pp_gas_1.sum())
print('pp_gas_sum_2: ', pp_gas_2.sum())
print('pp_gas_sum_3: ', pp_gas_3.sum())
print('pp_gas_sum_4: ', pp_gas_4.sum())
print('pp_gas_sum_5: ', pp_gas_5.sum())
print('pp_gas_sum_6: ', pp_gas_6.sum())
print('pp_gas_sum_7: ', pp_gas_7.sum())
print('pp_gas_sum_8: ', pp_gas_8.sum())
print('pp_gas_sum_9: ', pp_gas_9.sum())
print('pp_gas_sum_10: ', pp_gas_10.sum())
#
#print('demand_sum_1: ', demand_1.sum())
#print('demand_sum_2: ', demand_2.sum())
#print('demand_sum_3: ', demand_3.sum())
#print('demand_sum_4: ', demand_4.sum())
#print('demand_sum_5: ', demand_5.sum())
#print('demand_sum_6: ', demand_6.sum())
#print('demand_sum_7: ', demand_7.sum())
#print('demand_sum_8: ', demand_8.sum())
#print('demand_sum_9: ', demand_9.sum())
#print('demand_sum_10: ', demand_10.sum())
#
#print('demand_max_1: ', demand_1.max())
#print('demand_max_2: ', demand_2.max())
#print('demand_max_3: ', demand_3.max())
#print('demand_max_4: ', demand_4.max())
#print('demand_max_5: ', demand_5.max())
#print('demand_max_6: ', demand_6.max())
#print('demand_max_7: ', demand_7.max())
#print('demand_max_8: ', demand_8.max())
#print('demand_max_9: ', demand_9.max())
#print('demand_max_10: ', demand_10.max())
#
#print('pv_max_1: ', pv_1.max()/0.76474)
#print('pv_max_2: ', pv_2.max()/0.76474)
#print('pv_max_3: ', pv_3.max()/0.76474)
#print('pv_max_4: ', pv_4.max()/0.76474)
#print('pv_max_5: ', pv_5.max()/0.76474)
#print('pv_max_6: ', pv_6.max()/0.76474)
#print('pv_max_7: ', pv_7.max()/0.76474)
#print('pv_max_8: ', pv_8.max()/0.76474)
#print('pv_max_9: ', pv_9.max()/0.76474)
#print('pv_max_10: ', pv_10.max()/0.76474)
#
##print(energysystem.results[pv_1].add_out)
##print(energysystem.results[pv_2].add_out)
##print(energysystem.results[pv_3].add_out)
##print(energysystem.results[pv_4].add_out)
#
#print('pv_sum_1: ', pv_1.sum())
#print('pv_sum_2: ', pv_2.sum())
#print('pv_sum_3: ', pv_3.sum())
#print('pv_sum_4: ', pv_4.sum())
#print('pv_sum_5: ', pv_5.sum())
#print('pv_sum_6: ', pv_6.sum())
#print('pv_sum_7: ', pv_7.sum())
#print('pv_sum_8: ', pv_8.sum())
#print('pv_sum_9: ', pv_9.sum())
#print('pv_sum_10: ', pv_10.sum())
#
#print('objective: ', energysystem.results.objective)


#myplot = my_results.slice_unstacked(bus_type='gas',
#                               type='output',
#                               date_from="2012-01-01 00:00:00",
#                               date_to="2012-12-31 23:00:00")
#myplot.plot(linewidth=2, title="January 2012")
#myplot.ax.legend(loc='upper right')
#myplot.ax.set_ylabel('Power in MW')
#myplot.ax.set_xlabel('Hours')
##myplot.set_datetime_ticks(date_format='%d-%m-%Y', tick_distance=24*7)



import_1 = pp_gas_1.sort_values(by='val', ascending=False).reset_index()
import_2 = pp_gas_2.sort_values(by='val', ascending=False).reset_index()
import_3 = pp_gas_3.sort_values(by='val', ascending=False).reset_index()
import_4 = pp_gas_4.sort_values(by='val', ascending=False).reset_index()
import_5 = pp_gas_5.sort_values(by='val', ascending=False).reset_index()
import_6 = pp_gas_6.sort_values(by='val', ascending=False).reset_index()
import_7 = pp_gas_7.sort_values(by='val', ascending=False).reset_index()
import_8 = pp_gas_8.sort_values(by='val', ascending=False).reset_index()
import_9 = pp_gas_9.sort_values(by='val', ascending=False).reset_index()
import_10 = pp_gas_10.sort_values(by='val', ascending=False).reset_index()

#print(import_1)

#import_1 = import_1.reset_index()
#import_2 = import_2.reset_index()
#
imp = pd.DataFrame(dict(hh_1=import_1.val, hh_2=import_2.val,
                        hh_3=import_3.val, hh_4=import_4.val,
                        hh_5=import_5.val, hh_6=import_6.val,
                        hh_7=import_7.val, hh_8=import_8.val,
                        hh_9=import_9.val, hh_10=import_10.val),
                        index=import_1.index)
imp.plot(linewidth=1.5)

plt.show()