
import sys, os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPen, QPixmap
from PyQt5.QtCore import Qt

from threading import Event
from Ui.demo_mainwindow import *
from control_arduino import ControlTime, ControlArduino

img_path = os.path.abspath(os.path.join(os.path.dirname('__file__'), 'icons'))
print (img_path)

class MyWindow(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        #===================== define pen ========================
        pen = QPen(Qt.red)
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        pen.setCosmetic(True)

        #====================== add GraphicsScene ==================
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(QPixmap(img_path + '/back.png'))

        self.item = scene.addLine(60, 170, 97, 97, pen) #(center to other side)

        #================= add ellipse to graphics scence ========================
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.gray))
        brush = QtGui.QBrush(pen.color().darker(100))
        scene.addEllipse(87, 87, 20, 20, pen, brush)
        
        self.item.setTransformOriginPoint(97, 97)
        self.graphicsView.setScene(scene)


        #====================== get data from control arduino file ========================
        self.stop_flag_time = Event()
        self.stop_flag_arduino = Event()

        self.getControltime = ControlTime(self.stop_flag_time)
        self.getControltime.start()
        self.getControltime.newTime.connect(self.updateTime)


        self.getControlArduino = ControlArduino(self.stop_flag_arduino)
        self.getControlArduino.check_Arduino.connect(self.updateInfoArduino)
        self.getControlArduino.ser_val.connect(self.getSerialData)
        self.getControlArduino.start()
    
    @pyqtSlot()
    def on_btnExit_clicked(self): # button ကိုနှိပ်လျှင် exit ပြုလုပ်ရန်အတွက် btnExit သည် button ၏ အမည်ဖြစ်သည် 
        self.stop_flag_time.set()
        self.stop_flag_arduino.set()
        sys.exit(0);
    
    def updateTime(self, n_time):
        self.label_time.setText(n_time)

    def updateInfoArduino(self, condi_ar):
        # print (condi_ar)
        if condi_ar:
            print (condi_ar)
            pixmap = QtGui.QPixmap(img_path + '/green-led-on.png')
            self.label_led.setPixmap(pixmap)
        else:
            pixmap = QtGui.QPixmap(img_path + '/led-red-on.png')
            self.label_led.setPixmap(pixmap)
    
    def getSerialData(self, s_d, s_d_line):
        self.label_val.setText(str(s_d))
        self.item.setRotation(s_d_line)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())



