from scipy.spatial.distance import pdist
import scipy.cluster.hierarchy as hierarchy
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import pylab as pl

def hclust_sort(df, sort_cols=True, sort_rows=True):
    '''Sort an array by the hierarchical leaf ordering.

    Parameters:
        sort_cols: apply hclust sorting to columns
        sort_rows: apply hclust sorting to rows

    Return:
        the dataframe sorted according to the hierarchical clustering leaf-order

    '''
    
    df_orig = df.copy()
    df = df.copy()
    scaler = MinMaxScaler((0.01,1.))
    scaled_values = scaler.fit_transform(df)
    df.loc[:,:] = scaled_values
        
    row_sorting = list(range(df.shape[0]))
    col_sorting = list(range(df.shape[1]))
    if sort_rows:
        D = pdist(df, 'euclidean')
        Z = hierarchy.linkage(D)
        row_sorting = hierarchy.leaves_list(Z)
    if sort_cols:
        D = pdist(df.T, 'euclidean')
        Z = hierarchy.linkage(D)
        col_sorting = hierarchy.leaves_list(Z)
    return df_orig.iloc[row_sorting][df_orig.columns[col_sorting]]

