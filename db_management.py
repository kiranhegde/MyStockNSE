from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# import pandas
import sqlite3
import sys,os
import random
from collections import defaultdict
from sqlite3 import Error


db_file = "MyInvestment.db"
class make_nested_dict0(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def make_nested_dict1():
    return defaultdict(make_nested_dict1)




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


def read_db():
    listAgency, stockDB = read_all_stocks()
    # List_of_agency=get_agency_list(listAgency)
    #
    # print('DB')
    # print(listAgency)
    # print(stockDB)
    # exit()
    return listAgency, stockDB


def read_all_transaction():
    con, cur = check_db(db_file)
    paymentDB = make_nested_dict0()
    amount = cur.execute("SELECT * FROM investment")
    for all_row_data in amount:
        agency=all_row_data[1]
        ref= all_row_data[0]
        # date0=all_row_data[4]
        # date1=all_row_data[5]
        # date1=QDateTime.fromString(date1,"ddmmyyyy")
        # # print(date0,type(date1))
        rowList=[]
        rowList.clear()
        rowList = list(all_row_data[2:])
        row_data = tuple(rowList)
        # print(row_data)
        # stocksDB.setdefault(agency,ref)
        paymentDB[agency][ref]=row_data

    ListAgency = []
    ListAgency.clear()
    for key in paymentDB.keys():
        ListAgency.append(key)

    return ListAgency, paymentDB



def read_all_sales():
    con, cur = check_db(db_file)
    salesDB = make_nested_dict0()
    stock = cur.execute("SELECT * FROM sale")
    for all_row_data in stock:
        agency=all_row_data[1]
        ref= all_row_data[0]
        # date0=all_row_data[4]
        # date1=all_row_data[5]
        # date1=QDateTime.fromString(date1,"ddmmyyyy")
        # # print(date0,type(date1))
        rowList=[]
        rowList.clear()
        rowList = list(all_row_data[2:])
        row_data = tuple(rowList)
        # print(row_data)
        # stocksDB.setdefault(agency,ref)
        salesDB[agency][ref]=row_data

    ListAgency = []
    ListAgency.clear()
    for key in salesDB.keys():
        ListAgency.append(key)


    return ListAgency, salesDB




def read_all_stocks():
    con, cur = check_db(db_file)
    stocksDB = make_nested_dict0()
    stock = cur.execute("SELECT * FROM purchase")
    for all_row_data in stock:
        agency=all_row_data[1]
        ref= all_row_data[0]
        # date0=all_row_data[4]
        # date1=all_row_data[5]
        # date1=QDateTime.fromString(date1,"ddmmyyyy")
        # # print(date0,type(date1))
        rowList=[]
        rowList.clear()
        rowList = list(all_row_data[2:])
        row_data = tuple(rowList)
        # print(row_data)
        # stocksDB.setdefault(agency,ref)
        stocksDB[agency][ref]=row_data

    ListAgency = []
    ListAgency.clear()
    for key in stocksDB.keys():
        ListAgency.append(key)


    return ListAgency, stocksDB

def get_agency_list(self,agency):
    self.agencyList.clear()
    self.agencyList.itemDoubleClicked.connect(self.showStocks)
    for itm in agency:
        self.agencyList.addItem(itm)

    return self.agencyList

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



#
# # def add_stock(db_file):
# #     con, cur = check_db(db_file)
# #     #print(con,cur)
# #     add_stocks(con,cur)
#
# def check_msg():
#     msgBox = QMessageBox()
#     msgBox.setWindowTitle("database file missing")
#     msgBox.setText('database file needs to present in current location')
#     msgBox.setInformativeText("Please keep the db file"
#                               "in the running folder"
#                               "and try once again")
#     # msgBox.setWindowIcon(QIcon(""))
#     msgBox.setIcon(QMessageBox.Critical)
#     msgBox.exec()


def gen_id():
    con, cur = check_db(db_file)
    stock = cur.execute("SELECT * FROM purchase")
    id_list = []
    for all_row_data in stock:
        id_list.append(all_row_data[0])

    stock = cur.execute("SELECT * FROM sale")
    for all_row_data in stock:
        id_list.append(all_row_data[0])

    stock = cur.execute("SELECT * FROM investment")
    for all_row_data in stock:
        id_list.append(all_row_data[0])

    # print(id_list)
    stock_id = f'{random.randrange(1000, 10 ** 6)}'
    m = len(id_list) - 1
    # stock_id=6463
    # print("#",m,range(m))
    for i in range(m):
        # print("##"+str(i),stock_id)
        if stock_id in id_list:
            stock_id = f'{random.randrange(1000, 10 ** 6)}'
            # print("->"+str(stock_id))
        else:
            break

    return int(stock_id)

def default_parameters():
    con, cur = check_db(db_file)
    cur.execute('SELECT * FROM defaults')

    default = cur.fetchall()
    brockerage = default[0][0]
    gst = default[0][1]
    stt = default[0][2]
    itax = default[0][3]

    defaults=brockerage,gst,stt,itax

    return defaults


def save_transactionDB(row_data,save_mode):

    con, cur = check_db(db_file)
    stock_id = gen_id()

    agency = row_data[0]
    tdate = row_data[1]
    amount =row_data[2]
    tr_id = row_data[3]
    bank0 = row_data[4]
    bank1 = row_data[5]
    comment = row_data[6]

    if save_mode == "append":
        print(save_mode)

        if agency != "" and tdate != "" and amount != "" and bank0 != "" and bank1 != "" :
            try:
                query = "INSERT INTO 'investment' (id,agency,tr_date,tr_id,amount,from_bank,to_bank,remarks) VALUES(?,?,?,?,?,?,?,?)"
                cur.execute(query, (stock_id, agency, tdate,tr_id,amount,bank0,bank1,comment))
                con.commit()
                # msg=QMessageBox.information("Info", "New Stock information has been added")
                # msg.exec()
                msgBox = QMessageBox()
                msgBox.setWindowTitle("New Transaction")
                msgBox.setText("new transaction added, ID: "+str(stock_id))
                msgBox.setIcon(QMessageBox.Information)
                msgBox.exec_()
            except:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText("Transaction information not been added")
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Missing !!")
            msgBox.setText("Fields can't be empty!!!")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.exec_()

    if save_mode == "update":
        stock_id = str(stock_id)
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Warning")
        msgBox.setText('Are you sure to save changes to transaction with reference number' + stock_id + " ?")
        msgBox.setInformativeText("  Updated informatoin will be "
                                  "  permanatly registered to the "
                                  "  database !")
        # msgBox.setWindowIcon(QIcon(""))
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        buttonY = msgBox.button(QMessageBox.Yes)
        # buttonY.setText('Evet')
        # buttonN = box.button(QtGui.QMessageBox.No)
        # buttonN.setText('Iptal')
        msgBox.exec_()

        if msgBox.clickedButton() == buttonY:
            # if msgBox == QMessageBox.Yes:
            try:
                query = "UPDATE investment SET agency=?,tr_date=?,tr_id=?,amount=?,from_bank=?,to_bank=?,remarks=? WHERE id=?"
                cur.execute(query, (agency, tdate,tr_id,amount,bank0,bank1,comment, stock_id))
                con.commit()
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Updated !")
                msgBox.setText("Transaction with reference number " + str(stock_id) + " has been updated")
                msgBox.setIcon(QMessageBox.Information)
                msgBox.exec_()
            except:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText('Transaction with reference number ' + str(stock_id) + ' has not been updated..')
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Aborted")
            msgBox.setText('Changes are not updated to the database...')
            msgBox.setIcon(QMessageBox.Information)
            msgBox.exec_()

    return stock_id



def delTransDB(invoice):
    con, cur = check_db(db_file)

    msgBox = QMessageBox()
    msgBox.setWindowTitle("Warning")
    msgBox.setText("Are you sure to delete transaction information with reference number " + invoice + " ?")
    msgBox.setInformativeText("transaction  information will be "
                              "permanatly removed from the "
                              "database !")
    # msgBox.setWindowIcon(QIcon(""))
    msgBox.setIcon(QMessageBox.Question)
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.No)
    buttonY = msgBox.button(QMessageBox.Yes)


    buttonY = msgBox.button(QMessageBox.Yes)
    # buttonY.setText('Evet')
    # buttonN = box.button(QtGui.QMessageBox.No)
    # buttonN.setText('Iptal')
    msgBox.exec_()

    if msgBox.clickedButton() == buttonY:
        # if mbox == QMessageBox.Yes:
        try:
            query = "DELETE FROM investment WHERE id=?"
            cur.execute(query, (invoice,))
            con.commit()

            msgBox = QMessageBox()
            msgBox.setWindowTitle("Deleted !")
            msgBox.setText("transaction with reference number " + invoice + " has been deleted..")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.exec_()
        except:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setText("transaction with reference number " + invoice + " has not been deleted..")
            msgBox.setIcon(QMessageBox.warning)
            msgBox.exec_()
    else:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Aborted")
        msgBox.setText("Selected  transaction (id: "+invoice +") has not been deleted")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.exec_()







