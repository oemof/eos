# -*- coding: utf-8 -*-

''' Plots.

Usage: households_boxplot.py [options]

Options:

  -n, --number=NUM         Number of run. [default: 1]
      --ssr=SSR            Self-sufficiency degree. [default: None]

'''

###############################################################################
# imports
###############################################################################
# import numpy as np
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
from docopt import docopt

arguments = docopt(__doc__)
print(arguments)

mpl.use('agg')

# read data

# collectn_1 = np.random.normal(100, 10, 200)
# print(collectn_1)

results = pickle.load(open('quartier_results_10_2_2_2005' +'_' +
                           str(arguments['--ssr']) + '_' +
                           str(arguments['--number']) + '_' +
                           'random' + '.p', 'rb'))

print(results.keys())

# print('storage_cap: ', results['storage_cap'])

# smb://192.168.10.14/Caros_Daten/quartier_1000/' +

