
import serial
from PyQt5 import QtWidgets, QtGui, QtCore
import sys


com = '/dev/cu.usbmodem14101'
ser = serial.Serial(com, '9600')

def get_data():
	while True:
		c = ser.readline().decode() # to convert byte to string
		c = c.rstrip()
		if c.isdigit():
			data = c
			print (f"{data}")

	return data



# try:
# 	ans = get_data()
# 	print (ans)

# except KeyboardInterrupt:
# 	print ("finished")



class My_Window(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.resize(300, 100)

		label = QtWidgets.QLabel("Card id")
		label_num = QtWidgets.QLabel('Card number')

		layout = QtWidgets.QHBoxLayout()
		layout.addWidget(label)
		layout.addWidget(label_num)

		self.setLayout(layout)
		self.show()


		self.timer = QtCore.QTimer()
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.get_card_id)
		self.timer.start()

	def get_card_id(self):
		ans = get_data()
		print (ans)
		self.label_num.setText(str(ans))
		QtWidgets.QApplication.processEvents()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	w = My_Window()
	w.setWindowTitle('RFID CARD NUMBER')
	sys.exit(app.exec_())








