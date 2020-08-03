from PyQt5.QtGui import *

def showStocks(self, item):
    # https://www.tutorialexample.com/pyqt-table-add-row-data-dynamically-a-beginner-guide-pyqt-tutorial/
    agncy = item.text()
    self.stockList.setFont(QFont("Times", 9))
    for i in reversed(range(self.stockList.rowCount())):
        self.stockList.removeRow(i)

    for key, value in self.stockDB.items():
        if key == agncy:
            for k1, val1 in value.items():
                row_number = self.stockList.rowCount()
                self.stockList.setRowCount(row_number + 1)

                rowList = list(val1)
                rowList.insert(0, k1)

                price = rowList[5]
                Numb = rowList[6]
                brock = rowList[7]
                gst = rowList[8]
                stt = rowList[9]
                itax = rowList[10]
                comments = rowList[11]

                input_data = price, Numb, brock, gst, stt, itax
                output_data = self.stock_calc(input_data)
                # output_data=list(output_data)
                rowList.insert(7, output_data[0])
                rowList.insert(12, output_data[1])
                rowList.insert(11, output_data[2])
                rowList.insert(14, output_data[3])
                rowList.insert(15, output_data[4])
                # print(type(rowList[15]))
                # rowList.insert(15,comments)
                row_data = tuple(rowList)
                # print("->",row_data)
                for column_number, data in enumerate(row_data):
                    self.stockList.setSortingEnabled(False)
                    self.stockList.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.stockList.setSortingEnabled(True)

    column_numbers = [2, 14, 15]

    # self.setColortoColumn(self.stockList,column_numbers, QColor(0, 255, 0))
    # self.setColortoColumn(self.stockList,2, QColor(0, 255, 0))
    # self.stockList.sortByColumn(11,Qt.AscendingOrder)
    # self.stockList.setSortingEnabled(True)
    # self.stockList.setSor

    self.buttonBox.addButton(self.resets, QDialogButtonBox.ResetRole)
    self.buttonBox.accepted.connect(self.accept)
    self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        # self.output="hi"
        super(update_stocks, self).accept()

    def clearAll(self):

        self.agencyEntry.setText("")
        self.exchangeEntry.setText("")
        self.equityEntry.setText("")
        self.trade_dateEntry.setDate(QDate.currentDate())
        self.trade_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.settle_dateEntry.setDate(QDate.currentDate())
        self.settle_dateEntry.setDisplayFormat("dd/MM/yyyy")
        self.trade_priceEntry.setText("")
        self.quantityEntry.setText("")
        self.unit_brockEntry.setText("")
        self.gst_brockEntry.setText("")
        self.stt_Entry.setText("")
        self.it_Entry.setText("")
        self.remarksEntry.setText("")


    def get_inp(self):
        return self.output







