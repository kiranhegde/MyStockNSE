from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint,pyqtSlot,QDateTime,QVariant

import ast
from collections import defaultdict
from db_management import read_db,check_db,add_stocks,update_stocks,saveStockDB,check_msg



class FloatDelegate(QStyledItemDelegate):
    def __init__(self, decimals, parent=None):
        super(FloatDelegate, self).__init__(parent=parent)
        self.nDecimals = decimals

    def displayText(self, value, locale):
        # https: // stackoverflow.com / questions / 651794 / whats - the - best - way - to - initialize - a - dict - of - dicts - in -python
        try:
            number = float(value)
        except ValueError:
            return super(FloatDelegate, self).displayText(value, locale)
        else:
            return locale.toString(number, format="f", precision=self.nDecimals)

class make_nested_dict0(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

# https: // stackoverflow.com / questions / 12009134 / adding - widgets - to - qtablewidget - pyqt
def set_column_sort(table,columnIndex):
    if table.rowCount() > 0:
        for i in range(table.rowCount()):
            # print("#",i)
            for j in columnIndex:
                value=(table.item(i,j)).text()
                item = QTableWidgetItem()

                # if type(value) == QDateTime:
                #     val=QDateTime.fromString(value,"ddmmyyyy")
                #     item.setData(Qt.DisplayRole, QVariant(val))
                #     print(i,j,val)
                # else:
                val = parse_str(value)
                item.setData(Qt.DisplayRole, val)

                table.setItem(i,j,item)
                table.setEditTriggers(QTableWidget.NoEditTriggers)
                # table.itemDoubleClicked.connect(self.edit_item)
                # print(j,value,type(value))

def table_sort_color(table):
    columnIndex1 = []
    columnIndex1.clear()
    columnIndex1 = [i for i in range(6, 16)]
    columnIndex1.insert(0, 0)
    set_column_sort(table, columnIndex1)
    table.sortByColumn(2, Qt.AscendingOrder)

    columnIndex = []
    columnIndex.clear()
    columnIndex = [2, 5, 14, 15]
    setColortoColumn(table, columnIndex, QColor(0, 255, 0))
    columnIndex.clear()
    table.setSortingEnabled(True)

def setColortoColumn(table, columnIndex, color):
    fnt = QFont()
    fnt.setPointSize(13)
    fnt.setBold(True)
    fnt.setFamily("Arial")

    if table.rowCount() > 0:
        for i in range(table.rowCount()):
            for j in columnIndex:
                # table.setItemDelegateForColumn(i,FloatDelegate(3))
                table.item(i, j).setBackground(color)
                table.item(i, j).setFont(fnt)



def make_nested_dict1():
    return defaultdict(make_nested_dict1)


def get_nested_dist_value(data, *args):
    # print(args)
    if args and data:
        element = args[0]
        if element:
            value = data.get(element)
            if len(args) == 1 :
                return value
            else :
                return get_nested_dist_value(value, * args[1:])

def parse_str(s):
   try:
      return ast.literal_eval(str(s))
   except:
      return


class purchase_list(QWidget):

    # def __init__(self,agency,stocks):
    def __init__(self):
        super().__init__()
        #self.setWindowTitle("Investment")
        #self.setGeometry(450,150,750,600)
        # self.agencyList=agency
        # self.stockList=stocks
        self.UI()
        self.show()


    def UI(self):
       self.widgets()
       # self.load_from_db()
       self.layouts()


    def widgets(self):
        # https: // programming.vip / docs / pyqt5 - quick - start - pyqt5 - basic - window - components.html
        self.refreshAll = QPushButton('Refresh')
        self.refreshAll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.refreshAll.setToolTip('Re-read database \n and calculate')
        self.save2db = QPushButton('SaveDB')
        self.save2db.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.save2db.setToolTip("Data updated will \n be saved Permanatly")
        self.calculate = QPushButton('Compute')
        self.calculate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.calculate.setToolTip("Recalculate to \n updated values")

        self.List_of_agency = QListWidget()
        agency,self.stockDB =read_db()
        self.List_of_agency=self.load_agency(agency)

        self.stockInfo=self.store_stocks()
        self.stockList = self.tabulateStocks()
        self.stockList.setSortingEnabled(True)

        self.stockList.installEventFilter(self)
        self.stockList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.stockList.customContextMenuRequested.connect(self.rightClickMenu)

        self.List_of_agency.itemDoubleClicked.connect(self.get_stocks)
        item = self.List_of_agency.item(0)
        self.List_of_agency.setCurrentItem(item)
        self.get_stocks(item)



    def load_agency(self,agency):
        # List of stock brocker agencies
        List_of_agency = QListWidget()
        for itm in agency:
            # print(itm)
            List_of_agency.addItem(itm)

        return List_of_agency


    def get_stocks(self, item):
        # https://www.tutorialexample.com/pyqt-table-add-row-data-dynamically-a-beginner-guide-pyqt-tutorial/

        agncy = item.text()
        self.stockList.setRowCount(0)

        stocks=get_nested_dist_value(self.stockInfo,agncy)

        for key, val in stocks.items():
            row_number = self.stockList.rowCount()
            self.stockList.setRowCount(row_number + 1)
            rowList = list(val)
            rowList.insert(0,key)
            row_data = tuple(rowList)
            for column_number, data in enumerate(row_data):
                self.stockList.setSortingEnabled(False)
                self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))


        self.stockList.setSortingEnabled(True)
        table_sort_color(self.stockList)


    def store_stocks(self):
        # stocksInfo = make_nested_dict1()
        stocksInfo=make_nested_dict0()
        for key, value in self.stockDB.items():
            for k1, val1 in value.items():
                rowList = list(val1)
                # rowList.insert(0, k1)
                price = rowList[4]
                Numb = rowList[5]
                brock = rowList[6]
                gst = rowList[7]
                stt = rowList[8]
                itax = rowList[9]
                comments = rowList[10]

                input_data = price, Numb, brock, gst, stt, itax
                output_data = self.stock_calc(input_data)
                rowList.insert(6, output_data[0])
                rowList.insert(11, output_data[1])
                rowList.insert(10, output_data[2])
                rowList.insert(13, output_data[3])
                rowList.insert(14, output_data[4])
                row_data = tuple(rowList)
                stocksInfo[key][k1] = row_data

        return stocksInfo


    def edit_item(self,item):
        items = self.stockList.currentItem()
        # print(item.text())
        print(len(items))
        # print(items.text())


    def stock_calc(self, input_data):
        price, Quant, Brockerage, gst, stt, itax = input_data
        # print( price,Quant,Brockerage,gst,stt,itax)
        price=parse_str(price)
        Quant=parse_str(Quant)
        Brockerage = parse_str(Brockerage) / 100.0
        gst = parse_str(gst) / 100.0
        stt = parse_str(stt) / 100.0
        itax = parse_str(itax) / 100.0

        unit_brockerage = price * Brockerage
        net_rate = price + unit_brockerage
        net_total = net_rate * Quant
        taxable_brockerage = unit_brockerage * Quant
        gst_brockerage = taxable_brockerage * gst
        stt_net_total = stt * net_total
        contr_amount = price * Quant
        net_amount = net_total + gst_brockerage + stt_net_total
        gst_stt_brk = net_amount - contr_amount
        actual_price = net_amount / Quant

        contr_amount = round(contr_amount, 3)
        net_amount = round(net_amount, 3)
        gst_stt_brk = round(gst_stt_brk, 3)
        actual_price = round(actual_price, 3)
        Zero_profit = round((actual_price + gst_stt_brk / Quant) * 1.0001, 3)

        return contr_amount, net_amount, gst_stt_brk, actual_price, Zero_profit

    def tabulateStocks(self):
        stockTable = QTableWidget()
        stockTable.setColumnCount(17)
        stockTable.setHorizontalHeaderItem(0, QTableWidgetItem("Reference \n Number"))
        stockTable.setHorizontalHeaderItem(1, QTableWidgetItem("Exchange"))
        stockTable.setHorizontalHeaderItem(2, QTableWidgetItem("Equity"))
        stockTable.setHorizontalHeaderItem(3, QTableWidgetItem("Trade Date"))
        stockTable.setHorizontalHeaderItem(4, QTableWidgetItem("Settlement \n Date"))
        stockTable.setHorizontalHeaderItem(5, QTableWidgetItem("Trade \n Price"))
        stockTable.setHorizontalHeaderItem(6, QTableWidgetItem("Quantity"))
        stockTable.setHorizontalHeaderItem(7, QTableWidgetItem("Contract \n Amount"))
        stockTable.setHorizontalHeaderItem(8, QTableWidgetItem("Broackerage \n (% per unit)"))
        stockTable.setHorizontalHeaderItem(9, QTableWidgetItem("GST(%) on \n Brockerage"))
        stockTable.setHorizontalHeaderItem(10, QTableWidgetItem("STT(%)"))
        stockTable.setHorizontalHeaderItem(11, QTableWidgetItem("GST+STT+ \n Brockerage"))
        stockTable.setHorizontalHeaderItem(12, QTableWidgetItem("Income \n tax(%)"))
        stockTable.setHorizontalHeaderItem(13, QTableWidgetItem("Net \n Amount"))
        stockTable.setHorizontalHeaderItem(14, QTableWidgetItem("Overall \n Price(per unit)"))
        stockTable.setHorizontalHeaderItem(15, QTableWidgetItem("Zero Profit \n Price(per unit)"))
        stockTable.setHorizontalHeaderItem(16, QTableWidgetItem("Remarks"))

        stockTable.setAlternatingRowColors(True)

        header = stockTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSelectionMode(QAbstractItemView.SingleSelection)
        header.setStretchLastSection(True)

        stockTable.setFont(QFont("Times", 9))
        stockTable.setSortingEnabled(False)

        # header.setStyleSheet( "QHeaderView::section { border-bottom: 5px solid black; }" )
        # header.setFrameStyle(QFrame.Box | QFrame.Plain)
        # header.setLineWidth(1)
        header.setFont(QFont("Times", 12))
        stockTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        stockTable.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # stockTable.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)


        return stockTable

    @pyqtSlot(QPoint)
    def rightClickMenu(self, pos):
        indexes = self.sender().selectedIndexes()
        mdlIdx = self.stockList.indexAt(pos)
        # print("position",pos)
        if not mdlIdx.isValid():
            return

        # self.case=self.stockList.itemFromIndex(mdlIdx)
        # print("Case :"+str(self.case.text()))
        row = self.stockList.currentRow()
        self.invoice = int(self.stockList.item(row, 0).text())
        # print("#"+str(self.invoice))

        self.menu = QMenu(self)
        remAct = QAction(QIcon(""), "Delete", self, triggered=self.delStock)
        # saveAct = QAction(QIcon(""), "Save", self, triggered=self.saveStock)
        addAct = QAction(QIcon(""), "Add Stock", self, triggered=self.new_share)
        # remAct.setStatusTip('Delete stock from database')
        updateAct = QAction(QIcon(""), 'Update', self, triggered=self.update_Stock)
        refreshAct = QAction(QIcon(""), 'Refresh', self, triggered=self.refresh_Stock)
        addAct = self.menu.addAction(addAct)
        editStk = self.menu.addAction(updateAct)
        # saveStk = self.menu.addAction(saveAct)
        remStk = self.menu.addAction(remAct)
        refrStk = self.menu.addAction(refreshAct)

        self.menu.exec_(self.sender().viewport().mapToGlobal(pos))

    # def addStock(self):
    #     agency = self.List_of_agency.currentItem().text()
    #     print("ag",agency)
    #     stk=new_stock(agency)
    #     stk.exec_()
        # print("adding")

    def new_share(self, agency=""):
        # con, cur = check_db(db_file)
        row_number=self.stockList.rowCount()
        self.stockList.setRowCount(row_number + 1)
        agency = self.List_of_agency.currentItem().text()
        print("ag",agency,self.stockList.currentRow())
        invoice=""

        if agency:
            add_inp = add_stocks(agency)
        else:
            add_inp = add_stocks()


        if add_inp.exec_() == add_inp.Accepted:
            new_row = add_inp.get_inp()
            print("New : ",new_row)
            new_row = list(add_inp.get_inp())
            save_db = new_row[12]
            del new_row[-1]

            if save_db:
                print(save_db)
                # check_msg()
                invoice=saveStockDB(new_row, invoice)

            print('New row:', row_number)
            print(invoice, new_row)

            # print(type(updated_row))
            # self.add_update_row(updated_row,row,invoice)
            price = new_row[5]
            Numb = new_row[6]
            brock = new_row[7]
            gst = new_row[8]
            stt = new_row[9]
            itax = new_row[10]

            # print( price, Numb, brock, gst, stt, itax)
            input_data = price, Numb, brock, gst, stt, itax
            output_data = self.stock_calc(input_data)
            new_row.insert(7, str(output_data[0]))
            new_row.insert(11, str(output_data[2]))
            new_row.insert(13, str(output_data[1]))
            new_row.insert(14, str(output_data[3]))
            new_row.insert(15, str(output_data[4]))
            # print('Updated row:',row_number)
            # print(invoice,updated_row)
            # print(output_data)
            new_row[0] = invoice
            # print(updated_row)

            for column_number, data in enumerate(new_row):
                self.stockList.setSortingEnabled(False)
                self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            table_sort_color(self.stockList)
        else:
            pass
            # Message box


    def delStock(self):
        print("del")

    def saveStock(self):
        print("save")

    def update_Stock(self,item):
        agency = self.List_of_agency.currentItem().text()
        if self.stockList.selectedItems():
            row_number = self.stockList.currentRow()
            invoice = self.stockList.item(row_number, 0).text()
            row_val=[]
            for i in range(1,self.stockList.columnCount()):
                row_val.append(self.stockList.item(row_number,i).text())

            row_val.insert(0,agency)
            # print(invoice, row_val)

            update_inp=update_stocks(row_val)
            if update_inp.exec_() == update_inp.Accepted:
            # if update_inp == update_inp.Accepted:
               updated_row=list(update_inp.get_inp())
               save_db = updated_row[12]
               del updated_row[-1]

               if save_db :
                  print(save_db)
                  # check_msg()

                  saveStockDB(updated_row,invoice)


               print('Updated row:', row_number)
               print(invoice, updated_row)

               # print(type(updated_row))
               # self.add_update_row(updated_row,row,invoice)
               price=updated_row[5]
               Numb=updated_row[6]
               brock=updated_row[7]
               gst=updated_row[8]
               stt=updated_row[9]
               itax=updated_row[10]


               # print( price, Numb, brock, gst, stt, itax)
               input_data = price, Numb, brock, gst, stt, itax
               output_data = self.stock_calc(input_data)
               updated_row.insert(7,str(output_data[0]))
               updated_row.insert(11,str(output_data[2]))
               updated_row.insert(13,str(output_data[1]))
               updated_row.insert(14,str(output_data[3]))
               updated_row.insert(15,str(output_data[4]))
               # print('Updated row:',row_number)
               # print(invoice,updated_row)
               # print(output_data)
               updated_row[0]=invoice
               # print(updated_row)

               for column_number, data in enumerate(updated_row):
                   self.stockList.setSortingEnabled(False)
                   self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))

               table_sort_color(self.stockList)

            else:
                pass
                # Message box

    # def add_update_row(self,row_data,row="",invoice=""):
    #
    #     rowList = list(row_data)
    #     if row != "" and invoice !="":
    #         row_number=row
    #         invoiceCode=invoice
    #     else:
    #        row_number = self.stockList.rowCount()
    #
    #
    #     rowList.insert(0, key)
    #     row_data = tuple(rowList)
    #
    #     for column_number, data in enumerate(row_data):
    #         self.stockList.setSortingEnabled(False)
    #         self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))



    def refresh_Stock(self):
        print("refresh")



    def layouts(self):
        self.mainLayout=QHBoxLayout()
        self.horizontalSplitter=QSplitter(Qt.Horizontal)
        self.leftVsplitter=QSplitter(Qt.Vertical)
        self.rightVsplitter=QSplitter(Qt.Vertical)

        self.buttons=QWidget()
        self.controlLayout=QHBoxLayout()
        # self.controlLayout.addStretch()
        self.controlLayout.addWidget(self.refreshAll)
        self.controlLayout.addWidget(self.calculate)
        self.controlLayout.addWidget(self.save2db)
        self.buttons.setLayout(self.controlLayout)

        self.leftLayout=QVBoxLayout()
        self.rightLayout=QVBoxLayout()
        self.leftTopGroupBox=QGroupBox("Agency List")
        self.rightTopGroupBox=QGroupBox("Stock List")
        # self.leftTop.addWidget(self.treeListAgency)
        # self.leftVsplitter.a
        self.leftLayout.addWidget(self.List_of_agency)
        self.rightLayout.addWidget(self.buttons,4)
        self.rightLayout.addWidget(self.stockList,96)
        self.leftTopGroupBox.setLayout(self.leftLayout)
        self.rightTopGroupBox.setLayout(self.rightLayout)

        self.leftVsplitter.addWidget(self.leftTopGroupBox)
        self.rightVsplitter.addWidget(self.rightTopGroupBox)

        self.horizontalSplitter.addWidget(self.leftVsplitter)
        self.horizontalSplitter.addWidget(self.rightVsplitter)
        self.horizontalSplitter.setStretchFactor(0, 10)
        self.horizontalSplitter.setStretchFactor(1, 90)
        self.horizontalSplitter.setContentsMargins(0, 0, 0, 0)
        self.horizontalSplitter.handle(0)

        self.mainLayout.addWidget(self.horizontalSplitter)
        self.setLayout(self.mainLayout)