def saveStockSaleDB(row_data,stock_id,save_mode):

    con, cur = check_db(db_file)
    # stock = cur.execute("SELECT * FROM sale")
    # stock_id = gen_id()
    if save_mode=="update":
        con, cur = check_db(db_file)
        stock = cur.execute("SELECT * FROM sale")
        id_list = []
        for all_row_data in stock:
            # print(type(all_row_data[0]))
            id_list.append(all_row_data[0])

        if stock_id in id_list:
            save_mode = "update"
        else:
            save_mode = "append"

    #   0      1      2       3         4         5    6   7         8      9
    # tdate, sdate, price, quantity, unit_brock, gst, stt, itax, comment, self.save_db
    #
    # print(row_data)
    # query = "SELECT id FROM sale WHERE id=? "
    # cur.execute(query,[(stock_id)])
    # # cur.execute("""SELECT id FROM sale WHERE id=? """, (stock_id))
    # result=list(cur.fetchone())
    #
    # if stock_id in result:
    #     print("yes",result[0])
    # else:
    #     print(stock_id, 'not found')

    # print(row_data)
    #
    #
    # exit()

    agency= row_data[0]
    exchange = row_data[1]
    equity = row_data[2]
    Bdate = row_data[3]
    Bprice = row_data[4]
    Tdate = row_data[5]
    Sdate = row_data[6]
    TPrice = row_data[7]
    quantity = row_data[8]
    brokerage = row_data[9]
    gst = row_data[10]
    stt = row_data[11]
    itax = row_data[12]
    comments = row_data[13]



    defaults=default_parameters()

    if brokerage == "":
        brokerage = defaults[0]
    if gst == "":
        gst = defaults[1]
    if stt == "":
        stt = defaults[2]
    if itax == "":
        itax = defaults[3]

    # print(row_data)

    if save_mode == "append":
        if agency != "" and exchange != "" and equity != "" and Bdate != "" and Bprice != "" and Tdate != "" and Sdate != "" and TPrice != ""  and quantity != "":
            try:
                query = "INSERT INTO 'sale' (id,agency,exchange,equity,buy_date,buy_price,trade_date,settle_date,trade_price,quantity,brokerage,gst,stt,itax,remarks)" \
                        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                cur.execute(query, (stock_id, agency, exchange, equity, Bdate,Bprice,Tdate,Sdate,TPrice,quantity,brokerage,gst,stt,itax,comments))
                con.commit()
                # msg=QMessageBox.information("Info", "New Stock information has been added")
                # msg.exec()
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Sold Stock")
                msgBox.setText("Sold Stock data has been added. Stock ID: "+str(stock_id))
                msgBox.setIcon(QMessageBox.Information)
                msgBox.exec_()
            except:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText("Sold Stock data has not been added. Stock ID: "+str(stock_id))
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Missing !!")
            msgBox.setText("Fields can't be empty!!!")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.exec_()

    if save_mode == "update":
        # print("update",stock_id,type(brokerage))

        msgBox = QMessageBox()
        msgBox.setWindowTitle("Warning")
        msgBox.setText('Are you sure to save changes to sold stock with reference number' + str(stock_id) + " ?")
        msgBox.setInformativeText("  Updated informatoin will be "
                                  "  permanatly registered to the "
                                  "  database !")
        # msgBox.setWindowIcon(QIcon(""))
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        buttonY = msgBox.button(QMessageBox.Yes)
        # buttonY.setText('Evet')
        # buttonN = box.button(QtGui.QMessageBox.No)
        # buttonN.setText('Iptal')
        msgBox.exec_()


        if msgBox.clickedButton() == buttonY:
            # if msgBox == QMessageBox.Yes:
            #             (id, agency, exchange, equity, buy_date, buy_price, trade_date, settle_date, trade_price, quantity, brokerage, gst, stt, itax, remarks)
            try:
                query = "UPDATE sale SET trade_date=?,settle_date=?,trade_price=?,quantity=?,brokerage=?,gst=?,stt=?,itax=?,remarks=? WHERE id=?"
                cur.execute(query, (Tdate, Sdate, TPrice, quantity, brokerage, gst, stt, itax, comments, stock_id))
                con.commit()
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Updated !")
                msgBox.setText("Stock sold with reference number " + str(stock_id) + " has been updated")
                msgBox.setIcon(QMessageBox.Information)
                msgBox.exec_()
            except:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText('Stock sold with reference number ' + str(stock_id) + ' has not been updated..')
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Aborted")
            msgBox.setText('Changes are not updated to the database...')
            msgBox.setIcon(QMessageBox.Information)
            msgBox.exec_()


