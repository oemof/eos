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

#try:
#    from docopt import docopt
#except ImportError:
#    print("Unable to import docopt.\nIs the 'docopt' package installed?")

# Outputlib
#from oemof.outputlib import to_pandas as tpd

# Default logger of oemof
from oemof.tools import logger

# import oemof core and solph classes to create energy system objects
from oemof.core import energy_system as core_es
import oemof.solph as solph
from oemof.solph import (Bus, Source, Sink, Flow, Storage)
from oemof.solph.network import Investment
from oemof.solph import OperationalModel
from eos import helper_parchim as hlp


def initialise_energysystem(number_timesteps=8760):
    """initialize the energy system
    """
    logging.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2012', periods=number_timesteps,
                                    freq='H')

    return core_es.EnergySystem(groupings=solph.GROUPINGS,
                                time_idx=date_time_index)


def optimise_storage_size(energysystem,
                          solvername='cbc'):
						  
    # read load data in kW
    data_load = \
            pd.read_csv(
                 "../example/example_data/example_data_load_hourly_mean.csv",
                 sep=",") / 1000
				 
	# read household specific pv data
    data_pv = \
            pd.read_csv(
                 "../example/example_data/households_pv.csv",
                 sep=";")
	# pv_max = data_pv['hh_2'][0] #TODO in kW????
	# azimuth = data_pv['hh_2'][1]
	# tilt = data_pv['hh_2'][2]
	# albedo = data_pv['hh_2'][3]

    ##########################################################################
    # Create oemof object
    ##########################################################################
	
    number_hh = np.shape(data_pv)[1] - 1
	
    loc = {
        'tz': 'Europe/Berlin',
        'latitude': 53.41,
        'longitude': 11.84}    #Parchim
    price_el = 52
    max_feedin = 0.5
    fit = -5
    sc_tax = 8
    hh_start = 11 #todo: softcode
    
        # Calculate ep_costs from capex to compare with old solph
    #TODO ????
    capex = 375
    lifetime = 10
    wacc = 0.07
    epc = capex * (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)

    hh_to_choose = np.arange(hh_start, hh_start + number_hh)
    print(hh_to_choose)
	
    hh = {}
	
    for n in range(0, number_hh):
        hh['demand_' + str(n+1)] = 'hh_' + str(hh_to_choose[n])

    households = []
    for x in hh_to_choose:
        households.append('hh_' + str(x))
    print(households)

    logging.info('Create oemof objects')
	#create objects for every hh
	
	# create electricity bus for grid demand
    bel_grid = Bus(label="electricity_grid")
    		# create commodity object for import electricity resource
    Source(label='gridsource', outputs={bel_grid: Flow(
									variable_costs=price_el)})
         
    house_pv = 0
   	
    for house in households:
        house_pv = house_pv + 1
        label_pv = 'hh_' + str(house_pv)
        print(label_pv)
        # create electricity bus for pv
        bel_pv = Bus(label="electricity_pv_"+house)
			
        # create electricity bus for battery           
        bel_bat = Bus(label="electricity_bat_"+house)
		
# create excess component for the electricity bus to allow overproduction
        Sink(label="excess_"+house, inputs={bel_pv: Flow()})

		# create fixed source objects for pv
        Source(label=house+ '_pv', outputs={bel_pv: Flow(
                        actual_value=hlp.get_pv_generation(
                        	azimuth=data_pv[label_pv][1], 
					tilt=data_pv[label_pv][2], 
     					albedo=data_pv[label_pv][3],
					loc=loc),
     				  nominal_value=data_pv[label_pv][0],
                        fixed=True, fixed_costs=15)})
        print('pv erstellt mit richtigemoutputbus')

											  
		# create excess component for the pv feedin
        Sink(label=house+'_feedin', inputs={bel_pv: Flow(
								variable_costs=fit,
								nominal_value=data_pv[label_pv][0],
								max=max_feedin)})
        #TODO stimmt das mit nominalvalue und max???


    # create simple sink objects for demands 
        [Sink(
            label="demand_"+house,
            inputs={bel_pv: Flow(
						actual_value=data_load[str(house)],
						fixed=True, 
						nominal_value=1,
						variable_costs=sc_tax), 
				bel_grid: Flow(),
				bel_bat: Flow()})]
    
    
            # create storage transformer object for storage
        Storage(
            label='bat'+house,
            inputs={bel_pv: Flow(variable_costs=sc_tax)},
            outputs={bel_bat: Flow(variable_costs=0)},
            capacity_loss=0.01,
            nominal_input_capacity_ratio=1/6,
            nominal_output_capacity_ratio=1/6,
            inflow_conversion_factor=0.9, outflow_conversion_factor=0.9,
            fixed_costs=0,
            investment=Investment(ep_costs=epc))
    



    # create storage transformer object for storage
#    Storage(
#        label='ces',
#        inputs={bel: Flow(variable_costs=0)},
#        outputs={bel: Flow(variable_costs=0)},
#        capacity_loss=0.00,
#        nominal_input_capacity_ratio=1/6,
#        nominal_output_capacity_ratio=1/6,
#        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
#        fixed_costs=0,
#        investment=Investment(ep_costs=epc),
#    )

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


if __name__ == "__main__":
    # arguments = docopt(__doc__)
    # print(arguments)
    # if arguments["--dry-run"]:
    #     print("This is a dry run. Exiting before doing anything.")
    #     exit(0)
    # arguments = validate(**arguments)

    logger.define_logging()
    esys = initialise_energysystem()
    esys = optimise_storage_size(esys)
    # esys.dump()
    # esys.restore()
#    import pprint as pp
#    pp.pprint(get_result_dict(esys))
#    create_plots(esys)

