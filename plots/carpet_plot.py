# -*- coding: utf-8 -*-

''' Carpet plots.

Usage: carpet_plot.py [options]

Options:

  -c, --cost=COST          The cost scenario. [default: 1]
      --num-hh=NUM         Number of households. [default: 84]
      --year=YEAR          Weather year. [default: 2010]
      --ssr=SSR            Self-sufficiency degree. [default: None]
      --profile=PROFILE    Choose between random, summer, winter,
                           day and night.
                           [default: random]
  -h, --help               Display this help.

'''

###############################################################################
# imports
###############################################################################
from docopt import docopt
import numpy as np
import matplotlib.pyplot as plt
import quartier_plots


class Carpet:
    """
    A carpet class.
    """

    def __init__(self, name=None):
        self.name = name

    def carpet_plot(res):
        '''
        Empty docstring.
        '''
        print(res.max())
        matrix = np.reshape(res, (365, 24))
        a = np.transpose(matrix)
        b = np.flipud(a)

        print(b)

        ax = plt.subplots()

        # plt.scatter(a)
        plt.imshow(b, cmap='PuRd', interpolation='nearest',
                   aspect='auto')
        # ax.set_xlabel('Days of year')
        # ax.set_ylabel('Hours of day')
        clb = plt.colorbar()
        clb.set_label('results in xx/xxx')
        plt.show()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    quartier_results = quartier_plots.Quartier
    results = quartier_results.get_results(arguments)
    carpet = Carpet
    carpet.carpet_plot(results)
