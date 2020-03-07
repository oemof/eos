# -*- coding: utf-8 -*-

''' Plots.

Usage: read_results.py [options]

Options:

  -c, --cost=COST          The cost scenario. [default: 1]
  -t, --tech=TECH          The tech scenario. [default: 1]
  -n, --number=NUM         Number of run. [default: 1]
      --num-hh=NUM         Number of households. [default: 84]
      --region=REG         Region.
      --year=YEAR          Weather year. [default: 2005]
      --scenario=SC        Path including the results
      --scenario-year=SY   Scenario year. [default: 2030]
      --ssr=SSR            Self-sufficiency degree. [default: None]
      --profile=PROFILE    Choose between random, summer, winter,
                           day, night, slp_h0, slp and include_g0_l0.
                           [default: random]
      --pv_installed=PV    PV installed.
      --save               Save figure.
  -h, --help               Display this help.

'''

###############################################################################
# imports
###############################################################################
import pickle
import pandas as pd
from docopt import docopt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


class System:
    """
    A quartier class.
    """

    def __init__(self, name=None):
        self.name = name

    def get_results_and_make_dataframe(arguments):

        # smb://192.168.10.14/Caros_Daten/quartier_1000/' +



# HOUSEHOLDS AUTARKIE NICHT VORGEGEBEN
        results_1_bis_20_None = pd.read_pickle('../results/HOUSEHOLDS_QUARTIER/' +
                                       'households_results_' +
                                       '1_bis_20'+
                                       '_1_1_' +
                                        str(arguments['--year']) +
                                       '_None' +
                                       '_' +
                                       '.p')

        results_21_bis_40_None = pd.read_pickle('../results/HOUSEHOLDS_QUARTIER/' +
                                       'households_results_' +
                                       '21_bis_40'+
                                       '_1_1_' +
                                        str(arguments['--year']) +
                                       '_None' +
                                       '_' +
                                       '.p')

        results_41_bis_60_None = pd.read_pickle('../results/HOUSEHOLDS_QUARTIER/' +
                                       'households_results_' +
                                       '41_bis_60'+
                                       '_1_1_' +
                                        str(arguments['--year']) +
                                       '_None' +
                                       '_' +
                                       '.p')

        results_61_bis_74_None = pd.read_pickle('../results/HOUSEHOLDS_QUARTIER/' +
                                       'households_results_' +
                                       '61_bis_74'+
                                       '_1_1_' +
                                        str(arguments['--year']) +
                                       '_None' +
                                       '_' +
                                       '.p')

###################################################################

# DATAFRAME ERSTELLEN
# -------------------------------------------------------------------
        df_None = pd.DataFrame(columns=['storage_cap_None'])
        for house in np.arange(20):
            df_None = df_None.append({'storage_cap_None': results_1_bis_20_None['demand_house_' + str(house+1)]}, ignore_index=True)
        for house in np.arange(20):
            df_None = df_None.append({'storage_cap_None': results_21_bis_40_None['demand_house_' + str(house+1)]}, ignore_index=True)
        for house in np.arange(20):
            df_None = df_None.append({'storage_cap_None': results_41_bis_60_None['demand_house_' + str(house+1)]}, ignore_index=True)
        for house in np.arange(14):
            df_None = df_None.append({'storage_cap_None': results_61_bis_74_None['demand_house_' + str(house+1)]}, ignore_index=True)
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# DEMAND
        df = df_None
        df_ohne_lastprofil_46 = df.drop(axis=0, index=45)
        # with pd.option_context('display.max_rows', 999):
            # print(df_ohne_lastprofil_46)
# -------------------------------------------------------------------

        return (df, df_ohne_lastprofil_46)

# FINAL PLOTS
# -------------------------------------------------------------------
def boxplot(dataframe):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

##############################################################
# ALT: groups nicht möglich
    # dataframe.plot.box(ax=ax,
    #         color=color,
    #         boxprops=dict(linewidth=2),
    #         whiskerprops=dict(linewidth=2),
    #         medianprops=dict(linewidth=2.5, linestyle='--'),
    #         capprops=dict(linewidth=2),
    #         flierprops=dict(markersize=10),
    #         grid=False,
    #         fontsize=28)

    # Add jitter
    # ax = sns.swarmplot(data=dataframe, color=main_color)

