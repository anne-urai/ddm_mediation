#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Load in ground-truth simulations together with fits from lavaan, HDDMnn and pyDDM. Visualize the results.
Created on Fri Mar 11 10:35:42 2022

@author: urai
"""

import pandas as pd
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

mypath = '/Users/urai/Documents/code/ddm_mediation'

#%%
def corrfunc(x, y, **kws):

    # compute spearmans correlation
    r, pval = sp.stats.spearmanr(x, y, nan_policy='omit')
    print('%s, %s, %.2f, %.3f'%(x.name, y.name, r, pval))

    if 'ax' in kws.keys():
        ax = kws['ax']
    else:
        ax = plt.gca()

    # if this correlates, draw a regression line across groups
    if pval < 0.0001:
        sns.regplot(x, y, truncate=True, color='gray',
        scatter=False, ci=None, robust=True, ax=ax)

    # now plot the datapoints
    sns.regplot(x=x, y=y, fit_reg=False, truncate=True, **kws)
    plt.axis('tight')

    # annotate with the correlation coefficient + n-2 degrees of freedom
    txt = r"$\rho$({}) = {:.3f}".format(len(x)-2, r) + "\n" + "p = {:.4f}".format(pval)
    if pval < 0.0001:
        txt = r"$\rho$({}) = {:.3f}".format(len(x)-2, r) + "\n" + "p < 0.0001"
    ax.annotate(txt, xy=(.7, .1), xycoords='axes fraction', fontsize='small')
    
    # indicate identity line?


#%%

for eff_x in ['v', 'z',  'no']:
    for eff_m in ['v', 'z',  'no']:
        
        ## load ground-truth data
        sim_df = pd.read_csv('%s/data/param_df_X%s_M%s.csv'%(mypath, eff_x, eff_m))
        sim_df.columns = sim_df.columns.map(lambda x: 'sim_' + str(x))
        sim_df = sim_df.rename(columns={'sim_subj_idx':'subj_idx'})
        
        ## load lavaan-fitted data
        lavaan_df = pd.read_csv('%s/data/fit_lavaan_X%s_M%s.csv'%(mypath, eff_x, eff_m))
        lavaan_df = lavaan_df.pivot_table(values='est', index='subj_idx', columns='label').reset_index()
        lavaan_df.columns = lavaan_df.columns.map(lambda x: 'lav_' + str(x))
        lavaan_df = lavaan_df.rename(columns={'lav_subj_idx':'subj_idx'})

        # merge
        df = pd.merge(lavaan_df, sim_df, on='subj_idx')
        print(df.columns)

        # force the same kind of plot regardless of the dataset
        sim_vars = ['sim_v_S', 'sim_v_X', 'sim_z_X', 'sim_v_M', 'sim_z_M']
        for s in sim_vars:
            if s not in df.columns:
                df[s] = np.nan
    
        g = sns.PairGrid(data=df, y_vars=['lav_s0', 'lav_direct', 'lav_indirect', 'lav_total'],
                   x_vars=sim_vars)
        g.map(corrfunc)
        plt.suptitle('X affects %s, M affects %s'%(eff_x, eff_m))
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        g.savefig(os.path.join(mypath, 'figures', 'recover_sim_lavaal_X%s_M%s.pdf'%(eff_x, eff_m)),
                                facecolor='white')