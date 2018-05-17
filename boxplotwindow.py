#import GEOparse

#gse = GEOparse.get_GEO(geo="GSE1563", destdir="./")

#print()
#print("GSM example:")
#for gsm_name, gsm in gse.gsms.items():
#    print("Name: ", gsm_name)
#    print("Metadata:",)
#    print(gsm.metadata)
    #for key, value in gsm.metadata.items():
    #    print(" - %s : %s" % (key, ", ".join(value)))
#    print ("Table data:",)
#    print (gsm.table.head())
#    break
import sys
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "boxplotwindow.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self,filename):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.image = QtGui.QImage()
        self.image.load("./"+filename+"/"+filename+'_boxplot.png')
        self.image = self.image.scaledToHeight(850)
        self.image = self.image.scaledToWidth(1100)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
