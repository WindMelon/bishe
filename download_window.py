#-*- coding:utf-8 -*-
#@author:zhanhao
#@project:Graduation Project
import sys
from PyQt4 import QtCore, QtGui, uic
import pandas as pd
import geo2py
import analyze
import draw_maps
import boxplotwindow

qtCreatorFile = "downloadwindow.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self,gse_acc,gse):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.gse_acc = gse_acc
        self.DF = gse.pivot_samples('VALUE')
        self.gse = gse
        self.refresh(self.DF)
        self.pushButton.clicked.connect(self.download_full)
        self.pushButton_3.clicked.connect(self.geo2py)
        self.pushButton_2.clicked.connect(self.log2_transform)
        self.log2_transform_flag = 0
        self.normalized_flag = 0
        self.pushButton_4.clicked.connect(self.view_boxplot)
        self.pushButton_5.clicked.connect(self.normalize)
        self.boxplot_window = 0



    def refresh(self,dataframe):
        dataframe = dataframe.head(250)
        row_n = len(dataframe.index)
        col_n = len(dataframe.columns)
        self.tableWidget.setColumnCount(col_n)
        self.tableWidget.setRowCount(row_n)
        self.tableWidget.setHorizontalHeaderLabels(dataframe.columns.tolist())
        self.tableWidget.setVerticalHeaderLabels([str(x) for x in dataframe.index.tolist()])
        #print(dataframe.columns)
        for i in range(col_n):
            self.tableWidget.horizontalHeader().resizeSection(i,150)
        for i in range(col_n):
            for j in range(row_n):
                self.tableWidget.setItem(j,i,QtGui.QTableWidgetItem(str(dataframe.iat[j,i])))

    def download_full(self):
        self.gse.pivot_samples('VALUE').to_csv(path_or_buf = "./"+self.gse_acc+"/"+self.gse_acc+".csv",sep = "\t")

    def geo2py(self):
        self.geo2py_app = geo2py.MyApp(self.gse,self.DF,self.gse_acc)
        self.geo2py_app.show()

    def log2_transform(self):
        if self.log2_transform_flag == 0:
            self.DF = analyze.log2_transform(self.gse.pivot_samples('VALUE'))
            self.log2_transform_flag = 1
            self.refresh(self.DF)
        else:
            pass

    def normalize(self):
        if self.normalized_flag == 0:
            self.DF = analyze.normalize(self.gse.pivot_samples('VALUE'))
            self.normalized_flag = 1
            self.refresh(self.DF)
        else:
            pass

    def view_boxplot(self):
        draw_maps.draw_boxplot(self.gse_acc,self.DF)
        self.boxplot_window = boxplotwindow.MyApp(self.gse_acc)
        self.boxplot_window.show()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())