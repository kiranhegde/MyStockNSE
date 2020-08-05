import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint,pyqtSlot
# from PIL import Image


# import sqlite3

from purchase import purchase_list
from sales import sold_list
from profit_list import  gain_shares
from db_management import check_db,set_defaults,add_stocks,saveStockDB

db_file = "MyInvestment.db"


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow,self).__init__(parent)
        self.setWindowTitle("My Investment")
        self.setGeometry(450,150,750,600)
        self.statusBar()
        self.showMaximized()
        self.UI()


    def UI(self):
        self.toolBar()
        self.tabWidgets()
        self.widgets()
        # self.layouts()

    def toolBar(self):
        tb=self.addToolBar("Tool Bar")
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        tb.addSeparator()
        addShare=QAction(QIcon(""),"addStockDB",self)
        addShare.triggered.connect(self.add_stockDB)
        addShare.setStatusTip("Adding newly purchased stock")
        addShare.setToolTip("Adding newly purchased stock")
        tb.addAction(addShare)
        tb.addSeparator()

        delShare = QAction(QIcon(""), "delStockDB", self)
        delShare.triggered.connect(self.del_shareDB)
        delShare.setStatusTip("Removing stock from list")
        delShare.setToolTip("Removing stock from list")
        tb.addAction(delShare)
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
        self.tabs.addTab(purchase_list(), "Investment")
        self.tabs.addTab(sold_list(), "Sold")
        self.tabs.addTab(gain_shares(), "Gain")


def main():
    APP=QApplication(sys.argv)
    window=MyMainWindow()
    sys.exit(APP.exec_())

if __name__=='__main__':
    main()