
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCalendarWidget, QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import sql_connector 
import csv

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

    patient = 0
    def __init__(self):
        super(RegisterPatient,self).__init__()
        loadUi("registerPatient.ui", self)
        self.addButton.clicked.connect(self.insertToDatabase)
        self.nextButton.clicked.connect(self.xray)
        


    def insertToDatabase(self):
        
        if self.phoneno.text() == '':
            phoneno = None
        else:
            try:
                phoneno = int(self.phoneno.text())
            except:
                print("cant convert to integer")
        
        if len(self.history.toPlainText() and self.name.text() and self.address.toPlainText()) == 0:
            print("error")
        else:
            name = self.name.text()
            address = self.address.toPlainText()
            history = self.history.toPlainText()
            case = self.N_O.currentText()
            try:
                # global patientToRegister 
                patientToRegister = sql_connector.Patient(name,phoneno,address,history,case)
                patientToRegister.insertPatient() 
                RegisterPatient.patient = patientToRegister

                
                
              
            except:
                print("failed to add patient")
            
        
    def xray(self):
        if RegisterPatient.patient.p_id != 0:
            self.name.clear()
            self.address.clear()
            self.history.clear()
            self.phoneno.clear()
            GoToXray.gotoxray(self,1,RegisterPatient.patient)
        else:
            print("failed to get id")
class SearchIntoDatabase(QDialog):
    
    patient = 0

    def __init__(self) :
        super(SearchIntoDatabase,self).__init__()
        loadUi("search.ui",self)
        self.back.clicked.connect(self.gotocase)
        self.updateDetails.clicked.connect(self.gotoupdate)
        self.searchButton.clicked.connect(self.search)
        self.nextButton.clicked.connect(self.xray)
        
        

    def search(self):
        try:
            
            
            details = sql_connector.Patient.getPatient(int(self.id.text()))
            self.name.setText(details[1]) 
            self.phoneno.setText(str(details[2]))
            self.address.setText(details[3])
            patientToSearch = sql_connector.Patient(details[1],details[2],details[3],details[4],'O')
            patientToSearch.p_id = self.id.text()
            patientToSearch.insertCase()
            SearchIntoDatabase.patient = patientToSearch
            
        except:
            print("sserror")

    def gotocase(self):
        self.id.clear()
        self.name.clear()
        self.phoneno.clear()
        self.address.clear()
        widget.setCurrentIndex(0)

    def gotoupdate(self):
        self.id.clear()
        self.name.clear()
        self.phoneno.clear()
        self.address.clear()
        widget.setCurrentIndex(3)

    def xray(self):
        if SearchIntoDatabase.patient.p_id != 0:
            self.id.clear()
            self.name.clear()
            self.phoneno.clear()
            self.address.clear()
            GoToXray.gotoxray(self,2,SearchIntoDatabase.patient)
        else:
            print("failed to get id")
        
        

class GoToXray(SearchIntoDatabase, RegisterPatient):
    def gotoxray(self,index,obj):
        if index == 2:
            obj = SearchIntoDatabase.patient
        
        elif index == 1:
            obj =RegisterPatient.patient 
            

        xray = Xray(obj)
        widget.addWidget(xray)          # index: 4
        widget.setCurrentIndex(4)

        

class Xray(QDialog):

    def __init__(self,patient) :
        super(Xray,self).__init__()
        self.address = ''
        self.patient = patient
        loadUi("xray.ui",self)
        self.browseButton.clicked.connect(self.openFileDialog)
        self.addButton.clicked.connect(self.addtoDatabase)
        self.nextButton.clicked.connect(self.gotoappointment)

        

    def openFileDialog(self):
        img = QFileDialog.getOpenFileNames()
        if img[0] != []:
            self.address = img[0][0]
            self.path.setText(self.address)

    
        
        

        


    def addtoDatabase(self):
        try:
            self.patient.insertXray(self.address)
            print("done")
        except:
            print("error")


    def gotoappointment(self):
        appointment = Appointment(self.patient)
        widget.addWidget(appointment)
        widget.setCurrentIndex(5)
        

class UpdateIntoDatabase(QDialog):
    def __init__(self) :
        super(UpdateIntoDatabase,self).__init__()
        loadUi("update.ui",self)
        self.updateButton.clicked.connect(self.month)

    def month(self):
            
        rows = sql_connector.Patient.get_yearlyRevenue() 
        fp = open('C:/Users/ASUS/Desktop/m.csv', 'w')
        myFile = csv.writer(fp)
        myFile.writerows(rows)
        fp.close()

    

class Appointment(QDialog):
    def __init__(self,patient):
        super(Appointment,self).__init__()
        self.patient = patient 
        loadUi("appointment.ui",self)
        self.calander = self.findChild(QCalendarWidget, "calanderWidget")
        self.addButton.clicked.connect(self.bookAppointment)
        self.nextButton.clicked.connect(self.gotoinvoice)

    def bookAppointment(self):
        date = self.calander.selectedDate().toPyDate()
        
        self.patient.insertAppointment(date)
        print("done")

    def gotoinvoice(self):
        # self.calander.setCurrentPage(2021,7)
        invoice = createInvoice(self.patient)
        widget.addWidget(invoice)
        widget.setCurrentIndex(6)
        
class createInvoice(QDialog):
    def __init__(self,patient) :
        super(createInvoice,self).__init__()
        self.patient = patient
        loadUi("invoice.ui",self)
        self.finishButton.clicked.connect(self.invoice)
        

    def invoice(self):
        
        self.patient.createInvoice(self.consulting.text(),self.paid.text(),self.pending.text())
        print("done")
        widget.setCurrentIndex(0)

        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = Case()
    patient = RegisterPatient() 
    search = SearchIntoDatabase()
    update = UpdateIntoDatabase()
    widget = QtWidgets.QStackedWidget()
    #stacking Ui's
    widget.addWidget(mainwindow)    
    widget.addWidget(patient)
    widget.addWidget(search)
    widget.addWidget(update)


    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    app.exec_()