def saveStockDB(row_data,stock_id,save_mode):
    con, cur = check_db(db_file)

    if save_mode=="update":
        con, cur = check_db(db_file)
        stock = cur.execute("SELECT * FROM purchase")
        id_list = []
        for all_row_data in stock:
            # print(type(all_row_data[0]))
            id_list.append(all_row_data[0])

        if stock_id in id_list:
            save_mode = "update"
        else:
            save_mode = "append"


    # print("db append:",row_data)


    agency= row_data[0]
    exchange = row_data[1]
    equity = row_data[2]
    tradeDate = row_data[3]
    settleDate = row_data[4]
    tradPrice = row_data[5]
    quantity = row_data[6]
    brockerage = row_data[7]
    gst = row_data[8]
    stt = row_data[9]
    itax = row_data[10]
    comments = row_data[11]

    defaults=default_parameters()

    if brockerage == "":
        brockerage = defaults[0]
    if gst == "":
        gst = defaults[1]
    if stt == "":
        stt = defaults[2]
    if itax == "":
        itax = defaults[3]

    if save_mode == "append":
        if agency != "" and exchange != "" and equity != "" and tradeDate != "" and settleDate != "" and tradPrice != "" and quantity != "":
            try:
                query = "INSERT INTO 'purchase' (id,agency,exchange,equity,trade_date,settle_date,trade_price,quantity,unit_brockerage,gst_brockerage,stt,income_tax,remarks)" \
                        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
                cur.execute(query, (stock_id, agency, exchange, equity, tradeDate, settleDate, tradPrice, quantity, brockerage, gst, stt, itax, comments))
                con.commit()
                # msg=QMessageBox.information("Info", "New Stock information has been added")
                # msg.exec()
                msgBox = QMessageBox()
                msgBox.setWindowTitle("New Stock")
                msgBox.setText("New Stock data has been added. Stock ID: "+str(stock_id))
                msgBox.setIcon(QMessageBox.Information)
                msgBox.exec_()
            except:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText("New Stock data has not been added. Stock ID: "+str(stock_id))
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Missing !!")
            msgBox.setText("Fields can't be empty!!!")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.exec_()


    if save_mode=="update":
        # stock_id=str(stock_id)
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Warning")
        msgBox.setText('Are you sure to save changes to stock with reference number'+ str(stock_id) + " ?")
        msgBox.setInformativeText("  Updated informatoin will be "
                                  "  permanatly registered to the "
                                  "  database !")
        # msgBox.setWindowIcon(QIcon(""))
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        buttonY = msgBox.button(QMessageBox.Yes)
        # buttonY.setText('Evet')
        # buttonN = box.button(QtGui.QMessageBox.No)
        # buttonN.setText('Iptal')
        msgBox.exec_()

        if msgBox.clickedButton() == buttonY:
        # if msgBox == QMessageBox.Yes:
            try:
                query = "UPDATE purchase SET agency=?,exchange=?,equity=?,trade_date=?,settle_date=?,trade_price=?,quantity=?,unit_brockerage=?,gst_brockerage=?,stt=?,income_tax=?,remarks=? WHERE id=?"
                cur.execute(query, (agency, exchange, equity, tradeDate, settleDate, tradPrice, quantity, brockerage, gst, stt, itax,comments, stock_id))
                con.commit()
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Updated !")
                msgBox.setText("Stock with reference number " + str(stock_id) + " has been updated")
                msgBox.setIcon(QMessageBox.Information)
                msgBox.exec_()
            except:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText('Stock with reference number ' + str(stock_id) + ' has not been updated..')
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Aborted")
            msgBox.setText('Changes are not updated to the database...')
            msgBox.setIcon(QMessageBox.Information)
            msgBox.exec_()

    return stock_id


def delStockDB(invoice):
    con, cur = check_db(db_file)

    msgBox = QMessageBox()
    msgBox.setWindowTitle("Warning")
    msgBox.setText("Are you sure to delete stock with reference number " + invoice + " ?")
    msgBox.setInformativeText("Stock  information will be "
                              "permanatly removed from the "
                              "database !")
    # msgBox.setWindowIcon(QIcon(""))
    msgBox.setIcon(QMessageBox.Question)
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.No)
    buttonY = msgBox.button(QMessageBox.Yes)


    buttonY = msgBox.button(QMessageBox.Yes)
    # buttonY.setText('Evet')
    # buttonN = box.button(QtGui.QMessageBox.No)
    # buttonN.setText('Iptal')
    msgBox.exec_()

    if msgBox.clickedButton() == buttonY:
        # if mbox == QMessageBox.Yes:
        try:
            query = "DELETE FROM purchase WHERE id=?"
            cur.execute(query, (invoice,))
            con.commit()

            msgBox = QMessageBox()
            msgBox.setWindowTitle("Deleted !")
            msgBox.setText("Stock with reference number " + invoice + " has been deleted..")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.exec_()
        except:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Stock with reference number " + invoice + " has not been deleted..")
            msgBox.setIcon(QMessageBox.warning)
            msgBox.exec_()
    else:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Aborted")
        msgBox.setText("Selected  stock (id: "+invoice +") has not been deleted")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.exec_()

