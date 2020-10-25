
from PyQt5.QtWidgets import QApplication, QLCDNumber, QDialog, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime
import sys


class Clock(QDialog):
	def __init__(self):
		super().__init__()

		title = "Digital Clock"

		self.setWindowTitle(title)
		self.setGeometry(400, 400, 450, 300)

		timer = QTimer()
		timer.timeout.connect(self.showTime)
		timer.start(1000)

		self.showTime()
		self.show()

	def showTime(self):
		vbox = QVBoxLayout()
		lcd = QLCDNumber()
		lcd.setStyleSheet('color:green')
		lcd.setStyleSheet('background:yellow')

		vbox.addWidget(lcd)

		time = QTime.currentTime()
		text = time.toString('hh:mm')

		lcd.display(text)

		self.setLayout(vbox)


app = QApplication(sys.argv)
clock = Clock()
clock.show()
sys.exit(app.exec_())







