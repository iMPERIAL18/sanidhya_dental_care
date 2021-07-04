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
        self.old_case.clicked.connect(self.gotosearch)


    def gotosearch(self):
        widget.setCurrentIndex(2)

    def gotoregister(self):
        widget.setCurrentIndex(1)

class RegisterPatient(QDialog):
    def __init__(self):
        super(RegisterPatient,self).__init__()
        loadUi("registerPatient.ui", self)
        self.nextButton.clicked.connect(self.insertToDatabase)

    def insertToDatabase(self):
        
        if self.phoneno.text() == '':
            phoneno = None
        else:
            phoneno = int(self.phoneno.text())

        
        if len(self.history.toPlainText() and self.name.text() and self.address.toPlainText()) == 0:
            print("error")
        else:
            name = self.name.text()
            address = self.address.toPlainText()
            history = self.history.toPlainText()
            case = self.N_O.currentText()
            try:
                patient = sql_connector.Patient(name,phoneno,address,history,case)
                patient.insertPatient() 
                print(patient.p_id)
            except:
                print("failed to add patient")
 
        
class SearchIntoDatabase(QDialog):
    def __init__(self) :
        super(SearchIntoDatabase,self).__init__()
        loadUi("search.ui",self)
        self.back.clicked.connect(self.gotocase)
        self.updateDetails.clicked.connect(self.gotoupdate)
        self.searchButton.clicked.connect(self.search)
        

    def search(self):
        details = sql_connector.Patient.getPatient(int(self.id.text()))
        self.name.setText(details[0]) 
        self.phoneno.setText(str(details[1]))
        self.address.setText(details[2])

    def gotocase(self):
        widget.setCurrentIndex(0)

    def gotoupdate(self):
        widget.setCurrentIndex(3)

class UpdateIntoDatabase(QDialog):
    def __init__(self) :
        super(UpdateIntoDatabase,self).__init__()
        loadUi("update.ui",self)








if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = Case()
    patient = RegisterPatient() 
    search = SearchIntoDatabase()
    update = UpdateIntoDatabase()
    widget = QtWidgets.QStackedWidget()
    #stacking Ui's
    widget.addWidget(mainwindow)    # index: 0
    widget.addWidget(patient)       # index: 1
    widget.addWidget(search)        # index: 2
    widget.addWidget(update)        # index: 3 

    widget.show()
    app.exec_()