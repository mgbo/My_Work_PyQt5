

'''

Using Threading 

'''

from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from demo_rfid_ui import *
import serial
import time
import threading


com = '/dev/cu.usbmodem14101'
ser = serial.Serial(com, 9600, timeout=10)


class My_Window(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		# timer = QtCore.QTimer()
		# timer.timeout.connect(self.get_card_id)
		# timer.start(1000)

		self.show()


class myThread(threading.Thread):
	def __init__(self, w):
		threading.Thread.__init__(self)
		self.w = w
		self.app = app

	def run(self):
		while True:
			if ser.is_open == True:
				# time.sleep(1)
				# self.ui.label_2.setText()
				c = ser.readline().decode() # to convert byte to string
				c = c.rstrip()
				if c.isdigit():
					data = int(c)
					w.ui.label_2.setText(str(data))
					print (f"{data}")
			else:
				ser.close()


		

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	w = My_Window()
	w.setWindowTitle('RFID CARD NUMBER')
	thread1 = myThread(w)
	thread1.start()
	sys.exit(app.exec_())




