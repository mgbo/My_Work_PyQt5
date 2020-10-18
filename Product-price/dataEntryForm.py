

import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton,
 							QAction, QHeaderView, QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
 							QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPainter, QStandardItemModel, QIcon
from PyQt5.Qt import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries
import os

im_p = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
print (im_p)

class DataEntryForm(QWidget):
	def __init__(self):
		super().__init__()
		self.items = 0
		self._data = {'Phone bill':50, "Gas": 30, "Rent": 1850, "Car Payment": 420.0}

		#=============== left side ======================
		self.table = QTableWidget()
		self.table.setColumnCount(2)
		self.table.setHorizontalHeaderLabels(('Description', 'price'))
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		
		#============== Chart widget =================
		self.chartView = QChartView()
		self.chartView.setRenderHint(QPainter.Antialiasing)


		#=============== layout button and entry ================
		self.layoutRight = QVBoxLayout()
		self.lineEditDescription = QLineEdit()
		self.lineEditPrice = QLineEdit()
		self.buttonAdd = QPushButton("Add")
		self.buttonClear = QPushButton("Clear")
		self.buttonQuit = QPushButton("Quit")
		self.buttonPlot = QPushButton("Plot")

		self.buttonAdd.setEnabled(False)
		# self.buttonAdd.hide()

		self.layoutRight.setSpacing(10)
		self.layoutRight.addWidget(QLabel("Description"))
		self.layoutRight.addWidget(self.lineEditDescription)
		self.layoutRight.addWidget(QLabel("Price"))
		self.layoutRight.addWidget(self.lineEditPrice)
		self.layoutRight.addWidget(self.buttonAdd)
		self.layoutRight.addWidget(self.buttonPlot)
		self.layoutRight.addWidget(self.chartView)
		self.layoutRight.addWidget(self.buttonClear)
		self.layoutRight.addWidget(self.buttonQuit)

		#================= connect function to button =====================
		self.buttonAdd.clicked.connect(self.add_entry)
		self.buttonPlot.clicked.connect(self.graph_chart)
		self.buttonQuit.clicked.connect(lambda: app.quit())

		self.layout = QHBoxLayout()
		self.layout.addWidget(self.table, 50)
		self.layout.addLayout(self.layoutRight, 50) # 50% proportional locaction

		self.setLayout(self.layout)

		self.lineEditDescription.textChanged[str].connect(self.check_disable)
		self.lineEditPrice.textChanged[str].connect(self.check_disable)
		self.fill_table() # upload data into table

	def fill_table(self, data=None):
		data = self._data
		print (data)

		for desc, price in data.items():
			descItem = QTableWidgetItem(desc)
			priceItem = QTableWidgetItem("${0:.2f}".format(price))
			priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

			self.table.insertRow(self.items)
			self.table.setItem(self.items, 0, descItem) # setItem(row, column, value)
			self.table.setItem(self.items, 1, priceItem)
			self.items +=1

	def add_entry(self):
		desc = self.lineEditDescription.text()
		price = self.lineEditPrice.text()

		try: 
			descItem = QTableWidgetItem(desc)
			priceItem = QTableWidgetItem('${0:.2f}'.format(float(price)))
			priceItem.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)

			self.table.insertRow(self.items)
			self.table.setItem(self.items, 0, descItem)
			self.table.setItem(self.items, 1, priceItem)
			self.items += 1

			self.lineEditDescription.setText('')
			self.lineEditPrice.setText('')
		except ValueError:
			pass

	def check_disable(self):
		if self.lineEditDescription.text() and self.lineEditPrice.text():
			self.buttonAdd.setEnabled(True)
		else:
			self.buttonAdd.setEnabled(False)

	def graph_chart(self):
		series = QPieSeries()

		for i in range(self.table.rowCount()):
			text = self.table.item(i, 0).text()
			val = float(self.table.item(i, 1).text().replace('$', ''))
			series.append(text, val)

		chart = QChart()
		chart.addSeries(series)
		chart.legend().setAlignment(Qt.AlignTop)
		self.chartView.setChart(chart)


class MainWindow(QMainWindow):
	def __init__(self, widget):
		super().__init__()
		self.setWindowTitle("Expense Data Entry Form")
		self.setWindowIcon(QIcon(im_p + "/numbers-black-icon.png"))
		self.resize(1200, 600)


		self.menuBar = self.menuBar()
		self.fileMenu = self.menuBar.addMenu('File')

		# ================ export to csv file action =================
		# exportAction = QAction('Export to csv', self)
		# exportAction.setShortcut('Ctrl+E')
		# exportAction.triggered.connect(self.export_to_csv) # TODO

		# ================= Exit Action ====================
		exitAction = QAction('Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		# exitAction.triggered.connect(lambda: app.quit())

		# self.fileMenu.addAction(exportAction)
		self.fileMenu.addAction(exitAction)

		self.setCentralWidget(widget)

	def export_to_csv(self):
		print ('Export to csv')
		# try:
		# 	with open(file_name, 'w', newline='') as file:
		# except Exception as e:
		# 	print (e)



if __name__ == "__main__":
	app = QApplication(sys.argv)

	w = DataEntryForm()
	mw = MainWindow(w)
	mw.show()

	sys.exit(app.exec_())








