
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import QThread
from example_2 import *
import time

class ProgressBarThread(QThread):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

    def run(self):
        value = self.mainWindow.ui.progressBar.value()
        while value < 100:
            value += 10
            print (value)
            self.mainWindow.ui.progressBar.setValue(value)
            time.sleep(0.5)
            # app.processEvents()


class MyWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


        self.ui.pushButton.clicked.connect(self.increase_val)

    # def increase_val(self):
    #     # print ("hello")
        # value = int(self.ui.progressBar.value())
        # while value < 100:
        #     time.sleep(0.5)
        #     value += 10
        #     print (value)
        #     self.ui.progressBar.setValue(value)
        #     app.processEvents()

        self.my_thread = ProgressBarThread(mainWindow=self)

    def increase_val(self):
        self.my_thread.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())



