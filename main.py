import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCalendarWidget, QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import sql_connector 
# import csv
patient = 0

class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__() 
        loadUi("main.ui",self)
        self.revenue.clicked.connect(self.gotorevenue)
        self.case_2.clicked.connect(self.gotocase)
    
    def gotorevenue(self):
        widget.setCurrentIndex(8)
        
    def gotocase(self):
        widget.setCurrentIndex(7)
   


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
                global patient 
                patientToRegister = sql_connector.Patient(name,phoneno,address,history,case)
                patientToRegister.insertPatient() 
                patient = patientToRegister
  
            except:
                print("failed to add patient")
            
        
    def xray(self):
        if patient.p_id != 0:
            self.name.clear()
            self.address.clear()
            self.history.clear()
            self.phoneno.clear()
            GoToXray.gotoxray(patient)
        else:
            print("failed to get id")
class SearchIntoDatabase(QDialog):
    
    

    def __init__(self) :
        super(SearchIntoDatabase,self).__init__()
        loadUi("search.ui",self)
        self.back.clicked.connect(self.gotocase)
        self.updateDetails.clicked.connect(self.gotoupdate)
        self.searchButton.clicked.connect(self.search)
        self.nextButton.clicked.connect(self.xray)
        
        

    def search(self):
        try:
            
            global patient
            details = sql_connector.Patient.getPatient(int(self.id.text()))
            self.name.setText(details[1]) 
            self.phoneno.setText(str(details[2]))
            self.address.setText(details[3])
            patientToSearch = sql_connector.Patient(details[1],details[2],details[3],details[4],'O')
            patientToSearch.p_id = self.id.text()
            print(patientToSearch.p_id)
            patientToSearch.insertCase()
            patient = patientToSearch
            
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
        if patient.p_id != 0:
            self.id.clear()
            self.name.clear()
            self.phoneno.clear()
            self.address.clear()
            GoToXray.gotoxray(patient)
        else:
            print("failed to get id")
        
        

class GoToXray():
    def gotoxray(self):
        widget.setCurrentIndex(4)
        
        

class Xray(QDialog):

    def __init__(self) :
        super(Xray,self).__init__()
        self.address = ''
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
            global patient
            patient.insertXray(self.address)
            print(patient.p_id)
            print("done")
        except:
            print("error")


    def gotoappointment(self):
        widget.setCurrentIndex(5)
        

class UpdateIntoDatabase(QDialog):
    def __init__(self) :
        super(UpdateIntoDatabase,self).__init__()
        loadUi("update.ui",self)
    

class Appointment(QDialog):
    def __init__(self):
        super(Appointment,self).__init__()
        loadUi("appointment.ui",self)
        self.calander = self.findChild(QCalendarWidget, "calanderWidget")
        self.addButton.clicked.connect(self.bookAppointment)
        self.nextButton.clicked.connect(self.gotoinvoice)

    def bookAppointment(self):
        date = self.calander.selectedDate().toPyDate()
        global patient
        patient.insertAppointment(date)
        print("done")

    def gotoinvoice(self):
        # self.calander.setCurrentPage(2021,7)
        widget.setCurrentIndex(6)
        
class createInvoice(QDialog):
    def __init__(self) :
        super(createInvoice,self).__init__()
        loadUi("invoice.ui",self)
        self.finishButton.clicked.connect(self.invoice)
        

    def invoice(self):
        global patient
        patient.createInvoice(self.consulting.text(),self.paid.text(),self.pending.text())
        print("done")
        widget.setCurrentIndex(0)

class Revenue(QDialog):
    def __init__(self) :
        super(Revenue,self).__init__()
        loadUi("revenue.ui",self)
        self.daily.clicked.connect(self.dailyRev)
        self.monthly.clicked.connect(self.monthlyRev)
        self.yearly.clicked.connect(self.yearlyRev)
        self.custom.clicked.connect(self.customRev)

    def dailyRev(self):
        sql_connector.GetRevenue.get_dailyRevenue()
        print("generated")

    def monthlyRev(self):
        sql_connector.GetRevenue.get_monthlyRevenue()
        print("generated")

    def yearlyRev(self):
        sql_connector.GetRevenue.get_yearlyRevenue()
        print("generated")

    def customRev(self):
        pass
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = Main()
    case = Case()
    patient = RegisterPatient() 
    search = SearchIntoDatabase()
    update = UpdateIntoDatabase()
    invoice = createInvoice()
    xray = Xray()
    appointment = Appointment()
    widget = QtWidgets.QStackedWidget()
    revenue = Revenue()

    #stacking Ui's
    widget.addWidget(mainwindow)    # index: 0   
    widget.addWidget(patient)       # index: 1
    widget.addWidget(search)        # index: 2
    widget.addWidget(update)        # index: 3
    widget.addWidget(xray)          # index: 4
    widget.addWidget(appointment)   # index: 5
    widget.addWidget(invoice)       # index: 6
    widget.addWidget(case)          # index: 7
    widget.addWidget(revenue)       # index: 8
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    app.exec_()
