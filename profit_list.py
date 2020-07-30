from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class gain_shares(QWidget):

    def __init__(self):
        super().__init__()
        #self.setWindowTitle("Investment")
        #self.setGeometry(450,150,750,600)
        self.UI()
        self.show()


    def UI(self):
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.employeeList=QListWidget()
        self.btnNew=QPushButton("New")
        # self.btnNew.clicked.connect(self.addEmployee)
        self.btnUpdate=QPushButton("Update")
        self.btnDelete=QPushButton("Delete")



    def layouts(self):
        pass
