import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint,pyqtSlot,QDateTime,QVariant,QDate

from babel.numbers import format_currency
from Purchase.purchase import  make_nested_dict0,get_nested_dist_value,parse_str,table_sort_color
from db_management import read_all_transaction,save_transactionDB,delTransDB

class show_transactions(QDialog):

    def __init__(self, parent=None):
        super(show_transactions, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Transaction Details")
        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(350, 350, 1150, 600)
        self.setFixedSize(self.size())
        # self.stock_id=stock_id
        # self.stock_info=stock_info
        self.UI()
        self.show()

    def UI(self):
        self.table_header_info()
        self.widgets()
        self.layouts()


    def table_header_info(self):
        self.headerName = []
        self.headerName.append("Reference")  # 0
        self.headerName.append("Agency")  # 1
        self.headerName.append("Transaction Date")  # 2
        self.headerName.append("Transaction id")  # 3
        self.headerName.append("Transaction \n amount")  # 4
        self.headerName.append("From Bank")  # 5
        self.headerName.append("To Bank")  # 6
        self.headerName.append("Remarks")  # 7

        self.col_N = 8
        self.index_disp = []
        self.index_disp = [0, 1, 2, 3, 4, 5, 6, 7]
        self.col_disp = len(self.index_disp)
        self.db_index = []
        self.db_index = ['id', 'agency', 'TransactionDate', 'TransactionID', 'TransactionAmount', 'FromBank','ToBank', 'Remarks']

        self.stock_key = []
        self.stockInfo_key = ['id', 'agency', 'TransactionDate', 'TransactionID', 'TransactionAmount', 'FromBank','ToBank', 'Remarks']

        self.stock_disp_key = []
        self.stock_disp_key = ['id', 'agency', 'TransactionDate', 'TransactionID', 'TransactionAmount', 'FromBank','ToBank', 'Remarks']

        self.sort_colmn_by_index = []
        # self.sort_colmn_by_index = [0,3]
        # self.sort_colmn_by_index.insert(0, 0)
        # self.sort_colmn_by_index.insert(0, 4)
        self.Red_colmn_by_index = []
        # self.Red_colmn_by_index = [10, 14, 15]
        self.Green_colmn_by_index = []
        self.Green_colmn_by_index = [4]

    def widgets(self):

        fnt = QFont()
        fnt.setPointSize(13)
        fnt.setBold(True)
        fnt.setFamily("Arial")

        self.agencyName = QLabel("AgencyName")
        self.agencyName.setFont(fnt)

        self.agencyInvestmt = QLabel("0")
        self.agencyInvestmt.setFont(fnt)

        self.add_trans=QPushButton("Add")
        self.add_trans.clicked.connect(self.new_trans)

        self.transactionList = self.tabulatePayment()
        self.transactionList.setSortingEnabled(True)
        self.transactionList.installEventFilter(self)
        self.transactionList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.transactionList.customContextMenuRequested.connect(self.rightClickMenu)

        self.List_of_agency = QListWidget()
        agency, self.paymentDB = read_all_transaction()
        self.transInfoz = self.store_trans()

        self.List_of_agency = self.load_agency(agency)
        self.List_of_agency.itemClicked.connect(self.get_trans)

        # print(agency)
        # print(self.paymentDB)
        # for key,value in self.transInfoz.items():
        #     print(key)
        #     for k1,v1 in value.items():
        #         print(k1,v1)

        item = self.List_of_agency.item(0)
        self.List_of_agency.setCurrentItem(item)
        self.get_trans(item)


    def tabulatePayment(self):

        Table = QTableWidget()
        Table.setColumnCount(self.col_disp)
        j=0
        for i in self.index_disp:
            hname=str(self.headerName[i])
            Table.setHorizontalHeaderItem(j, QTableWidgetItem(hname))
            j=j+1

        Table.setAlternatingRowColors(True)
        header = Table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSelectionMode(QAbstractItemView.SingleSelection)
        header.setStretchLastSection(True)
        Table.setFont(QFont("Times", 9))
        Table.setSortingEnabled(False)
        header.setFont(QFont("Times", 12))
        Table.setSelectionBehavior(QAbstractItemView.SelectRows)
        Table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        Table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # stockTable.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)

        return Table

    @pyqtSlot(QPoint)
    def rightClickMenu(self, pos):
        indexes = self.sender().selectedIndexes()
        mdlIdx = self.transactionList.indexAt(pos)
        # print("position",pos)
        if not mdlIdx.isValid():
            return

        # self.case=self.stockList.itemFromIndex(mdlIdx)
        # print("Case :"+str(self.case.text()))
        row = self.transactionList.currentRow()
        # self.invoice = int(self.stockList.item(row, 0).text())
        # print("#"+str(self.invoice))

        self.menu = QMenu(self)
        remAct = QAction(QIcon(""), "Delete", self, triggered=self.delTrans)
        dbremAct = QAction(QIcon(""), "DeleteDB", self, triggered=self.del_transDB)
        # saveAct = QAction(QIcon(""), "Save", self, triggered=self.saveStock)
        addAct = QAction(QIcon(""), "Add Transaction", self, triggered=self.new_trans)
        # remAct.setStatusTip('Delete stock from database')
        updateAct = QAction(QIcon(""), 'Update Transaction', self, triggered=self.update_trans)
        # refreshAct = QAction(QIcon(""), 'Refresh', self, triggered=self.refresh_Stock)
        # dispAct = QAction(QIcon(""), 'Show', self, triggered=self.show_Stock)
        # soldAct = QAction(QIcon(""), 'Sold', self, triggered=self.stock_sold)
        addAct = self.menu.addAction(addAct)
        editStk = self.menu.addAction(updateAct)
        # dispStk = self.menu.addAction(dispAct)
        # saveStk = self.menu.addAction(saveAct)
        remStk = self.menu.addAction(remAct)
        dbremStk = self.menu.addAction(dbremAct)
        # refrStk = self.menu.addAction(refreshAct)
        # self.menu.addSeparator()
        # soldStk = self.menu.addAction(soldAct)

        self.menu.exec_(self.sender().viewport().mapToGlobal(pos))

    def new_trans(self):
        agency = parse_str(self.List_of_agency.currentItem().text())

        tr_inp = add_new_trans(agency)
        if tr_inp.exec_() == tr_inp.Accepted:
            # new_row = tr_inp.get_inp()
            rowList = list(tr_inp.get_inp())
            # print(rowList)
            save_db=rowList[7]
            del rowList[-1]


            if save_db:
                trns = save_transactionDB(rowList,"append")


    def del_transDB(self):
        agency = self.List_of_agency.currentItem().text()
        invoice = ""
        if self.transactionList.selectedItems():
            row_number = self.transactionList.currentRow()
            invoice = self.transactionList.item(row_number, 0).text()
            agency = str(agency)
            deltransDB = delTransDB(invoice)
            mbox = QMessageBox.question(self, "Delete from table ?",
                                        "Display table still showing transaction with  ID: " + str(invoice),
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    row_number = self.transactionList.currentRow()
                    invoice = self.transactionList.item(row_number, 0).text()
                    agency = str(agency)
                    invoice = parse_str(invoice)
                    del (self.transInfoz[agency][invoice])
                    self.stockList.removeRow(row_number)
                    QMessageBox.information(self, "Info", "transaction with reference number " + str(
                        invoice) + " has been deleted from table")
                except:
                    QMessageBox.information(self, "Warning", "transaction with reference number " + str(
                        invoice) + " has not been deleted from table")

        item = self.List_of_agency.currentItem()
        self.get_trans(item)


    def update_trans(self):
        pass

    def delTrans(self):
        agency = self.List_of_agency.currentItem().text()
        if self.transactionList.selectedItems():
            row_number = self.transactionList.currentRow()
            invoice = int(self.transactionList.item(row_number, 0).text())
            # agency = str(agency)
            # invoice = int(invoice)
            del (self.transInfoz[agency][invoice])
            self.transactionList.removeRow(row_number)

            item = self.List_of_agency.currentItem()
            self.get_trans(item)

    def layouts(self):
        # pass
        self.mainLayout = QVBoxLayout()
        self.horizontalSplitter = QSplitter(Qt.Horizontal)
        self.rightLayout = QVBoxLayout()
        self.rightWidget = QWidget()

        self.agency_summaryLayout = QGridLayout()
        self.agency_summaryLayout.addWidget(self.agencyName, 0, 0)
        self.agency_summaryLayout.addWidget(QLabel('Total Transaction : '), 0, 1)
        self.agency_summaryLayout.addWidget(self.agencyInvestmt, 0, 2)

        self.summaryGroupBox = QGroupBox("Agency")
        self.summaryGroupBox.setLayout(self.agency_summaryLayout)

        self.leftTopGroupBox = QGroupBox("Agency List")
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.List_of_agency)
        self.leftTopGroupBox.setLayout(self.leftLayout)


        self.rightTopGroupBox = QGroupBox("Transactions")
        self.rightTopLayout = QVBoxLayout()
        self.rightTopLayout.addWidget(self.transactionList)
        self.rightTopGroupBox.setLayout(self.rightTopLayout)

        self.rightLayout.addWidget(self.rightTopGroupBox,95)
        self.rightLayout.addWidget(self.summaryGroupBox,5)
        self.rightWidget.setLayout(self.rightLayout)

        self.horizontalSplitter.addWidget(self.leftTopGroupBox)
        self.horizontalSplitter.addWidget(self.rightWidget)
        self.horizontalSplitter.setStretchFactor(0, 10)
        self.horizontalSplitter.setStretchFactor(1, 90)
        self.horizontalSplitter.setContentsMargins(0, 0, 0, 0)
        self.horizontalSplitter.handle(0)

        self.mainLayout.addWidget(self.horizontalSplitter)
        self.setLayout(self.mainLayout)

    def store_trans(self):

        transInfoz = make_nested_dict0()
        transInfoz.clear()

        for key, value in self.paymentDB.items():
            for k1, val1 in value.items():
                rowList = list(val1)
                # print("#",key,k1,rowList)

                # 'id', 'agency', 'TransactionDate', 'TransactionAmount', 'TransactionID', 'FromBank', 'ToBank', 'Remarks'


                transInfoz[key][k1]['id'] = k1
                transInfoz[key][k1]['agency'] = key
                transInfoz[key][k1]['TransactionDate'] = rowList[0]
                transInfoz[key][k1]['TransactionAmount'] = rowList[2]
                transInfoz[key][k1]['TransactionID'] = rowList[1]
                transInfoz[key][k1]['FromBank'] = rowList[3]
                transInfoz[key][k1]['ToBank'] = rowList[4]
                transInfoz[key][k1]['Remarks'] = rowList[5]


        return transInfoz

    def load_agency(self, agency):
        # List of stock brocker agencies
        List_of_agency = QListWidget()
        for itm in agency:
            # print(itm)
            List_of_agency.addItem(itm)

        return List_of_agency


    def get_trans(self, item):
        # https://www.tutorialexample.com/pyqt-table-add-row-data-dynamically-a-beginner-guide-pyqt-tutorial/

        agncy = item.text()
        # print("ag",agncy)
        # print(type(agncy))
        self.transactionList.setRowCount(0)
        self.agencyName.setText(agncy)

        # print(self.transactionList)

        stockz=get_nested_dist_value(self.transInfoz,agncy)
        one_stock = make_nested_dict0()
        one_stock.clear()

        for key, val in stockz.items():
            row_number = self.transactionList.rowCount()
            self.transactionList.setRowCount(row_number + 1)
            one_stock=val


            new_table = []
            new_table.clear()
            for info in self.stock_disp_key:
                data = one_stock[info]
                new_table.append(data)

            new_table = tuple(new_table)

            self.add_update_disp(row_number,new_table,agncy,False)

        self.transactionList.setSortingEnabled(True)
        table_sort_color(self.transactionList, self.sort_colmn_by_index, self.Red_colmn_by_index, self.Green_colmn_by_index)

        self.calculate_tr_sum()

        return

    def add_update_disp(self, row, row_data, agency, do_sum):

        for column_number, data in enumerate(row_data):
            # print(data,type(parse_str(data)))
            newItem = QTableWidgetItem()
            data = parse_str(data)
            newItem.setData(Qt.DisplayRole, data)
            self.transactionList.setSortingEnabled(False)
            self.transactionList.setItem(row, column_number, newItem)
            # print(data,type(data))
        # exit()
        self.transactionList.setSortingEnabled(True)

        # if do_sum:
        #     self.calculate_sum(agency)

    def calculate_tr_sum(self, agency=""):

        if not agency:
            item = self.List_of_agency.currentItem()
            agency = str(item.text())

        tranz = self.transInfoz[agency]
        net_invetment = 0.0
        net_extra = 0.0

        for key, value in tranz.items():
            net_invetment = net_invetment + parse_str(value['TransactionAmount'])

        agencyInvestmt = "{:.{}f}".format(net_invetment, 3)
        self.agencyInvestmt.setText(format_currency(agencyInvestmt, 'INR', locale='en_IN'))
        self.agencyInvestmt.setStyleSheet('color: blue')

        return


class add_new_trans(QDialog):

    # def __init__(self,con,cur,agency=""):
    def __init__(self, agency="", dbsave="", parent=None):
        super(add_new_trans, self).__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle("Add Transaction")
        # self.con=con
        # self.cur=cur
        self.dbsave = False
        self.agency0 = ""
        if agency:
            self.agency0 = agency
        #
        if dbsave:
            self.dbsave = True

        # self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 450, 300)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        # self.get_db()
        # self.get_default_paramters()
        self.widgets()
        self.layouts()

    # def get_db(self):
    #     self.con, self.cur = check_db(db_file)

    # def get_default_paramters(self):
    #     default = default_parameters()
    #     self.brockerage = default[0]
    #     self.gst = default[1]
    #     self.stt = default[2]
    #     self.itax = default[3]

    def widgets(self):
        self.save_db = False
        self.titleText = QLabel("Add New transaction")
        self.agencyEntry = QLineEdit()
        self.agencyEntry.setPlaceholderText("Enter name of agency (Eg. Kotak, Zerodha, etc)")
        self.tr_dateEntry = QDateEdit(self)
        self.tr_dateEntry.setDate(QDate.currentDate())
        self.tr_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.tr_idEntry = QLineEdit()
        self.tr_idEntry.setPlaceholderText("Enter transaction id")
        self.amountEntry = QLineEdit()
        self.amountEntry.setPlaceholderText("Enter transaction amount")
        self.fromBnkEntry = QLineEdit()
        self.fromBnkEntry.setPlaceholderText("source bank")
        self.toBnkEntry = QLineEdit()
        self.toBnkEntry.setPlaceholderText("destination bank")
        self.remarksEntry = QLineEdit()
        self.remarksEntry.setPlaceholderText("Type your remarks ..")

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

        # self.agencyEntry.setText("Kotak")
        # # self.tr_dateEntry.setText("16/08/2020")
        # # self.tr_dateEntry.setDateTime(QDateTime(QDate(2020, 08, 16)))
        # self.amountEntry.setText("109")
        # self.tr_idEntry.setText("200")
        self.fromBnkEntry.setText("SBI")
        self.toBnkEntry.setText("Kotak Mahindra securities ltd")
        self.remarksEntry.setText("Equity")

    def state_changed(self):
        self.save_db = True

    def accept(self):
        agency=self.agencyEntry.text()
        tdate=self.tr_dateEntry.text()
        amount=self.amountEntry.text()
        tr_id=self.tr_idEntry.text()
        bank0=self.fromBnkEntry.text()
        bank1=self.toBnkEntry.text()
        comment = self.remarksEntry.text()

        self.output = agency, tdate,amount,tr_id,bank0,bank1,comment, self.save_db
        super(add_new_trans, self).accept()

    def clearAll(self):
        self.agencyEntry.setText("")
        self.tr_dateEntry.setDate(QDate.currentDate())
        self.tr_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.amountEntry.setText("")
        self.tr_idEntry.setText("")
        self.fromBnkEntry.setText("")
        self.toBnkEntry.setText("")
        self.remarksEntry.setText("")


    def get_inp(self):
        return self.output

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.mainTopLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.bottomLayout = QHBoxLayout()
        self.topFrame = QFrame()

        self.topGroupBox = QGroupBox("Transaction Information")
        self.bottomGroupBox = QGroupBox("Control")

        self.topLayout.addRow(QLabel("Agency: "), self.agencyEntry)
        self.topLayout.addRow(QLabel("Transaction Date: "), self.tr_dateEntry)
        self.topLayout.addRow(QLabel("Transaction Amount: "), self.amountEntry)
        self.topLayout.addRow(QLabel("Transaction ID: "), self.tr_idEntry)
        self.topLayout.addRow(QLabel("From Bank: "), self.fromBnkEntry)
        self.topLayout.addRow(QLabel("To Bank: "), self.toBnkEntry)
        self.topLayout.addRow(QLabel("Remarks: "), self.remarksEntry)

        # self.bottomLayout.addWidget(self.addBtn)
        # self.bottomLayout.addWidget(self.clrBtn)
        self.bottomLayout.addWidget(self.buttonBox)

        self.topGroupBox.setLayout(self.topLayout)
        self.bottomGroupBox.setLayout(self.bottomLayout)

        # self.topFrame.setLayout(self.topLayout)
        # self.topGroupBox.add setLayout(self.topLayout)
        # self.bottomGroupBox.setLayout(self.bottomLayout)
        self.mainTopLayout.addWidget(self.topGroupBox)
        self.mainTopLayout.addWidget(self.saveDB)
        self.mainTopLayout.addWidget(self.bottomGroupBox)

        self.mainLayout.addLayout(self.mainTopLayout)
        self.setLayout(self.mainLayout)




#
# def main():
#     APP=QApplication(sys.argv)
#     window=show_transactions()
#     sys.exit(APP.exec_())
#
# if __name__=='__main__':
#     main()