class average_stocks(QDialog):

    # def __init__(self,con,cur,agency=""):
    def __init__(self,stock_data,parent=None):
        super(average_stocks,self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Weighted Average of Stocks")
        # self.con=con
        # self.cur=cur
        self.stock_data=stock_data

        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,450,450)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.fetch_data()
        # self.default_paramters()
        self.widgets()
        self.layouts()

    def fetch_data(self):
        self.xchange=self.stock_data[0]
        self.equity=self.stock_data[1]
        self.trade_date=self.stock_data[2]
        self.price=str(self.stock_data[3])
        self.quantity=str(self.stock_data[4])
        self.Oprice=self.stock_data[5]


    def widgets(self):
        fnt = QFont()
        fnt.setPointSize(12)
        fnt.setBold(True)
        fnt.setFamily("Arial")


        self.save_db = False
        self.titleText=QLabel("Stock Averaging")
        # self.agencyEntry=QLineEdit()
        # self.agencyEntry.setText(self.agency)
        # self.agencyEntry.setReadOnly(1)
        # self.agencyEntry.setDisabled(True)
        # self.exchangeEntry=QLineEdit()
        # self.exchangeEntry.setText(self.xchange)

        self.exchangeEntry = QLineEdit()
        self.exchangeEntry.setText(self.xchange)
        self.exchangeEntry.setDisabled(True)

        self.equityEntry=QLineEdit()
        self.equityEntry.setText(self.equity)
        self.equityEntry.setDisabled(True)

        self.trade_dateEntry = QDateEdit(self)
        self.trade_dateEntry.setDate(QDate.fromString(self.trade_date,"dd/MM/yyyy"))
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.trade_dateEntry.setDisabled(True)

        self.trade_priceEntry = QLineEdit()
        self.trade_priceEntry.setText(self.price)

        self.quantityEntry = QLineEdit()
        self.quantityEntry.setText(self.quantity)

        self.current_priceEntry = QLineEdit()
        self.current_priceEntry.setPlaceholderText("Enter current price")
        self.current_quantityEntry = QLineEdit()
        self.current_quantityEntry.setPlaceholderText("Enter current quantity of stocks")
        self.current_price=0
        self.current_quantity=0


        self.avg_priceEntry=QLabel()
        self.avg_priceEntry.setFont(fnt)
        self.avg_priceEntry.setText("Average Price: ")
        self.delta_Entry = QLabel()
        self.delta_Entry.setFont(fnt)
        self.delta_Entry.setText("Gain/Loss per stock: ")

        self.overalldelta_Entry = QLabel()
        self.overalldelta_Entry.setFont(fnt)
        self.overalldelta_Entry.setText("Overall Gain/Loss : ")

        self.total_priceEntry = QLabel()
        self.total_priceEntry.setFont(fnt)
        self.total_priceEntry.setText("Total Price: ")

        self.avg_priceEntry.setStyleSheet('color: blue')
        self.delta_Entry.setStyleSheet('color: blue')
        self.overalldelta_Entry.setStyleSheet('color: blue')
        self.total_priceEntry.setStyleSheet('color: blue')

        # self.exchangeEntry.setPlaceholderText("Enter name of exchange(Eg. BSE,NSE, etc)")
        self.equityEntry.setPlaceholderText("Enter Equity name (Eg. SBI, ITC, etc)")
        # self.trade_dateEntry.setDate(QDate.currentDate())
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        # self.settle_dateEntry.setDate(QDate.currentDate())

        self.trade_priceEntry.setPlaceholderText("Enter trade price")
        self.quantityEntry.setPlaceholderText("Enter quantity of stocks")
        # self.remarksEntry.setPlaceholderText("Type your remarks ..")
        # https: // www.programcreek.com / python / example / 108071 / PyQt5.QtWidgets.QDialogButtonBox
        # self.buttonBox=QDialogButtonBox(QDialogButtonBox.Ok |QDialogButtonBox.Reset |QDialogButtonBox.Cancel)
        # self.buttonBox=QDialogButtonBox(QDialogButtonBox.Ok |QDialogButtonBox.Cancel)
        self.buttonBox=QDialogButtonBox(QDialogButtonBox.Cancel)
        # self.resets=QPushButton("Reset")
        # self.resets.clicked.connect(self.clearAll)
        self.calcAvg = QPushButton("Calculate")
        self.calcAvg.clicked.connect(self.getAvg)
        # self.addBtn=QPushButton("Submit")
        # self.addBtn.clicked.connect(self.add_stock)
        # self.clrBtn = QPushButton("Clear")
        # self.clrBtn.clicked.connect(self.clear_stock)
        # self.buttonBox.addButton(self.resets,QDialogButtonBox.ResetRole)
        self.buttonBox.addButton(self.calcAvg,QDialogButtonBox.ResetRole)
        # self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # self.buttonBox.clear.connect(self.clearAll)
        self.spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding,QSizePolicy.Minimum )

        # self.saveDB=QCheckBox("Update to database")
        # self.saveDB=QCheckBox("Update to Database:")
        # self.saveDB.stateChanged.connect(self.state_changed)

        # if self.agency0:
        #     self.agencyEntry.setText(self.agency0)
        # self.exchangeEntry.setText("NSE")
        # self.equityEntry.setText("SBI")
        # self.trade_priceEntry.setText("200")
        # self.quantityEntry.setText("100")

    def state_changed(self):
        self.save_db=True

    def getAvg(self):
        q1=int(self.quantityEntry.text())
        q2=int(self.current_quantityEntry.text())
        if q2 == "":
            q2=0
        p1=float(self.price)
        p2=float(self.current_priceEntry.text())
        if p2 == "":
            p2=0.0
        # print(q1,q2,p1,p2)
        avg=(p1*q1+p2*q2)/(q1+q2)
        avg=round(avg,3)

        delta=round(avg-p1,3)
        total=round(p2*q2,3)
        overallPL=round((q1+q2)*delta,3)

        self.avg_priceEntry.setText("Average Price: "+str(avg))
        self.delta_Entry.setText("Gain/Loss per stock: "+str(delta))
        self.overalldelta_Entry.setText("Overall Gain/Loss : "+str(overallPL))
        self.total_priceEntry.setText("Total Price: "+str(total))

        return


    def accept(self):
        # self.output="hi"
        agency = self.agencyEntry.text()
        # xchange = self.exchangeEntry.text()
        xchange = self.exchangeEntry.currentText()
        equity = self.equityEntry.text()
        tdate = self.trade_dateEntry.text()
        sdate = self.settle_dateEntry.text()
        price = self.trade_priceEntry.text()
        quantity = self.quantityEntry.text()
        unit_brock = self.unit_brockEntry.text()
        gst = self.gst_brockEntry.text()
        stt = self.stt_Entry.text()
        itax = self.it_Entry.text()
        comment = self.remarksEntry.text()
        self.output = agency, xchange, equity, tdate, sdate, price, quantity, unit_brock, gst, stt, itax, comment,self.save_db
        super(update_stocks,self).accept()


    def clearAll(self):

        # self.agencyEntry.setText("")
        # self.exchangeEntry.setText("")
        self.equityEntry.setText("")
        self.trade_dateEntry.setDate(QDate.currentDate())
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.settle_dateEntry.setDate(QDate.currentDate())
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.trade_priceEntry.setText("")
        self.quantityEntry.setText("")
        self.unit_brockEntry.setText("")
        self.gst_brockEntry.setText("")
        self.stt_Entry.setText("")
        self.it_Entry.setText("")
        self.remarksEntry.setText("")


    def get_inp(self):
        return self.output

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.mainTopLayout=QVBoxLayout()
        self.topLayout=QFormLayout()
        self.bottomLayout=QHBoxLayout()
        self.topFrame=QFrame()

        # self.symbolLabel = QLabel("Equity symbol")
        # self.symbolEntry = QLineEdit()
        # self.intervalLabel = QLabel("Time Interval")
        # self.intervalEntry = QLineEdit()


        self.topGroupBox=QGroupBox("Stock Information")
        # self.bottomGroupBox=QGroupBox("Control")
        self.bottomGroupBox=QGroupBox()

        # self.topLayout.addRow(QLabel("Agency: "),self.agencyEntry)
        self.topLayout.addRow(QLabel("Exchange: "),self.exchangeEntry)
        self.topLayout.addRow(QLabel("Equity: "),self.equityEntry)
        self.topLayout.addRow(QLabel("Trade Date: "),self.trade_dateEntry)
        # self.topLayout.addRow(QLabel("Settlement Date: "),self.settle_dateEntry)
        self.topLayout.addRow(QLabel("trade Price: "),self.trade_priceEntry)
        self.topLayout.addRow(QLabel("Quantity: "),self.quantityEntry)
        self.topLayout.addRow(QLabel("Current Price: "), self.current_priceEntry)
        self.topLayout.addRow(QLabel("Current Quantity: "), self.current_quantityEntry)
        self.topLayout.addWidget(self.avg_priceEntry)
        self.topLayout.addWidget(self.delta_Entry)
        self.topLayout.addWidget(self.overalldelta_Entry)
        self.topLayout.addWidget(self.total_priceEntry)

        # self.topLayout.addRow(self.avg_priceEntry)
        # self.topLayout.addRow(QLabel("Brockerage per unit: "),self.unit_brockEntry)
        # self.topLayout.addRow(QLabel("GST on Brockerage: "),self.gst_brockEntry)
        # self.topLayout.addRow(QLabel("STT on Share: "),self.stt_Entry)
        # self.topLayout.addRow(QLabel("Income Tax: "),self.it_Entry)
        # self.topLayout.addRow(QLabel("Remarks: "),self.remarksEntry)

        # self.topLayout.addItem(self.spaceItem)
        # self.topLayout.addRow(QLabel("Update to Database: "),self.saveDB)

        # self.bottomLayout.addWidget(self.addBtn)
        # self.bottomLayout.addWidget(self.clrBtn)
        # self.topLayout.addWidget(self.saveDB)
        self.bottomLayout.addWidget(self.buttonBox)
        self.topGroupBox.setLayout(self.topLayout)
        self.bottomGroupBox.setLayout(self.bottomLayout)

        # self.topFrame.setLayout(self.topLayout)
        #self.topGroupBox.add setLayout(self.topLayout)
        # self.bottomGroupBox.setLayout(self.bottomLayout)
        self.mainTopLayout.addWidget(self.topGroupBox)
        # self.mainTopLayout.addWidget(self.saveDB)
        self.mainTopLayout.addWidget(self.bottomGroupBox)
        self.mainLayout.addLayout(self.mainTopLayout)
        self.setLayout(self.mainLayout)





