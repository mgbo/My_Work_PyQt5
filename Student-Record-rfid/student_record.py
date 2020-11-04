
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtPrintSupport
import sys, sqlite3, time
import os
from sqlite3 import Error


from datetime import datetime
from datetime import date

import serial
from PyQt5 import QtSerialPort



file_path = os.getcwd()
img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'icon/'))


# com = '/dev/cu.usbmodem14101'
# ser = serial.Serial(com)

# def get_card_id():
#     if ser.is_open == True:
#         while True:
#             c = ser.readline().decode()
#             c = c.rstrip()
#             if c.isdigit():
#                 data = int(c)
#                 print (f"Card id : {data}")
#                 return data
#             else:
#                 return


class InsertDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img_b = "" # define for user image
        self.user_card_id = "" # for rfid card number


        #================= For Serial Data From Arduino ======================
        self.serial = QtSerialPort.QSerialPort(
            '/dev/cu.usbmodem14101',
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive
        )

        self.setWindowTitle("Add Student")
        # self.setFixedWidth(350)
        # self.setFixedHeight(350)

        #===================== image browser ======================
        self.Qbtn_img = QtWidgets.QPushButton()
        img_icon = QtGui.QPixmap(img_path +  "/img_browse.png")
        self.Qbtn_img.setIcon(QtGui.QIcon(img_icon))
        self.Qbtn_img.setIconSize(QtCore.QSize(300,130))
        # self.Qbtn_img.setGeometry(QtCore.QRect(1030, 500, 161, 61))

        #=================== Register Button ======================
        self.Qbtn = QtWidgets.QPushButton()
        self.Qbtn.setText("Register")

        # ============ add Vertical container ==============
        layout = QtWidgets.QVBoxLayout()

        # =========== add line edit(name) in to vertical container ===============
        self.nameinput = QtWidgets.QLineEdit() 
        self.nameinput.setPlaceholderText("Name")
        layout.addWidget(self.nameinput)

        # =========== add Combobox in to vertical container ===============
        self.branchinput = QtWidgets.QComboBox()
        self.branchinput.addItem("Chemical Engg")
        self.branchinput.addItem("Civil")
        self.branchinput.addItem("Electircal Power")
        self.branchinput.addItem("Electronics and Communication")
        self.branchinput.addItem("Computer Engineering")
        self.branchinput.addItem("Information Technology")
        layout.addWidget(self.branchinput)

        # =========== add line edit(mobile) in to vertical container ===============
        self.mobileinput = QtWidgets.QLineEdit()
        self.mobileinput.setPlaceholderText("Mobile No.")
        layout.addWidget(self.mobileinput)

        # =========== add line edit (Address) in to vertical container ===============
        self.addressinput = QtWidgets.QLineEdit()
        self.addressinput.setPlaceholderText("Address")
        layout.addWidget(self.addressinput)


        # self.lab_img = QtWidgets.QLabel("PUT IMAGE")
        # self.lab_img.setAlignment(QtCore.Qt.AlignCenter)
        # self.lab_img.setStyleSheet("border: 3px solid green;")
        # layout.addWidget(self.lab_img)

        # self.rfid_card_id = QtWidgets.QLabel("Put RFID Card to Sensor")
        # self.rfid_card_id.setAlignment(QtCore.Qt.AlignCenter)
        # self.rfid_card_id.setStyleSheet("border :3px solid green;")
        # self.rfid_card_id.resize(100, 1)


        self.Qbtn_img.clicked.connect(self.add_img)
        self.Qbtn.clicked.connect(self.addstudent)



        self.put_card= QtWidgets.QPushButton('put card', checkable=True,toggled=self.on_toggled)


        # =========== add Buttons (add student) in to vertical container ===============
        layout.addWidget(self.Qbtn_img)
        layout.addWidget(self.put_card)
        layout.addWidget(self.Qbtn)

        self.setLayout(layout) # add vertical container to QDialog box


    def add_img(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, caption='Open file', directory=file_path, filter="All (*);;Image files (*.jpg *.gif *.ico)") 
        # print (fname)
        if fname[0] !='':
            # img_icon = QtGui.QPixmap(img_path +  "/Click to browse.png")
            # self.Qbtn_img.setIcon(QtGui.QIcon(img_icon))
            # self.Qbtn_img.setScaledContents(True)
            pixmap = QtGui.QPixmap(fname[0])
            self.Qbtn_img.setIcon(QtGui.QIcon(pixmap))

            with open(fname[0], 'rb') as f:
                self.img_b = f.read()
            
            f.close()

    @QtCore.pyqtSlot()
    def receive(self):

        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            print ("Audrino dat : ",text)
            self.user_card_id = str(text)
            self.put_card.setText(str(text))


    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.put_card.setText("Disconnect" if checked else "Connect")
        if checked:
            if not self.serial.isOpen():
                if not self.serial.open(QtCore.QIODevice.ReadWrite):
                    self.put_card.setChecked(False)

        else:
            self.serial.close()


    def addstudent(self):
        name = ""
        photo = ""
        branch = ""
        mobile = ""
        address = ""
        date_time = str(date.today())
        # print (date_time)
        current_time = str(datetime.now().strftime("%H:%M:%S"))
        # print (current_time)
        card = ''

        photo = self.img_b
        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        mobile = self.mobileinput.text()
        address = self.addressinput.text()
        card = str(self.user_card_id)
        print ("for database :", card)

        try:
            self.conn = sqlite3.connect("Stu-Database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO students (photo,name,branch,mobile,address,date,time,card_id) VALUES (?,?,?,?,?,?,?,?)",(photo,name,branch,mobile,address,date_time,current_time,card))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QtWidgets.QMessageBox.information(self,'Successful','Student is added successfully to the database.')
            self.close()
        except Error as e:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Could not add student to the database. Error on accessing table')
            # self.close()

class SearchDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Search User")
        self.setFixedHeight(100)
        self.setFixedWidth(300)

        self.searchinput = QtWidgets.QLineEdit()
        self.searchinput.setPlaceholderText("Roll No.")

        self.btn = QtWidgets.QPushButton()
        self.btn.setText("Search")
        self.btn.clicked.connect(self.searchstudent)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.searchinput)
        layout.addWidget(self.btn)

        self.setLayout(layout)
    
    def searchstudent(self):
        searchrol = ""
        searchrol = self.searchinput.text()
        sqlstatement = f"SELECT * FROM students WHERE roll='{searchrol}'"
        # print (sqlstatement)
        try:
            self.conn = sqlite3.connect("Stu-Database.db")
            self.cur = self.conn.cursor()
            result = self.cur.execute(sqlstatement)
            row = result.fetchone()
            serachresult = "Rollno : "+str(row[0])+'\n'+"Name : "+str(row[2])+'\n'+"Branch : "+str(row[3])+'\n'+"Address : "+str(row[4])
            QtWidgets.QMessageBox.information(self, 'Successful', serachresult)
            self.conn.commit()
            self.cur.close()
            self.conn.close()

        except Error as e:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Could not find student')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(img_path + 'iogo-1.ico'))

        #================== FOR ARDUINO DATA ========================
        self.serial = QtSerialPort.QSerialPort(
            '/dev/cu.usbmodem14101',
            baudRate=QtSerialPort.QSerialPort.Baud9600,
            readyRead=self.receive
        )

        #======================================== FOR DATABASE ==========================================
        self.conn = sqlite3.connect("Stu-Database.db")
        self.cur = self.conn.cursor()
        sqlStatement = "CREATE TABLE IF NOT EXISTS students(roll INTEGER PRIMARY KEY AUTOINCREMENT, photo BLOB, name TEXT, branch TEXT, mobile INTEGER, address TEXT, date TEXT, time TEXT, card_id TEXT)"
        # print (sqlStatement)
        self.cur.execute(sqlStatement)
        self.cur.close()

        self.setMinimumSize(1000, 700) # window အရွယ်အစား သတ်မှတ်

        #===================== QtWidgets.QTableWidget() ကို အသုံးပြုပြီ Table တည်ဆောက် ========================
        self.tableWidget = QtWidgets.QTableWidget()
        self.setCentralWidget(self.tableWidget) # table ကို mainwindow ထဲထည့် SDI
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(9) # Table အတွက် Column အရေအတွက်သတ်မှတ်
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Roll No.", "Photo", "Name", "Branch", "Mobile","Address","Date", "Time", "Card ID"))



        #=================== Table အပေါ်မှာ toolbar ထည့်ရန်အတွက် ============
        toolbar = QtWidgets.QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)


        btn_ac_adduser = QtWidgets.QAction(QtGui.QIcon(img_path + "/user-add-icon.png"), "Add Student", self)   #add student icon
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Student")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QtWidgets.QAction(QtGui.QIcon( img_path + "/r3.png"),"Refresh",self)   #refresh icon
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        search_img = QtGui.QIcon( img_path + "/s1.png")
        btn_ac_search = QtWidgets.QAction(search_img, "Search", self)  #search icon
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QtWidgets.QAction(QtGui.QIcon(img_path + "/d1.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        # btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        btn_connect = QtWidgets.QAction(QtGui.QIcon(img_path + "/Usb-Cable-icon.png"), "Connect", self)
        btn_connect.triggered.connect(self.serial_connect)
        btn_connect.setStatusTip("Connect RFID")
        toolbar.addAction(btn_connect)


        # ======================== Table အောက်ခြေ က toolbar ================
        statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(statusbar)

    def insert(self):
        # print('insert')
        qd_insert = InsertDialog()
        qd_insert.exec_() # для отображение

    def loaddata(self):
        con = sqlite3.connect("Stu-Database.db")
        sqlStatement = "SELECT * FROM students"
        cur = con.cursor()
        cur.execute(sqlStatement)
        rows = cur.fetchall()
        # print (rows)
        self.tableWidget.setRowCount(0) # This very importan
        for row_num, row_data in enumerate(rows):
            self.tableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                if col_num == 1:
                    # print (data)
                    itm_img = self.getImageLabel(data)
                    self.tableWidget.setCellWidget(row_num, col_num, itm_img)
                else:
                    self.tableWidget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))
        
        self.tableWidget.verticalHeader().setDefaultSectionSize(80)
        con.close()

    def getImageLabel(self, image):
        imageLabel = QtWidgets.QLabel()
        imageLabel.setText("")
        imageLabel.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image)
        imageLabel.setPixmap(pixmap)
        return imageLabel


    @QtCore.pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            # print ("Audrino dat : ",text)
            card_id = int(text)
            print (f"Card_id is : {card_id}")
            # self.output_te.append(text)
            # self.output_te.setText(str(text))


    def search(self):
        search = SearchDialog()
        search.exec_()
        

    def delete(self):
        print ("delete")


    @QtCore.pyqtSlot()
    def serial_connect(self):
        checked = True
        if checked:
            if not self.serial.isOpen():
                if not self.serial.open(QtCore.QIODevice.ReadWrite):
                    pass
        else:
            self.serial.close()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


