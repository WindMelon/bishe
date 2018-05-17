#-*- coding:utf-8 -*-
#@author:zhanhao
#@project:Graduation Project
import numpy as np
from scipy.stats import ttest_ind

def normalize(df):
    df_norm = df.apply(lambda x: (x - np.mean(x)) / (np.std(x)))
    return df_norm

def log2_transform(df):
    df_norm = df.apply(lambda x: np.log2(x))
    return df_norm

def diff_gene(df,control,test,log2fc_cutoff,p_cutoff,gse_acc):
    col_n = len(df.columns)
    row_n = len(df.index)
    log2_fc = list()
    P_value = list()
    for i in range(row_n):
        log2_fc.append(np.mean(df[control].ix[i])-np.mean(df[test].ix[i]))
        P_value.append(ttest_ind(df[control].ix[i], df[test].ix[i])[1])
    df['log2_fc'] = log2_fc
    df['P_value'] = P_value
    df = df[df.P_value < float(p_cutoff)][df.log2_fc > float(log2fc_cutoff)]
    df.to_csv(path_or_buf="./"+gse_acc+"/"+gse_acc+".txt", sep="\t")
    return (df[control+test],log2_fc,P_value)