def new_stock(agency=""):
    con, cur = check_db(db_file)
    if agency:
        stk = add_stocks(agency)
    else:
        stk = add_stocks()
    # stk.exec_()

class show_stock_info(QDialog):

    def __init__(self,stock_id,stock_info, parent=None):
        super(show_stock_info, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Stock Details")
        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(550, 350, 250, 350)
        self.setFixedSize(self.size())
        self.stock_id=stock_id
        self.stock_info=stock_info
        self.UI()
        self.show()

    def UI(self):
        self.productDetails()
        self.widgets()
        self.layouts()

    def productDetails(self):

        self.xchange=self.stock_info[0]
        self.equity=self.stock_info[1]
        self.Tdate=self.stock_info[2]
        self.Sdate=self.stock_info[3]
        self.price=self.stock_info[4]
        self.quantity=self.stock_info[5]
        self.cont_amount=self.stock_info[6]
        self.brokerage=self.stock_info[7]
        self.gst=self.stock_info[8]
        self.stt=self.stock_info[9]
        self.itax=self.stock_info[10]
        # print(self.stock_info)

        # exit()

    def widgets(self):
        fnt = QFont()
        fnt.setPointSize(13)
        fnt.setBold(True)
        fnt.setFamily("Arial")

        self.stock_idLabel = QLabel()
        self.stock_idLabel.setFont(fnt)
        self.stock_idLabel.setText(str(self.stock_id))


        self.xchangeLabel=QLabel()
        self.xchangeLabel.setFont(fnt)
        self.xchangeLabel.setText(self.xchange)

        self.equityLabel = QLabel(self.equity)
        self.equityLabel.setFont(fnt)
        self.equityLabel.setText(self.equity)

        self.TdateLabel = QLabel()
        self.TdateLabel.setFont(fnt)
        self.TdateLabel.setText(self.Tdate)

        self.SdateLabel = QLabel()
        self.SdateLabel.setFont(fnt)
        self.SdateLabel.setText(self.Sdate)

        self.priceLabel = QLabel()
        self.priceLabel.setFont(fnt)
        self.priceLabel.setText(str(self.price))

        self.quantityLabel = QLabel()
        self.quantityLabel.setFont(fnt)
        self.quantityLabel.setText(str(self.quantity))

        self.cont_amountLabel = QLabel()
        self.cont_amountLabel.setFont(fnt)
        self.cont_amountLabel.setText(str(self.cont_amount))

        self.brokerageLabel = QLabel()
        self.brokerageLabel.setFont(fnt)
        self.brokerageLabel.setText(str(self.brokerage))

        self.gstLabel = QLabel()
        self.gstLabel.setFont(fnt)
        self.gstLabel.setText(str(self.gst))

        self.sttLabel = QLabel(str(self.stt))
        self.sttLabel.setFont(fnt)
        self.itaxLabel = QLabel(str(self.itax))
        self.itaxLabel.setFont(fnt)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.bottomFrame = QFrame()
        self.bottomLayout = QFormLayout()
        self.bottomLayout.addRow(QLabel("Stock ID: "), self.stock_idLabel)
        self.bottomLayout.addRow(QLabel("Exchange: "), self.xchangeLabel)
        self.bottomLayout.addRow(QLabel("Equity: "), self.equityLabel)
        self.bottomLayout.addRow(QLabel("Trade Date: "), self.TdateLabel)
        self.bottomLayout.addRow(QLabel("Settlement Date: "), self.SdateLabel)
        self.bottomLayout.addRow(QLabel("Price: "), self.priceLabel)
        self.bottomLayout.addRow(QLabel("Quantity: "), self.quantityLabel)
        self.bottomLayout.addRow(QLabel("Contract Amount: "), self.cont_amountLabel)
        self.bottomLayout.addRow(QLabel("Brokerage "), self.brokerageLabel)
        self.bottomLayout.addRow(QLabel("GST"), self.gstLabel)
        self.bottomLayout.addRow(QLabel("STT"), self.sttLabel)
        self.bottomLayout.addRow(QLabel("Income Tax"), self.itaxLabel)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)


