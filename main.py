import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint,pyqtSlot
# from cStringIO import StringIO
# from PIL import Image


# import sqlite3

from Purchase.purchase import purchase_list
from sales import sold_list
from profit_list import  gain_shares
from db_management import check_db,set_defaults,add_stocks,saveStockDB
from transaction import show_transactions
from get_nse_data import get_recommendation

db_file = "MyInvestment.db"


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow,self).__init__(parent)
        self.setWindowTitle("My Investment")
        self.setGeometry(450,150,750,600)
        self.statusBar()
        self.UI()
        self.showMaximized()


    def UI(self):
        self.toolBar()
        self.tabWidgets()
        self.widgets()
        # self.layouts()

    def toolBar(self):
        tb=self.addToolBar("Tool Bar")
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        tb.addSeparator()
        addShare=QAction(QIcon(""),"New \n StockDB",self)
        addShare.triggered.connect(self.add_stockDB)
        addShare.setStatusTip("Adding newly purchased stock")
        addShare.setToolTip("Adding newly purchased stock")
        tb.addAction(addShare)
        tb.addSeparator()

        delShare = QAction(QIcon(""), "Delete \n StockDB", self)
        delShare.triggered.connect(self.del_shareDB)
        delShare.setStatusTip("Removing stock from list")
        delShare.setToolTip("Removing stock from list")
        tb.addAction(delShare)
        tb.addSeparator()

        delShare = QAction(QIcon(""), "Bank \nTransaction", self)
        delShare.triggered.connect(self.bank_transaction)
        delShare.setStatusTip("Removing stock from list")
        delShare.setToolTip("Removing stock from list")
        tb.addAction(delShare)
        tb.addSeparator()

        recShare = QAction(QIcon(""), "Stock \nAnalysis", self)
        recShare.triggered.connect(self.recommend_stock)
        recShare.setStatusTip("Analys stock")
        recShare.setToolTip("Analys stock for sell/buy")
        tb.addAction(recShare)
        tb.addSeparator()

        refreshShare = QAction(QIcon(""), "Refresh", self)
        refreshShare.triggered.connect(self.refresh)
        refreshShare.setStatusTip("loading latest  from database")
        refreshShare.setToolTip("loading latest  from database")
        tb.addAction(refreshShare)
        tb.addSeparator()

        defaultVal = QAction(QIcon(""), "Defaults", self)
        defaultVal.triggered.connect(self.default_setting)
        defaultVal.setStatusTip("default paramter settings")
        defaultVal.setToolTip("default paramter settings")
        tb.addAction(defaultVal)
        tb.addSeparator()

        # defaultVal = QAction(QIcon(""), "getCurrent", self)
        # defaultVal.triggered.connect(self.fetch_from_nse)
        # defaultVal.setStatusTip("default paramter settings")
        # defaultVal.setToolTip("default paramter settings")
        # tb.addAction(defaultVal)
        # tb.addSeparator()

    def recommend_stock(self):

         get_info=stock_recommendation()
         get_info.exec_()

    def bank_transaction(self):

        bank_data = show_transactions()
        bank_data.exec_()
        # pass


    def add_stockDB(self):
        agency=""
        invoice=""
        db_save=True
        add_inp = add_stocks(agency,db_save)

        if add_inp.exec_() == add_inp.Accepted:
            new_stock = add_inp.get_inp()
            invoice = saveStockDB(new_stock, invoice)
            # print("New : ",invoice,new_stock)


    def del_shareDB(self):
        # self.del_share=purchase_list.del_shareDB()
        # print(self.del_share)
        pass

    def default_setting(self):
        con, cur = check_db(db_file)
        self.defa=set_defaults(con,cur)


    def tabWidgets(self):
        self.tabs=QTabWidget()
        self.setCentralWidget( self.tabs)

    def refresh(self):
        self.LoadAll()
        # self.listAgency, self.stockDB = self.read_all_stocks()
        # self.List_of_agency=self.get_agency_list(self.listAgency)


    def widgets(self):

        # self.tabs.addTab(purchase_list(),"Investment")
        # self.tabs.addTab(sold_list(),"Sold")
        # self.tabs.addTab(gain_shares(),"Gain")
        self.LoadAll()

    def LoadAll(self):
        self.tabs.clear()
        self.tabs.addTab(purchase_list(), "Stocks")
        self.tabs.addTab(sold_list(), "Sold")
        self.tabs.addTab(gain_shares(), "Gain")


