# from PyQt5.QtGui import QGroupBox, QCheckBox, QDialog, QHBoxLayout
#
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
#
#
# def toggleGroupBox(state):
#     if state > 0:
#         gb.setEnabled(True)
#     else:
#         gb.setEnabled(False)
#
# d = QDialog()
# gb = QGroupBox("Groupbox")
# gb.setEnabled(False)
# cb = QCheckBox("Set active")
# l = QHBoxLayout(d)
# l.addWidget(gb)
# l.addWidget(cb)
# cb.stateChanged.connect(toggleGroupBox)
# d.show()

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,pyqtSlot
import sys

#
# class GroupBox(QWidget):
#
#     def __init__(self):
#         QWidget.__init__(self)
#
#         self.setWindowTitle("GroupBox")
#         layout = QGridLayout()
#         self.setLayout(layout)
#
#         groupbox = QGroupBox("GroupBox Example")
#         groupbox.setCheckable(True)
#         layout.addWidget(groupbox)
#
#         vbox = QVBoxLayout()
#         groupbox.setLayout(vbox)
#
#         radiobutton = QRadioButton("RadioButton 1")
#         vbox.addWidget(radiobutton)
#
#         radiobutton = QRadioButton("RadioButton 2")
#         vbox.addWidget(radiobutton)
#
#         radiobutton = QRadioButton("RadioButton 3")
#         vbox.addWidget(radiobutton)
#
#         radiobutton = QRadioButton("RadioButton 4")
#         vbox.addWidget(radiobutton)
#
#
# app = QApplication(sys.argv)
# screen = GroupBox()
# screen.show()
# sys.exit(app.exec_())

class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.mylayout=QVBoxLayout()

        self.label1=QLabel("Input1")
        self.checks1=QCheckBox()
        self.checks1.setChecked (False)
        self.checks1.toggled.connect(self.onToggled1)
        self.toggle_button = QToolButton(text="", checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.setEnabled(False)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.control1=QHBoxLayout()
        self.control1.addWidget(self.label1)
        self.control1.addWidget(self.toggle_button)
        self.control1.addWidget(self.checks1)


        # self.toggle_button.pressed.connect(self.on_pressed)

        self.checks2 = QCheckBox("check ?")
        self.checks2.setChecked(False)
        self.checks2.toggled.connect(self.onToggled2)
        # self.arrow1 = Qt.RightArrow()


        self.mylayout.addLayout(self.control1)
        self.GroupBox1 = QGroupBox('rotor')
        self.GroupBox1.hide()
        self.mylayout.addWidget(self.GroupBox1)

        self.mylayout.addWidget(self.checks2)
        self.GroupBox2 = QGroupBox('blade')
        self.GroupBox2.hide()
        self.mylayout.addWidget(self.GroupBox2)


        self.setLayout(self.mylayout)

        self.glayout1=QVBoxLayout()
        self.GroupBox1.setLayout(self.glayout1)
        self.input1=QLineEdit("length")
        self.input2=QLineEdit("width")
        self.glayout1.addWidget(self.input1)
        self.glayout1.addWidget(self.input2)

        self.glayout2 = QVBoxLayout()
        self.GroupBox2.setLayout(self.glayout2)
        self.input3 = QLineEdit("length")
        self.input4 = QLineEdit("width")
        self.glayout2.addWidget(self.input3)
        self.glayout2.addWidget(self.input4)


        # for i in range(1):
        #     checkbox = QCheckBox("{}".format(i), self.GroupBox)
        #     self.glayout.addWidget(checkbox)

        # self.mylayout.addLayout(self.GroupBox)        #
        # # self.layout().addWidget(self.GroupBox)
        # self.GroupBox.toggled.connect(self.onToggled)
        # self.GroupBox.setCheckable(True)

    @pyqtSlot()
    def on_pressed(self):
        if self.checks1.isChecked():
            if self.GroupBox1.isHidden():
                self.toggle_button.setArrowType(Qt.DownArrow)
                self.GroupBox1.show()
            elif not self.GroupBox1.isHidden():
                self.toggle_button.setArrowType(Qt.RightArrow)
                self.GroupBox1.hide()

        self.setFixedSize(self.mylayout.sizeHint())




    def onToggled1(self, on):
        if not on:
            self.GroupBox1.hide()
            self.toggle_button.setArrowType(Qt.RightArrow)
            self.toggle_button.setEnabled(False)
        else:
            self.toggle_button.setArrowType(Qt.DownArrow)
            self.toggle_button.setEnabled(True)
            self.GroupBox1.show()
            self.GroupBox2.hide()
        self.setFixedSize(self.mylayout.sizeHint())

    def onToggled2(self, on):
        if not on:
            self.GroupBox2.hide()
        else:
            self.GroupBox2.show()
            self.GroupBox1.hide()
        self.setFixedSize(self.mylayout.sizeHint())

        # for box in self.sender().findChildren(QCheckBox):
        #     box.setChecked(on)
        #     box.setEnabled(True)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())