class add_stocks(QDialog):

    # def __init__(self,con,cur,agency=""):
    def __init__(self,agency="",dbsave="",parent=None):
        super(add_stocks,self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Add stock")
        # self.con=con
        # self.cur=cur
        self.dbsave=False
        self.agency0=""
        if agency:
            self.agency0=agency

        if dbsave:
           self.dbsave = True

        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,450,450)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.get_db()
        self.get_default_paramters()
        self.widgets()
        self.layouts()

    def get_db(self):
        self.con, self.cur = check_db(db_file)


    def get_default_paramters(self):
        default=default_parameters()
        self.brockerage = default[0]
        self.gst = default[1]
        self.stt = default[2]
        self.itax = default[3]


    def widgets(self):
        self.save_db = False
        self.titleText=QLabel("Add New stock")
        self.agencyEntry=QLineEdit()
        self.agencyEntry.setPlaceholderText("Enter name of agency (Eg. Kotak, Zerodha, etc)")
        # self.exchangeEntry=QLineEdit()
        # self.exchangeEntry.setPlaceholderText("Enter name of exchange(Eg. BSE,NSE, etc)")
        self.exchangeEntry = QComboBox()
        self.exchangeEntry.addItems(["NSE","BSE"])
        ns1="NSE"
        indx= self.exchangeEntry.findText(ns1)
        self.exchangeEntry.setCurrentIndex(indx)
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

        # self.addBtn=QPushButton("Submit")
        # self.addBtn.clicked.connect(self.add_stock)
        # self.clrBtn = QPushButton("Clear")
        # self.clrBtn.clicked.connect(self.clear_stock)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.resets = QPushButton("Reset")
        self.resets.clicked.connect(self.clearAll)
        self.buttonBox.addButton(self.resets, QDialogButtonBox.ResetRole)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.saveDB = QCheckBox("Update to Database:")
        if self.dbsave:
            self.saveDB.setChecked(True)
            self.saveDB.setDisabled(True)
        else:
            self.saveDB.stateChanged.connect(self.state_changed)

        if self.agency0:
            self.agencyEntry.setText(self.agency0)

        # self.exchangeEntry.setText("NSE")
        self.equityEntry.setText("SBI")
        self.trade_priceEntry.setText("200")
        self.quantityEntry.setText("100")
        self.remarksEntry.setText(" Testing...")

    def state_changed(self):
        self.save_db = True

    def accept(self):
        # self.output="hi"
        agency=self.agencyEntry.text()
        xchange=self.exchangeEntry.currentText()
        equity=self.equityEntry.text()
        tdate=self.trade_dateEntry.text()
        sdate=self.settle_dateEntry.text()
        price=self.trade_priceEntry.text()
        quantity=self.quantityEntry.text()
        unit_brock=self.unit_brockEntry.text()
        gst=self.gst_brockEntry.text()
        stt=self.stt_Entry.text()
        itax=self.it_Entry.text()
        comment=self.remarksEntry.text()
        self.output=agency,xchange,equity,tdate,sdate,price,quantity,unit_brock,gst,stt,itax,comment,self.save_db

        super(add_stocks, self).accept()

    def clearAll(self):
        self.agencyEntry.setText("")
        self.exchangeEntry.setText("")
        self.equityEntry.setText("")
        self.trade_dateEntry.setDate(QDate.currentDate())
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.settle_dateEntry.setDate(QDate.currentDate())
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.trade_priceEntry.setText("")
        self.quantityEntry.setText("")
        self.unit_brockEntry.setText("")
        self.gst_brockEntry.setText("")
        self.stt_Entry.setText("")
        self.it_Entry.setText("")
        self.remarksEntry.setText("")


    def get_inp(self):
        return self.output


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

        # self.bottomLayout.addWidget(self.addBtn)
        # self.bottomLayout.addWidget(self.clrBtn)
        self.bottomLayout.addWidget(self.buttonBox)

        self.topGroupBox.setLayout(self.topLayout)
        self.bottomGroupBox.setLayout(self.bottomLayout)

        # self.topFrame.setLayout(self.topLayout)
        #self.topGroupBox.add setLayout(self.topLayout)
        # self.bottomGroupBox.setLayout(self.bottomLayout)
        self.mainTopLayout.addWidget(self.topGroupBox)
        self.mainTopLayout.addWidget(self.saveDB)
        self.mainTopLayout.addWidget(self.bottomGroupBox)

        self.mainLayout.addLayout(self.mainTopLayout)
        self.setLayout(self.mainLayout)


