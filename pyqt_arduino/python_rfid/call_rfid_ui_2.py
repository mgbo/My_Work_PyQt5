
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from demo_rfid_ui import *
import serial
import time
import threading
import random


com = '/dev/cu.usbmodem14101'
ser = serial.Serial(com, timeout=10)



class My_Window(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.show()

		self.data = ''

		self.timer = QtCore.QTimer()
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.get_card_id)
		self.timer.start()

	def get_card_id(self):
		if ser.is_open == True:
			c = ser.readline().decode()
			c = c.rstrip()
			print (c)
			if c.isdigit():
				self.data = int(c)
			else:
				return

		self.ui.label_2.setText(str(self.data))
		# QtWidgets.QApplication.processEvents()



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	w = My_Window()
	w.setWindowTitle('RFID CARD NUMBER')
	sys.exit(app.exec_())




