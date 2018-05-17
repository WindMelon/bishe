import sys
from PyQt4 import QtCore, QtGui, uic
import analyze
import draw_maps

qtCreatorFile = "geo2py.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self,gse,df,gse_acc):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.CheckBox1 = 0
        self.CheckBox2 = 0
        self.df = df
        self.gse_acc = gse_acc
        self.refresh(gse)
        self.p_cutoff = self.comboBox.currentText()
        self.log2fc_cutoff = self.comboBox_2.currentText()
        self.pushButton.clicked.connect(self.Go_analyze)


    def refresh(self,gse):
        col_n = 5
        row_n = len(gse.gsms.items())
        self.tableWidget.setColumnCount(col_n)
        self.tableWidget.setRowCount(row_n)
        self.tableWidget.setHorizontalHeaderLabels(["group1","group2","Accession","Title","Source name"])
        self.tableWidget.horizontalHeader().resizeSection(0, 70)
        self.tableWidget.horizontalHeader().resizeSection(1, 70)
        self.tableWidget.horizontalHeader().resizeSection(2,160)
        self.tableWidget.horizontalHeader().resizeSection(3,500)
        self.tableWidget.horizontalHeader().resizeSection(4,160)
        i = 0
        self.CheckBox1 = [None] * row_n
        self.CheckBox2 = [None] * row_n
        for gsm_name, gsm in gse.gsms.items():
            self.CheckBox1[i] = QtGui.QCheckBox()
            self.CheckBox1[i].setText('')
            self.CheckBox2[i] = QtGui.QCheckBox()
            self.CheckBox2[i].setText('')
            self.tableWidget.setCellWidget(i, 0, self.CheckBox1[i])
            self.tableWidget.setCellWidget(i, 1, self.CheckBox2[i])
            self.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(gsm_name))
            self.tableWidget.setItem(i, 3, QtGui.QTableWidgetItem(", ".join(gsm.metadata["title"])))
            self.tableWidget.setItem(i, 4, QtGui.QTableWidgetItem(", ".join(gsm.metadata["source_name_ch1"])))
            i += 1

    def Go_analyze(self):
        control = list()
        test = list()
        for i in range(len(self.CheckBox1)):
            if self.CheckBox1[i].isChecked():
                control.append(self.tableWidget.item(i, 2).text())
        for i in range(len(self.CheckBox2)):
            if self.CheckBox2[i].isChecked():
                test.append(self.tableWidget.item(i, 2).text())
        diff_gene = analyze.diff_gene(self.df, control, test, self.log2fc_cutoff, self.p_cutoff, self.gse_acc)

        draw_maps.draw_heatmap(self.gse_acc,diff_gene[0])
        #draw_maps.draw_vocalno(diff_gene[1],diff_gene[2])

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())