import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint,pyqtSlot
# from PIL import Image


# import sqlite3

from purchase import purchase_list
from sales import sold_list
from profit_list import  gain_shares
from db_management import read_sales_db,read_stock_db,check_db,add_stocks,set_defaults

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
        addShare=QAction(QIcon(""),"addStock",self)
        addShare.triggered.connect(self.new_share)
        addShare.setStatusTip("Adding newly purchased stock")
        addShare.setToolTip("Adding newly purchased stock")
        tb.addAction(addShare)
        tb.addSeparator()

        delShare = QAction(QIcon(""), "delStock", self)
        delShare.triggered.connect(self.del_share)
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


    def new_share(self,agency=""):
        # con, cur = check_db(db_file)
        if agency:
            self.stk=add_stocks(agency)
        else:
            self.stk = add_stocks()
        # self.stck.exec_()


    def del_share(self):
        pass

    def default_setting(self):
        con, cur = check_db(db_file)
        self.defa=set_defaults(con,cur)


    def tabWidgets(self):
        self.tabs=QTabWidget()
        self.setCentralWidget( self.tabs)

    def refresh(self):
        self.listAgency, self.stockDB = self.read_all_stocks()
        self.List_of_agency=self.get_agency_list(self.listAgency)


    def widgets(self):

        self.tabs.addTab(purchase_list(),"Investment")
        self.tabs.addTab(sold_list(),"Sold")
        self.tabs.addTab(gain_shares(),"Gain")

def main():
    APP=QApplication(sys.argv)
    window=MyMainWindow()
    sys.exit(APP.exec_())

if __name__=='__main__':
    main()