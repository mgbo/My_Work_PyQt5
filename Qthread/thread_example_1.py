
import sys, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from example_1 import *

class DlgMain(QDialog):
	def __init__(self):
		super().__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.setWindowTitle("My GUI")

		self.ui.prg.setStyle(QStyleFactory.create("windows"))
		self.ui.prg.setTextVisible(True)
		self.ui.btnStart.clicked.connect(self.evt_btnStart_clicked)
		

		self.ui.dial.valueChanged.connect(self.ui.lcd.display)

	# def evt_btnStart_clicked(self):
	# 	for x in range(20, 101, 20):
	# 		print (x)
	# 		time.sleep(2)
	# 		self.ui.prg.setValue(x)
	# 		app.processEvents()

	def evt_btnStart_clicked(self):
		self.worker = WorkerThread()
		self.worker.start()
		self.worker.finished.connect(self.evt_worker_finished)
		self.worker.update_progress.connect(self.evt_update_progess)

	def evt_worker_finished(self):
		QMessageBox.information(self, "Done!", 'worker thread completed!')

	def evt_update_progess(self, val):
		self.ui.prg.setValue(val)


class WorkerThread(QThread):
	update_progress = pyqtSignal(int)
	def run(self):
		for x in range(20, 101, 20):
			print (x)
			time.sleep(2)
			self.update_progress.emit(x)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	dlgMain = DlgMain()
	dlgMain.show()
	sys.exit(app.exec_())


























