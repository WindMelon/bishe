# -*- coding:utf-8 -*-
# @author:zhanhao
# @project:Graduation Project
import sys
import main_window

from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "welcome.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.main_window = 0

    def start(self):
        self.main_window = main_window.MyApp()
        self.main_window.show()
        window.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
