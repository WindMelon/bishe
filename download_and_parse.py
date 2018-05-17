#-*- coding:utf-8 -*-
#@author:zhanhao
#@project:Graduation Project
import GEOparse

def fetch_data(gse_acc):
    mkdir("./" + gse_acc + "/")
    gse = GEOparse.get_GEO(geo=gse_acc,destdir="./"+gse_acc+"/")
    #pivoted_control_samples = gse.pivot_samples('VALUE')

    return gse
    #print(pivoted_control_samples.head().index.values)
    #heatmap.draw(pivoted_control_samples.head(200))

def download_soft(gse_acc):
    mkdir("./" + gse_acc + "/")
    GEOparse.get_GEO(geo=gse_acc,destdir="./"+gse_acc+"/")


def mkdir(path):
    import os

    path = path.strip()
    path = path.rstrip("\\")

    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False