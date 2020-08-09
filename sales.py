from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class sold_list(QWidget):

    def __init__(self):
        super().__init__()
        #self.setWindowTitle("Investment")
        #self.setGeometry(450,150,750,600)
        self.UI()
        self.show()


    def UI(self):
        self.widgets()
        self.table_header_info()
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
        self.index_disp = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.col_disp = len(self.index_disp)
        self.db_index = []
        self.db_index = ['id', 'agency', 'exchange', 'equity', 'trade_date', 'settle_date', 'trade_price', 'quantity',
                         'unit_brokerage', 'gst', 'stt', 'itax', 'remarks']

        self.stock_key = []
        self.stockInfo_key = ['exchange', 'equity', 'Tdate', 'Sdate', 'Tprice', 'quantity', 'ContAmount',
                              'unit_brokerage', 'gst', 'stt', 'gst_stt_br', 'itax',
                              'NetAmount', 'Oprice', 'Zprice', 'remarks', 'invoice']

        self.stock_disp_key = []
        self.stock_disp_key = ['invoice', 'exchange', 'equity', 'Tdate', 'Tprice', 'quantity', 'gst_stt_br',
                               'NetAmount', 'Oprice', 'Zprice', 'current_price',
                               'unit_gain', 'total_gain', 'remarks']

    def widgets(self):
        pass

    def mainDesign(self):
        self.employeeList=QListWidget()
        self.btnNew=QPushButton("New")
        # self.btnNew.clicked.connect(self.addEmployee)
        self.btnUpdate=QPushButton("Update")
        self.btnDelete=QPushButton("Delete")



    def layouts(self):
        pass