class stock_recommendation(QDialog):

    def __init__(self,parent=None):
        super(stock_recommendation, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Stock Recommendation")
        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(550, 350, 500, 370)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        fnt = QFont()
        fnt.setPointSize(13)
        fnt.setBold(True)
        fnt.setFamily("Arial")

        self.symbolLabel=QLabel("Equity symbol")
        self.symbolEntry=QLineEdit()
        self.intervalLabel=QLabel("Time Interval")
        self.intervalEntry=QLineEdit()
        self.timeEntry = QComboBox()
        # (1m, 1h, 1d, 1W, 1M)
        self.timeEntry.addItems(["Minute", "Hour","Day","Week","Month"])
        ns1 = "Month"
        indx = self.timeEntry.findText(ns1)
        self.timeEntry.setCurrentIndex(indx)

        self.analysBtn=QPushButton("Analys")
        self.analysBtn.clicked.connect(self.recommend)

        self.clearBtn = QPushButton("Clear")
        self.clearBtn.clicked.connect(self.clear_info)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setTextColor(QColor(0, 0, 255))
        self.output.setText("")

        self.symbolEntry.setText("COROMANDEL")
        self.intervalEntry.setText("1")

    def recommend(self):

        units={}
        units={"Minute":"m", "Hour":"h","Day":"d","Week":"W","Month":"M"}

        symbol=self.symbolEntry.text()
        delta0=self.intervalEntry.text()
        unit0=str(self.timeEntry.currentText())
        unit=units[unit0]
        delta=delta0+unit

        # print("*",symbol,delta)

        if symbol!="" and delta!="":

            try:
                # sys.stdout = sys.__stdout__
                reco=get_recommendation(symbol,delta)
                # print(sys.stdout)

                recom=(reco['RECOMMENDATION'])
                buy=(reco['BUY'])
                sell=(reco['SELL'])
                ntrl=(reco['NEUTRAL'])
                header="Equity: "+str(symbol),", TimeInterval:",str(delta0)+unit0
                self.output.append("--------------------------------start-------------------------------------------")
                self.output.append(str(header))
                self.output.setTextColor(QColor(0, 230, 255))
                self.output.append("   (Based on Oscillators & Moving Average Analysis)")
                self.output.setTextColor(QColor(0, 0, 255))
                v1="RECOMMENDATION : "+recom +" ( BUY="+str(buy)+", "+" SELL="+str(sell)+", "+" NEUTRAL="+str(ntrl)+")"
                self.output.append("-----------------------------------------------------------------------------")
                self.output.setTextColor(QColor(255, 0, 0))
                self.output.append(v1)
                self.output.setTextColor(QColor(0, 0, 255))
                self.output.append("---------------------------------end--------------------------------------------")
                self.output.append("")
            except:
                self.output.append("")
                self.output.append("Issues with symbol... \n Please check the input.")


        else:
            QMessageBox.information(self, "Info", "Fields can't be empty!!!")

    def clear_info(self):
        self.symbolEntry.setText("")
        self.intervalEntry.setText("")
        ns1 = "Day"
        indx = self.timeEntry.findText(ns1)
        self.timeEntry.setCurrentIndex(indx)
        self.output.clear()



    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QGridLayout()
        self.bottomLayout = QVBoxLayout()
        self.btnLayout=QGridLayout()

        # self.bottomLayout.addRow(self.symbolLabel, self.symbolEntry)
        self.topLayout.addWidget(self.symbolLabel, 0,0)
        self.topLayout.addWidget(self.intervalLabel, 0, 1)
        self.topLayout.addWidget(self.symbolEntry, 1,0)
        self.topLayout.addWidget(self.intervalEntry, 1, 1)
        self.topLayout.addWidget(self.timeEntry, 1, 2)
        # self.bottomLayout.addWidget(self.output)

        self.btnLayout.addWidget(self.analysBtn,0,0)
        self.btnLayout.addWidget(self.clearBtn,0,2)

        self.bottomLayout.addWidget(self.output)

        self.inputWidget=QWidget()
        self.inputWidget.setLayout(self.topLayout)
        self.outputWidget = QWidget()
        self.outputWidget.setLayout(self.bottomLayout)
        self.btnWidget=QWidget()
        self.btnWidget.setLayout(self.btnLayout)


        self.mainLayout.addWidget(self.inputWidget)
        self.mainLayout.addWidget(self.btnWidget)
        self.mainLayout.addWidget(self.outputWidget)

        self.setLayout(self.mainLayout)




def main():
    APP=QApplication(sys.argv)
    window=MyMainWindow()
    sys.exit(APP.exec_())

if __name__=='__main__':
    main()