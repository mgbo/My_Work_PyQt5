
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread
import datetime, time
import serial

value = 0

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
    check_Arduino = pyqtSignal(object)
    ser_val = pyqtSignal(object, object)


    def __init__(self, event):
        QThread.__init__(self)
        self.stopped = event
    
    def run(self):
        try:
            self.serArduino = serial.Serial('/dev/cu.usbmodem14101', 115200, timeout=0) # Mac
            # self.serArduino = serial.Serial('COM4', 115200, timeout=0) # Window
            self.condi_Arduino = 1
            self.check_Arduino.emit(1)
        
        except:
            print ("Arduino is not found")
            self.condi_Arduino = 0
            self.check_Arduino.emit(0)

        while not self.stopped.wait(0.1):
            self.Arduinoloop()
    
    def Arduinoloop(self):
        global value

        if self.condi_Arduino:
            self.serArduino.write(b'p')
            time.sleep(0.01)
            wert = self.serArduino.read(5)

            try:
                wert = wert.split()
                intwert = int(wert[0]) # for display number
                value = int(22 + (intwert/3.84)) # for line rotate 

                self.ser_val.emit(intwert, value)

            except:
                print ("Arduino error!")















