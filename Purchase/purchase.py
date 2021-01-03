from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint,pyqtSlot
from babel.numbers import format_currency

import ast
from collections import defaultdict
from db_management import read_db,add_stocks,update_stocks,saveStockDB,delStockDB,\
    show_stock_info,gen_id,sold_stocks,saveStockSaleDB,average_stocks
from get_nse_data import download_data_for_month,get_latest_price



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
                    # if j ==12:
                    #     print(i,j,val,type(val))

                    table.setItem(i,j,item)
                    table.setEditTriggers(QTableWidget.NoEditTriggers)
                    # table.itemDoubleClicked.connect(self.edit_item)
                    # print(j,value,type(value))

def table_sort_color(table,sortIdx,RedIdx,GreenIdx,sortColNo=""):

    set_column_sort(table, sortIdx)
    if sortColNo != "":
        table.sortByColumn(sortColNo, Qt.AscendingOrder)
    else:
        table.sortByColumn(2, Qt.AscendingOrder)

    setColortoColumn(table, GreenIdx, QColor(0, 255, 0))
    setColortoColumn(table, RedIdx, QColor(255, 0, 0))
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
      return str(s)


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
        self.table_header_info()
        self.display_color_sort()
        self.widgets()
        # self.load_from_db()
        self.layouts()

    def table_header_info(self):
        self.headerName = []
        self.headerName.append("Reference \n Number")  # 0
        self.headerName.append("Exchange")  # 1
        self.headerName.append("Equity")  # 2
        self.headerName.append("Trade Date")  # 3
        self.headerName.append("Settlement \n Date")  # 4
        self.headerName.append("Trade \n Price")  # 5
        self.headerName.append("Quantity")  # 6
        self.headerName.append("Contract \n Amount")  # 7
        self.headerName.append("Brokerage \n (% per unit)")  # 8
        self.headerName.append("GST(%) on \n Brokerage)")  # 9
        self.headerName.append("STT(%))")  # 10
        self.headerName.append("GST+STT+ \n Brokerage")  # 11
        self.headerName.append("Income \n tax(%)")  # 12
        self.headerName.append("Net \n Amount")  # 13
        self.headerName.append("Overall \n unit Price")  # 14
        self.headerName.append("Zero Profit \n unit Price")  # 15
        self.headerName.append("Current\n unit Price")  # 16
        self.headerName.append("Gain \n per unit")  # 17
        self.headerName.append("Overall \n Gain")  # 18
        self.headerName.append("Remarks")  # 19
        self.col_N = 20
        self.index_disp = []
        self.index_disp = [0, 1, 2, 3, 5, 6, 11, 13, 14, 15, 16, 17, 18, 19]
        self.col_disp = len(self.index_disp)
        self.db_index=[]
        self.db_index=['id','agency','exchange','equity','trade_date','settle_date','trade_price','quantity','unit_brokerage','gst','stt','itax','remarks']

        self.stock_key=[]
        self.stockInfo_key=['exchange', 'equity', 'Tdate', 'Sdate', 'Tprice', 'quantity', 'ContAmount', 'unit_brokerage', 'gst', 'stt', 'gst_stt_br', 'itax',
                            'NetAmount', 'Oprice', 'Zprice', 'remarks', 'invoice' ]

        self.stock_disp_key=[]
        self.stock_disp_key = ['invoice','exchange', 'equity', 'Tdate', 'Tprice', 'quantity','gst_stt_br', 'NetAmount', 'Oprice', 'Zprice', 'current_price',
                               'unit_gain', 'total_gain','remarks']

    def display_color_sort(self):
        self.sort_colmn_by_index = []
        self.sort_colmn_by_index = [i for i in range(4, 12)]
        self.sort_colmn_by_index.insert(0, 0)
        self.Red_colmn_by_index = []
        self.Red_colmn_by_index = [11, 12]
        self.Green_colmn_by_index = []
        self.Green_colmn_by_index = [2, 4, 5, 9, 10]



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
        self.nse_delta_history=QLineEdit()
        self.nse_delta_history.setAlignment(Qt.AlignCenter)
        self.nse_delta_history.setText("0")
        self.nse_days=QLabel("Days")

        self.nse_delta_history.setToolTip("number of days from today \n (0-for only today)")

        # https: // programming.vip / docs / pyqt5 - quick - start - pyqt5 - basic - window - components.html

        # self.refreshAll = QPushButton('Refresh')
        # self.refreshAll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.refreshAll.setToolTip('Re-read database \n and calculate')
        # self.save2db = QPushButton('SaveDB')
        # self.save2db.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.save2db.setToolTip("Data updated will \n be saved Permanatly")
        # self.calculate = QPushButton('Compute')
        # self.calculate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.calculate.setToolTip("Recalculate to \n updated values")

        self.List_of_agency = QListWidget()
        agency,self.stockDB =read_db()
        self.List_of_agency=self.load_agency(agency)

        self.stocksInfoz=self.store_stocks()
        # for k1,v1 in self.stocksInfoz.items():
        #     print(k1)
        #     for k2,v2 in v1.items():
        #         print(k2,v2)

        # exit()


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

        # print("1",self.stocksInfoz)
        self.get_stocks(item)

    def get_nse_data(self):
        delta=parse_str(self.nse_delta_history.text())
        n_rows = self.stockList.rowCount()
        j=2
        jj=8
        k=10
        kk=11

        total_gain=0.0
        for i in range(n_rows):
            ref=self.stockList.item(i,0).text()
            symbol=self.stockList.item(i,j).text()
            myPrice=self.stockList.item(i,jj).text()
            Numb=1 #self.stockList.item(i,jj).text()
            Quantity=self.stockList.item(i,5).text()
            brock=0.4
            gst=18.0
            stt=0.1
            itax=10.0
            # print(symbol)

            try:
                # current=download_data_for_month(symbol,delta)
                current=get_latest_price(symbol+".NS")
                price=current
                input_data = price, Numb, brock, gst, stt, itax
                output_data = self.stock_sale_calc(input_data)
                FinalPrice=output_data[1]

                # print(symbol,":",Quantity,current,output_data)
                print(symbol,":","#"+str(Quantity),current)
                diff =0.0
                Total=0.0
                if current != 0:
                    # diff=parse_str(current)-parse_str(myPrice)
                    diff=parse_str(FinalPrice)-parse_str(myPrice)
                    diff= float("{:.2f}".format(diff))
                    Total=float(Quantity)*diff
                    Total=float("{:.2f}".format(Total))
                    total_gain=total_gain+Total

                Item1 = QTableWidgetItem()
                current = parse_str(current)
                Item1.setData(Qt.DisplayRole, current)

                Item2 = QTableWidgetItem()
                diff = parse_str(diff)
                Item2.setData(Qt.DisplayRole, diff)

                Item3 = QTableWidgetItem()
                Total = parse_str(Total)
                Item3.setData(Qt.DisplayRole, Total)
                self.stockList.setSortingEnabled(False)
                self.stockList.setItem(i,k, Item1)
                self.stockList.setItem(i,kk, Item2)
                self.stockList.setItem(i,kk+1, Item3)

            except:
                print(symbol,"not found")


        self.display_color_sort()
        table_sort_color(self.stockList,self.sort_colmn_by_index,self.Red_colmn_by_index,self.Green_colmn_by_index,12)
        self.stockList.setSortingEnabled(True)

        self.agencyGain.setText(format_currency(total_gain,'INR',locale='en_IN'))
        self.agencyGain.setStyleSheet('color: blue')

        # for i in range(n_rows):
        #     var=self.stockList.item(i,12).text()
        #     print(i,j,var,type(var))



    def layouts(self):
        self.mainLayout=QHBoxLayout()
        self.horizontalSplitter=QSplitter(Qt.Horizontal)
        self.leftVsplitter=QSplitter(Qt.Vertical)
        self.rightVsplitter=QSplitter(Qt.Vertical)
        self.rightBottomLayout=QHBoxLayout()

        # self.buttons=QWidget()
        self.controlLayout=QHBoxLayout()
        # self.controlLayout.addStretch()
        self.controlLayout.addWidget(self.nse_delta_history)
        self.controlLayout.addWidget(self.nse_days)
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
        # print(type(agncy))
        self.stockList.setRowCount(0)
        self.agencyName.setText(agncy)
        self.agencyGain.setText("0")

        stockz=get_nested_dist_value(self.stocksInfoz,agncy)
        one_stock = make_nested_dict0()
        one_stock.clear()

        for key, val in stockz.items():
            row_number = self.stockList.rowCount()
            self.stockList.setRowCount(row_number + 1)
            one_stock=val
            # print(key,one_stock)
            one_stock['invoice'] = key
            one_stock['current_price'] = 0.0
            one_stock['unit_gain'] = 0.0
            one_stock['total_gain'] = 0.0

            new_table = []
            new_table.clear()
            for info in self.stock_disp_key:
                data = one_stock[info]
                new_table.append(data)

            new_table = tuple(new_table)
            self.add_update_disp(row_number,new_table,agncy,False)

        self.stockList.setSortingEnabled(True)
        # table_sort_color(self.stockList)
        table_sort_color(self.stockList, self.sort_colmn_by_index, self.Red_colmn_by_index, self.Green_colmn_by_index)

        self.calculate_sum()

        return

    def add_update_disp(self,row,row_data,agency,do_sum):

        for column_number, data in enumerate(row_data):
            # print(data,type(parse_str(data)))
            newItem = QTableWidgetItem()
            data=parse_str(data)
            newItem.setData(Qt.DisplayRole,data)
            self.stockList.setSortingEnabled(False)
            self.stockList.setItem(row, column_number,newItem)
            # print(data,type(data))
        # exit()
        self.stockList.setSortingEnabled(True)

        if do_sum:
           self.calculate_sum(agency)

    def store_stocks(self):

        stocksInfoz=make_nested_dict0()
        stocksInfoz.clear()

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

                stocksInfoz[key][k1]['exchange']=rowList[0]
                stocksInfoz[key][k1]['equity']=rowList[1]
                stocksInfoz[key][k1]['Tdate']=rowList[2]
                stocksInfoz[key][k1]['Sdate']=rowList[3]
                stocksInfoz[key][k1]['Tprice']=rowList[4]
                stocksInfoz[key][k1]['quantity']=rowList[5]
                stocksInfoz[key][k1]['ContAmount']=rowList[6]
                stocksInfoz[key][k1]['unit_brokerage']=rowList[7]
                stocksInfoz[key][k1]['gst']=rowList[8]
                stocksInfoz[key][k1]['stt']=rowList[9]
                stocksInfoz[key][k1]['gst_stt_br']=rowList[10]
                stocksInfoz[key][k1]['itax']=rowList[11]
                stocksInfoz[key][k1]['NetAmount']=rowList[12]
                stocksInfoz[key][k1]['Oprice']=rowList[13]
                stocksInfoz[key][k1]['Zprice']=rowList[14]
                stocksInfoz[key][k1]['remarks']=rowList[15]

        return stocksInfoz


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
        if Quant == 0:
            Quant=1
        actual_price = net_amount / Quant

        contr_amount = round(contr_amount, 3)
        net_amount = round(net_amount, 3)
        gst_stt_brk = round(gst_stt_brk, 3)
        actual_price = round(actual_price, 3)
        Zero_profit = round((actual_price + gst_stt_brk / Quant) * 1.0001, 3)

        return contr_amount, net_amount, gst_stt_brk, actual_price, Zero_profit

    def stock_sale_calc(self, input_data):
        price, Quant, Brockerage, gst, stt, itax = input_data
        # print('price,Quant,Brockerage,gst,stt,itax')
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
        gst_stt_brk = taxable_brockerage+gst_brockerage+stt_net_total
        actual_price = net_amount / Quant

        contr_amount = round(contr_amount, 3)
        net_amount = round(net_amount, 3)
        gst_stt_brk = round(gst_stt_brk, 3)
        actual_price = round(actual_price, 3)
        Zero_profit = round((actual_price + gst_stt_brk /float(Quant)), 3)

        print('contr_amount, net_amount, gst_stt_brk, actual_price, Zero_profit')
        print(contr_amount, net_amount, gst_stt_brk, actual_price, Zero_profit)

        return contr_amount, net_amount, gst_stt_brk, actual_price, Zero_profit



    def tabulateStocks(self):

        stockTable = QTableWidget()
        stockTable.setColumnCount(self.col_disp)
        j=0
        for i in self.index_disp:
            hname=str(self.headerName[i])
            stockTable.setHorizontalHeaderItem(j, QTableWidgetItem(hname))
            j=j+1

        stockTable.setAlternatingRowColors(True)
        header = stockTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSelectionMode(QAbstractItemView.SingleSelection)
        header.setStretchLastSection(True)
        stockTable.setFont(QFont("Times", 9))
        stockTable.setSortingEnabled(False)
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
        soldAct = QAction(QIcon(""), 'Sold', self, triggered=self.stock_sold)
        avgAct = QAction(QIcon(""), 'Average', self, triggered=self.stock_avg)
        addAct = self.menu.addAction(addAct)
        editStk = self.menu.addAction(updateAct)
        dispStk = self.menu.addAction(dispAct)
        avgStk = self.menu.addAction(avgAct)
        # saveStk = self.menu.addAction(saveAct)
        remStk = self.menu.addAction(remAct)
        dbremStk = self.menu.addAction(dbremAct)
        # refrStk = self.menu.addAction(refreshAct)
        self.menu.addSeparator()
        soldStk = self.menu.addAction(soldAct)

        self.menu.exec_(self.sender().viewport().mapToGlobal(pos))

    def stock_avg(self):

        if self.stockList.selectedItems():
            agency = self.List_of_agency.currentItem().text()
            row_number = self.stockList.currentRow()
            invoice = int(self.stockList.item(row_number, 0).text())
            one_stock = self.get_stock_info(agency, invoice)

            stock_data = []
            stock_data.clear()
            stock_data.append(one_stock["exchange"])
            stock_data.append(one_stock["equity"])
            stock_data.append(one_stock["Tdate"])
            stock_data.append(one_stock["Tprice"])
            stock_data.append(one_stock["quantity"])
            stock_data.append(one_stock["Oprice"])

            if invoice:
                # print(stock_data)
                showInfo = average_stocks(stock_data)
                showInfo.exec_()
            else:
                pass



    def show_Stock(self):

        if self.stockList.selectedItems():
            agency = self.List_of_agency.currentItem().text()
            row_number = self.stockList.currentRow()
            invoice = int(self.stockList.item(row_number, 0).text())
            one_stock =self.get_stock_info(agency,invoice)

            stock_data = []
            stock_data.clear()
            stock_data.append(one_stock["exchange"])
            stock_data.append(one_stock["equity"])
            stock_data.append(one_stock["Tdate"])
            stock_data.append(one_stock["Sdate"])
            stock_data.append(one_stock["Tprice"])
            stock_data.append(one_stock["quantity"])
            stock_data.append(one_stock["ContAmount"])
            stock_data.append(one_stock["unit_brokerage"])
            stock_data.append(one_stock["gst"])
            stock_data.append(one_stock["stt"])
            stock_data.append(one_stock["itax"])
            # stock_data.append(one_stock["remarks"])

            if invoice:
                showInfo = show_stock_info(invoice,stock_data)
                showInfo.exec_()
            else:
                pass

    def get_stock_info(self,agency,invoice):

        if invoice != "":
            invoice=int(invoice)
            agency=str(agency)
            agencyStock = get_nested_dist_value(self.stocksInfoz,agency)
            searchCase = get_nested_dist_value(agencyStock,invoice)

            # print("--", searchCase)

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
                    del (self.stocksInfoz[agency][invoice])
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
            invoice = int(self.stockList.item(row_number, 0).text())
            # agency = str(agency)
            # invoice = int(invoice)
            del (self.stocksInfoz[agency][invoice])
            self.stockList.removeRow(row_number)

            item = self.List_of_agency.currentItem()
            self.get_stocks(item)







    def new_share(self, agency=""):
        # con, cur = check_db(db_file)

        agency = parse_str(self.List_of_agency.currentItem().text())
        invoice=gen_id()

        if agency:
            add_inp = add_stocks(agency)
        else:
            add_inp = add_stocks()

        if add_inp.exec_() == add_inp.Accepted:
            #   0        1       2       3      4     5       6          7         8    9    10     11       12
            # agency, xchange, equity, tdate, sdate, price, quantity, unit_brock, gst, stt, itax, comment, save_db
            new_row = add_inp.get_inp()
            rowList = list(add_inp.get_inp())

            price = rowList[5]
            Numb = rowList[6]
            brock = rowList[7]
            gst = rowList[8]
            stt = rowList[9]
            itax = rowList[10]
            comments = rowList[11]
            save_db = new_row[12]
            del rowList[-1]

            # print("new",new_row)
            # exit()

            if save_db:
                invoice = saveStockDB(new_row,invoice,"append")

            # rowList.insert(0, k1)
            #   0        1       2       3      4     5       6          7         8    9    10     11       12
            # agency, xchange, equity, tdate, sdate, price, quantity, unit_brock, gst, stt, itax, comment, save_db
            input_data = price, Numb, brock, gst, stt, itax
            output_data = self.stock_purchase_calc(input_data)
            # contr_amount, net_amount, gst_stt_brk, actual_price, Zero_profit
            # self.stockInfo_key = ['0 exchange', '1 equity', '2 Tdate', '3 Sdate', '5 Tprice', '6 quantity', '7 ContAmount',
            #                       '8 unit_brokerage', '9 gst', '10 stt', '11 gst_stt_br', '12 itax',
            #                       '13 NetAmount', '14 Oprice', '15 Zprice', '16 remarks', '17 invoice']

            # print(output_data)
            rowList.insert(7, output_data[0])
            rowList.insert(11, output_data[2])
            rowList.insert(13, output_data[1])
            rowList.insert(14, output_data[3])
            rowList.insert(15, output_data[4])

            del rowList[0]


            key = agency
            k1 = invoice

            self.stocksInfoz[key][k1]['exchange'] = rowList[0]
            self.stocksInfoz[key][k1]['equity'] = rowList[1]
            self.stocksInfoz[key][k1]['Tdate'] = rowList[2]
            self.stocksInfoz[key][k1]['Sdate'] = rowList[3]
            self.stocksInfoz[key][k1]['Tprice'] = parse_str(rowList[4])
            self.stocksInfoz[key][k1]['quantity'] = parse_str(rowList[5])
            self.stocksInfoz[key][k1]['ContAmount'] = parse_str(rowList[6])
            self.stocksInfoz[key][k1]['unit_brokerage'] = parse_str(rowList[7])
            self.stocksInfoz[key][k1]['gst'] = parse_str(rowList[8])
            self.stocksInfoz[key][k1]['stt'] = parse_str(rowList[9])
            self.stocksInfoz[key][k1]['gst_stt_br'] = parse_str(rowList[10])
            self.stocksInfoz[key][k1]['itax'] = parse_str(rowList[11])
            self.stocksInfoz[key][k1]['NetAmount'] = parse_str(rowList[12])
            self.stocksInfoz[key][k1]['Oprice'] = parse_str(rowList[13])
            self.stocksInfoz[key][k1]['Zprice'] = parse_str(rowList[14])
            self.stocksInfoz[key][k1]['remarks'] = rowList[15]


            row_number = self.stockList.rowCount()
            self.stockList.setRowCount(row_number + 1)
            one_stock = make_nested_dict0()
            one_stock.clear()
            one_stock = self.get_stock_info(key, k1)

            one_stock['invoice'] = int(k1)
            one_stock['current_price'] = 0.0
            one_stock['unit_gain'] = 0.0
            one_stock['total_gain'] = 0.0

            new_table = []
            new_table.clear()
            for info in self.stock_disp_key:
                data = one_stock[info]
                new_table.append(data)

            new_table = tuple(new_table)
            self.add_update_disp(row_number, new_table, agency, True)

            # table_sort_color(self.stockList)
            table_sort_color(self.stockList, self.sort_colmn_by_index, self.Red_colmn_by_index, self.Green_colmn_by_index)
            item = self.List_of_agency.currentItem()
            self.get_stocks(item)

        else:
            pass

        return


    def stock_sold(self):

        if self.stockList.selectedItems():
            agency = parse_str(self.List_of_agency.currentItem().text())
            row_number = self.stockList.currentRow()
            invoice = int(self.stockList.item(row_number, 0).text())

            one_stock = make_nested_dict0()
            one_stock.clear()
            one_stock = self.get_stock_info(agency, invoice)

            # print("sold1", self.stocksInfoz[agency][int(invoice)])
            # print("sold2", one_stock)

            row_val = []
            row_val.clear()
            row_val.append(agency)
            row_val.append(one_stock["exchange"])
            row_val.append(one_stock["equity"])
            row_val.append(one_stock["Tdate"])
            row_val.append(one_stock["Sdate"])
            row_val.append(one_stock["Oprice"])
            row_val.append(one_stock["quantity"])
            row_val.append(one_stock["unit_brokerage"])
            row_val.append(one_stock["gst"])
            row_val.append(one_stock["stt"])
            row_val.append(one_stock["itax"])
            # row_val.append(one_stock["Oprice"])

            # print(row_val)
            # print(type(row_val))


            sold_inp = sold_stocks(row_val)
            if sold_inp.exec_() == sold_inp.Accepted:
                #   0       1        2        3         4        5      6       7       8        9          10  11    12    13       14
                # agency, xchange, equity, buy_date, buy_price, tdate, sdate, price, quantity, unit_brock, gst, stt, itax, comment, self.save_db
                new_row = sold_inp.get_inp()
                rowList = list(sold_inp.get_inp())

                bprice = float(rowList[4])
                Numb = rowList[6]
                # brock = rowList[7]
                # gst = rowList[8]
                # stt = rowList[9]
                # itax = rowList[10]
                # comments = rowList[11]
                save_db = new_row[14]

                del rowList[-1]

                # print(rowList)

                # exit()


                # price=rowList[7]
                # Numb=float(rowList[8])
                # brok=rowList[9]
                # gst=rowList[10]
                # stt=rowList[11]
                # itax=rowList[12]
                # input_data = price, Numb, brok, gst, stt, itax
                # output_data = self.stock_sale_calc(input_data)
                #
                # net_amountSale=float(output_data[1])
                #
                # print(type(bprice))
                # print(type(Numb))
                # net_amountBuy=bprice*Numb
                # NetGain=net_amountSale-net_amountBuy
                #
                # print(output_data)
                # print(NetGain)


                # contr_amount, net_amount, gst_stt_brk, actual_price, Zero_profit

                # price, Quant, Brockerage, gst, stt, itax = input_data



                if save_db:
                    # print(save_db)
                    ids = saveStockSaleDB(rowList, invoice,"append")





    def update_Stock(self,item):

        if self.stockList.selectedItems():
            agency = parse_str(self.List_of_agency.currentItem().text())
            row_number = self.stockList.currentRow()
            invoice = int(self.stockList.item(row_number, 0).text())

            one_stock = make_nested_dict0()
            one_stock.clear()
            one_stock = self.get_stock_info(agency, invoice)

            # print("updated1", self.stocksInfoz[agency][int(invoice)])
            # print("updated2", one_stock)


            row_val = []
            row_val.clear()
            row_val.append(agency)
            row_val.append(one_stock["exchange"])
            row_val.append(one_stock["equity"])
            row_val.append(one_stock["Tdate"])
            row_val.append(one_stock["Sdate"])
            row_val.append(one_stock["Tprice"])
            row_val.append(one_stock["quantity"])
            row_val.append(one_stock["unit_brokerage"])
            row_val.append(one_stock["gst"])
            row_val.append(one_stock["stt"])
            row_val.append(one_stock["itax"])
            row_val.append(one_stock["remarks"])

            # print(row_val)

            update_inp = update_stocks(row_val)
            if update_inp.exec_() == update_inp.Accepted:
                new_row = update_inp.get_inp()
                rowList = list(update_inp.get_inp())

                price = rowList[5]
                Numb = rowList[6]
                brock = rowList[7]
                gst = rowList[8]
                stt = rowList[9]
                itax = rowList[10]
                comments = rowList[11]
                save_db = new_row[12]
                del rowList[-1]


                if save_db:
                    ids = saveStockDB(new_row, invoice, "update")


                # rowList.insert(0, k1)
                #   0        1       2       3      4     5       6          7         8    9    10     11       12
                # agency, xchange, equity, tdate, sdate, price, quantity, unit_brock, gst, stt, itax, comment, save_db
                input_data = price, Numb, brock, gst, stt, itax
                output_data = self.stock_purchase_calc(input_data)

                rowList.insert(7, output_data[0])
                rowList.insert(11, output_data[2])
                rowList.insert(13, output_data[1])
                rowList.insert(14, output_data[3])
                rowList.insert(15, output_data[4])

                del rowList[0]


                key = agency
                k1 = invoice
                # print(type(key))
                # print(type(k1))

                self.stocksInfoz[key][k1]['exchange'] = rowList[0]
                self.stocksInfoz[key][k1]['equity'] = rowList[1]
                self.stocksInfoz[key][k1]['Tdate'] = rowList[2]
                self.stocksInfoz[key][k1]['Sdate'] = rowList[3]
                self.stocksInfoz[key][k1]['Tprice'] = parse_str(rowList[4])
                self.stocksInfoz[key][k1]['quantity'] = parse_str(rowList[5])
                self.stocksInfoz[key][k1]['ContAmount'] = parse_str(rowList[6])
                self.stocksInfoz[key][k1]['unit_brokerage'] = parse_str(rowList[7])
                self.stocksInfoz[key][k1]['gst'] = parse_str(rowList[8])
                self.stocksInfoz[key][k1]['stt'] = parse_str(rowList[9])
                self.stocksInfoz[key][k1]['gst_stt_br'] = parse_str(rowList[10])
                self.stocksInfoz[key][k1]['itax'] = parse_str(rowList[11])
                self.stocksInfoz[key][k1]['NetAmount'] = parse_str(rowList[12])
                self.stocksInfoz[key][k1]['Oprice'] = parse_str(rowList[13])
                self.stocksInfoz[key][k1]['Zprice'] = parse_str(rowList[14])
                self.stocksInfoz[key][k1]['remarks'] = rowList[15]

                row_number = self.stockList.rowCount()
                # self.stockList.setRowCount(row_number + 1)
                one_stock = make_nested_dict0()
                one_stock.clear()
                one_stock = self.get_stock_info(key, k1)

                # print(rowList[15])

                one_stock['invoice'] = int(k1)
                one_stock['current_price'] = 0.0
                one_stock['unit_gain'] = 0.0
                one_stock['total_gain'] = 0.0

                # print( self.stocksInfoz[key][k1])

                # print("up-->", one_stock)
                # exit()

                new_table = []
                new_table.clear()
                for info in self.stock_disp_key:
                    data = one_stock[info]
                    new_table.append(data)
                    # print(info,data)

                new_table = tuple(new_table)
                self.add_update_disp(row_number, new_table, agency, True)
                # table_sort_color(self.stockList)
                table_sort_color(self.stockList, self.sort_colmn_by_index, self.Red_colmn_by_index, self.Green_colmn_by_index)
                # print("update",new_table)
                item = self.List_of_agency.currentItem()
                self.get_stocks(item)
        else:
            pass


    def calculate_sum(self,agency=""):

        if not agency:
            item = self.List_of_agency.currentItem()
            agency = str(item.text())

        stockz=self.stocksInfoz[agency]
        net_invetment=0.0
        net_extra=0.0

        for key,value in  stockz.items():
            net_invetment=net_invetment+parse_str(value['NetAmount'])
            net_extra=net_extra+parse_str(value['gst_stt_br'])

        agencyInvestmt="{:.{}f}".format(net_invetment,3)
        agencyCharges="{:.{}f}".format(net_extra, 3)

        self.agencyInvestmt.setText(format_currency(agencyInvestmt,'INR',locale='en_IN'))
        # color=QColor(0, 255, 0)
        # self.agencyInvestmt.set
        self.agencyCharges.setText(format_currency(agencyCharges,'INR',locale='en_IN'))

        self.agencyInvestmt.setStyleSheet('color: blue')
        self.agencyCharges.setStyleSheet('color: blue')

        return


    def refresh_Stock(self):
        print("refresh")



