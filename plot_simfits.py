#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Load in ground-truth simulations together with fits from lavaan, HDDMnn and pyDDM. Visualize the results.
Created on Fri Mar 11 10:35:42 2022

@author: urai
"""

import pandas as pd
import seaborn as sns

mypath = '/Users/urai/Documents/code/ddm_mediation'

#%%

for eff_x in ['v', 'z', 'no']:
    for eff_m in ['v', 'z', 'no']:
        
        ## load ground-truth data
        sim_df = pd.read_csv('%s/data/param_df_X%s_M%s.csv'%(mypath, eff_x, eff_m))
        
        ## load lavaan-fitted data
        lavaan_df = pd.read_csv('%s/data/fit_lavaan_X%s_M%s.csv'%(mypath, eff_x, eff_m))
        lavaan_df = lavaan_df.pivot_table(values='est', index='subj_idx', columns='label').reset_index()
        
        # merge
        df = pd.merge(lavaan_df, sim_df, on='subj_idx')

    