class update_stocks(QDialog):

    # def __init__(self,con,cur,agency=""):
    def __init__(self,stock_data,parent=None):
        super(update_stocks,self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Update stock")
        # self.con=con
        # self.cur=cur
        self.stock_data=stock_data

        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,450,450)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.fetch_data()
        # self.default_paramters()
        self.widgets()
        self.layouts()

    def fetch_data(self):
        self.agency=self.stock_data[0]
        self.xchange=self.stock_data[1]
        self.equity=self.stock_data[2]
        self.trade_date=self.stock_data[3]
        self.settle_date=self.stock_data[4]
        self.price=str(self.stock_data[5])
        self.quantity=str(self.stock_data[6])
        self.brockerage=str(self.stock_data[7])
        self.gst=str(self.stock_data[8])
        self.stt=str(self.stock_data[9])
        self.itax=str(self.stock_data[10])
        self.comment=self.stock_data[11]


    def default_paramters(self):
        cur=self.cur
        cur.execute('SELECT * FROM defaults')
        default = cur.fetchall()
        self.brockerage = default[0][0]
        self.gst = default[0][1]
        self.stt = default[0][2]
        self.itax = default[0][3]

    def widgets(self):
        self.save_db = False
        self.titleText=QLabel("Add New stock")
        self.agencyEntry=QLineEdit()
        self.agencyEntry.setText(self.agency)
        # self.agencyEntry.setReadOnly(1)
        self.agencyEntry.setDisabled(True)
        # self.exchangeEntry=QLineEdit()
        # self.exchangeEntry.setText(self.xchange)

        self.exchangeEntry = QComboBox()
        self.exchangeEntry.addItems(["NSE", "BSE"])
        ns1 = self.xchange
        indx = self.exchangeEntry.findText(ns1)
        self.exchangeEntry.setCurrentIndex(indx)

        self.equityEntry=QLineEdit()
        self.equityEntry.setText(self.equity)
        self.trade_dateEntry = QDateEdit(self)
        #self.dateEdit.setDateTime(QDateTime(QDate(2019, 2, 23),QTime(0, 0, 0)))        #
        self.trade_dateEntry.setDate(QDate.fromString(self.trade_date,"dd/MM/yyyy"))
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.settle_dateEntry = QDateEdit(self)
        self.settle_dateEntry.setDate(QDate.fromString(self.settle_date,"dd/MM/yyyy"))
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")
        # self.trade_dateEntry = QLineEdit()
        # self.trade_dateEntry.setPlaceholderText("Enter trade date(DD/MM/YEAR)")
        # self.settle_dateEntry=QLineEdit()
        # self.settle_dateEntry.setPlaceholderText("Enter settlement date(DD/MM/YEAR)")
        self.trade_priceEntry = QLineEdit()
        self.trade_priceEntry.setText(self.price)


        self.quantityEntry = QLineEdit()
        self.quantityEntry.setText(self.quantity)

        self.unit_brockEntry = QLineEdit()
        self.unit_brockEntry.setText(str(self.brockerage))

        self.gst_brockEntry = QLineEdit()
        self.gst_brockEntry.setText(str(self.gst))

        self.stt_Entry = QLineEdit()
        self.stt_Entry.setText(str(self.stt))
        self.it_Entry = QLineEdit()

        self.it_Entry.setText(str(self.itax))
        self.remarksEntry = QLineEdit()
        self.remarksEntry.setText(self.comment)

        self.agencyEntry.setPlaceholderText("Enter name of agency (Eg. Kotak, Zerodha, etc)")
        # self.exchangeEntry.setPlaceholderText("Enter name of exchange(Eg. BSE,NSE, etc)")
        self.equityEntry.setPlaceholderText("Enter Equity name (Eg. SBI, ITC, etc)")
        # self.trade_dateEntry.setDate(QDate.currentDate())
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        # self.settle_dateEntry.setDate(QDate.currentDate())
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.trade_priceEntry.setPlaceholderText("Enter trade price")
        self.quantityEntry.setPlaceholderText("Enter quantity of stocks")
        self.unit_brockEntry.setPlaceholderText("Enter brockerage(%) per unit")
        self.gst_brockEntry.setPlaceholderText("Enter gst(%) on brockerage")
        self.stt_Entry.setPlaceholderText("Enter stt(%) of share value")
        self.it_Entry.setPlaceholderText("Enter Income tax slab(%)")
        self.remarksEntry.setPlaceholderText("Type your remarks ..")
        # https: // www.programcreek.com / python / example / 108071 / PyQt5.QtWidgets.QDialogButtonBox
        # self.buttonBox=QDialogButtonBox(QDialogButtonBox.Ok |QDialogButtonBox.Reset |QDialogButtonBox.Cancel)
        self.buttonBox=QDialogButtonBox(QDialogButtonBox.Ok |QDialogButtonBox.Cancel)
        self.resets=QPushButton("Reset")
        self.resets.clicked.connect(self.clearAll)
        # self.addBtn=QPushButton("Submit")
        # self.addBtn.clicked.connect(self.add_stock)
        # self.clrBtn = QPushButton("Clear")
        # self.clrBtn.clicked.connect(self.clear_stock)
        self.buttonBox.addButton(self.resets,QDialogButtonBox.ResetRole)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # self.buttonBox.clear.connect(self.clearAll)
        self.spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding,QSizePolicy.Minimum )

        # self.saveDB=QCheckBox("Update to database")
        self.saveDB=QCheckBox("Update to Database:")
        self.saveDB.stateChanged.connect(self.state_changed)

        # if self.agency0:
        #     self.agencyEntry.setText(self.agency0)
        # self.exchangeEntry.setText("NSE")
        # self.equityEntry.setText("SBI")
        # self.trade_priceEntry.setText("200")
        # self.quantityEntry.setText("100")

    def state_changed(self):
        self.save_db=True

    def accept(self):
        # self.output="hi"
        agency = self.agencyEntry.text()
        # xchange = self.exchangeEntry.text()
        xchange = self.exchangeEntry.currentText()
        equity = self.equityEntry.text()
        tdate = self.trade_dateEntry.text()
        sdate = self.settle_dateEntry.text()
        price = self.trade_priceEntry.text()
        quantity = self.quantityEntry.text()
        unit_brock = self.unit_brockEntry.text()
        gst = self.gst_brockEntry.text()
        stt = self.stt_Entry.text()
        itax = self.it_Entry.text()
        comment = self.remarksEntry.text()
        self.output = agency, xchange, equity, tdate, sdate, price, quantity, unit_brock, gst, stt, itax, comment,self.save_db
        super(update_stocks,self).accept()


    def clearAll(self):

        # self.agencyEntry.setText("")
        # self.exchangeEntry.setText("")
        self.equityEntry.setText("")
        self.trade_dateEntry.setDate(QDate.currentDate())
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.settle_dateEntry.setDate(QDate.currentDate())
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.trade_priceEntry.setText("")
        self.quantityEntry.setText("")
        self.unit_brockEntry.setText("")
        self.gst_brockEntry.setText("")
        self.stt_Entry.setText("")
        self.it_Entry.setText("")
        self.remarksEntry.setText("")


    def get_inp(self):
        return self.output

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

        # self.topLayout.addItem(self.spaceItem)
        # self.topLayout.addRow(QLabel("Update to Database: "),self.saveDB)

        # self.bottomLayout.addWidget(self.addBtn)
        # self.bottomLayout.addWidget(self.clrBtn)
        # self.topLayout.addWidget(self.saveDB)
        self.bottomLayout.addWidget(self.buttonBox)


        self.topGroupBox.setLayout(self.topLayout)
        self.bottomGroupBox.setLayout(self.bottomLayout)

        # self.topFrame.setLayout(self.topLayout)
        #self.topGroupBox.add setLayout(self.topLayout)
        # self.bottomGroupBox.setLayout(self.bottomLayout)
        self.mainTopLayout.addWidget(self.topGroupBox)
        self.mainTopLayout.addWidget(self.saveDB)
        self.mainTopLayout.addWidget(self.bottomGroupBox)

        self.mainLayout.addLayout(self.mainTopLayout)

        self.setLayout(self.mainLayout)


