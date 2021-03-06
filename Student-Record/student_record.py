
from PyQt5 import QtWidgets, QtGui, QtCore
# from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtPrintSupport
import sys, sqlite3, time
import os
from sqlite3 import Error

file_path = os.getcwd()
img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'icon/'))
print(img_path)



class InsertDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img_b = "" # define for user image
        self.Qbtn = QtWidgets.QPushButton()
        self.Qbtn_img = QtWidgets.QPushButton()
        self.Qbtn.setText("Register")
        self.Qbtn_img.setText("Choose image")

        self.setWindowTitle("ကျောင်းသားထပ်ထည့်ရန်")
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        layout = QtWidgets.QVBoxLayout() # ============ add Vertical container ==============

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

        self.lab_img = QtWidgets.QLabel("")
        self.lab_img.setStyleSheet("border: 3px solid green")
        layout.addWidget(self.lab_img)

        self.Qbtn_img.clicked.connect(self.add_img)
        self.Qbtn.clicked.connect(self.addstudent)

        # =========== add Buttons (add student) in to vertical container ===============
        layout.addWidget(self.Qbtn_img)
        layout.addWidget(self.Qbtn)

        self.setLayout(layout) # add vertical container to QDialog box

    def add_img(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, caption='Open file', directory=file_path, filter="All (*);;Image files (*.jpg *.gif *.ico)") 
        print (fname)
        if fname[0] !='':
            self.lab_img.setScaledContents(True)
            pixmap = QtGui.QPixmap(fname[0])
            self.lab_img.setPixmap(pixmap)

            with open(fname[0], 'rb') as f:
                self.img_b = f.read()
            
            f.close()

    def addstudent(self):
        name = ""
        photo = ""
        branch = ""
        mobile = ""
        address = ""

        photo = self.img_b
        name = self.nameinput.text()
        branch = self.branchinput.itemText(self.branchinput.currentIndex())
        mobile = self.mobileinput.text()
        address = self.addressinput.text()

        try:
            self.conn = sqlite3.connect("Stu-Database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO students (photo,name,branch,mobile,address) VALUES (?,?,?,?,?)",(photo,name,branch,mobile,address))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QtWidgets.QMessageBox.information(self,'Successful','Student is added successfully to the database.')
            self.close()
        except Error as e:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Could not add student to the database. Error on accessing table')

class SearchDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("ရှာဖွေရန်")
        self.setFixedHeight(100)
        self.setFixedWidth(300)

        self.searchinput = QtWidgets.QLineEdit()
        self.searchinput.setPlaceholderText("Roll No.") # lineedit box မှာ placeholder ထည့်ထားရန်အတွက် 

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
        
        finally:
            self.conn.close()

class DeleteDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Delete data")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.qbtn = QtWidgets.QPushButton()
        self.qbtn.setText("Delete")
        self.qbtn.clicked.connect(self.deletestudent)

        self.deleteinput = QtWidgets.QLineEdit()
        self.onlyInt = QtGui.QIntValidator() # interger အမျိုးအစားပဲ lineedit မှာ ရိုက်လို့ရအောင် ပြုလုပ် 
        self.deleteinput.setValidator(self.onlyInt)

        self.deleteinput.setPlaceholderText("Roll No.")
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.qbtn)

        self.setLayout(layout)

    def deletestudent(self):
        # print ("delete")
        delrol = ""
        delrol = self.deleteinput.text()
        sqlStatement = "DELETE from students WHERE roll=" + str(delrol)
        print (sqlStatement)

        try:
            self.conn = sqlite3.connect("Stu-Database.db")
            self.c = self.conn.cursor()
            self.c.execute(sqlStatement)
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QtWidgets.QMessageBox.information(self, 'ပယ်ဖျက်ပြီးစီးမူ', 'အောင်မြင်စွာ ပယ်ဖျက်ပြီးပါပြီ')
            self.close()
        except Exception:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox, 'Error', 'could not delete data from the database')
        finally:
            self.conn.close()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(img_path + '/logo-1.ico'))
        self.setWindowTitle("ကျောင်းသားမှတ်တမ်း")

        #======================================== FOR DATABASE ==========================================
        self.conn = sqlite3.connect("Stu-Database.db")
        self.cur = self.conn.cursor()
        sqlStatement = "CREATE TABLE IF NOT EXISTS students(roll INTEGER PRIMARY KEY AUTOINCREMENT, photo BLOB, name TEXT, branch TEXT, mobile INTEGER, address TEXT)"
        # print (sqlStatement)
        self.cur.execute(sqlStatement)
        self.cur.close()

        # ============ window ပေါ် မှာ menubar ထည့်ရန် အတွက် =====================
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        help_menu = menu_bar.addMenu("&About")

        self.setMinimumSize(800, 600) # window အရွယ်အစား သတ်မှတ်

        #===================== QtWidgets.QTableWidget() ကို အသုံးပြုပြီ Table တည်ဆောက် ========================
        self.tableWidget = QtWidgets.QTableWidget()
        self.setCentralWidget(self.tableWidget) # table ကို mainwindow ထဲထည့် SDI
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(6) # Table အတွက် Column အရေအတွက်သတ်မှတ်
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("စဉ်", "ဓာတ်ပုံ", "အမည်", "အထူးပြုဘာသာရပ်", "တယ်လီဖုန်းနံပါတ်","ဆက်သွယ်ရန်လိပ်စာ"))

        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents) # # ခေါင်းစဉ် နှင့် အကျယ် တစ်ထက်တည်ကျအောင်လုပ် (အကြီး မှ အသေး )
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch) # ခေါင်းစဉ် နှင့် အကျယ် တစ်ထက်တည်ကျအောင်လုပ် (အသေး မှ အကြီး)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch) # ခေါင်းစဉ် နှင့် အကျယ် တစ်ထက်တည်ကျအောင်လုပ် (အသေး မှ အကြီး)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch) # ခေါင်းစဉ် နှင့် အကျယ် တစ်ထက်တည်ကျအောင်လုပ် (အသေး မှ အကြီး)
        self.tableWidget.setFont(QtGui.QFont('Pyidaungsu', 14)) # table အတွက် font သတ်မှတ်


        #=================== Table အပေါ်မှာ toolbar ထည့်ရန်အတွက် ============
        toolbar = QtWidgets.QToolBar()
        toolbar.setFont(QtGui.QFont('Pyidaungsu', 14))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)


        btn_ac_adduser = QtWidgets.QAction(QtGui.QIcon(img_path + "/add_stu.png"), "ကျောင်းသားထပ်ထည့်ရန်", self)   #add student icon
        btn_ac_adduser.triggered.connect(self.insert)
        # btn_ac_adduser.setStatusTip("Add Student")
        toolbar.addAction(btn_ac_adduser)
        file_menu.addAction(btn_ac_adduser) # file menu bar ထဲကို btn_ac_adduser ကိုထည့် 


        btn_ac_refresh = QtWidgets.QAction(QtGui.QIcon( img_path + "/Reload-icon.png"),"Refresh",self)   #refresh icon
        btn_ac_refresh.triggered.connect(self.loaddata)
        # btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        search_img = QtGui.QIcon( img_path + "/chart-search-icon.png")
        btn_ac_search = QtWidgets.QAction(search_img, "ရှာဖွေရန်", self)  #search icon
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User") # table အောက်က statusbar မှာ သတ်မှတ်ထားသောစာတမ်း ပေါ် ရန် အတွက်
        toolbar.addAction(btn_ac_search)
        

        about_icon = QtGui.QIcon(img_path + "/users-icon.png")
        about_btn = QtWidgets.QAction(about_icon, "အကြောင်း", self)
        about_btn.triggered.connect(self.about)
        about_btn.setStatusTip("အကြောင်း")
        toolbar.addAction(about_btn)
        

        btn_ac_delete = QtWidgets.QAction(QtGui.QIcon(img_path + "/Recycle-Bin-icon.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)
        file_menu.addAction(btn_ac_delete) # file menu bar ထဲသို့ btn_ac_delete ကိုထည့်သွင်း 


        # ======================== Table အောက်ခြေ က toolbar ================
        statusbar = QtWidgets.QStatusBar()
        statusbar.setFont(QtGui.QFont('Pyidaungsu', 14))
        self.setStatusBar(statusbar)

    def insert(self):
        print('insert')
        qd_insert = InsertDialog()
        qd_insert.exec_() # для отображение
        self.loaddata() # for adding image into a database

    # ============== For load and add image ============================================
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

    def search(self):
        search = SearchDialog()
        search.exec_()
        

    def delete(self):
        # print ("delete")
        dlg = DeleteDialog()
        dlg.exec_()

    
    def about(self):
        print ("I am free coder \
        and keeping studing to get my goal")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())







