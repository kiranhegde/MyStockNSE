from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# import pandas
import sqlite3
import sys,os
import random
from sqlite3 import Error



def check_db(db_file):
    con=None

    if os.path.isfile(db_file):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        # print("sqlite: "+ sqlite3.version)
        return con,cur
    else :
        msgBox=QMessageBox()
        msgBox.setWindowTitle("database file missing")
        msgBox.setText('database file needs to present in current location')
        msgBox.setInformativeText("Please keep the db file"
                                  "in the running folder"
                                  "and try once again")
        # msgBox.setWindowIcon(QIcon(""))
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.exec_()

    return None,None


def read_stock_db(db_file):
    con,cur=check_db(db_file)
    if con != None and cur !=None :
        try:
            stock=cur.execute("SELECT *FROM purchase")
            # print(stock)

        except:
            QMessageBox.information("Info", "Empty ")


def read_sales_db(db_file,sale_list):
    check_db(db_file)


# def add_stock(db_file):
#     con, cur = check_db(db_file)
#     #print(con,cur)
#     add_stocks(con,cur)







class add_stocks(QWidget):

    def __init__(self,con,cur,agency=""):
        super().__init__()
        self.setWindowTitle("Add stock")
        self.con=con
        self.cur=cur
        self.agency0=""
        if agency:
            self.agency0=agency

        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,450,350)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.default_paramters()
        self.widgets()
        self.layouts()

    def default_paramters(self):
        cur=self.cur
        cur.execute('SELECT * FROM defaults')
        default = cur.fetchall()
        self.brockerage = default[0][0]
        self.gst = default[0][1]
        self.stt = default[0][2]
        self.itax = default[0][3]


    def widgets(self):
        self.titleText=QLabel("Add New stock")
        self.agencyEntry=QLineEdit()
        self.agencyEntry.setPlaceholderText("Enter name of agency (Eg. Kotak, Zerodha, etc)")
        self.exchangeEntry=QLineEdit()
        self.exchangeEntry.setPlaceholderText("Enter name of exchange(Eg. BSE,NSE, etc)")
        self.equityEntry=QLineEdit()
        self.equityEntry.setPlaceholderText("Enter Equity name (Eg. SBI, ITC, etc)")

        self.trade_dateEntry = QDateEdit(self)
        #self.dateEdit.setDateTime(QDateTime(QDate(2019, 2, 23),QTime(0, 0, 0)))
        self.trade_dateEntry.setDate(QDate.currentDate())
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")

        self.settle_dateEntry = QDateEdit(self)
        # self.dateEdit.setDateTime(QDateTime(QDate(2019, 2, 23),QTime(0, 0, 0)))
        self.settle_dateEntry.setDate(QDate.currentDate())
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")

        # self.trade_dateEntry = QLineEdit()
        # self.trade_dateEntry.setPlaceholderText("Enter trade date(DD/MM/YEAR)")
        # self.settle_dateEntry=QLineEdit()
        # self.settle_dateEntry.setPlaceholderText("Enter settlement date(DD/MM/YEAR)")
        self.trade_priceEntry = QLineEdit()
        self.trade_priceEntry.setPlaceholderText("Enter trade price")
        self.quantityEntry = QLineEdit()
        self.quantityEntry.setPlaceholderText("Enter quantity of stocks")
        self.unit_brockEntry = QLineEdit()
        # self.unit_brockEntry.setPlaceholderText("Enter brockerage(%) per unit")
        self.unit_brockEntry.setText(str(self.brockerage))
        self.gst_brockEntry = QLineEdit()
        # self.gst_brockEntry.setPlaceholderText("Enter gst(%) on brockerage")
        self.gst_brockEntry.setText(str(self.gst))
        self.stt_Entry = QLineEdit()
        # self.stt_Entry.setPlaceholderText("Enter stt(%) of share value")
        self.stt_Entry.setText(str(self.stt))
        self.it_Entry = QLineEdit()
        # self.it_Entry.setPlaceholderText("Enter Income tax slab(%)")
        self.it_Entry.setText(str(self.itax))
        self.remarksEntry = QLineEdit()
        self.remarksEntry.setPlaceholderText("Type your remarks ..")

        self.addBtn=QPushButton("Submit")
        self.addBtn.clicked.connect(self.add_stock)
        self.clrBtn = QPushButton("Clear")
        self.clrBtn.clicked.connect(self.clear_stock)

        if self.agency0:
            self.agencyEntry.setText(self.agency0)
        # self.exchangeEntry.setText("NSE")
        # self.equityEntry.setText("SBI")
        # self.trade_priceEntry.setText("200")
        # self.quantityEntry.setText("100")


    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.mainTopLayout=QVBoxLayout()
        self.topLayout=QFormLayout()
        self.bottomLayout=QHBoxLayout()
        self.topFrame=QFrame()

        self.topGroupBox=QGroupBox("Stock Information")
        self.bottomGroupBox=QGroupBox("Control")

        self.topLayout.addRow(QLabel("Agency: "),self.agencyEntry)
        self.topLayout.addRow(QLabel("Exchange: "),self.exchangeEntry)
        self.topLayout.addRow(QLabel("Equity: "),self.equityEntry)
        self.topLayout.addRow(QLabel("Trade Date: "),self.trade_dateEntry)
        self.topLayout.addRow(QLabel("Settlement Date: "),self.settle_dateEntry)
        self.topLayout.addRow(QLabel("trade Price: "),self.trade_priceEntry)
        self.topLayout.addRow(QLabel("Quantity: "),self.quantityEntry)
        self.topLayout.addRow(QLabel("Brockerage per unit: "),self.unit_brockEntry)
        self.topLayout.addRow(QLabel("GST on Brockerage: "),self.gst_brockEntry)
        self.topLayout.addRow(QLabel("STT on Share: "),self.stt_Entry)
        self.topLayout.addRow(QLabel("Income Tax: "),self.it_Entry)
        self.topLayout.addRow(QLabel("Remarks: "),self.remarksEntry)

        self.bottomLayout.addWidget(self.addBtn)
        self.bottomLayout.addWidget(self.clrBtn)

        self.topGroupBox.setLayout(self.topLayout)
        self.bottomGroupBox.setLayout(self.bottomLayout)

        # self.topFrame.setLayout(self.topLayout)
        #self.topGroupBox.add setLayout(self.topLayout)
        # self.bottomGroupBox.setLayout(self.bottomLayout)
        self.mainTopLayout.addWidget(self.topGroupBox)
        self.mainTopLayout.addWidget(self.bottomGroupBox)

        self.mainLayout.addLayout(self.mainTopLayout)

        self.setLayout(self.mainLayout)


    def add_stock(self):
        #print("Hi")
        cur = self.cur
        con = self.con

        agency=self.agencyEntry.text()
        exchange=self.exchangeEntry.text()
        equity=self.equityEntry.text()
        tradeDate=self.trade_dateEntry.text()
        settleDate=self.settle_dateEntry.text()
        tradPrice=self.trade_priceEntry.text()
        quantity=self.quantityEntry.text()
        unitBrock=self.unit_brockEntry.text()
        gst_Brock=self.gst_brockEntry.text()
        stt=self.stt_Entry.text()
        itax=self.it_Entry.text()
        comments="N/A"

        if self.remarksEntry.text() != "":
            comments=self.remarksEntry.text()

        stock = cur.execute("SELECT * FROM purchase")
        id_list = []
        for all_row_data in stock:
            id_list.append(all_row_data[0])

        # print(id_list)
        stock_id = f'{random.randrange(1000, 10 ** 6)}'
        m=len(id_list)-1
        # stock_id=6463
        # print("#",m,range(m))
        for i in range(m):
            # print("##"+str(i),stock_id)
            if stock_id in id_list:
                stock_id = f'{random.randrange(1000, 10 ** 6)}'
                # print("->"+str(stock_id))
            else:
                break

        #print(f'{random.randrange(1000, 10 ** 6):07}')
        # print("#",stock_id)

        if unitBrock != "":
            unitBrock=self.brockerage
        if gst_Brock !="":
            gst_Brock=self.gst
        if stt !="":
            stt=self.stt
        if itax !="":
            itax=self.itax


        if agency!=""  and exchange!=""  and equity!=""  and tradeDate!=""  and settleDate!=""  and tradPrice!=""  and quantity!="" :
            try:
                query="INSERT INTO 'purchase' (id,agency,exchange,equity,trade_date,settle_date,trade_price,quantity,unit_brockerage,gst_brockerage,stt,income_tax,remarks)" \
                      " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
                cur.execute(query,(stock_id,agency,exchange,equity,tradeDate,settleDate,tradPrice,quantity,unitBrock,gst_Brock,stt,itax,comments))
                con.commit()
                QMessageBox.information(self,"Info","New Stock information has been added")
            except:
                QMessageBox.information(self, "Info", "New Stock information has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cant be empty!!!")


    def clear_stock(self):
        self.agencyEntry.setText("")
        self.exchangeEntry.setText("")
        self.equityEntry.setText("")
        self.trade_dateEntry.setDate(QDate.currentDate())
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.settle_dateEntry.setDate(QDate.currentDate())
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")
        # self.trade_dateEntry.setText("")
        # self.settle_dateEntry.setText("")
        self.trade_priceEntry.setText("")
        self.quantityEntry.setText("")
        self.unit_brockEntry.setText("")
        self.gst_brockEntry.setText("")
        self.stt_Entry.setText("")
        self.it_Entry.setText("")
        self.remarksEntry.setText("")


