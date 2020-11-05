
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from demo_employee import *
import os


img_p = os.path.abspath(os.path.join(os.path.dirname('__file__'), ''))
print (img_p)


class My_window(QtWidgets.QWidget):
    employee_list = ['mg chit', 'mg kyaw', 'mg mg', 'ko ko']
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Employee List")
        self.setWindowIcon(QtGui.QIcon(img_p + "/worker-icon.png"))

        self.ui.listWidget.addItems(self.employee_list)
        self.ui.listWidget.setCurrentRow(0) # for selecting by index
        self.show()

        self.ui.pushButton_add.clicked.connect(self.add)
        self.ui.pushButton_edit.clicked.connect(self.edit)
        self.ui.pushButton_remove.clicked.connect(self.remove)
        self.ui.pushButton_up.clicked.connect(self.up)
        self.ui.pushButton_down.clicked.connect(self.down)
    
    def add(self):
        row = self.ui.listWidget.currentRow()
        print (row)

        text, ok = QtWidgets.QInputDialog().getText(self, "Employee Dialog", "Employee Name")

        if text and ok is not None:
            self.ui.listWidget.insertItem(row, text)
    
    def edit(self):
        row = self.ui.listWidget.currentRow()
        item = self.ui.listWidget.item(row)
        print (item)

        if item is not None:
            string, ok = QtWidgets.QInputDialog().getText(self, "Employee Dialog", "Edit Employee Name", QtWidgets.QLineEdit.Normal, item.text())

            if ok and string is not None:
                item.setText(string)
    
    def remove(self):
        row = self.ui.listWidget.currentRow()
        item = self.ui.listWidget.item(row)
        # print (item)

        if item is None:
            return
        
        reply = QtWidgets.QMessageBox.question(self, "Remove Employee", "Do you Want Remove Employee " + str(item.text()))

        if reply == QtWidgets.QMessageBox.Yes:
            item = self.ui.listWidget.takeItem(row)
            print (item)
            del item
    
    def up(self):
        row = self.ui.listWidget.currentRow()
        if row>=1:
            item = self.ui.listWidget.takeItem(row)
            self.ui.listWidget.insertItem(row - 1, item)
            self.ui.listWidget.setCurrentItem(item) # လက်ရှိ item ကို select ပေးရန်အတွက်
    
    def down(self):
        row = self.ui.listWidget.currentRow()
        
        if row < self.ui.listWidget.count() - 1:
            item = self.ui.listWidget.takeItem(row)
            self.ui.listWidget.insertItem(row+1, item)
            self.ui.listWidget.setCurrentItem(item)
    
    @pyqtSlot()
    def on_btnClose_clicked(self):
        sys.exit(0)


    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    my_w = My_window()
    my_w.show()
    sys.exit(app.exec_())








