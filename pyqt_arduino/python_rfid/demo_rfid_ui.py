# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rfid_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 161)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 70, 71, 21))
        self.label.setStyleSheet("font: 18pt \".SF NS Text\";\n"
"color: rgb(81, 255, 42);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(130, 70, 231, 21))
        self.label_2.setStyleSheet("font: 18pt \".SF NS Text\";\n"
"color: rgb(252, 0, 18);")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Card id :"))
        self.label_2.setText(_translate("Dialog", "Please Put Card to Sensor"))
