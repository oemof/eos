
# -*- coding: utf-8 -*-

''' Plots.

Usage: quartier_heat_map.py [options]

Options:

'''

###############################################################################
# imports
###############################################################################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib import ticker
# from matplotlib.colors import LogNorm


def read_data():
    data = pd.read_csv('csv/quartier_strompreis_ssr_detailled.csv', delimiter=',')
    return data


def contour_plot(data):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # x = 500 / np.arange(50, 1050, 50)
    x = 500 / np.arange(450, 1050, 50)
    y = data['strompreis']
    print(y)
    X, Y = np.meshgrid(x, y)
    # Z = data[['50', '100', '150', '200', '250', '300', '350', '400', '450',
    #           '500', '550', '600', '650', '700', '750', '800', '850', '900',
    #           '950', '1000']]  # / 500000  # / 500
    Z = data[['450',
              '500', '550', '600', '650', '700', '750', '800', '850', '900',
              '950', '1000']]  # / 500
    print(Z)
    axim = ax.contourf(X, Y, Z)
    cb = fig.colorbar(axim)
    cb.set_label('Self-sufficiency degree in %', size=30)
    plt.xscale('log')
    ax.tick_params(axis='x', which='minor', width=2, length=5, color='r')
    plt.xlabel('Demand to PV capacity in MWh/kWp', size=30)
    plt.ylabel('Electricity cost from grid in EUR/kWh', size=30)
    plt.rcParams.update({'font.size': 24})

    plt.show()


if __name__ == '__main__':
    data = read_data()
    contour_plot(data)
