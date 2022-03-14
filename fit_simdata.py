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

# HDDM
import hddm

# find path depending on location and dataset
usr = os.environ['USER']
if 'aeurai' in usr: # lisa/snellius
  mypath = '/home/aeurai/code/ddm_mediation'
elif 'uraiae' in usr: # alice
  mypath = '/home/uraiae/code/ddm_mediation'
elif 'urai' in usr:  # mbp laptop
  mypath = '/Users/urai/Documents/code/ddm_mediation'
print(mypath)

#%% ============================================================= ##
## generate some artificial choice data with mediation variable
##  ============================================================= ##

for eff_x in ['v', 'no']: #, 'z', 'vz', 'no']:
  for eff_m in ['v', 'no']: #, 'z', 'vz', 'no']:

        t_start = time.time()
        
        # grab datafile from home directory (can also read from GitHub)
        data = pd.read_csv('%s/data/data_df_X%s_M%s.csv'%(mypath, eff_x, eff_m))
        
        # Set up the regressors
        reg_model_v = {'model': 'v ~ 1 + S + M + X', 'link_func': lambda x: x}
        # reg_model_z = {'model': 'z ~ 1 + prevresp', 'link_func': lambda x: x}
        reg_descr = [reg_model_v]
        
        model = 'ddm' # start simple
        n_samples = 1000
        hddmnn_model = hddm.HDDMnn(data,
                                   model = model,
                                   include = hddm.simulators.model_config[model]['hddm_include'],
                                   p_outlier = 0.05,
                                   is_group_model = True,
                                   informative = False)
        hddmnn_model.sample(n_samples, burn = n_samples/10)
        # 
        md_summ = hddmnn_model.gen_stats().reset_index()
        # df_summ = hddm.utils.results_long2wide(md_summ, name_col='index', val_col='mean')
        
        # see https://colab.research.google.com/notebooks/io.ipynb#scrollTo=p2E4EKhCWEC5
        md_summ.to_csv('%s/fit_hddmnn_X%s_M%s.csv'%(mypath, eff_x, eff_m))
        # files.download('fit_hddmnn_X%s_M%s.csv'%(eff_x, eff_m))
        
        elapsed = time.time() - t_start
        
        print('Elapsed time: %.2f seconds' % (elapsed))
         
