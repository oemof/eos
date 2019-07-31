# -*- coding: utf-8 -*-

''' Plot various load profiles in carpet.

Usage: carpet_plot.py [options]

Options:

  -l, --load=LOAD          The load profile.
  -c, --cost=COST          The cost scenario. [default: 1]
  -t, --tech=TECH          The tech scenario. [default: 1]
      --num-hh=NUM         Number of households. [default: 84]
      --year=YEAR          Weather year. [default: 2010]
      --ssr=SSR            Self-sufficiency degree. [default: None]
      --profile=PROFILE    Choose between random, summer, winter,
                           day, night, slp_h0, slp and incl_g0_l0.
                           [default: random]
      --single-result=RES  The result you want to plot. Choose between
                           ts_demand_house_1 (or any house number you want)
                           ts_pv_house_1 (or any house number you want)
                           ts_excess_house_1 (or any house number you want)
                           ts_feedin_house_1 (or any house number you want)
      --sum-result=SRES    The result you want to plot. Choose between
                           ts_demand, ts_pv, ts_excess and ts_feedin.
      --stand              Standardize profile to 1.
      --carpet             Plot carpet.
      --line               Plot line.
      --save               Save figure.
  -h, --help               Display this help.

'''

###############################################################################
# imports
###############################################################################
from docopt import docopt
import pandas as pd
import os
import quartier_plots
import carpet_plot


def get_profile(args):
    # profiles = pd.read_csv(
    #     '../example/example_data/example_data_load_hourly_mean_74_profiles.csv',
    #     delimiter=',') / 1000

    # profile = profiles['hh_' + str(arguments['--load'])]

    # profile = profile/profile.sum()*1000
    # print(profile)

    if arguments['--single-result']:
        results = quartier_results.get_results(arguments)
        profile = results[str(arguments['--single-result'])].val

    elif arguments['--sum-result']:
        results = quartier_results.get_results(arguments)
        profile = results[str(arguments['--sum-result'])]
        summed_profile = profile.sum(axis=1)

    return summed_profile


def standardize_profile(summed_profile):

    standardized_profile = summed_profile / summed_profile.max()

    return standardized_profile


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    quartier_results = quartier_plots.Quartier
    profile = get_profile(arguments)
    print(profile.size)
    print(profile.sum())
    if arguments['--stand']:
        profile = standardize_profile(profile)
    if arguments['--carpet']:
        carpet = carpet_plot.Carpet
        fig = carpet.carpet_plot(profile,
                                 res_name=str(arguments['--sum-result']),
                                 show=True)
    if arguments['--line']:
        line = carpet_plot.Line
        fig = line.line_plot(profile,
                             res_name=str(arguments['--sum-result']),
                             show=True)
    if arguments['--save']:
        if arguments['--carpet']:
            if arguments['--single-result']:
                fig.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures') +
                                         '/' + 'quartier_fig_' +
                                         'carpet' + '_' +
                                         str(arguments['--num-hh']) + '_' +
                                         str(arguments['--cost']) + '_' +
                                         str(arguments['--year']) + '_' +
                                         str(arguments['--ssr']) + '_' +
                                         str(arguments['--profile']) + '_' +
                                         str(arguments['--single-result']) + '_' +
                                         str(arguments['--stand']) +
                                         '.png')

            elif arguments['--sum-result']:
                fig.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures') +
                                         '/' + 'quartier_fig_' +
                                         'carpet' + '_' +
                                         str(arguments['--num-hh']) + '_' +
                                         str(arguments['--cost']) + '_' +
                                         str(arguments['--year']) + '_' +
                                         str(arguments['--ssr']) + '_' +
                                         str(arguments['--profile']) + '_' +
                                         str(arguments['--sum-result']) + '_' +
                                         str(arguments['--stand']) +
                                         '.png')

        if arguments['--line']:
            if arguments['--single-result']:
                fig.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures') +
                                         '/' + 'quartier_fig_' +
                                         'line' + '_' +
                                         str(arguments['--num-hh']) + '_' +
                                         str(arguments['--cost']) + '_' +
                                         str(arguments['--year']) + '_' +
                                         str(arguments['--ssr']) + '_' +
                                         str(arguments['--profile']) + '_' +
                                         str(arguments['--single-result']) + '_' +
                                         str(arguments['--stand']) +
                                         '.png')

            elif arguments['--sum-result']:
                fig.savefig(os.path.join(os.path.dirname(__file__), 'saved_figures') +
                                         '/' + 'quartier_fig_' +
                                         'line' + '_' +
                                         str(arguments['--num-hh']) + '_' +
                                         str(arguments['--cost']) + '_' +
                                         str(arguments['--year']) + '_' +
                                         str(arguments['--ssr']) + '_' +
                                         str(arguments['--profile']) + '_' +
                                         str(arguments['--sum-result']) + '_' +
                                         str(arguments['--stand']) +
                                         '.png')


