#-*- coding:utf-8 -*-
#@author:zhanhao
#@project:Graduation Project
import Alert_window
from search import *
import sys
from PyQt4 import QtCore, QtGui, uic
import download_window
import download_and_parse

qtCreatorFile = "mainwindow.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.CheckBox = 0
        self.start_flag = 0
        self.result = 0
        self.cur_page = 0
        self.analyze_app = 0
        self.error = 0
        self.terms.returnPressed.connect(self.start_search)
        self.lineEdit.returnPressed.connect(self.start_search)
        self.search_button.clicked.connect(self.start_search)
        self.First_button.clicked.connect(self.First_page)
        self.Last_button.clicked.connect(self.Last_page)
        self.Prev_button.clicked.connect(self.Prev_page)
        self.Next_button.clicked.connect(self.Next_page)
        self.checkBox.clicked.connect(self.select_all)
        self.download_button.clicked.connect(self.download)
        self.tableWidget.clicked.connect(self.analyze)
        self.tableWidget.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)


    def show_on_table(self):
        self.lineEdit.setText(str(self.cur_page))
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().resizeSection(0, 30)
        self.tableWidget.horizontalHeader().resizeSection(1, 100)
        self.tableWidget.horizontalHeader().resizeSection(2, 100)
        self.tableWidget.horizontalHeader().resizeSection(3, 100)
        self.tableWidget.horizontalHeader().resizeSection(4, 100)
        self.tableWidget.horizontalHeader().resizeSection(5, 400)
        self.tableWidget.horizontalHeader().resizeSection(6, 400)
        self.tableWidget.horizontalHeader().resizeSection(7, 300)
        self.tableWidget.setHorizontalHeaderLabels(['','Accession', 'GPL', 'type','samples_n', 'title', 'summary', 'ftplink'])
        gses , types= self.result.fetch_by_page(self.cur_page)
        self.CheckBox = [None] * 20
        for i in range(20):
            self.CheckBox[i] = QtGui.QCheckBox()
            self.CheckBox[i].setText('')
        i = 0
        for gse in gses:
            # print(str(gse['Accession'])+'\t'+str(gse['GPL'])+'\t'+str(gse['n_samples'])+'\t'+str(gse['title'])+'\t'+str(gse['summary'])+'\t'+str(gse['FTPLink']))
            # print(i)
            self.tableWidget.insertRow(i)
            self.tableWidget.setCellWidget(i, 0, self.CheckBox[i])
            self.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(str(gse['Accession'])))
            self.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(str(gse['GPL'])))
            self.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(str(types[i])))
            self.tableWidget.setItem(i, 4, QtGui.QTableWidgetItem(str(gse['n_samples'])))
            self.tableWidget.setItem(i, 5, QtGui.QTableWidgetItem(str(gse['title'])))
            self.tableWidget.setItem(i, 6, QtGui.QTableWidgetItem(str(gse['summary'])))
            self.tableWidget.setItem(i, 7, QtGui.QTableWidgetItem(str(gse['FTPLink'])))
            i += 1

    def start_search(self):
        self.start_flag = 1
        #self.tableWidget.setColumnCount(6)
        #self.tableWidget.setRowCount(0)
        #self.tableWidget.horizontalHeader().resizeSection(0,250)
        #self.tableWidget.horizontalHeader().resizeSection(1,250)
        #self.tableWidget.horizontalHeader().resizeSection(2,250)
        #self.tableWidget.horizontalHeader().resizeSection(3,400)
        #self.tableWidget.horizontalHeader().resizeSection(4,400)
        #self.tableWidget.horizontalHeader().resizeSection(5,300)
        #self.tableWidget.setHorizontalHeaderLabels(['Accession','GPL','sample_number','title','summary','ftplink'])
        #self.terms.setText(str(self.comboBox.currentText()+self.comboBox_2.currentText()))
        #print(self.terms.text())
        self.result = esearch(query=self.terms.text(),gdsType=self.comboBox.currentText(),species=self.comboBox_2.currentText())
        self.label_2.setText(str(self.result.pages))
        self.cur_page = int(self.lineEdit.text())
        self.show_on_table()

    def First_page(self):
        self.cur_page = 1
        self.show_on_table()

    def Last_page(self):
        self.cur_page = self.result.pages
        self.show_on_table()

    def Prev_page(self):
        if self.cur_page == 1:
            pass
        else:
            self.cur_page -= 1
            self.show_on_table()

    def Next_page(self):
        if self.cur_page == self.result.pages:
            pass
        else:
            self.cur_page += 1
            self.show_on_table()

    def select_all(self):
        if self.start_flag == 0:
            pass
        else:
            if self.checkBox.isChecked():
                for i in range(20):
                    self.CheckBox[i].setChecked(True)
            else:
                for i in range(20):
                    self.CheckBox[i].setChecked(False)

    def download(self):
        for i in range(20):
            if self.CheckBox[i].isChecked():
                gse_acc = self.tableWidget.item(i, 1).text()
                download_and_parse.download_soft(gse_acc)

    def analyze(self):
        if self.tableWidget.currentColumn() != 1:
            pass
        else:
            try:
                GSE_acc = self.tableWidget.item(self.tableWidget.currentRow(), self.tableWidget.currentColumn()).text()
                gse = download_and_parse.fetch_data(GSE_acc)
                self.analyze_app = download_window.MyApp(GSE_acc,gse)
                self.analyze_app.show()
            except KeyError:
                self.error = Alert_window.MyApp()
                self.error.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