# DIESER HIER HAT NICHT ZUSAMMEN MIT COLOR FUNKTIONIERT
    # dataframe.boxplot(ax=ax,
    #         # column=['storage_cap_50', 'storage_cap_60', 'storage_cap_70'],
    #         # column=['storage_cap_None', 'storage_cap_None_BW'],
    #         column=['ssr_None', 'ssr_None_BW'],
    #         color=color,
    #         grid=False,
    #         fontsize=28)
    ##############################################################

    sns.boxplot(data=dataframe,
            width=0.4,
            # width=0.5,
            boxprops=dict(linewidth=2),
            whiskerprops=dict(linewidth=2),
            medianprops=dict(linewidth=2.5, linestyle='--'),
            capprops=dict(linewidth=2),
            flierprops=dict(markersize=10, marker='o', markeredgecolor='black', markerfacecolor='None'),
            palette=['#2ca25f'], ax=ax)

    for i,artist in enumerate(ax.artists):
        artist.set_edgecolor('black')
        # artist.set_facecolor('None')

        for j in range(i*6,i*6+6):
            line = ax.lines[j]
            line.set_color('black')

    # ax.set_xticklabels(['0,50', '0,60', '0,70'], fontsize=28, color=diagram_color)
    # ax.set_xticklabels(['aus SYS-Sicht', 'aus BW-Sicht'], fontsize=28, color=diagram_color)
    # ax.set_ylim([-1, 20])
    # ax.set_ylim([-0.05, 0.8])
    # ax.set_yticks([0, 500, 1000])
    # ax.set_yticks([0, 5, 10, 15, 20])
    # ax.set_yticklabels([0, 5, 10, 15, 20], fontsize=28, color=diagram_color)
    # ax.set_yticks([0, 400, 800, 1200])
    # ax.set_yticklabels([0, 400, 800, 1200], fontsize=28, color=diagram_color)
    # ax.set_yticks([0, 0.20, 0.40, 0.60, 0.80])
    # ax.set_yticklabels(['0', '0,20', '0,40', '0,60', '0,80'], fontsize=28, color=diagram_color)

    # plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    # plt.xlabel('Kostenoptimum', fontsize=28, color=diagram_color)

    # plt.ylabel('Speicherkapazität in kWh', fontsize=28, color=diagram_color)
    # plt.ylabel('Autarkiegrad', fontsize=28, color=diagram_color)
    # # plt.ylabel('Installierte PV-Leistung in kW', fontsize=28, color=diagram_color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    leg = plt.legend(loc='upper left', frameon=False, prop={'size': 28})
    leg._legend_box.align = 'left'
    for color,text in zip(['#FF5050','#ffc000'],leg.get_texts()):
        # for text in leg.get_texts():
            text.set_color(color)

    plt.show()

    return fig


