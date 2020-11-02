
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from demo_rfid_ui import *
import serial
import time
import threading
import random


com = '/dev/cu.usbmodem14101'
ser = serial.Serial(com)


def readline():
    SOF = '02'
    EOF = '03'
    # FIND START OF FRAME
    while ser.read().encode('hex') != SOF:
        continue
    # RECORD UNTIL END OF FRAME
    while True:
        temp = serif.read()
        if temp.encode('hex') == EOF:
            break
        else:
            sensor_data += temp
            print (sensor_data)

try:
	while True:
		readline()

except KeyboardInterrupt:
	print ('finished!')




# class My_Window(QtWidgets.QWidget):
# 	def __init__(self):
# 		super().__init__()

# 		self.ui = Ui_Dialog()
# 		self.ui.setupUi(self)
# 		self.show()

# 		self.data = ''

# 		self.timer = QtCore.QTimer()
# 		self.timer.setInterval(100)
# 		self.timer.timeout.connect(self.get_card_id)
# 		self.timer.start()

# 	def get_card_id(self):
# 		c = ser.readline().decode()
# 		c = c.rstrip()
# 		print (c)
# 		if c.isdigit():
# 			self.data = c

# 		self.ui.label_2.setText(str(self.data))
# 		# QtWidgets.QApplication.processEvents()



# if __name__ == "__main__":
# 	app = QtWidgets.QApplication(sys.argv)
# 	w = My_Window()
# 	w.setWindowTitle('RFID CARD NUMBER')
# 	sys.exit(app.exec_())




