

# BG: Light Blue Font COlor: Black
# xray fees
# import time 
# start = time.time()

from sys import argv
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QCalendarWidget, QCheckBox, QDialog, QApplication, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import sql_connector
from os import startfile, system



patient = 0

class Main(QDialog):
    def __init__(self):
        super(Main,self).__init__() 
        loadUi("main.ui",self)
        icon = '001.png'
        self.setWindowIcon(QIcon(icon))
        self.revenue.clicked.connect(self.gotorevenue)
        self.case_2.clicked.connect(self.gotocase)
        self.appointments.clicked.connect(self.gotoshow)
        self.report.clicked.connect(self.gotoreport)
        

        
    
    def gotorevenue(self):
        widget.setCurrentIndex(8)
        
    def gotocase(self):
        widget.setCurrentIndex(7)

    def gotoshow(self):
        widget.setCurrentIndex(10)

    def gotoreport(self):
        widget.setCurrentIndex(11)

    
   
class Case(QDialog):
    def __init__(self):
        super(Case,self).__init__() 
        loadUi("case.ui",self)
        self.new_case.clicked.connect(self.gotoregister)
        self.old_case.clicked.connect(self.gotosearch)
        self.homeButton.clicked.connect(self.gotohome)
     
    def gotosearch(self):
        
        widget.setCurrentIndex(2)
 
    def gotoregister(self):
        
        widget.setCurrentIndex(1)

    def gotohome(self):
        widget.setCurrentIndex(0)


## register patient using below class 

class RegisterPatient(QDialog):
    

    def __init__(self):
        super(RegisterPatient,self).__init__()
        loadUi("registerPatient.ui", self)
        self.addButton.clicked.connect(self.insertToDatabase)
        self.backButton.clicked.connect(self.gotocase)
        validator = QIntValidator()
        self.phoneno.setValidator(validator)
        


    def insertToDatabase(self):
    
        if len(self.history.toPlainText() and self.name.text() and self.address.toPlainText()) == 0:
            msg = QMessageBox()
            msg.setWindowTitle("")
            msg.setText("Name or History or Address cannot be empty")
            msg.setIcon(QMessageBox.Warning)

            x = msg.exec_()
        else:
            if self.phoneno.text() == '':
                phoneno = None
            else:
                phoneno = self.phoneno.text()
            name = self.name.text()
            address = self.address.toPlainText()
            history = self.history.toPlainText()
            case = self.N_O.currentText()
            try:
                if len(phoneno) < 10: 
                    raise ValueError 
                global patient 
                patient = sql_connector.Patient(name,phoneno,address,history,case)
                patient.insertPatient()
                msg = QMessageBox()
                msg.setWindowTitle("added to Database")
                msg.setText(f"Patient ID: {patient.p_id}")
                msg.setIcon(QMessageBox.Information)

                msg.buttonClicked.connect(self.xray)

                x = msg.exec_()
  
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("")
                msg.setText("Check the Phone Number")
                msg.setIcon(QMessageBox.Information)

                x = msg.exec_()

            
        
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

    # def popup(self,i):
    #     print(i.text())


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
            
            
            
        except TypeError:
            msg = QMessageBox()
            msg.setWindowTitle("Not Found")
            msg.setText("Patient not found")
            msg.setIcon(QMessageBox.Warning)
            self.name.clear()
            self.phoneno.clear()
            self.address.clear()
            x = msg.exec_()
            
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("Value error")
            msg.setText("Please Enter Number")
            msg.setIcon(QMessageBox.Warning)
            self.name.clear()
            self.phoneno.clear()
            self.address.clear()
            x = msg.exec_()

        

    def getPatient(self):
        try:
            global patient
            patient = sql_connector.Patient(self.details[1],self.details[2],self.details[3],self.details[4],self.N_O.currentText())
            patient.p_id = self.id.text()
            print(patient.p_id)
            patient.insertCase()
            print(self.N_O.currentText())
        except AttributeError:
            print("something Went Wrong")

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
        self.skipButton.clicked.connect(self.gotoappointment)

        

    def openFileDialog(self):
        dlg = QFileDialog()
        img = dlg.getOpenFileNames(self,filter = "Image (*jpg *png)",directory= r'D:\Hemin')
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
        self.homeButton.clicked.connect(self.gotohome)
        validator = QIntValidator()
        self.phoneno.setValidator(validator)
        self.id.setValidator(validator)

    def gotosearch(self):
        widget.setCurrentIndex(2)

    def gotohome(self):
        widget.setCurrentIndex(0)
        
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
        try:
            self.details = sql_connector.Patient.getPatient(int(self.id.text()))
            self.name.setText(self.details[1]) 
            self.phoneno.setText(str(self.details[2]))
            self.address.setText(self.details[3])
            self.history.setText(self.details[4])
        
        except TypeError:
            msg = QMessageBox()
            msg.setWindowTitle("Not Found")
            msg.setText("Patient not found")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()
            
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("Value error")
            msg.setText("Please Enter Number")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

    def updatePatient(self): 
        try:
            sql_connector.Patient.updatePatientDetails(self.id.text(),self.name.text(),self.phoneno.text(),self.address.toPlainText(),self.history.toPlainText()) 
            msg = QMessageBox()
            msg.setWindowTitle("UPDATED")
            msg.setText("Patient Inforamtion has been updated")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Something Went Wrong")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
    
