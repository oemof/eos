print('check_autarky_degree: ', 1 - pp_gas.sum()/demand.sum())



# -*- coding: utf-8 -*-

import pandas as pd
import random
import numpy as np
import NEW_example_households_seperate_grid_10hh_random_with_autLoop as app

# read load data in W
data_load = pd.read_csv("../example_data/example_data_load_hourly_mean.csv",
                        sep=",")

# create list of random households
hh_list = range(1, 81, 1)

number_of_hh_to_select = 10

list_of_random_hh = random.sample(hh_list, number_of_hh_to_select)

# loop over app with changing autarchy degrees
# grid_share = [0, 0.05, 0,1, 0.2, 0.3, 0.4, 0.5]
for grid_share in np.arange(0, 0.5, 0.1):
    (bgas_1, bgas_2, bgas_3,
     bgas_4, bgas_5, bgas_6,
     bgas_7, bgas_8, bgas_9, bgas_10) = app.create_gas_bus(data_load,
                                                           list_of_random_hh,
                                                           grid_share)

    app.caros_app(bgas_1, bgas_2, bgas_3, bgas_4, bgas_5,
                  bgas_6, bgas_7, bgas_8, bgas_9, bgas_10,
                  list_of_random_hh)
