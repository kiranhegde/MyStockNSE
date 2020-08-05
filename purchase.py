from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint,pyqtSlot,QDateTime,QVariant

import ast
from collections import defaultdict
from db_management import read_db,check_db,add_stocks,update_stocks,saveStockDB,delStockDB,show_stock_info
from get_nse_data import download_data_for_month



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

def delete_keys_from_dict(d, to_delete):
    if isinstance(to_delete, str):
        to_delete = [to_delete]
    if isinstance(d, dict):
        for single_to_delete in set(to_delete):
            if single_to_delete in d:
                del d[single_to_delete]
        for k, v in d.items():
            delete_keys_from_dict(v, to_delete)
    elif isinstance(d, list):
        for i in d:
            delete_keys_from_dict(i, to_delete)
    return d


# https: // stackoverflow.com / questions / 12009134 / adding - widgets - to - qtablewidget - pyqt
def set_column_sort(table,columnIndex):

    if table.rowCount() > 0:
        for i in range(table.rowCount()):
            # print("#",i)
            for j in columnIndex:

                if isinstance(table.item(i, j),type(None)):
                    pass
                else:
                    value = (table.item(i, j)).text()
                    # print("#"+str(j),value)

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
    # Sort column
    columnIndex1 = []
    columnIndex1.clear()
    columnIndex1 = [i for i in range(4,12)]
    columnIndex1.insert(0, 0)
    set_column_sort(table, columnIndex1)
    table.sortByColumn(2, Qt.AscendingOrder)

    # Color column background
    columnIndex = []
    columnIndex.clear()
    columnIndex = [2, 5,9,10]
    setColortoColumn(table, columnIndex, QColor(0, 255, 0))
    columnIndex.clear()
    columnIndex = [11,12]
    setColortoColumn(table, columnIndex, QColor(255, 0, 0))
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
                if isinstance(table.item(i, j), type(None)):
                    pass
                else:
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

        fnt = QFont("Arial", 13,QFont.Bold)
        # fnt.setPointSize(13)
        # fnt.setBold(True)
        # fnt.setFamily("Arial")
        # fnt.QColor(0, 255, 0)

        # self.totalInvestment = QLabel("0")
        # self.totalInvestment.setFont(fnt)
        # self.totalCharges = QLabel("0")
        # self.totalCharges.setFont(fnt)


        self.agencyGain = QLabel("0")
        self.agencyGain.setFont(fnt)

        self.agencyInvestmt=QLabel("0")
        self.agencyInvestmt.setFont(fnt)
        self.agencyCharges=QLabel("0")
        self.agencyCharges.setFont(fnt)

        self.agencyName = QLabel("AgencyName")
        self.agencyName.setFont(fnt)

        self.nse = QPushButton('NSE')
        self.nse.setGeometry(10,1,100,25)
        # self.nse.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.nse.clicked.connect(self.get_nse_data)
        self.nse.setToolTip('Get latest stock price \n from NSE')

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

        # self.List_of_agency.itemDoubleClicked.connect(self.get_stocks)
        self.List_of_agency.itemClicked.connect(self.get_stocks)
        # self.List_of_agency.currentItemChanged.connect(lambda:  self.agencyName.setText(self.List_of_agency.CurrentItem()))
        # self.List_of_agency.currentItemChanged.connect(self.get_agencyName)

        # abc=self.List_of_agency.currentItem()
        item = self.List_of_agency.item(0)
        self.List_of_agency.setCurrentItem(item)
        self.get_stocks(item)

    def get_nse_data(self):
        delta=0
        n_rows = self.stockList.rowCount()
        j=2
        jj=8
        k=10
        kk=11

        total_gain=0.0
        for i in range(n_rows):
            symbol=self.stockList.item(i,j).text()
            myPrice=self.stockList.item(i,jj).text()
            Numb=1 #self.stockList.item(i,jj).text()
            Quantity=self.stockList.item(i,5).text()
            brock=0.4
            gst=18.0
            stt=0.1
            itax=30.0
            # print(symbol)
            try:
                current=download_data_for_month(symbol,delta)

                price=current
                input_data = price, Numb, brock, gst, stt, itax
                output_data = self.stock_sale_calc(input_data)
                FinalPrice=output_data[1]

                print(symbol,":",Quantity,current,output_data)
                diff =0.0
                Total=0.0
                if current != 0:
                    # diff=parse_str(current)-parse_str(myPrice)
                    diff=parse_str(FinalPrice)-parse_str(myPrice)
                    diff= float("{:.2f}".format(diff))
                    Total=float(Quantity)*diff
                    Total=float("{:.2f}".format(Total))
                    total_gain=total_gain+Total

                self.stockList.setItem(i,k, QTableWidgetItem(str(current)))
                self.stockList.setItem(i,kk, QTableWidgetItem(str(diff)))
                self.stockList.setItem(i,kk+1, QTableWidgetItem(str(Total)))

            except:

                print(symbol,"not found")

        table_sort_color(self.stockList)

        self.agencyGain.setText(str(total_gain))




    def layouts(self):
        self.mainLayout=QHBoxLayout()
        self.horizontalSplitter=QSplitter(Qt.Horizontal)
        self.leftVsplitter=QSplitter(Qt.Vertical)
        self.rightVsplitter=QSplitter(Qt.Vertical)
        self.rightBottomLayout=QHBoxLayout()

        # self.buttons=QWidget()
        self.controlLayout=QHBoxLayout()
        # self.controlLayout.addStretch()
        self.controlLayout.addWidget(self.nse)
        # self.controlLayout.addWidget(self.refreshAll)
        # self.controlLayout.addWidget(self.calculate)
        # self.controlLayout.addWidget(self.save2db)
        # self.buttons.setLayout(self.controlLayout)

        # self.totalInvestment = QLabel("0")
        # self.totalCharges = QLabel("0")
        #
        # self.agencyInvestmt = QLabel("0")
        # self.agencyCharges = QLabel("0")

        self.agency_summaryLayout=QGridLayout()
        self.agency_summaryLayout.addWidget(self.agencyName,0,0)
        self.agency_summaryLayout.addWidget(QLabel('Total tax and brokerage : '),0,1)
        self.agency_summaryLayout.addWidget(self.agencyCharges,0,2)
        self.agency_summaryLayout.addWidget(QLabel('Total Investment : '), 0, 3)
        self.agency_summaryLayout.addWidget(self.agencyInvestmt, 0, 4)
        self.agency_summaryLayout.addWidget(QLabel('Total Gain[Rs] : '), 0, 5)
        self.agency_summaryLayout.addWidget(self.agencyGain, 0, 6)


        self.overallSummaryLayout=QGridLayout()
        self.overallSummaryLayout.addWidget(QLabel('Total tax and brokerage:'), 0, 0)
        # self.overallSummaryLayout.addWidget(QLineEdit(),0,1)
        self.overallSummaryLayout.addWidget(QLabel('Total Investment:'), 0, 1)
        # self.overallSummaryLayout.addWidget(QLineEdit(), 0, 3)

        # self.summaryGroupBox = QGroupBox(self.agencyName.text())
        self.summaryGroupBox = QGroupBox("Agency")
        self.summaryGroupBox.setLayout(self.agency_summaryLayout)

        self.overallsummaryGroupBox = QGroupBox('Total Investment')
        self.overallsummaryGroupBox.setLayout(self.overallSummaryLayout)

        self.buttonGroupBox=QGroupBox("Internet")
        self.buttonGroupBox.setLayout(self.controlLayout)

        self.rightBottomLayout.addWidget(self.summaryGroupBox,47)
        self.rightBottomLayout.addWidget(self.overallsummaryGroupBox,47)
        self.rightBottomLayout.addWidget(self.buttonGroupBox,6)
        self.rightBottomWidget=QWidget()
        self.rightBottomWidget.setLayout(self.rightBottomLayout)


        self.leftLayout=QVBoxLayout()
        self.rightLayout=QVBoxLayout()
        self.leftTopGroupBox=QGroupBox("Agency List")
        self.rightTopGroupBox=QGroupBox("Stock List")

        self.leftLayout.addWidget(self.List_of_agency)
        # self.rightLayout.addWidget(self.buttons,4)
        self.rightLayout.addWidget(self.stockList)
        self.leftTopGroupBox.setLayout(self.leftLayout)
        self.rightTopGroupBox.setLayout(self.rightLayout)

        self.leftVsplitter.addWidget(self.leftTopGroupBox)
        self.rightVsplitter.addWidget(self.rightTopGroupBox)
        # self.rightVsplitter.addWidget(self.summaryGroupBox)
        self.rightVsplitter.addWidget(self.rightBottomWidget)
        self.rightVsplitter.setStretchFactor(0,97)
        self.rightVsplitter.setStretchFactor(1,3)

        self.horizontalSplitter.addWidget(self.leftVsplitter)
        self.horizontalSplitter.addWidget(self.rightVsplitter)
        self.horizontalSplitter.setStretchFactor(0, 10)
        self.horizontalSplitter.setStretchFactor(1, 90)
        self.horizontalSplitter.setContentsMargins(0, 0, 0, 0)
        self.horizontalSplitter.handle(0)

        self.mainLayout.addWidget(self.horizontalSplitter)
        self.setLayout(self.mainLayout)




    #
    # @pyqtSlot()
    # def get_agencyName(self):
    #     item=self.List_of_agency.currentItem()
    #     self.agencyName.setText(item.text())

        # print(self.agencyName.text())
        # return self.agencyName


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

        # item = self.List_of_agency.currentItem()
        self.agencyName.setText(agncy)
        # self.summaryGroupBox.setTitle(agncy)
        # print(self.agencyName.text())

        stocks=get_nested_dist_value(self.stockInfo,agncy)

        # print(agncy,stocks)

        for key, val in stocks.items():
            row_number = self.stockList.rowCount()
            self.stockList.setRowCount(row_number + 1)
            rowList = list(val)
            rowList.insert(0,key)
            new_table=[]
            new_table=rowList[0:4]
            new_table.insert(5,rowList[5])
            new_table.insert(6,rowList[6])
            new_table.insert(7,rowList[11])
            new_table.insert(8,rowList[13])
            new_table.insert(9,rowList[14])
            new_table.insert(10,rowList[15])
            new_table.insert(11,0)
            new_table.insert(12,0)
            new_table.insert(13,0)
            new_table.insert(14,rowList[-1])

            # print(new_table)
            # exit()
            # row_data = tuple(rowList)
            row_data = tuple(new_table)
            # print(row_data)


            for column_number, data in enumerate(row_data):
                self.stockList.setSortingEnabled(False)
                self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))



        # print(type(self.stockList))
        # exit()

        self.stockList.setSortingEnabled(True)
        table_sort_color(self.stockList)

        output=self.calculate_sum(agncy)

        self.agencyInvestmt.setText(str(output[0]))
        self.agencyCharges.setText(str(output[1]))
        # self.agencyGain.setText(str(output[2]))
        # print(self.agencyCharges.text(), self.agencyInvestmt.text())


    # def stock_table_to_info(self,agency):
    #
    #     for key, val in stocks.items():
    #         row_number = self.stockList.rowCount()
    #         self.stockList.setRowCount(row_number + 1)
    #         rowList = list(val)
    #         rowList.insert(0, key)
    #         row_data = tuple(rowList)
    #
    #         for column_number, data in enumerate(row_data):
    #             self.stockList.setSortingEnabled(False)
    #             self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))


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
                output_data = self.stock_purchase_calc(input_data)
                rowList.insert(6, output_data[0])
                rowList.insert(11, output_data[1])
                rowList.insert(10, output_data[2])
                rowList.insert(13, output_data[3])
                rowList.insert(14, output_data[4])
                row_data = tuple(rowList)
                stocksInfo[key][k1] = row_data

        return stocksInfo




    def stock_purchase_calc(self, input_data):
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

    def stock_sale_calc(self, input_data):
        price, Quant, Brockerage, gst, stt, itax = input_data
        # print( price,Quant,Brockerage,gst,stt,itax)
        price = parse_str(price)
        Quant = parse_str(Quant)
        Brockerage = parse_str(Brockerage) / 100.0
        gst = parse_str(gst) / 100.0
        stt = parse_str(stt) / 100.0
        itax = parse_str(itax) / 100.0

        unit_brockerage = price * Brockerage
        net_rate = price - unit_brockerage
        net_total = net_rate * Quant
        taxable_brockerage = unit_brockerage * Quant
        gst_brockerage = taxable_brockerage * gst
        stt_net_total = stt * net_total
        contr_amount = price * Quant
        net_amount = net_total - gst_brockerage - stt_net_total
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
        stockTable.setColumnCount(14)
        stockTable.setHorizontalHeaderItem(0, QTableWidgetItem("Reference \n Number"))
        stockTable.setHorizontalHeaderItem(1, QTableWidgetItem("Exchange"))
        stockTable.setHorizontalHeaderItem(2, QTableWidgetItem("Equity"))
        stockTable.setHorizontalHeaderItem(3, QTableWidgetItem("Trade Date"))
        # stockTable.setHorizontalHeaderItem(4, QTableWidgetItem("Settlement \n Date"))
        stockTable.setHorizontalHeaderItem(4, QTableWidgetItem("Trade \n Price"))
        stockTable.setHorizontalHeaderItem(5, QTableWidgetItem("Quantity"))
        # stockTable.setHorizontalHeaderItem(7, QTableWidgetItem("Contract \n Amount"))
        # stockTable.setHorizontalHeaderItem(8, QTableWidgetItem("Brokerage \n (% per unit)"))
        # stockTable.setHorizontalHeaderItem(9, QTableWidgetItem("GST(%) on \n Brokerage"))
        # stockTable.setHorizontalHeaderItem(10, QTableWidgetItem("STT(%)"))
        stockTable.setHorizontalHeaderItem(6, QTableWidgetItem("GST+STT+ \n Brokerage"))
        # stockTable.setHorizontalHeaderItem(12, QTableWidgetItem("Income \n tax(%)"))
        stockTable.setHorizontalHeaderItem(7, QTableWidgetItem("Net \n Amount"))
        stockTable.setHorizontalHeaderItem(8, QTableWidgetItem("Overall \n unit Price"))
        stockTable.setHorizontalHeaderItem(9, QTableWidgetItem("Zero Profit \n unit Price"))
        stockTable.setHorizontalHeaderItem(10, QTableWidgetItem("Current\n unit Price"))
        stockTable.setHorizontalHeaderItem(11, QTableWidgetItem("Gain \n per unit "))
        stockTable.setHorizontalHeaderItem(12, QTableWidgetItem("Overall \n Gain "))
        stockTable.setHorizontalHeaderItem(13, QTableWidgetItem("Remarks"))
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
        # self.invoice = int(self.stockList.item(row, 0).text())
        # print("#"+str(self.invoice))

        self.menu = QMenu(self)
        remAct = QAction(QIcon(""), "Delete", self, triggered=self.delStock)
        dbremAct = QAction(QIcon(""), "DeleteDB", self, triggered=self.del_shareDB)
        # saveAct = QAction(QIcon(""), "Save", self, triggered=self.saveStock)
        addAct = QAction(QIcon(""), "Add Stock", self, triggered=self.new_share)
        # remAct.setStatusTip('Delete stock from database')
        updateAct = QAction(QIcon(""), 'Update', self, triggered=self.update_Stock)
        # refreshAct = QAction(QIcon(""), 'Refresh', self, triggered=self.refresh_Stock)
        dispAct = QAction(QIcon(""), 'Show', self, triggered=self.show_Stock)
        addAct = self.menu.addAction(addAct)
        editStk = self.menu.addAction(updateAct)
        dispStk = self.menu.addAction(dispAct)
        # saveStk = self.menu.addAction(saveAct)
        remStk = self.menu.addAction(remAct)
        dbremStk = self.menu.addAction(dbremAct)
        # refrStk = self.menu.addAction(refreshAct)


        self.menu.exec_(self.sender().viewport().mapToGlobal(pos))


    def show_Stock(self):

        if self.stockList.selectedItems():
            agency = self.List_of_agency.currentItem().text()
            row_number = self.stockList.currentRow()
            invoice = self.stockList.item(row_number, 0).text()
            # print(invoice)
            stock_data =list(self.get_stock_info(agency,invoice))
            # print(stock_data)

            if invoice:
                showInfo = show_stock_info(invoice,stock_data)
                showInfo.exec_()
            else:
                pass

    def get_stock_info(self,agency,invoice):


        if invoice:
            invoice=parse_str(invoice)
            # agency=parse_str(agency)
            agencyStock = get_nested_dist_value(self.stockInfo,agency)
            searchCase = get_nested_dist_value(agencyStock,invoice)
            #
            # print(type(invoice), type(stocks))
            # print(agencyStock)
            # print(searchCase)
            # exit()
            # for key, val in stocks.items():
            #     rowList = list(val)
            #     rowList.insert(0, key)
            #     row_data = tuple(rowList)

                #
                # for column_number, data in enumerate(row_data):
                #     self.stockList.setSortingEnabled(False)
                #     self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            # print(row_data)
            return searchCase




    def del_shareDB(self):
        agency = self.List_of_agency.currentItem().text()
        invoice=""
        if self.stockList.selectedItems():
            row_number = self.stockList.currentRow()
            invoice = self.stockList.item(row_number, 0).text()
            agency = str(agency)
            delShareDB=delStockDB(invoice)
            mbox = QMessageBox.question(self, "Delete from table ?", "Display table still showing stock with  ID: "+ str(invoice), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    row_number = self.stockList.currentRow()
                    invoice = self.stockList.item(row_number, 0).text()
                    agency = str(agency)
                    invoice = parse_str(invoice)
                    del (self.stockInfo[agency][invoice])
                    self.stockList.removeRow(row_number)
                    QMessageBox.information(self, "Info", "Stock with reference number " + str(invoice) + " has been deleted from table")
                except:
                    QMessageBox.information(self, "Warning", "Stock with reference number " + str(invoice) + " has not been deleted from table")

        item = self.List_of_agency.currentItem()
        self.get_stocks(item)


    def delStock(self):
        agency = self.List_of_agency.currentItem().text()
        if self.stockList.selectedItems():
            row_number = self.stockList.currentRow()
            invoice = self.stockList.item(row_number, 0).text()
            agency = str(agency)
            invoice = parse_str(invoice)
            del (self.stockInfo[agency][invoice])
            self.stockList.removeRow(row_number)

            item = self.List_of_agency.currentItem()
            self.get_stocks(item)


    def new_share(self, agency=""):
        # con, cur = check_db(db_file)
        row_number=self.stockList.rowCount()
        self.stockList.setRowCount(row_number + 1)
        agency = self.List_of_agency.currentItem().text()
        # print("ag",agency,self.stockList.currentRow())
        invoice="0"

        if agency:
            add_inp = add_stocks(agency)
        else:
            add_inp = add_stocks()


        if add_inp.exec_() == add_inp.Accepted:
            new_row = add_inp.get_inp()
            # print("New : ",new_row)
            new_row = list(add_inp.get_inp())
            save_db = new_row[12]
            del new_row[-1]

            if save_db:
                # print(save_db)
                # check_msg()
                invoice=saveStockDB(new_row)
            #
            # print('New row:', row_number)
            # print(invoice, new_row)

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
            output_data = self.stock_purchase_calc(input_data)
            new_row.insert(7, str(output_data[0]))
            new_row.insert(11, str(output_data[2]))
            new_row.insert(13, str(output_data[1]))
            new_row.insert(14, str(output_data[3]))
            new_row.insert(15, str(output_data[4]))


            # print('Updated row:',row_number)
            # print(invoice,updated_row)
            # print(output_data)
            # new_row[0] = invoice
            # print(new_row)
            for i in range(5, len(new_row) - 1):
                data = new_row[i]
                # print(i,type(data),type(parse_str(data)),data )
                new_row[i] = parse_str(data)

            agency = str(agency)
            inv = parse_str(invoice)
            # data1 = self.stockInfo[agency][inv]
            update1 = new_row[1:]

            self.stockInfo[agency][inv] = tuple(update1)
            data2 = self.stockInfo[agency][inv]

            # print(invoice)
            # # print(data1)
            # print(update1)
            # print(data2)
            # print(new_row)
            #
            # exit()

            # for column_number, data in enumerate(new_row):
            #     self.stockList.setSortingEnabled(False)
            #     self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            # table_sort_color(self.stockList)
        else:
            pass
            # Message box

        item = self.List_of_agency.currentItem()
        self.get_stocks(item)



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
                  # print(save_db)
                  # check_msg()
                  id=saveStockDB(updated_row,invoice)


               # print('Updated row:', row_number)
               # print(invoice, updated_row)

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
               output_data = self.stock_purchase_calc(input_data)
               updated_row.insert(7,output_data[0])
               updated_row.insert(11,output_data[2])
               updated_row.insert(13,output_data[1])
               updated_row.insert(14,output_data[3])
               updated_row.insert(15,output_data[4])
               # print('Updated row:',row_number)
               # print(invoice,updated_row)
               # print(output_data)
               for i in range(5,len(updated_row)-1):
                   data=updated_row[i]
                   # print(i,type(data),type(parse_str(data)),data )
                   updated_row[i]=parse_str(data)

               agency = str(agency)
               inv = parse_str(invoice)
               data1 = self.stockInfo[agency][inv]
               update1=updated_row[1:]
               self.stockInfo[agency][inv]=tuple(update1)
               data2 = self.stockInfo[agency][inv]

               updated_row[0] = invoice

               # print(invoice)
               # print(data1)
               # print(update1)
               # print(data2)
               # print(updated_row)
               #
               # exit()

               # for column_number, data in enumerate(updated_row):
               #     self.stockList.setSortingEnabled(False)
               #     self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))
               #
               # table_sort_color(self.stockList)

            else:
                pass
                # Message box

            item = self.List_of_agency.currentItem()
            self.get_stocks(item)

    def calculate_total_gain(self):
        pass


    def calculate_sum(self,agency=""):

        currentAgency=self.stockInfo[agency]
        net_invetment=0.0
        net_extra=0.0
        # net_gain=0.0
        for key,value in  currentAgency.items():
            value=list(value)
            # print("#",value)
            net_invetment=net_invetment+value[12]
            # net_gain=net_gain+value[13]
            net_extra=net_extra+value[10]

            # print(key,value)
        agencyInvestmt="{:.{}f}".format(net_invetment, 3)
        agencyCharges="{:.{}f}".format(net_extra, 3)
        # agencyGain="{:.{}f}".format(net_gain, 3)
        # self.totalInvestment="{:.{}f}".format(net_invetment, 3)
        # print(net_invetment,net_extra)


        return agencyInvestmt,agencyCharges


    def refresh_Stock(self):
        print("refresh")



