# -*- coding: utf-8 -*-

''' Carpet plots.

Usage: carpet_plot.py [options]

Options:

  -c, --cost=COST          The cost scenario. [default: 1]
      --num-hh=NUM         Number of households. [default: 84]
      --year=YEAR          Weather year. [default: 2010]
      --ssr=SSR            Self-sufficiency degree. [default: None]
      --profile=PROFILE    Choose between random, summer, winter,
                           day, night, slp_h0, slp and include_g0_l0.
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

    def carpet_plot(res, res_name, show=True):
        '''
        Empty docstring.
        '''
        # print(res.max())
        matrix = np.reshape(res, (365, 24))
        a = np.transpose(matrix)
        b = np.flipud(a)

        print(b)

        fig = plt.figure()
        # plt.scatter(a)
        # cmap: 'RdPu', 'YlOrBr', 'PuBu', 'Greens'
        plt.imshow(b, cmap='YlOrBr', interpolation='nearest',
                   aspect='auto')
        plt.xlabel('Days of year')
        plt.ylabel('Hours of day')
        clb = plt.colorbar()
        clb.set_label(res_name)

        if show:
            plt.show()

        return fig


class Line:
    """
    A line class.
    """

    def __init__(self, name=None):
        self.name = name

    def line_plot(res, res_name, show=True):
        '''
        Empty docstring.
        '''
        fig = plt.figure()
        plt.plot(res)
        plt.xlabel('Hours of the year')
        plt.ylabel(res_name)

        if show:
            plt.show()

        return fig


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    quartier_results = quartier_plots.Quartier
    results = quartier_results.get_results(arguments)
    carpet = Carpet
    carpet.carpet_plot(results)
    line = Line
    line.line_plot(results)
