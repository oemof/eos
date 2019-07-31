# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 15:44:27 2017

@author: RL-INSTITUT\caroline.moeller
"""
import numpy as np
import matplotlib.pyplot as plt

wind_regions = [0.0, 62.0, 110.0, 242.0, 49.0, 7.0, 38.0, 182.0, 15.0, 7.0, 22.0, 24.0, 85.0, 67.0, 47.0, 34.0, 33.0, 341.0, 89.0]
pv_regions = [42.8, 85.7, 80.1, 151.6, 62.4, 29.9, 30.0, 32.7, 35.6, 18.6, 33.2, 27.3, 25.3, 50.1, 15.9, 19.3, 19.1, 73.4, 24.4]

wind_regions_sorted = np.sort(wind_regions)
pv_regions_sorted = np.sort(pv_regions)

plt.hist(wind_regions_sorted, normed=False, range=(wind_regions_sorted.min(),
     wind_regions_sorted.max()))
plt.xlabel('Installed wind capacity in MW')
plt.ylabel('Number of sub regions')
plt.ylim([0, 11])
plt.savefig('wind_hist.png')
plt.show()

plt.hist(pv_regions_sorted, normed=False, range=(wind_regions_sorted.min(),
    wind_regions_sorted.max()), color='y')
plt.xlabel('Installed PV capacity in MW')
plt.ylabel('Number of sub regions')
plt.savefig('pv_hist.png')
plt.show()
