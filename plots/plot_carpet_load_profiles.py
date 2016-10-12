# -*- coding: utf-8 -*-

''' Plot various load profiles in carpet.

Usage: carpet_plot.py [options]

Options:

  -l, --load=LOAD          The load profile.
  -h, --help               Display this help.

'''

###############################################################################
# imports
###############################################################################
from docopt import docopt
import pandas as pd
import carpet_plot


def read_profile(args):
    profiles = pd.read_csv(
        '../example/example_data/example_data_load_hourly_mean_74_profiles.csv',
        delimiter=',') / 1000

    profile = profiles['hh_' + str(arguments['--load'])]

    profile = profile/profile.sum()*1000
    print(profile)

    return profile


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    profile = read_profile(arguments)
    carpet = carpet_plot.Carpet
    carpet.carpet_plot(profile)
