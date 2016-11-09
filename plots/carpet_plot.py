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
import matplotlib.patches as mpatches
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
        # plt.clim(-1800, 300)
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

    def line_plot(res_name, show=True, **kwargs):
        '''
        Empty docstring.
        '''
        fig = plt.figure()

        lw = 2

        if kwargs.get('wind') is not None:
            plt.plot(np.arange(0, 8760), kwargs.get('wind'), linewidth=lw)
        if kwargs.get('pv') is not None:
            plt.plot(np.arange(0, 8760), kwargs.get('pv'))
        if kwargs.get('demand') is not None:
            plt.plot(np.arange(0, 8760), kwargs.get('demand'))
        if kwargs.get('residual_1') is not None:
            plt.plot(np.arange(0, 8760), kwargs.get('residual_1'),
                    linewidth=lw,
                    label=kwargs.get('label_res_1'))
        if kwargs.get('residual_2') is not None:
            plt.plot(np.arange(0, 8760), kwargs.get('residual_2'),
                    linewidth=lw,
                    label=kwargs.get('label_res_2'))
        if kwargs.get('residual_3') is not None:
            plt.plot(np.arange(0, 8760), kwargs.get('residual_3'),
                    linewidth=lw,
                    label=kwargs.get('label_res_3'))
        if kwargs.get('residual_4') is not None:
            plt.plot(np.arange(0, 8760), kwargs.get('residual_4'), linewidth=lw)

        plt.axhline(0, color='black')

        plt.xlabel('Hours of the year')
        plt.ylabel(res_name)
        # plt.legend(kwargs.keys())

        # res_1_patch = mpatches.Patch(color='red', label='OS')
        # res_2_patch = mpatches.Patch(color='blue', label='LKOS')
        # res_3_patch = mpatches.Patch(color='green', label='OS + LKOS')

        # plt.legend(handles=[res_1_patch, res_2_patch, res_3_patch])
        plt.legend()

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