class Appointment(QDialog):
    def __init__(self):
        super(Appointment,self).__init__()
        loadUi("appointment.ui",self)
        self.calander = self.findChild(QCalendarWidget, "calanderWidget")
        self.addButton.clicked.connect(self.bookAppointment)
        self.nextButton.clicked.connect(self.gotoinvoice)
        self.skipButton.clicked.connect(self.gotoinvoice)

    def bookAppointment(self):
        date = self.calander.selectedDate().toPyDate()
        global patient
        patient.insertAppointment(date)
        print("done")

    def gotoinvoice(self):
        # createInvoice.patientLabel.setText(f"Patient ID: {patient.getPatientId()}")
        # self.calander.setCurrentPage(2021,7)
        widget.setCurrentIndex(6)
        
class createInvoice(QDialog):
    def __init__(self) :
        # global patient
        super(createInvoice,self).__init__()
        loadUi("invoice.ui",self)
        self.finishButton.clicked.connect(self.invoice)
        # self.patientLabel.setText(f"Patient ID: {patient.getPatientId()}")
        self.pendingButton.clicked.connect(self.get_amount)
        self.autofillButton.toggled.connect(self.autofill)
        validator = QIntValidator()
        self.consulting.setValidator(validator)
        self.pending.setValidator(validator)
        self.paid.setValidator(validator)

    def invoice(self):
        try:
            global patient
            patient.createInvoice(self.consulting.text(),self.xray.text(),self.paid.text(),self.pending.text())
            print("done")
            patient = 0
            self.consulting.clear()
            self.paid.clear()
            self.pending.clear()
            self.xray.clear()
            widget.setCurrentIndex(7)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Something Went Wrong")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
    
            

    def get_amount(self):
        
        try:
            msg = QMessageBox()
            msg.setWindowTitle("Pending")
            msg.setText(f'''
            Patient ID: {patient.getPatientId()}

            Patient Name: {patient.getPatientName()}
            
            Pending Amount: {patient.get_amount()}
            ''')
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        except TypeError:
            msg = QMessageBox()
            msg.setWindowTitle("Pending")
            msg.setText(f'''
            Patient ID: {patient.getPatientId()}

            Patient Name: {patient.getPatientName()}
            
            Pending Amount: 0''')
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            
    def autofill(self):
        try:
            if self.autofillButton.isChecked():
                self.paid.setReadOnly(True)
                self.pending.setReadOnly(True)
                paid = int(self.paid.text())
                pending = patient.get_amount() - paid 
                self.pending.setText(f"{pending}")
            else:
                self.paid.setReadOnly(False)
                self.pending.setReadOnly(False)
                self.pending.setText("")
        except ValueError:
            
            msg = QMessageBox()
            msg.setWindowTitle("Pending")
            msg.setText("Paid Amount is empty")
            msg.setIcon(QMessageBox.Information) 
            x = msg.exec_()
            self.autofillButton.setChecked(False)
        except TypeError:
            	

            msg = QMessageBox()
            msg.setWindowTitle("")
            msg.setText("No Pending Amount Found")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            self.autofillButton.setChecked(False)
            
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
        url = sql_connector.GetRevenue()
        url = url.get_dailyRevenue()
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("Daily Revenue has been Generated")
        msg.setIcon(QMessageBox.Information)
        openFile = msg.addButton('Open File',QMessageBox.YesRole)
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()
        if msg.clickedButton() == openFile:
            startfile(url)
            system(url)

    def monthlyRev(self):
        url = sql_connector.GetRevenue()
        url = url.get_monthlyRevenue()
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("Monthly Revenue has been Generated")
        msg.setIcon(QMessageBox.Information)
        openFile = msg.addButton('Open File',QMessageBox.YesRole)
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()
        if msg.clickedButton() == openFile:
            startfile(url)
            system(url)

    def yearlyRev(self):
        url = sql_connector.GetRevenue()
        url = url.get_yearlyRevenue()
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("Yearly Revenue has been Generated")
        msg.setIcon(QMessageBox.Information)
        openFile = msg.addButton('Open File',QMessageBox.YesRole)
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()
        if msg.clickedButton() == openFile:
            startfile(url)
            system(url)

        

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
        url = sql_connector.GetRevenue()
        url = url.custom(date1, date2)
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("Yearly Revenue has been Generated")
        msg.setIcon(QMessageBox.Information)
        openFile = msg.addButton('Open File',QMessageBox.YesRole)
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()
        if msg.clickedButton() == openFile:
            startfile(url)
            system(url)


    def gotorev(self):
        widget.setCurrentIndex(8)

    def gotohome(self):
        widget.setCurrentIndex(0)
