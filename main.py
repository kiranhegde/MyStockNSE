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
        con, cur = check_db(db_file)
        if agency:
            self.stk=add_stocks(con,cur,agency)
        else:
            self.stk = add_stocks(con, cur)
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
        # self.get_stock_list()
        # self.showStocks()

    def widgets(self):
        # print(self.listAgency)
        #
        # for key, value in self.stockDB.items():
        #     print(key)
        #     for k1, val1 in value.items():
        #         print(k1, val1)

        self.agencyList=QListWidget()
        self.listAgency, self.stockDB = self.read_all_stocks()
        self.List_of_agency = self.get_agency_list(self.listAgency)



        self.stockList=self.tabulateStocks()
        self.stockList.installEventFilter(self)
        self.stockList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.stockList.customContextMenuRequested.connect(self.rightClickMenu)

        item = self.List_of_agency.item(0)
        self.List_of_agency.setCurrentItem(item)
        self.showStocks(item)


        self.tabs.addTab(purchase_list(self.List_of_agency, self.stockList),"Investment")
        self.tabs.addTab(sold_list(),"Sold")
        self.tabs.addTab(gain_shares(),"Gain")

    def showStocks(self,item):
        # https://www.tutorialexample.com/pyqt-table-add-row-data-dynamically-a-beginner-guide-pyqt-tutorial/
        agncy=item.text()
        self.stockList.setFont(QFont("Times", 9))
        for i in reversed(range(self.stockList.rowCount())):
            self.stockList.removeRow(i)

        for key, value in self.stockDB.items():
            if key == agncy:
                for k1, val1 in value.items():
                    row_number = self.stockList.rowCount()
                    self.stockList.setRowCount(row_number + 1)

                    rowList=list(val1)
                    rowList.insert(0,k1)

                    price = rowList[5]
                    Numb = rowList[6]
                    brock = rowList[7]
                    gst = rowList[8]
                    stt = rowList[9]
                    itax = rowList[10]
                    comments=rowList[11]

                    input_data = price,Numb,brock,gst,stt,itax
                    output_data=self.stock_calc(input_data)
                    # output_data=list(output_data)
                    rowList.insert(7,output_data[0])
                    rowList.insert(12,output_data[1])
                    rowList.insert(11,output_data[2])
                    rowList.insert(14,output_data[3])
                    rowList.insert(15,output_data[4])
                    # print(type(rowList[15]))
                    # rowList.insert(15,comments)
                    row_data=tuple(rowList)
                    # print("->",row_data)
                    for column_number, data in enumerate(row_data):
                        self.stockList.setSortingEnabled(False)
                        self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                        self.stockList.setSortingEnabled(True)

        column_numbers=[2,14,15]

        # self.setColortoColumn(self.stockList,column_numbers, QColor(0, 255, 0))
        # self.setColortoColumn(self.stockList,2, QColor(0, 255, 0))
        # self.stockList.sortByColumn(11,Qt.AscendingOrder)
        # self.stockList.setSortingEnabled(True)
        # self.stockList.setSor


    def setColortoColumn(self,table, columnIndex, color):
        fnt = QFont()
        fnt.setPointSize(13)
        fnt.setBold(True)
        fnt.setFamily("Arial")

        for j in range(table.rowCount()):
            for i in columnIndex:
                # table.setItemDelegateForColumn(i,FloatDelegate(3))
                table.item(j, i).setBackground(color)
                table.item(j, i).setFont(fnt)



    def stock_calc(self,input_data):
        price,Quant,Brockerage,gst,stt,itax = input_data
        # print( price,Quant,Brockerage,gst,stt,itax)

        Brockerage = Brockerage/100.0
        gst=gst/100.0
        stt=stt/100.0
        itax=itax/100.0

        unit_brockerage=price*Brockerage
        net_rate =price+unit_brockerage
        net_total =net_rate*Quant
        taxable_brockerage=unit_brockerage*Quant
        gst_brockerage=taxable_brockerage*gst
        stt_net_total=stt*net_total
        contr_amount = price * Quant
        net_amount=net_total+gst_brockerage+stt_net_total
        gst_stt_brk=net_amount-contr_amount
        actual_price=net_amount/Quant

        contr_amount=round(contr_amount,3)
        net_amount=round(net_amount,3)
        gst_stt_brk=round(gst_stt_brk,3)
        actual_price=round(actual_price,3)
        Zero_profit = round((actual_price+gst_stt_brk/Quant)*1.0001,3)

        return contr_amount,net_amount,gst_stt_brk,actual_price,Zero_profit


    # def get_stock_list(self):
    #     con, cur = check_db(db_file)
    #     self.stockList.setFont(QFont("Times", 9))
    #     for i in reversed(range(self.stockList.rowCount())):
    #         self.stockList.removeRow(i)
    #
    #     stock = cur.execute("SELECT * FROM purchase")
    #     for all_row_data in stock:
    #         row_number = self.stockList.rowCount()
    #         self.stockList.insertRow(row_number)
    #         rowList = list(all_row_data[2:])
    #         rowList.insert(0, all_row_data[0])
    #         row_data = tuple(rowList)
    #
    #         for column_number, data in enumerate(row_data):
    #             self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def tabulateStocks(self):
        stockTable = QTableWidget()
        stockTable.setColumnCount(17)
        stockTable.setHorizontalHeaderItem(0,QTableWidgetItem("Reference \n Number"))
        stockTable.setHorizontalHeaderItem(1,QTableWidgetItem("Exchange"))
        stockTable.setHorizontalHeaderItem(2,QTableWidgetItem("Equity"))
        stockTable.setHorizontalHeaderItem(3,QTableWidgetItem("Trade Date"))
        stockTable.setHorizontalHeaderItem(4,QTableWidgetItem("Settlement \n Date"))
        stockTable.setHorizontalHeaderItem(5,QTableWidgetItem("Trade \n Price"))
        stockTable.setHorizontalHeaderItem(6,QTableWidgetItem("Quantity"))
        stockTable.setHorizontalHeaderItem(7, QTableWidgetItem("Contract \n Amount"))
        stockTable.setHorizontalHeaderItem(8,QTableWidgetItem("Broackerage \n (% per unit)"))
        stockTable.setHorizontalHeaderItem(9,QTableWidgetItem("GST(%) on \n Brockerage"))
        stockTable.setHorizontalHeaderItem(10,QTableWidgetItem("STT(%)"))
        stockTable.setHorizontalHeaderItem(11, QTableWidgetItem("GST+STT+ \n Brockerage"))
        stockTable.setHorizontalHeaderItem(12,QTableWidgetItem("Income \n tax(%)"))
        stockTable.setHorizontalHeaderItem(13,QTableWidgetItem("Net \n Amount"))
        stockTable.setHorizontalHeaderItem(14,QTableWidgetItem("Overall \n Price(per unit)"))
        stockTable.setHorizontalHeaderItem(15,QTableWidgetItem("Zero Profit \n Price(per unit)"))
        stockTable.setHorizontalHeaderItem(16,QTableWidgetItem("Remarks"))

        stockTable.setAlternatingRowColors(True)

        header=stockTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSelectionMode(QAbstractItemView.SingleSelection)
        header.setStretchLastSection(True)

        stockTable.setSortingEnabled(False)

        # header.setStyleSheet( "QHeaderView::section { border-bottom: 5px solid black; }" )
        # header.setFrameStyle(QFrame.Box | QFrame.Plain)
        # header.setLineWidth(1)
        header.setFont(QFont("Times",11))
        stockTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        stockTable.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        # stockTable.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
        return stockTable

    def get_agency_list(self,agency):
        self.agencyList.clear()
        self.agencyList.itemDoubleClicked.connect(self.showStocks)
        for itm in agency:
            self.agencyList.addItem(itm)

        return self.agencyList

    def stock_to_agency(self,item):
        print(item.text())



    @pyqtSlot(QPoint)
    def rightClickMenu(self, pos):
        indexes=self.sender().selectedIndexes()
        mdlIdx=self.stockList.indexAt(pos)
        # print("position",pos)
        if not mdlIdx.isValid():
            return

        # self.case=self.stockList.itemFromIndex(mdlIdx)
        # print("Case :"+str(self.case.text()))
        row=self.stockList.currentRow()
        self.invoice=int(self.stockList.item(row,0).text())
        # print("#"+str(self.invoice))

        self.menu = QMenu(self)
        remAct = QAction(QIcon(""),"Delete", self, triggered=self.delStock)
        saveAct = QAction(QIcon(""),"Save", self, triggered=self.saveStock)
        addAct = QAction(QIcon(""),"Add Stock", self, triggered=self.addStock)
        # remAct.setStatusTip('Delete stock from database')
        editAct = QAction(QIcon(""),'Edit', self, triggered=self.editStock)
        updateAct = QAction(QIcon(""),'Refresh', self, triggered=self.update_Stock)
        addAct = self.menu.addAction(addAct)
        # editStk = self.menu.addAction(editAct)
        saveStk = self.menu.addAction(saveAct)
        remStk = self.menu.addAction(remAct)
        upStk = self.menu.addAction(updateAct)

        self.menu.exec_(self.sender().viewport().mapToGlobal(pos))

    def addStock(self):
        agency=self.List_of_agency.currentItem().text()
        # print("ag",agency)
        self.new_share(agency)
        # print("adding")

    def saveStock(self):
        con, cur = check_db(db_file)
        items=self.List_of_agency.currentItem()
        agency = items.text()
        print(agency)



        if self.stockList.selectedItems():
            row=self.stockList.currentRow()
            id=self.stockList.item(row, 0).text()
            # agency=self.stockList.item(row, 1).text()
            exchange=self.stockList.item(row, 1).text()
            equity=self.stockList.item(row, 2).text()
            tradeDate=self.stockList.item(row, 3).text()
            settleDate=self.stockList.item(row, 4).text()
            price=self.stockList.item(row, 5).text()
            quantity=self.stockList.item(row, 6).text()
            brockerage=self.stockList.item(row, 8).text()
            gst=self.stockList.item(row, 9).text()
            stt=self.stockList.item(row, 10).text()
            itax=self.stockList.item(row, 12).text()
            comments=self.stockList.item(row, 16).text()


            # query=("SELECT * FROM purchase WHERE id=?")
            # stock=cur.execute(query,(invoice)).fetchone()
            mbox=QMessageBox.question(self,"Warning","Are you sure to save changes to stock with reference number "+id+" ?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query="UPDATE purchase SET agency=?,exchange=?,equity=?,trade_date=?,settle_date=?,trade_price=?,quantity=?,unit_brockerage=?,gst_brockerage=?,stt=?,income_tax=?,remarks=? WHERE id=?"
                    cur.execute(query,(agency,exchange,equity,tradeDate,settleDate,price,quantity,brockerage,gst,stt,itax,comments,id))
                    con.commit()
                    QMessageBox.information(self,"Info", "Stock with reference number "+id+" has been updated")

                    self.refresh()
                    # self.update_Stock()
                    self.showStocks(items)
                    # self.close()
                except:
                    QMessageBox.information(self, "Warning","Stock with reference number " + id + " has not been updated..")
        else:
            QMessageBox.information(self, "Warning !!!", "Please select the stock to be updated/saved")



    def delStock(self):
        con, cur = check_db(db_file)
        #print("Removing",self.invoice)
        if self.stockList.selectedItems():
            row=self.stockList.currentRow()
            invoice=self.stockList.item(row, 0).text()

            # query=("SELECT * FROM purchase WHERE id=?")
            # stock=cur.execute(query,(invoice)).fetchone()
            mbox=QMessageBox.question(self,"Warning","Are you sure to delete stock with reference number "+invoice+" ?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query="DELETE FROM purchase WHERE id=?"
                    cur.execute(query,(invoice,))
                    con.commit()
                    self.stockList.removeRow(row)
                    QMessageBox.information(self,"Info", "Stock with reference number "+invoice+" has been deleted..")
                    self.refresh()
                    # self.update_Stock()
                    # self.showStocks()
                    # self.close()
                except:
                    QMessageBox.information(self, "Warning","Stock with reference number " + invoice + " has not been deleted..")
        else:
            QMessageBox.information(self, "Warning !!!", "Please select the stock to be deleted")

    def editStock(self):
        print("Editing",self.invoice)

    def update_Stock(self):
        self.refresh()
        #print("Editing")

    def read_all_stocks(self):
        con, cur = check_db(db_file)

        stocksDB=QTreeWidget()
        stocksDB={}

        stock = cur.execute("SELECT * FROM purchase")
        for all_row_data in stock:
            agency=all_row_data[1]
            stocksDB[agency] =""

        ListAgency = []
        ListAgency.clear()
        for key in stocksDB.keys():
            ListAgency.append(key)

        # print(ListAgency)
        # print(stocksDB)
        # print(agency)

        for key in stocksDB.keys():
            stock = cur.execute("SELECT * FROM purchase")
            # print(key)
            refNo = {}
            for all_row_data in stock:
                agency = all_row_data[1]
                if key == agency:
                    ref = all_row_data[0]
                    refNo[ref] =""


            stocksDB[key]=refNo

        for key in stocksDB.keys():
            # print(key,val)
            stock = cur.execute("SELECT * FROM purchase")
            for all_row_data in stock:
                agency=all_row_data[1]
                if agency == key :
                    ref= all_row_data[0]
                    # stocksDB[agency] = ref
                    rowList=[]
                    rowList.clear()
                    rowList = list(all_row_data[2:])
                    # rowList.insert(0,all_row_data[0])
                    row_data = tuple(rowList)

                    # stkInfo.setdefault(ref,row_data)
                    # print("#",row_data)
                    # refNo[ref]=row_data

                    stocksDB[key][ref] = row_data

        # print(stocksDB.keys())
        # print(stocksDB.values())
        # for key, value in stocksDB.items():
        #     print(key)
        #     for k1, val1 in value.items():
        #         print(k1, val1)
        # exit()
        return ListAgency, stocksDB

class FloatDelegate(QStyledItemDelegate):
    def __init__(self, decimals, parent=None):
        super(FloatDelegate, self).__init__(parent=parent)
        self.nDecimals = decimals

    def displayText(self, value, locale):
        try:
            number = float(value)
        except ValueError:
            return super(FloatDelegate, self).displayText(value, locale)
        else:
            return locale.toString(number, format="f", precision=self.nDecimals)



    # def get_agency_stocks(self):



    # def layouts(self):
    #     ### Layouts  #####
    #     self.mainLayout=QHBoxLayout()
    #     self.leftLayout=QFormLayout()
    #     self.rightMainLayout=QVBoxLayout()
    #     self.rightTopLayout=QHBoxLayout()
    #     self.rightBottomLayout=QHBoxLayout()
    #     # Adding child layouts to main layout
    #     self.rightMainLayout.addLayout(self.rightTopLayout)
    #     self.rightMainLayout.addLayout(self.rightBottomLayout)
    #     self.mainLayout.addLayout(self.leftLayout,40)
    #     self.mainLayout.addLayout(self.rightMainLayout,60)
    #     # adding widgets to layouts
    #     # self.rightTopLayout.addWidget(self.employeeList)
    #     # self.rightBottomLayout.addWidget(self.btnNew)
    #     # self.rightBottomLayout.addWidget(self.btnUpdate)
    #     # self.rightBottomLayout.addWidget(self.btnDelete)
    #     # setting main window layout
    #     self.setLayout(self.mainLayout)






def main():
    APP=QApplication(sys.argv)
    window=MyMainWindow()
    sys.exit(APP.exec_())

if __name__=='__main__':
    main()