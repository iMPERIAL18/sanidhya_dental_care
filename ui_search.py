# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\search.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(739, 637)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\001.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWindowOpacity(1.0)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 110, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 160, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(110, 210, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(110, 260, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.id = QtWidgets.QLineEdit(Dialog)
        self.id.setGeometry(QtCore.QRect(240, 120, 200, 22))
        self.id.setObjectName("id")
        self.name = QtWidgets.QLineEdit(Dialog)
        self.name.setGeometry(QtCore.QRect(240, 170, 350, 22))
        self.name.setReadOnly(True)
        self.name.setObjectName("name")
        self.phoneno = QtWidgets.QLineEdit(Dialog)
        self.phoneno.setGeometry(QtCore.QRect(240, 220, 350, 22))
        self.phoneno.setReadOnly(True)
        self.phoneno.setObjectName("phoneno")
        self.address = QtWidgets.QTextEdit(Dialog)
        self.address.setGeometry(QtCore.QRect(240, 270, 350, 120))
        self.address.setReadOnly(True)
        self.address.setObjectName("address")
        self.nextButton = QtWidgets.QPushButton(Dialog)
        self.nextButton.setGeometry(QtCore.QRect(270, 480, 100, 28))
        self.nextButton.setObjectName("nextButton")
        self.back = QtWidgets.QPushButton(Dialog)
        self.back.setGeometry(QtCore.QRect(420, 480, 100, 28))
        self.back.setObjectName("back")
        self.updateDetails = QtWidgets.QPushButton(Dialog)
        self.updateDetails.setGeometry(QtCore.QRect(270, 540, 250, 28))
        self.updateDetails.setObjectName("updateDetails")
        self.searchButton = QtWidgets.QPushButton(Dialog)
        self.searchButton.setGeometry(QtCore.QRect(460, 120, 130, 28))
        self.searchButton.setObjectName("searchButton")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(110, 410, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.N_O = QtWidgets.QComboBox(Dialog)
        self.N_O.setGeometry(QtCore.QRect(240, 410, 73, 22))
        self.N_O.setObjectName("N_O")
        self.N_O.addItem("")
        self.N_O.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Search"))
        self.label.setText(_translate("Dialog", "Patient ID"))
        self.label_2.setText(_translate("Dialog", "Name"))
        self.label_3.setText(_translate("Dialog", "Phone No"))
        self.label_4.setText(_translate("Dialog", "Address"))
        self.nextButton.setText(_translate("Dialog", "Next"))
        self.back.setText(_translate("Dialog", "Back"))
        self.updateDetails.setText(_translate("Dialog", "Update"))
        self.searchButton.setText(_translate("Dialog", "Search"))
        self.label_5.setText(_translate("Dialog", "Case"))
        self.N_O.setItemText(0, _translate("Dialog", "O"))
        self.N_O.setItemText(1, _translate("Dialog", "N"))