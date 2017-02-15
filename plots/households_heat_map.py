
# -*- coding: utf-8 -*-

''' Plots.

Usage: households_plots.py [options]

Options:

'''

###############################################################################
# imports
###############################################################################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_data():
    data = pd.read_csv('households.csv', delimiter=',')
    return data


def contour_plot(data):
    plt.figure()
    x = np.arange(50, 110, 10)
    y = data['demand']
    print(y)
    X, Y = np.meshgrid(x, y)
    Z = data[['50', '60', '70', '80', '90', '100']]
    print(Z)
    plt.contourf(X, Y, Z)
    cb = plt.colorbar()
    cb.set_label('Storage capacity in kWh', size=30)
    plt.xlabel('Self-sufficiency degree in %', size=30)
    plt.ylabel('Annual demand in kWh', size=30)
    plt.rcParams.update({'font.size': 24})

    plt.show()


if __name__ == '__main__':
    data = read_data()
    contour_plot(data)