def boxplot_grouped(dataframe_1, dataframe_2):

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot()

    lw = 3
    diagram_color = 'black'
    main_color = '#7f7f7f'
    colors = []

     # ssr
     #######################################################
    df_50 = pd.concat([dataframe_1['storage_cap_50'], dataframe_2['pv_50']], axis=1)

    df_60 = pd.concat([dataframe_1['storage_cap_60'], dataframe_2['pv_60']], axis=1)

    df_70 = pd.concat([dataframe_1['storage_cap_70'], dataframe_2['pv_70']], axis=1)

    df_50 = df_50.rename(columns={
         'storage_cap_50': 'RES in kWh',
         'pv_50': 'PV in kW'})
    df_50["Y"] = 1

    df_60 = df_60.rename(columns={
         'storage_cap_60': 'RES in kWh',
         'pv_60': 'PV in kW'})
    df_60["Y"] = 2

    df_70 = df_70.rename(columns={
         'storage_cap_70': 'RES in kWh',
         'pv_70': 'PV in kW'})
    df_70["Y"] = 3

    dataframe = pd.concat([df_50, df_60, df_70], axis=0)
    ######################################################

    # # no ssr
    # #######################################################
    # df_None = pd.concat([dataframe_1['storage_cap_None'], dataframe_2['pv_None']], axis=1)

    # df_None_BW = pd.concat([dataframe_1['storage_cap_None_BW'], dataframe_2['pv_None_BW']], axis=1)

    # df_None = df_None.rename(columns={
    #     'storage_cap_None': 'RES in kWh',
    #     'pv_None': 'PV in kW'})
    # df_None["Y"] = 1

    # df_None_BW = df_None_BW.rename(columns={
    #     'storage_cap_None_BW': 'RES in kWh',
    #     'pv_None_BW': 'PV in kW'})
    # df_None_BW["Y"] = 2

    # dataframe = pd.concat([df_None, df_None_BW], axis=0)
    #######################################################

    dataframe_2 = pd.melt(dataframe, id_vars="Y")
    dataframe_2.sort_values(["Y", "variable"], ascending=False, inplace=True)

    print(dataframe_2)

    #2ca25f
    #FF5050 # Speicher
    #ffc000

    # flierprops = {'marker':'o','markerfacecolor':None, 'markeredgecolor':'black'}

    sns.boxplot(x="Y", y="value", hue="variable", data=dataframe_2,
            # width=0.4,
            # width=0.5,
            width=0.7,
            boxprops=dict(linewidth=2),
            whiskerprops=dict(linewidth=2),
            medianprops=dict(linewidth=2.5, linestyle='--'),
            capprops=dict(linewidth=2),
            flierprops=dict(markersize=10, marker='o', markeredgecolor='black', markerfacecolor='None'),
            palette=['#FF5050','#ffc000'], ax=ax)

    for i,artist in enumerate(ax.artists):
        artist.set_edgecolor('black')
        # artist.set_facecolor('None')

        for j in range(i*6,i*6+6):
            line = ax.lines[j]
            line.set_color('black')

    ax.set_xticklabels(['0,50', '0,60', '0,70'], fontsize=28, color=diagram_color)
    # ax.set_xticklabels(['aus SYS-Sicht', 'aus BW-Sicht'], fontsize=28, color=diagram_color)
    # ax.set_ylim([-1, 20])
    # ax.set_ylim([-0.05, 0.8])
    # ax.set_yticks([0, 500, 1000])
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.set_yticklabels([0, 5, 10, 15, 20], fontsize=28, color=diagram_color)
    # ax.set_yticks([0, 400, 800, 1200])
    # ax.set_yticklabels([0, 400, 800, 1200], fontsize=28, color=diagram_color)
    # ax.set_yticks([0, 0.20, 0.40, 0.60, 0.80])
    # ax.set_yticklabels(['0', '0,20', '0,40', '0,60', '0,80'], fontsize=28, color=diagram_color)

    plt.xlabel('Autarkiegrad', fontsize=28, color=diagram_color)
    # plt.xlabel('Kostenoptimum', fontsize=28, color=diagram_color)

    plt.ylabel('Speicherkap. in kWh, PV in kW', fontsize=28, color=diagram_color)
    # plt.ylabel('Autarkiegrad', fontsize=28, color=diagram_color)
    # plt.ylabel('Installierte PV-Leistung in kW', fontsize=28, color=diagram_color)

    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(main_color)
    ax.spines['bottom'].set_color(main_color)

    leg = plt.legend(loc='upper left', frameon=False, prop={'size': 28})
    leg._legend_box.align = 'left'
    for color,text in zip(['#FF5050','#ffc000'],leg.get_texts()):
        # for text in leg.get_texts():
            text.set_color(color)

    plt.show()

    return fig

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    sys = System
    (df, df_ohne_lastprofil_46) = sys.get_results_and_make_dataframe(arguments)

    # dataframe_1 = df
    dataframe_1 = df_ohne_lastprofil_46

    fig = boxplot(dataframe_1)
    # fig = boxplot_grouped(dataframe_1, dataframe_2)

    # print('mean', dataframe.mean(0))
    # print('std', dataframe.std(0))
    # print('min', dataframe.min(0))
    # print('quantile_25', dataframe.quantile(0.25))
    # print('median', dataframe.median(0))
    # print('quantile_75', dataframe.quantile(0.75))
    # print('max', dataframe.max(0))
    # print('SUM', dataframe.sum())

    print('mean', dataframe_1.mean(0))
    print('std', dataframe_1.std(0))
    print('min', dataframe_1.min(0))
    print('quantile_25', dataframe_1.quantile(0.25))
    print('median', dataframe_1.median(0))
    print('quantile_75', dataframe_1.quantile(0.75))
    print('max', dataframe_1.max(0))
    print('SUM', dataframe_1.sum())

    # print('mean', dataframe_2.mean(0))
    # print('std', dataframe_2.std(0))
    # print('min', dataframe_2.min(0))
    # print('quantile_25', dataframe_2.quantile(0.25))
    # print('median', dataframe_2.median(0))
    # print('quantile_75', dataframe_2.quantile(0.75))
    # print('max', dataframe_2.max(0))
    # print('SUM', dataframe_2.sum())

    if arguments['--save']:
        fig.savefig(os.path.join(os.path.dirname(__file__)) +
                'current_figure' +
                '.pdf')
