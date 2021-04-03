
from PyQt5 import QtCore, QtGui, QtWidgets
from example_3 import *
import sys, time

class My_window(QtWidgets.QDialog):
	def __init__(self):
		super().__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.ui.probar_1.setStyle(QtWidgets.QStyleFactory.create("windows"))
		self.ui.probar_1.setTextVisible(True)
		self.ui.probar_2.setStyle(QtWidgets.QStyleFactory.create("windows"))
		self.ui.probar_2.setTextVisible(True)
		self.ui.probar_3.setStyle(QtWidgets.QStyleFactory.create("windows"))
		self.ui.probar_3.setTextVisible(True)

		self.thread = {}

		self.ui.pushButton_start_1.clicked.connect(self.start_worker_1)
		self.ui.pushButton_start_2.clicked.connect(self.start_worker_2)
		self.ui.pushButton_start_3.clicked.connect(self.start_worker_3)

		self.ui.pushButton_stop_1.clicked.connect(self.stop_worker_1)
		self.ui.pushButton_stop_2.clicked.connect(self.stop_worker_2)
		self.ui.pushButton_stop_3.clicked.connect(self.stop_worker_3)


	def start_worker_1(self):
		print ('start worker -1')
		self.thread[1] = ThreadClass(index=1)
		self.thread[1].start()
		self.thread[1].any_signal.connect(self.my_function)
		self.ui.pushButton_start_1.setEnabled(False)

	def start_worker_2(self):
		print ('start worker -2')
		self.thread[2] = ThreadClass(index=2)
		self.thread[2].start()
		self.thread[2].any_signal.connect(self.my_function)
		self.ui.pushButton_start_2.setEnabled(False)

	def start_worker_3(self):
		pass

	def stop_worker_1(self):
		self.thread[1].stop()
		self.ui.pushButton_start_1.setEnabled(True)
		self.ui.pushButton_stop_1.setEnabled(False)

	def stop_worker_2(self):
		self.thread[2].stop()
		self.ui.pushButton_start_2.setEnabled(True)
		self.ui.pushButton_stop_2.setEnabled(False)

	def stop_worker_3(self):
		pass

	def my_function(self, value):
		cnt = value
		index = self.sender().index
		print ("index : ",index)
		if index == 1:
			# print ("cnt :", cnt)
			self.ui.probar_1.setValue(value)

		if index == 2:
			# print ("cnt :", cnt)
			self.ui.probar_2.setValue(value)


class ThreadClass(QtCore.QThread):
	any_signal = QtCore.pyqtSignal(int)

	def __init__(self, parent=None, index=0):
		super().__init__()
		self.index = index
		# self.is_running = True

	def run(self):
		print ('Starting thread...', self.index)
		cnt = 0
		while True:
			cnt +=1
			if cnt == 99:
				cnt = 0
			time.sleep(0.1)
			self.any_signal.emit(cnt)

	def stop(self):
		# self.is_running = False
		print ('Stopping thread....', self.index)
		self.terminate()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	w = My_window()
	w.show()
	sys.exit(app.exec_())




