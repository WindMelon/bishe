#-*- coding:utf-8 -*-
#@author:zhanhao
#@project:Graduation Project
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.spatial.distance as distance
import scipy.cluster.hierarchy as sch


# helper for cleaning up axes by removing ticks, tick labels, frame, etc.
def clean_axis(ax):
    """Remove ticks, tick labels, and frame from axis"""
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

def draw_heatmap(filename,testDF):
    testDF.index = ['Sample ' + str(x) for x in testDF.index]
    testDF.columns = ['c' + str(x) for x in testDF.columns]
    # calculate pairwise distances for rows
    pairwise_dists = distance.squareform(distance.pdist(testDF))
    # cluster
    row_clusters = sch.linkage(pairwise_dists,method='complete')
    # calculate pairwise distances for columns
    col_pairwise_dists = distance.squareform(distance.pdist(testDF.T))
    # cluster
    col_clusters = sch.linkage(col_pairwise_dists,method='complete')

    # make dendrograms black rather than letting scipy color them
    sch.set_link_color_palette(['black'])

    # heatmap with row names
    fig = plt.figure()
    heatmapGS = gridspec.GridSpec(2,2,wspace=0.0,hspace=0.0,width_ratios=[0.25,1],height_ratios=[0.25,1])

    ### col dendrogram ###
    col_denAX = fig.add_subplot(heatmapGS[0,1])
    col_denD = sch.dendrogram(col_clusters,color_threshold=np.inf)
    clean_axis(col_denAX)

    ### row dendrogram ###
    row_denAX = fig.add_subplot(heatmapGS[1,0])
    row_denD = sch.dendrogram(row_clusters,color_threshold=np.inf,orientation='left')
    clean_axis(row_denAX)

    ### heatmap ####
    heatmapAX = fig.add_subplot(heatmapGS[1,1])
    axi = heatmapAX.imshow(testDF.ix[row_denD['leaves'],col_denD['leaves']],interpolation='nearest',aspect='auto',origin='lower',cmap=plt.cm.RdBu)
    clean_axis(heatmapAX)

    ## row labels ##
    heatmapAX.set_yticks(np.arange(testDF.shape[0]))
    heatmapAX.yaxis.set_ticks_position('right')
    heatmapAX.set_yticklabels(testDF.index[row_denD['leaves']])

    ## col labels ##
    heatmapAX.set_xticks(np.arange(testDF.shape[1]))
    xlabelsL = heatmapAX.set_xticklabels(testDF.columns[col_denD['leaves']])
    # rotate labels 90 degrees
    for label in xlabelsL:
        label.set_rotation(90)
    # remove the tick lines
    for l in heatmapAX.get_xticklines() + heatmapAX.get_yticklines():
        l.set_markersize(0)

    fig.tight_layout()
    plt.savefig("./"+filename+"/"+filename+'_heatmap.png',dpi = 200)

def draw_boxplot(filename,df):
    fig = plt.figure()
    df.boxplot(showfliers=False)
    plt.savefig("./"+filename+"/"+filename+'_boxplot.png',dpi = 200)

def draw_vocalno(filename,x,y):
    pass