import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sql_connector 

class Case(QDialog):
    def __init__(self):
        super(Case,self).__init__()
        loadUi("case.ui",self)
        self.new_case.clicked.connect(self.gotoregister)
        self.old_case.clicked.connect(self.pr)

    def pr(self):
        print("clicked")

    def gotoregister(self):
        register = RegisterPatient()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RegisterPatient(QDialog):
    def __init__(self):
        super(RegisterPatient,self).__init__()
        loadUi("registerPatient.ui", self)
        self.nextButton.clicked.connect(self.insertToDatabase)

    def insertToDatabase(self):
        name = self.name.text()
        phoneno = int(self.phoneno.text())
        address = self.address.toPlainText()
        history = self.history.toPlainText()

        try:
            patient = sql_connector.Patient(name,phoneno,address,history)
            patient.insertPatient()
            print("added without any error")
        except:
            print("failed to add patient")
        

        



app = QApplication(sys.argv)
mainwindow = Case()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)    
widget.show()
app.exec_()