import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCalendarWidget, QCheckBox, QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import sql_connector
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
        self.backButton.clicked.connect(self.gotocase)
        


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

    def gotocase(self):
        self.name.clear()
        self.address.clear()
        self.history.clear()
        self.phoneno.clear()
        widget.setCurrentIndex(7)

class SearchIntoDatabase(QDialog):
    
    

    def __init__(self) :
        super(SearchIntoDatabase,self).__init__()
        loadUi("search.ui",self)
        self.back.clicked.connect(self.gotocase)
        self.updateDetails.clicked.connect(self.gotoupdate)
        self.searchButton.clicked.connect(self.search)
        self.nextButton.clicked.connect(self.getPatient)
        self.nextButton.clicked.connect(self.xray)

        
        

    def search(self):
        try:
            self.details = sql_connector.Patient.getPatient(int(self.id.text()))
            self.name.setText(self.details[1]) 
            self.phoneno.setText(str(self.details[2]))
            self.address.setText(self.details[3])
            
            
            
        except:
            print("sserror")

    def getPatient(self):
        global patient
        patientToSearch = sql_connector.Patient(self.details[1],self.details[2],self.details[3],self.details[4],self.N_O.currentText())
        patientToSearch.p_id = self.id.text()
        print(patientToSearch.p_id)
        patientToSearch.insertCase()
        patient = patientToSearch
        print(self.N_O.currentText())

    def gotocase(self):
        self.id.clear()
        self.name.clear()
        self.phoneno.clear()
        self.address.clear()
        widget.setCurrentIndex(7)

    def gotoupdate(self):
        self.id.clear()
        self.name.clear()
        self.phoneno.clear()
        self.address.clear()
        widget.setCurrentIndex(3)

    def xray(self):
        try:
            if patient.p_id != 0:
                self.id.clear()
                self.name.clear()
                self.phoneno.clear()
                self.address.clear()
                GoToXray.gotoxray(patient)
            else:
                print("failed to get id")
        except:
            print("error")
        
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
        self.path.clear()
        widget.setCurrentIndex(5)
        
class UpdateIntoDatabase(QDialog):
    def __init__(self) :
        super(UpdateIntoDatabase,self).__init__()
        loadUi("update.ui",self)
        self.backButton.clicked.connect(self.gotosearch)
        self.nameBox.stateChanged.connect(self.namecheckBoxChanged)
        self.phoneBox.stateChanged.connect(self.phonecheckBoxChanged)
        self.addressBox.stateChanged.connect(self.addresscheckBoxChanged)
        self.historyBox.stateChanged.connect(self.historycheckBoxChanged)
        self.searchButton.clicked.connect(self.searchPatient)
        self.updateButton.clicked.connect(self.updatePatient)

    def gotosearch(self):
        widget.setCurrentIndex(2)
        
    def namecheckBoxChanged(self,state):
        if state == Qt.Checked:
            self.name.setReadOnly(False)
        else:
            self.name.setReadOnly(True)
        
    def phonecheckBoxChanged(self,state):
        if state == Qt.Checked:
            self.phoneno.setReadOnly(False)
        else:
            self.phoneno.setReadOnly(True)

    def addresscheckBoxChanged(self,state):
        if state == Qt.Checked:
            self.address.setReadOnly(False)
        else:
            self.address.setReadOnly(True)

    def historycheckBoxChanged(self,state):
        if state == Qt.Checked:
            self.history.setReadOnly(False)
        else:
            self.history.setReadOnly(True)

    def searchPatient(self):
        self.details = sql_connector.Patient.getPatient(int(self.id.text()))
        self.name.setText(self.details[1]) 
        self.phoneno.setText(str(self.details[2]))
        self.address.setText(self.details[3])
        self.history.setText(self.details[4])
        

    def updatePatient(self):
        
        
        sql_connector.Patient.updatePatientDetails(self.id.text(),self.name.text(),self.phoneno.text(),self.address.toPlainText(),self.history.toPlainText()) 
        print("updated")

    
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
        patient = 0
        self.consulting.clear()
        self.paid.clear()
        self.pending.clear()
        widget.setCurrentIndex(7)

class Revenue(QDialog):
    def __init__(self) :
        super(Revenue,self).__init__()
        loadUi("revenue.ui",self)
        self.daily.clicked.connect(self.dailyRev)
        self.monthly.clicked.connect(self.monthlyRev)
        self.yearly.clicked.connect(self.yearlyRev)
        self.custom.clicked.connect(self.gotocustomRev)
        self.homeButton.clicked.connect(self.gotohome)

    def dailyRev(self):
        sql_connector.GetRevenue.get_dailyRevenue()
        print("generated")

    def monthlyRev(self):
        sql_connector.GetRevenue.get_monthlyRevenue()
        print("generated")

    def yearlyRev(self):
        sql_connector.GetRevenue.get_yearlyRevenue()
        print("generated")

    def gotocustomRev(self):
        widget.setCurrentIndex(9)

    def gotohome(self):
        widget.setCurrentIndex(0)
        
class CustomRev(QDialog):
    def __init__(self) :
        super(CustomRev,self).__init__()
        loadUi("custom.ui",self)
        self.calander1 = self.findChild(QCalendarWidget, "date1")
        self.calander2 = self.findChild(QCalendarWidget, "date2")
        self.generate.clicked.connect(self.generateRev) 
        self.backButton.clicked.connect(self.gotorev)
        self.homeButton.clicked.connect(self.gotohome)

    def generateRev(self):
        date1 = self.calander1.selectedDate().toPyDate()
        date2 = self.calander2.selectedDate().toPyDate()
        sql_connector.GetRevenue.custom(date1, date2)
        print("generated")

    def gotorev(self):
        widget.setCurrentIndex(8)

    def gotohome(self):
        widget.setCurrentIndex(0)
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
    custom = CustomRev()
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
    widget.addWidget(custom)        # index: 9
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    app.exec_()

