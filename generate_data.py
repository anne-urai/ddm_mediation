#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:16:27 2022

@author: urai
"""

# MODULE IMPORTS ----
# warning settings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Data management
import pandas as pd
import numpy as np
import pickle, os, time

# Plotting
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# Stats functionality
from statsmodels.distributions.empirical_distribution import ECDF

# to download data
# from google.colab import files
import pprint

# HDDM
import hddm

# find path depending on location and dataset
usr = os.environ['USER']
if 'aeurai' in usr: # lisa/snellius
  mypath = '/home/aeurai/code/ddm_mediation'
elif 'urai' in usr:  # mbp laptop
  mypath = '/Users/urai/Documents/code/ddm_mediation'
print(mypath)

#%% ============================================================= ##
## generate some artificial choice data with mediation variable
##  ============================================================= ##

print('generating artificial choice data')
# first, previous choices ('X')
n_trials = int(1e4) # https://github.com/anne-urai/2019_Urai_choice-history-ddm/blob/master/simulations/1_ddm_rts.py#L84
n_subj = 40
df = pd.DataFrame(np.random.choice([-1,1], (n_trials*n_subj, 2)), columns=list('XS')) 

# make sure we have subj_idx and trial_idx
subj_idx = []
for s in np.arange(n_subj) + 1:
  for n in np.arange(n_trials):
    subj_idx.append(s)

trial_idx = []
for s in np.arange(n_subj) + 1:
  for n in np.arange(n_trials):
    trial_idx.append(n)

df['subj_idx'] = subj_idx
df['trial_idx'] = trial_idx
df.head(n=10)


#%% then a normally distributed random variable, that depends on X
a_path = np.random.normal(size=n_subj)

df['M'] = np.nan
for sjidx, (sj, sjdat) in enumerate(df.groupby(['subj_idx'])):
  this_M = np.random.normal(size=sjdat['X'].shape) + a_path[sjidx] * sjdat['X']
  df.loc[df.subj_idx == sj, 'M'] = this_M

df = df[['subj_idx', 'trial_idx', 'S', 'X', 'M']]

a_df = pd.DataFrame()
a_df['subj_idx'] = df.subj_idx.unique()
a_df['a_path'] = a_path
a_df

# #%% # DOES M DEPEND ON X (a-path)?
# import statsmodels.api as sm
# from patsy import dmatrices

# a_df['intercept'] = np.nan
# a_df['slope'] = np.nan
# for sjidx, (sj, sjdat) in enumerate(df.groupby(['subj_idx'])):

#   #fit linear regression model
#   y, X = dmatrices('M ~ 1 + X', 
#                    data=sjdat, return_type='dataframe')
#   model = sm.OLS(y, X).fit()
#   a_df.loc[a_df.subj_idx == sj, 'intercept'] = model.params[0]
#   a_df.loc[a_df.subj_idx == sj, 'slope'] = model.params[1]

# # # see the separation
# # g = sns.FacetGrid(data=df, col='subj_idx', col_wrap=5, hue='X')
# # g.map(sns.distplot, 'M')
# # sns.scatterplot(a_df.a_path, a_df.slope)

#%%
##  ============================================================= ##
# plug into the HDDMnn simulator to simulate choices and RTs
##  ============================================================= ##

# help(hddm.simulators.hddm_dataset_generators.simulator_h_c)
# see https://hddm.readthedocs.io/en/latest/lan_tutorial.html#section-5-regressors 
# forum request for bug: https://groups.google.com/g/hddm-users/c/bdKDkwuQ3tk
print('using HDDMnn simulator to generate choices and RTs')

for eff_x in ['v', 'z', 'vz', 'no']:
  for eff_m in ['v', 'z', 'vz', 'no']:

    t_start = time.time()

    # simulate a couple of datasets: where X/M affects v/z/nothing
    regr_v = 'v ~ 1 + S'
    if 'v' in eff_x:
      regr_v = regr_v + ' + X'
    if 'v' in eff_m:
      regr_v = regr_v + ' + M'

    regr_z = 'z ~ 1'
    if 'z' in eff_x:
      regr_z = regr_z + ' + X'
    if 'z' in eff_m:
      regr_z = regr_z + ' + M'

    print(eff_x, '; ', 
          eff_m, '; ',
          regr_v, '; ',
          regr_z)

    # plug this into the simulator
    data, full_parameter_dict = hddm.simulators.hddm_dataset_generators.simulator_h_c(data = df, 
                                                                                  model = 'ddm',
                                                                                  p_outlier = 0.00,
                                                                                  conditions = None, 
                                                                                  depends_on = None, 
                                                                                  regression_models = [regr_v, regr_z], 
                                                                                  regression_covariates = ['S', 'X'],
                                                                                  group_only = None,
                                                                                  group_only_regressors = False,
                                                                                  fixed_at_default = None)

    # export the parameter_dict into df
    # from https://github.com/anne-urai/MEG/blob/master/hddm_funcs_plot.py#L66
    # https://github.com/anne-urai/hddm/blob/master/hddm/utils.py#L925
    param_dict = {}
    for key, value in full_parameter_dict.items():
        if 'reg' not in key:
            param_dict[key] = value
    param_dict
    param_df = pd.DataFrame.from_dict(param_dict, orient='index').reset_index()
    param_df = hddm.utils.results_long2wide(param_df, 
                                            name_col="index", 
                                            val_col=0)
    # add the simulated a-path here
    param_df['subj_idx'] = param_df['subj_idx'].astype(np.int64)
    a_df['subj_idx'] = a_df['subj_idx'].astype(np.int64)
    param_df = pd.merge(param_df, a_df[['subj_idx', 'a_path']], on='subj_idx')

    # save the data and param_df to files for later fitting
    # see https://colab.research.google.com/notebooks/io.ipynb#scrollTo=p2E4EKhCWEC5
    
    param_df.to_csv('%s/data/param_df_X%s_M%s.csv'%(mypath, eff_x, eff_m))
    #files.download('param_df_X%s_M%s.csv'%(eff_x, eff_m))

    data.to_csv('%s/data/data_df_X%s_M%s.csv'%(mypath, eff_x, eff_m))
    #files.download('data_df_X%s_M%s.csv'%(eff_x, eff_m))
    
    elapsed = time.time() - t_start
    print('Elapsed time: %.2f seconds' % (elapsed))

