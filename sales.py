from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint,pyqtSlot,QDateTime,QVariant

from babel.numbers import format_currency

from db_management import read_all_sales
# from purchase import import load_agency
from purchase import  make_nested_dict0,get_nested_dist_value,parse_str,table_sort_color



class sold_list(QWidget):

    def __init__(self):
        super().__init__()
        #self.setWindowTitle("Investment")
        #self.setGeometry(450,150,750,600)
        self.UI()
        self.show()


    def UI(self):
        self.table_header_info()
        self.widgets()
        self.layouts()

    def table_header_info(self):
        self.headerName = []
        self.headerName.append("Reference \n Number")  # 0
        self.headerName.append("Exchange")  # 1
        self.headerName.append("Equity")  # 2
        self.headerName.append("Buy \n Date")  # 3
        self.headerName.append("Buy \n Price")  # 4
        self.headerName.append("Trade \n Date")  # 5
        self.headerName.append("Settlement \n Date")  # 6
        self.headerName.append("Trade \n Price")  # 7
        self.headerName.append("Quantity")  # 8
        self.headerName.append("Contract \n Amount")  # 9
        self.headerName.append("GST+STT+ \n Brokerage")  # 10
        self.headerName.append("Income \n tax(%)")  # 11
        self.headerName.append("Net \n Amount")  # 12
        self.headerName.append("Overall \n unit Price")  # 13
        self.headerName.append("Gain \n per unit")  # 14
        self.headerName.append("Overall \n Gain")  # 15
        self.headerName.append("Remarks")  # 16

        self.col_N = 20
        self.index_disp = []
        self.index_disp = [0, 1, 2, 3, 4,5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15,16]
        self.col_disp = len(self.index_disp)
        self.db_index = []
        self.db_index = ['id', 'agency', 'exchange', 'equity', 'trade_date', 'settle_date', 'trade_price', 'quantity',
                         'unit_brokerage', 'gst', 'stt', 'itax', 'remarks']

        self.stock_key = []
        self.stockInfo_key = ['exchange', 'equity', 'Bdate', 'Bprice','Tdate', 'Sdate', 'Tprice', 'quantity', 'ContAmount',
                              'unit_brokerage', 'gst', 'stt', 'gst_stt_br', 'itax','NetAmount', 'Oprice', 'Unit_gain',
                              'Total_gain','remarks', 'invoice']

        self.stock_disp_key = []
        self.stock_disp_key = ['invoice','exchange', 'equity', 'Bdate', 'Bprice', 'Tdate', 'Sdate','Tprice', 'quantity', 'ContAmount',
                               'gst_stt_br', 'itax','NetAmount', 'Oprice', 'Unit_gain','Total_gain','remarks']

        self.sort_colmn_by_index = []
        self.sort_colmn_by_index = [i for i in range(7, 15)]
        self.sort_colmn_by_index.insert(0, 0)
        self.sort_colmn_by_index.insert(0, 4)
        self.Red_colmn_by_index = []
        self.Red_colmn_by_index = [10,14,15]
        self.Green_colmn_by_index = []
        self.Green_colmn_by_index = [2, 4, 7, 12]


    def widgets(self):
        fnt = QFont("Arial", 13, QFont.Bold)
        # fnt.setPointSize(13)
        # fnt.setBold(True)
        # fnt.setFamily("Arial")
        # fnt.QColor(0, 255, 0)

        self.agencyGain = QLabel("0")
        self.agencyGain.setFont(fnt)

        self.agencyInvestmt = QLabel("0")
        self.agencyInvestmt.setFont(fnt)
        self.agencyCharges = QLabel("0")
        self.agencyCharges.setFont(fnt)

        self.agencyName = QLabel("AgencyName")
        self.agencyName.setFont(fnt)

        self.stockList = self.tabulateStocks()
        self.stockList.setSortingEnabled(True)



        self.List_of_agency = QListWidget()
        agency, self.stockDB = read_all_sales()

        self.stocksInfoz = self.store_stocks()
        self.List_of_agency = self.load_agency(agency)
        self.List_of_agency.itemClicked.connect(self.get_stocks)


        # for i in  range(0,self.List_of_agency.count()):
        #     item=self.List_of_agency.item(i)
        #     print(item.text())
        #
        # for key,value in self.stockDB.items():
        #     print(key)
        #     for k,v in value.items():
        #         print(k,v)


        # self.totalInvestment = QLabel("0")
        # self.totalInvestment.setFont(fnt)
        # self.totalCharges = QLabel("0")
        # self.totalCharges.setFont(fnt)

        # self.agencyGain = QLabel("0")
        # self.agencyGain.setFont(fnt)
        #
        # self.agencyInvestmt = QLabel("0")
        # self.agencyInvestmt.setFont(fnt)
        # self.agencyCharges = QLabel("0")
        # self.agencyCharges.setFont(fnt)
        #
        # self.agencyName = QLabel("AgencyName")
        # self.agencyName.setFont(fnt)

        # self.nse = QPushButton('NSE')
        # self.nse.setGeometry(10, 1, 100, 25)
        # self.nse.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.nse.clicked.connect(self.get_nse_data)
        # self.nse.setToolTip('Get latest stock price \n from NSE')

        # https: // programming.vip / docs / pyqt5 - quick - start - pyqt5 - basic - window - components.html

        item = self.List_of_agency.item(0)
        self.List_of_agency.setCurrentItem(item)

        # print("1",self.stocksInfoz)
        self.get_stocks(item)

    def load_agency(self, agency):
        # List of stock brocker agencies
        List_of_agency = QListWidget()
        for itm in agency:
            # print(itm)
            List_of_agency.addItem(itm)

        return List_of_agency

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

    def store_stocks(self):

        stocksInfoz = make_nested_dict0()
        stocksInfoz.clear()

        # return

        for key, value in self.stockDB.items():
            for k1, val1 in value.items():
                rowList = list(val1)
                # print(key,k1,rowList)

                Bprice=rowList[3]
                Tprice=rowList[6]
                quantity=rowList[7]
                ##break
                brokerage=rowList[8]
                gst = rowList[9]
                stt = rowList[10]
                itax = rowList[11]
                comments = rowList[12]

                #
                input_data = Tprice, quantity, brokerage, gst, stt, itax,Bprice
                output_data = self.stock_profit_calc(input_data)

                # contr_amount, gst_stt_brk, itax, net_amount, actual_price, unit_gain, total_gain

                # row_data = tuple(rowList)
                # self.stockInfo_key = ['exchange', 'equity', 'Bdate', 'Bprice', 'Tdate', 'Sdate', 'Tprice', 'quantity',
                #                       'ContAmount', 'unit_brokerage', 'gst', 'stt', 'gst_stt_br', 'itax', 'NetAmount',
                #                       'Oprice','Unit_gain','Total_gain', 'remarks', 'invoice']
                #    0       1          2           3           4            5          6     7    8    9    10    11    12
                # ['NSE', 'KSCL', '07/08/2020', 619.023, '07/08/2020', '11/08/2020', 677.35, 100, 0.4, 18.0, 0.1, 30.0, 'sold']

                stocksInfoz[key][k1]['exchange'] = rowList[0]
                stocksInfoz[key][k1]['equity'] = rowList[1]
                stocksInfoz[key][k1]['Bdate'] = rowList[2]
                stocksInfoz[key][k1]['Bprice'] = rowList[3]
                stocksInfoz[key][k1]['Tdate'] = rowList[4]
                stocksInfoz[key][k1]['Sdate'] = rowList[5]
                stocksInfoz[key][k1]['Tprice'] = rowList[6]
                stocksInfoz[key][k1]['quantity'] = rowList[7]
                stocksInfoz[key][k1]['ContAmount'] = output_data[0]
                stocksInfoz[key][k1]['unit_brokerage'] = rowList[8]
                stocksInfoz[key][k1]['gst'] = rowList[9]
                stocksInfoz[key][k1]['stt'] = rowList[10]
                stocksInfoz[key][k1]['gst_stt_br'] = output_data[1]
                stocksInfoz[key][k1]['itax'] = output_data[2]
                stocksInfoz[key][k1]['NetAmount'] = output_data[3]
                stocksInfoz[key][k1]['Oprice'] = output_data[4]
                stocksInfoz[key][k1]['Unit_gain'] = output_data[5]
                stocksInfoz[key][k1]['Total_gain'] = output_data[6]
                stocksInfoz[key][k1]['remarks'] = comments
                stocksInfoz[key][k1]['invoice'] = k1

        return stocksInfoz

    def stock_profit_calc(self, input_data):
        price, Quant, Brockerage, gst, stt, itax , Bprice = input_data
        # print(input_data)
        # print( price,Quant,Brockerage,gst,stt,itax)
        price = parse_str(price)
        Quant = parse_str(Quant)
        Brockerage = parse_str(Brockerage) / 100.0
        gst = parse_str(gst) / 100.0
        stt = parse_str(stt) / 100.0
        itax = parse_str(itax) / 100.0
        Bprice=parse_str(Bprice)


        unit_brockerage = price * Brockerage
        net_rate = price - unit_brockerage
        net_total = net_rate * Quant
        taxable_brockerage = unit_brockerage * Quant
        gst_brockerage = taxable_brockerage * gst
        stt_net_total = stt * net_total
        contr_amount = price * Quant
        net_amount = net_total - gst_brockerage - stt_net_total
        gst_stt_brk = taxable_brockerage + gst_brockerage + stt_net_total
        actual_price = net_amount / Quant

        contr_amount = round(contr_amount, 3)
        net_amount = round(net_amount, 3)
        gst_stt_brk = round(gst_stt_brk, 3)
        actual_price = round(actual_price, 3)
        profit = round((actual_price + gst_stt_brk / float(Quant)), 3)
        unit_gain=actual_price-Bprice
        total_gain=unit_gain*Quant

        return contr_amount, gst_stt_brk,itax,net_amount, actual_price,unit_gain,total_gain


    def get_stocks(self, item):
        # https://www.tutorialexample.com/pyqt-table-add-row-data-dynamically-a-beginner-guide-pyqt-tutorial/

        agncy = item.text()
        # print(type(agncy))
        self.stockList.setRowCount(0)
        self.agencyName.setText(agncy)

        stockz=get_nested_dist_value(self.stocksInfoz,agncy)
        one_stock = make_nested_dict0()
        one_stock.clear()

        for key, val in stockz.items():
            row_number = self.stockList.rowCount()
            self.stockList.setRowCount(row_number + 1)
            one_stock=val
            # print(key,one_stock)
            one_stock['invoice'] = key
            # one_stock['current_price'] = 0.0
            # one_stock['unit_gain'] = 0.0
            # one_stock['total_gain'] = 0.0

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

    def add_update_disp(self, row, row_data, agency, do_sum):

        for column_number, data in enumerate(row_data):
            # print(data,type(parse_str(data)))
            newItem = QTableWidgetItem()
            data = parse_str(data)
            newItem.setData(Qt.DisplayRole, data)
            self.stockList.setSortingEnabled(False)
            self.stockList.setItem(row, column_number, newItem)
            # print(data,type(data))
        # exit()
        self.stockList.setSortingEnabled(True)

        # if do_sum:
        #     self.calculate_sum(agency)



    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.horizontalSplitter = QSplitter(Qt.Horizontal)
        self.leftVsplitter = QSplitter(Qt.Vertical)
        self.rightVsplitter = QSplitter(Qt.Vertical)
        self.rightBottomLayout = QHBoxLayout()

        # self.buttons=QWidget()
        # self.controlLayout = QHBoxLayout()
        # self.controlLayout.addStretch()
        # self.controlLayout.addWidget(self.nse)
        # self.controlLayout.addWidget(self.refreshAll)
        # self.controlLayout.addWidget(self.calculate)
        # self.controlLayout.addWidget(self.save2db)
        # self.buttons.setLayout(self.controlLayout)

        # self.totalInvestment = QLabel("0")
        # self.totalCharges = QLabel("0")
        #
        # self.agencyInvestmt = QLabel("0")
        # self.agencyCharges = QLabel("0")

        self.agency_summaryLayout = QGridLayout()
        self.agency_summaryLayout.addWidget(self.agencyName, 0, 0)
        self.agency_summaryLayout.addWidget(QLabel('Total tax and brokerage : '), 0, 1)
        self.agency_summaryLayout.addWidget(self.agencyCharges, 0, 2)
        self.agency_summaryLayout.addWidget(QLabel('Total Investment : '), 0, 3)
        self.agency_summaryLayout.addWidget(self.agencyInvestmt, 0, 4)
        self.agency_summaryLayout.addWidget(QLabel('Total Gain[Rs] : '), 0, 5)
        self.agency_summaryLayout.addWidget(self.agencyGain, 0, 6)

        self.overallSummaryLayout = QGridLayout()
        self.overallSummaryLayout.addWidget(QLabel('Total tax and brokerage:'), 0, 0)
        # self.overallSummaryLayout.addWidget(QLineEdit(),0,1)
        self.overallSummaryLayout.addWidget(QLabel('Total Investment:'), 0, 1)
        # self.overallSummaryLayout.addWidget(QLineEdit(), 0, 3)

        self.summaryGroupBox = QGroupBox(self.agencyName.text())
        self.summaryGroupBox = QGroupBox("Agency")
        self.summaryGroupBox.setLayout(self.agency_summaryLayout)

        # self.overallsummaryGroupBox = QGroupBox('Total Investment')
        # self.overallsummaryGroupBox.setLayout(self.overallSummaryLayout)
        #
        # self.buttonGroupBox = QGroupBox("Internet")
        # self.buttonGroupBox.setLayout(self.controlLayout)
        #
        # self.rightBottomLayout.addWidget(self.summaryGroupBox, 47)
        # self.rightBottomLayout.addWidget(self.overallsummaryGroupBox, 47)
        # self.rightBottomLayout.addWidget(self.buttonGroupBox, 6)
        self.rightBottomWidget = QWidget()
        self.rightBottomWidget.setLayout(self.rightBottomLayout)

        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.leftTopGroupBox = QGroupBox("Agency List")
        self.rightTopGroupBox = QGroupBox("Stock Sold")

        self.leftLayout.addWidget(self.List_of_agency)
        # self.rightLayout.addWidget(self.buttons,4)
        self.rightLayout.addWidget(self.stockList)
        self.leftTopGroupBox.setLayout(self.leftLayout)
        self.rightTopGroupBox.setLayout(self.rightLayout)

        self.leftVsplitter.addWidget(self.leftTopGroupBox)
        self.rightVsplitter.addWidget(self.rightTopGroupBox)
        self.rightVsplitter.addWidget(self.summaryGroupBox)
        self.rightVsplitter.addWidget(self.rightBottomWidget)
        self.rightVsplitter.setStretchFactor(0, 97)
        self.rightVsplitter.setStretchFactor(1, 3)

        self.horizontalSplitter.addWidget(self.leftVsplitter)
        self.horizontalSplitter.addWidget(self.rightVsplitter)
        self.horizontalSplitter.setStretchFactor(0, 10)
        self.horizontalSplitter.setStretchFactor(1, 90)
        self.horizontalSplitter.setContentsMargins(0, 0, 0, 0)
        self.horizontalSplitter.handle(0)

        self.mainLayout.addWidget(self.horizontalSplitter)
        self.setLayout(self.mainLayout)


    def calculate_sum(self,agency=""):

        if not agency:
            item = self.List_of_agency.currentItem()
            agency = str(item.text())

        stockz=self.stocksInfoz[agency]
        net_invetment=0.0
        net_extra=0.0
        net_gain=0.0

        for key,value in  stockz.items():
            net_invetment=net_invetment+parse_str(value['NetAmount'])
            net_extra=net_extra+parse_str(value['gst_stt_br'])
            net_gain=net_gain+parse_str(value['Total_gain'])

        agencyInvestmt="{:.{}f}".format(net_invetment,3)
        agencyCharges="{:.{}f}".format(net_extra, 3)
        net_gain="{:.{}f}".format(net_gain, 3)

        # agencyInvestmt=locale.currency(float(agencyInvestmt), grouping=True)

        self.agencyInvestmt.setText(format_currency(agencyInvestmt,'INR',locale='en_IN'))
        self.agencyCharges.setText(format_currency(agencyCharges,'INR',locale='en_IN'))
        self.agencyGain.setText(format_currency(net_gain,'INR',locale='en_IN'))
        self.agencyInvestmt.setStyleSheet('color: blue')
        self.agencyCharges.setStyleSheet('color: blue')
        self.agencyGain.setStyleSheet('color: blue')

        return