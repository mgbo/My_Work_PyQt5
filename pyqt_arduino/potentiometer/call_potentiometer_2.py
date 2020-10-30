

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from demo_potentiometer_2 import *
import serial

ser = serial.Serial('/dev/cu.usbmodem14101', timeout=10)

class My_window(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.show()


		# self.count = 1

		self.timer = QtCore.QTimer()
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.get_data)
		self.timer.start()

	# def add_count(self):
	# 	self.count +=5
	# 	self.ui.labelDistance.setText(str(self.count))


	def get_data(self):
		if ser.is_open == True:
			c = ser.readline().decode()
			c = c.rstrip()

		self.ui.labelDistance.setText(str(c))


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	w = My_window()
	w.show()
	sys.exit(app.exec_())