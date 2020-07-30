from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

# from db_management import con,cur

class purchase_list(QWidget):

    def __init__(self,agency,stocks):
        super().__init__()
        #self.setWindowTitle("Investment")
        #self.setGeometry(450,150,750,600)
        self.agencyList=agency
        self.stockList=stocks
        self.UI()
        self.show()


    def UI(self):
       self.widgets()
       self.layouts()


    def widgets(self):
        # for key, value in self.stockDB.items():
        #     print(key)
        #     for k1, val1 in value.items():
        #         print(k1, val1)
        # pass
        # self.agencyList=QListWidget()
        # for itm in self.listagency:
        #     self.agencyList.addItem(itm)
        #     self.agencyList.itemDoubleClicked.connect(self.showStocks)

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
        self.leftLayout.addWidget(self.agencyList)
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