class set_defaults(QWidget):

    def __init__(self,con,cur):
        super().__init__()
        self.setWindowTitle("Default Settings")
        self.con=con
        self.cur=cur
        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,450,220)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.titleText = QLabel("Default Settings")
        self.unit_brockEntry = QLineEdit()
        self.unit_brockEntry.setPlaceholderText("Enter brockerage(%) per unit")
        self.gst_brockEntry = QLineEdit()
        self.gst_brockEntry.setPlaceholderText("Enter gst(%) on brockerage")
        self.stt_Entry = QLineEdit()
        self.stt_Entry.setPlaceholderText("Enter stt(%) of share value")
        self.it_Entry = QLineEdit()
        self.it_Entry.setPlaceholderText("Enter Income tax slab(%)")

        self.addBtn = QPushButton("Submit")
        self.addBtn.clicked.connect(self.save_defaults)
        self.clrBtn = QPushButton("Clear")
        self.clrBtn.clicked.connect(self.clear_defaults)

    def save_defaults(self):
        cur=self.cur
        con=self.con

        try:
            cur.execute('DELETE FROM defaults;',)
        except:
            pass

        unitBrock = self.unit_brockEntry.text()
        gst_Brock = self.gst_brockEntry.text()
        stt = self.stt_Entry.text()
        itax = self.it_Entry.text()

        if unitBrock  and gst_Brock and stt and itax:
            unitBrock=float(unitBrock)
            gst_Brock=float(gst_Brock)
            stt=float(stt)
            itax=float(itax)

            try:
                query="INSERT INTO 'defaults' (brockerage,gst,stt,itax) VALUES(?,?,?,?)"
                cur.execute(query, (unitBrock, gst_Brock, stt, itax))
                con.commit()
                QMessageBox.information(self, "Info", "Defaults are saved")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Defaults are not saved")
                self.close()
        else:
            QMessageBox.information(self, "Info", "Fields can't be empty!!!")



    def clear_defaults(self):
        self.unit_brockEntry.setText("")
        self.gst_brockEntry.setText("")
        self.stt_Entry.setText("")
        self.it_Entry.setText("")


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.mainTopLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.bottomLayout = QHBoxLayout()
        self.topFrame = QFrame()

        self.topGroupBox = QGroupBox("Default Information")
        self.bottomGroupBox = QGroupBox("Control")

        self.topLayout.addRow(QLabel("Brockerage per unit: "), self.unit_brockEntry)
        self.topLayout.addRow(QLabel("GST on Brockerage: "), self.gst_brockEntry)
        self.topLayout.addRow(QLabel("STT on Share: "), self.stt_Entry)
        self.topLayout.addRow(QLabel("Income Tax: "), self.it_Entry)

        # self.unit_brockEntry.setText("0.4")
        # self.gst_brockEntry.setText("18.0")
        # self.stt_Entry.setText("0.1")
        # self.it_Entry.setText("30.0")

        self.bottomLayout.addWidget(self.addBtn)
        self.bottomLayout.addWidget(self.clrBtn)

        self.topGroupBox.setLayout(self.topLayout)
        self.bottomGroupBox.setLayout(self.bottomLayout)

        # self.topFrame.setLayout(self.topLayout)
        # self.topGroupBox.add setLayout(self.topLayout)
        # self.bottomGroupBox.setLayout(self.bottomLayout)
        self.mainTopLayout.addWidget(self.topGroupBox)
        self.mainTopLayout.addWidget(self.bottomGroupBox)
        self.mainLayout.addLayout(self.mainTopLayout)
        self.setLayout(self.mainLayout)


# def main():
#     APP=QApplication(sys.argv)
#     db_file = "MyInvestment.db"
#     # add_stock(db_file)
#     con, cur = check_db(db_file)
#     window=add_stocks(con,cur)
#     # window=set_defaults(" "," ")
#     sys.exit(APP.exec_())
#
# if __name__=='__main__':
#     main()








# if __name__ == '__main__':
#     db_file = "MyInvestment.db"
#     add_stock(db_file)
    # con, cur = check_db(db_file)
    # hi=add_stocks(con, cur)