class sold_stocks(QDialog):

    # def __init__(self,con,cur,agency=""):
    def __init__(self,stock_data,parent=None):
        super(sold_stocks,self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Sold stock")
        self.stock_data=stock_data

        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,450,490)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.fetch_data()
        # self.default_paramters()
        self.widgets()
        self.layouts()

    def fetch_data(self):
        # print( type(self.stock_data))
        self.agency=self.stock_data[0]
        self.xchange=self.stock_data[1]
        self.equity=self.stock_data[2]
        self.trade_date=self.stock_data[3]
        self.settle_date=self.stock_data[4]
        self.price=str(self.stock_data[5])
        self.quantity=str(self.stock_data[6])
        self.brockerage=str(self.stock_data[7])
        self.gst=str(self.stock_data[8])
        self.stt=str(self.stock_data[9])
        self.itax=str(self.stock_data[10])
        # self.comment=self.stock_data[11]


    def default_paramters(self):
        cur=self.cur
        cur.execute('SELECT * FROM defaults')
        default = cur.fetchall()
        self.brockerage = default[0][0]
        self.gst = default[0][1]
        self.stt = default[0][2]
        self.itax = default[0][3]

    def widgets(self):
        self.save_db = False
        self.titleText=QLabel("Sell stock")
        self.agencyEntry=QLineEdit()
        self.agencyEntry.setText(self.agency)
        # self.agencyEntry.setReadOnly(1)
        self.agencyEntry.setDisabled(True)
        # self.exchangeEntry=QLineEdit()
        # self.exchangeEntry.setText(self.xchange)

        self.exchangeEntry = QComboBox()
        self.exchangeEntry.addItems(["NSE", "BSE"])
        ns1 = self.xchange
        indx = self.exchangeEntry.findText(ns1)
        self.exchangeEntry.setCurrentIndex(indx)
        self.exchangeEntry.setDisabled(True)

        self.equityEntry=QLineEdit()
        self.equityEntry.setText(self.equity)
        self.equityEntry.setDisabled(True)

        self.buy_dateEntry = QDateEdit(self)
        #self.dateEdit.setDateTime(QDateTime(QDate(2019, 2, 23),QTime(0, 0, 0)))        #
        self.buy_dateEntry.setDate(QDate.fromString(self.trade_date,"dd/MM/yyyy"))
        self.buy_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.buy_dateEntry.setDisabled(True)

        self.buy_priceEntry = QLineEdit()
        self.buy_priceEntry.setText(self.price)
        self.buy_priceEntry.setDisabled(True)

        self.trade_dateEntry = QDateEdit(self)
        # self.dateEdit.setDateTime(QDateTime(QDate(2019, 2, 23),QTime(0, 0, 0)))        #
        self.trade_dateEntry.setDate(QDate.currentDate())
        # self.trade_dateEntry.setDate(QDate.fromString(self.trade_date, "dd/MM/yyyy"))
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")

        self.settle_dateEntry = QDateEdit(self)
        self.settle_dateEntry.setDate(QDate.currentDate())
        # self.settle_dateEntry.setDate(QDate.fromString(self.settle_date,"dd/MM/yyyy"))
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")
        # self.trade_dateEntry = QLineEdit()
        # self.trade_dateEntry.setPlaceholderText("Enter trade date(DD/MM/YEAR)")
        # self.settle_dateEntry=QLineEdit()
        # self.settle_dateEntry.setPlaceholderText("Enter settlement date(DD/MM/YEAR)")
        self.trade_priceEntry = QLineEdit()
        self.trade_priceEntry.setPlaceholderText("Enter traded price when sold")

        self.quantityEntry = QLineEdit()
        self.quantityEntry.setPlaceholderText("Enter number of stocks sold")

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

        # https: // www.programcreek.com / python / example / 108071 / PyQt5.QtWidgets.QDialogButtonBox

        # self.buttonBox=QDialogButtonBox(QDialogButtonBox.Ok |QDialogButtonBox.Reset |QDialogButtonBox.Cancel)
        self.buttonBox=QDialogButtonBox(QDialogButtonBox.Ok |QDialogButtonBox.Cancel)
        # self.resets=QPushButton("Reset")
        # self.resets.clicked.connect(self.clearAll)
        # self.buttonBox.addButton(self.resets,QDialogButtonBox.ResetRole)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # self.buttonBox.clear.connect(self.clearAll)
        self.spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding,QSizePolicy.Minimum )

        self.saveDB=QCheckBox("Update to Database:")
        self.saveDB.stateChanged.connect(self.state_changed)

    def state_changed(self):
        self.save_db=True

    def accept(self):
        agency = self.agencyEntry.text()
        xchange = self.exchangeEntry.currentText()
        equity = self.equityEntry.text()
        buy_date = self.buy_dateEntry.text()
        buy_price = self.buy_priceEntry.text()
        tdate = self.trade_dateEntry.text()
        sdate = self.settle_dateEntry.text()
        price = self.trade_priceEntry.text()
        quantity = self.quantityEntry.text()
        unit_brock = self.unit_brockEntry.text()
        gst = self.gst_brockEntry.text()
        stt = self.stt_Entry.text()
        itax = self.it_Entry.text()
        comment = self.remarksEntry.text()
        self.output = agency, xchange, equity, buy_date,buy_price,tdate, sdate, price, quantity, unit_brock, gst, stt, itax, comment,self.save_db
        super(sold_stocks,self).accept()


    def get_inp(self):
        return self.output

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
        self.topLayout.addRow(QLabel("Buy Date: "),self.buy_dateEntry)
        self.topLayout.addRow(QLabel("Overall buy Price: "), self.buy_priceEntry)
        self.topLayout.addRow(QLabel("Trade Date: "),self.trade_dateEntry)
        self.topLayout.addRow(QLabel("Settlement Date: "),self.settle_dateEntry)
        self.topLayout.addRow(QLabel("Trade Price: "),self.trade_priceEntry)
        self.topLayout.addRow(QLabel("Quantity: "),self.quantityEntry)
        self.topLayout.addRow(QLabel("Brockerage per unit: "),self.unit_brockEntry)
        self.topLayout.addRow(QLabel("GST on Brockerage: "),self.gst_brockEntry)
        self.topLayout.addRow(QLabel("STT on Share: "),self.stt_Entry)
        self.topLayout.addRow(QLabel("Income Tax: "),self.it_Entry)
        self.topLayout.addRow(QLabel("Remarks: "),self.remarksEntry)

        self.bottomLayout.addWidget(self.buttonBox)
        self.topGroupBox.setLayout(self.topLayout)
        self.bottomGroupBox.setLayout(self.bottomLayout)
        self.mainTopLayout.addWidget(self.topGroupBox)
        self.mainTopLayout.addWidget(self.saveDB)
        self.mainTopLayout.addWidget(self.bottomGroupBox)
        self.mainLayout.addLayout(self.mainTopLayout)
        self.setLayout(self.mainLayout)



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
        # self.default_paramters()
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
        self.defltBtn = QPushButton("Default")
        self.defltBtn.clicked.connect(self.fill_defaults)

    def fill_defaults(self):
        # print('Hi')
        # print(self.brockerage)
        self.default_paramters()
        # print(self.unit_brockEntry.text(),self.gst_brockEntry.text(),self.stt_Entry.text())
        self.unit_brockEntry.setText(str(self.brockerage))
        self.gst_brockEntry.setText(str(self.gst))
        self.stt_Entry.setText(str(self.stt))
        self.it_Entry.setText(str(self.itax))


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

        self.bottomLayout.addWidget(self.defltBtn)
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