class ShowAppointment(QDialog):
    def __init__(self):
        super(ShowAppointment,self).__init__() 
        loadUi("showAppointments.ui",self)
        self.today.clicked.connect(self.todayAppointment)
        self.tmr.clicked.connect(self.tmrAppointment)
        self.homeButton.clicked.connect(self.gotohome)
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,120)
        self.tableWidget.setColumnWidth(3,125)
        

    def todayAppointment(self):
        values = sql_connector.Appointmemt()
        values = values.todaysAppointment()

        row = 0
        self.tableWidget.setRowCount(len(values))
        # for i in range(len(values)):
        #     for j in range(4):
        #         self.tableWidget.setItem(i, j, QTableWidgetItem(str(values[i][j]))) 

        for value in values:
            self.tableWidget.setItem(row,0,QTableWidgetItem(str(value[0])))
            self.tableWidget.setItem(row,1,QTableWidgetItem(str(value[1])))
            self.tableWidget.setItem(row,2,QTableWidgetItem(str(value[2])))
            self.tableWidget.setItem(row,3,QTableWidgetItem(str(value[3])))
            row += 1


        # Resize of the rows and columns based on the content
        # self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()

        self.tableWidget.show()

    def tmrAppointment(self):
        values = sql_connector.Appointmemt()
        values = values.tmrAppointment()
        row = 0
        self.tableWidget.setRowCount(len(values))
        for value in values:
            self.tableWidget.setItem(row,0,QTableWidgetItem(str(value[0])))
            self.tableWidget.setItem(row,1,QTableWidgetItem(str(value[1])))
            self.tableWidget.setItem(row,2,QTableWidgetItem(str(value[2])))
            self.tableWidget.setItem(row,3,QTableWidgetItem(str(value[3])))
            row += 1
    
    def gotohome(self):
        self.tableWidget.clearContents()
        widget.setCurrentIndex(0)


class Report(QDialog):
    def __init__(self):
        super(Report,self).__init__() 
        loadUi("report.ui",self)
        self.home.clicked.connect(self.gotohome)
        self.daily.clicked.connect(self.get_dailyreport)
        self.monthly.clicked.connect(self.get_monthlyreport)
        self.yearly.clicked.connect(self.get_yearlyreport)
        self.all.clicked.connect(self.get_alltimereport)

    def gotohome(self):
        widget.setCurrentIndex(0)

    def get_dailyreport(self):
        url = sql_connector.PatientReport()
        url = url.daily()
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("Daily report has been Generated")
        msg.setIcon(QMessageBox.Information)
        openFile = msg.addButton('Open File',QMessageBox.YesRole)
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()
        if msg.clickedButton() == openFile:
            startfile(url)
            system(url)

    def get_monthlyreport(self):
        url = sql_connector.PatientReport()
        url = url.monthly()
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("Monthly report has been Generated")
        msg.setIcon(QMessageBox.Information)
        openFile = msg.addButton('Open File',QMessageBox.YesRole)
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()
        if msg.clickedButton() == openFile:
            startfile(url)
            system(url)

    def get_yearlyreport(self):
        url = sql_connector.PatientReport()
        url = url.yearly()
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("Yearly report has been Generated")
        msg.setIcon(QMessageBox.Information)
        openFile = msg.addButton('Open File',QMessageBox.YesRole)
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()
        if msg.clickedButton() == openFile:
            startfile(url)
            system(url)

    def get_alltimereport(self):
        url = sql_connector.PatientReport()
        url = url.allTime()
        msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("Patient report has been Generated")
        msg.setIcon(QMessageBox.Information)
        openFile = msg.addButton('Open File',QMessageBox.YesRole)
        msg.setStandardButtons(QMessageBox.Cancel)
        x = msg.exec_()
        if msg.clickedButton() == openFile:
            startfile(url)
            system(url)

    


if __name__ == "__main__":
    app = QApplication(argv)
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
    show = ShowAppointment()
    report = Report()
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
    widget.addWidget(show)          # index: 10
    widget.addWidget(report)        # index: 11
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    app.exec_()
    # end = time.time()
    # print(end - start)