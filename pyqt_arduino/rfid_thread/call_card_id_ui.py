
import sys, os
import datetime
import time

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread

from card_id_ui import *

import serial
from threading import Event

icon_path = os.path.abspath(os.path.join(os.path.dirname('__file__'), 'icons'))
print (icon_path)

ICON_RED_LED = "/led-red-on.png"
ICON_GREEN_LED = "/green-led-on.png"  

class ControlTime(QThread):
    now = datetime.datetime.now()
    timeInterval = "%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)

    newTime = pyqtSignal(object)

    def __init__(self, event):
        super().__init__()
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1):
            self.inTime1()

    def inTime1(self):
        global timeInterval
        now = datetime.datetime.now()
        timeInterval = "%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)

        self.newTime.emit(timeInterval)


class ControlArduino(QThread):
    value = 0

    card_id = pyqtSignal(object)
    test_arduino = pyqtSignal(object)

    def __init__(self, event):
        super().__init__()
        self.stopped = event
        self.altValue = 0

    def run(self):
        try:
            self.serArduino = serial.Serial('/dev/cu.usbmodem14101', 9600)
            self.no_UNO = 1
            self.test_arduino.emit(1)
            # print ('found !!')

        except:
            print ("Arduino is not found!")
            self.no_UNO = 0
            self.test_arduino.emit(0)

        while not self.stopped.wait(0.1):
            self.ArduinoLoop()

    def ArduinoLoop(self):
        global value

        if self.no_UNO:
            data = self.serArduino.readline().decode()
            c = data.rstrip()
            # print ("data : ", c, len(c))
            try:
                c_data = int(c)
                print(c_data)
                self.card_id.emit(c_data)

            except:
                print ("data error in Arduino ")



class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.stop_flag_time = Event()
        self.stop_flag_arduino = Event()

        self.getControlTime = ControlTime(self.stop_flag_time)
        self.getControlTime.start()
        self.getControlTime.newTime.connect(self.updateTime)


        self.getControlArduino = ControlArduino(self.stop_flag_arduino)
        self.getControlArduino.card_id.connect(self.update_card)
        self.getControlArduino.test_arduino.connect(self.updateInfoArduino)
        self.getControlArduino.start()

    # @pyqtSlot()
    # def on_btnExit_clicked(self):
    #     self.stop_flag_time.set()
    #     self.stop_flag_arduino.set()
    #     sys.exit(0);

     
    def updateTime(self, timeInterval):
        self.ui.labeTime.setText(timeInterval)


    def update_card(self, c_data):
        self.ui.labelCardid.setText(str(c_data))


    def updateInfoArduino(self, condi):
        print (f"condition of Arduino : {condi}")

        if condi:
            pixmap = QtGui.QPixmap(icon_path + ICON_GREEN_LED)
            self.ui.label_text.setText('Arduino is open')
            self.ui.label_icon.setPixmap(pixmap)

        else:
            pixmap = QtGui.QPixmap(icon_path + ICON_RED_LED)
            self.ui.label_text.setText('Arduino is close')
            self.ui.label_icon.setPixmap(pixmap)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    app.exit(app.exec_())

















