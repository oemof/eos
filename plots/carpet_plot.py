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
        # fig = plt.figure(figsize=(6, 4))
        fig = plt.figure(figsize=(12, 8))
        ax = plt.subplot()

        lw = 3
        diagram_color = 'black'
        main_color = '#7f7f7f'
        colors = []

        if kwargs.get('wind') is not None:
            line, = ax.plot(kwargs.get('wind').reset_index()[0], linewidth=lw, label='Wind + PV + Bio-energy', color='grey')
            colors.append(plt.getp(line,'color'))
        if kwargs.get('pv') is not None:
            line, = ax.plot(kwargs.get('pv').reset_index()['demand_el'], linewidth=lw, label='Load ENTSO-E', color='mediumblue')
            colors.append(plt.getp(line,'color'))
        if kwargs.get('demand') is not None:
            line, = ax.plot(kwargs.get('demand').reset_index()['h0'], linewidth=2, label='Load BDEW H0', color='mediumblue', linestyle=':')
            colors.append(plt.getp(line,'color'))
        if kwargs.get('residual_1') is not None:
            line, = ax.plot(np.arange(0, 8760), kwargs.get('residual_1'),
                    color=main_color,
                    # color='#a6a6a6',
                    linestyle='--',
                    linewidth=lw,
                    # label='City of Osnabrück')
                    # label='LKOS + Stadt Osnabrück')
                    label='2020')
                    # label=kwargs.get('label_res_2'))
            colors.append(plt.getp(line,'color'))
        if kwargs.get('residual_2') is not None:
            line, = ax.plot(np.arange(0, 8760), kwargs.get('residual_2'),
                    # color='#da467d',
                    color='#99cc00',
                    # color='black',
                    linestyle='-',
                    linewidth=lw,
                    label='2030')
                    # label='Cross-linking with LKOS')
                    # label='Cross-linking with City of Osnabrück 2030')
                    # label='Landkreis Osnabrück')
                    # label='Stadt Osnabrück 2020')
                    #label=kwargs.get('label_res_1'))
            colors.append(plt.getp(line,'color'))
        if kwargs.get('residual_3') is not None:
            line, = ax.plot(np.arange(0, 8760), kwargs.get('residual_3'),
                    # color='black',
                    # color='#99cc00',
                    color=main_color,
                    # linestyle='-',
                    linestyle='-.',
                    linewidth=lw,
                    # label='Landkreis Osnabrück 2040')
                    # label='Cross-linking with LKOS and KRST')
                    # label='Kreis Steinfurt')
                    label='2040')
                    # label=kwargs.get('label_res_3'))
            colors.append(plt.getp(line,'color'))
        if kwargs.get('residual_4') is not None:
            print(kwargs.get('residual_4'))
            line, = ax.plot(np.arange(0, 8760), kwargs.get('residual_4'),
                    color=main_color,
                    # color='midnightblue',
                    # color='saddlebrown',
                    # color='skyblue',
                    linestyle=':',
                    # linestyle='-',
                    linewidth=3,
                    # label='Cross-linking with City of Osnabrück 2030')
                    label='2050')
                    # label='Stadt Osnabrück 2050')
                    # label=kwargs.get('label_res_3'))
            colors.append(plt.getp(line,'color'))

        plt.axhline(0, linewidth=0.5, color=main_color)

        # plt.xlabel('Hours', fontsize=28, color=diagram_color)
        plt.xlabel('Hours of the year', fontsize=28, color=diagram_color)
        plt.ylabel(res_name, fontsize=28, color=diagram_color)
        # plt.xlim(0, 336)
        # plt.xticks([0, 100, 200, 300], fontsize=28, color=diagram_color)
        plt.xlim(0, 8760)
        plt.xticks([0, 2000, 4000, 6000, 8000], fontsize=28, color=diagram_color)
        # plt.yticks([0, 200, 400, 600, 800], fontsize=28, color=diagram_color)
        # plt.yticks([-1500, -1000, -500, 0, 500], fontsize=28, color=diagram_color)
        plt.yticks([-2500, -2000, -1500, -1000, -500, 0, 500], fontsize=28, color=diagram_color)
        # plt.yticks([-2000, -1500, -1000, -500, 0, 500, 1000])
        # plt.ylim(-2500, +1000),  # plt.yticks([])
        # plt.ylim(-410, +210),  # plt.yticks([])
        # plt.rcParams.update({'font.size': 18})
        # plt.legend(kwargs.keys())

        # leg = plt.legend(loc='lower left', frameon=False, prop={'size': 24})
        leg = plt.legend(loc='lower left', frameon=False, prop={'size': 28})
        leg._legend_box.align = 'left'
        leg.set_title('Kreis Steinfurt', prop={'size': 28})
        for color,text in zip(colors,leg.get_texts()):
        # for text in l.get_texts():
            text.set_color(color)
        plt.tight_layout()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(main_color)
        ax.spines['bottom'].set_color(main_color)

        if show:
            plt.show()

        return fig

class Bar:
    """
    A bar class.
    """

    def __init__(self, name=None):
        self.name = name

    def bar_plot(res_name, show=True, **kwargs):

        fig = plt.figure(figsize=(12, 8))
        ax = plt.subplot()

        diagram_color = 'black'
        main_color = '#7f7f7f'
        colors = []

        n = 12
        X = np.arange(n)

        # Y1 = (1-X/float(n)) * np.random.uniform(0.5, 1.0, n)
        # Y2 = (1-X/float(n)) * np.random.uniform(0.5, 1.0, n)

        Y1 = kwargs.get('Y1') / 1e3
        Y2 = kwargs.get('Y2') / 1e3
        Y3 = kwargs.get('Y3') / 1e3

        # plt.axes([0.025, 0.025, 0.95, 0.95])
        ax.bar(X, Y3, facecolor='orangered', edgecolor='white',
                label='Deficit')
        ax.bar(X, Y1, facecolor='#a6a6a6', edgecolor='white',
                label='Covered demand')
        ax.bar(X, Y2, facecolor='darkcyan', edgecolor='white',
                label='Excess')

        plt.axhline(0, linewidth=0.5, color=main_color)

        # plt.xlabel('Monhts')
        plt.ylabel(res_name, fontsize=28, color=diagram_color)
        plt.xticks(X, ['Jan', 'Feb', 'Mar', 'Apr',
            'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec'], fontsize=28, color=diagram_color)

        plt.ylim(-100, 450)
        plt.yticks([-100, 0, 100, 200, 300, 400], fontsize=28, color=diagram_color)
        # plt.yticks([-100, 0, 100, 200, 300])

        leg = ax.legend(loc='upper center', frameon=False, prop={'size': 28})
        leg.set_title('Landkreis Osnabrück (LKOS)', prop={'size': 28})
        leg._legend_box.align = 'left'

        for bar,text in zip(leg.get_patches(), leg.get_texts()):
                text.set_color(bar.get_facecolor())
        # for color,text in zip(colors,leg.get_texts()):
        # for text in l.get_texts():
            # text.set_color(color)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(main_color)
        ax.spines['bottom'].set_color(main_color)

        plt.tight_layout()

        # plt.tight_layout()

        # for x, y in zip(X, Y1):
        #     plt.text(x+0.4, y+0.05, '%.2f' % y, ha='center', va='bottom')

        # for x, y in zip(X, Y2):
        #     plt.text(x+0.4, -y-0.05, '%.2f' % y, ha='center', va='top')

        # plt.xlim(-.5, n)  # plt.xticks([])

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
