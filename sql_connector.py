from datetime import date
import mysql.connector  

# connecting database
try:
    clinic_db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@-B&E^wEEgqSm9u3',
        database = 'clinic'
    )
    mycursor = clinic_db.cursor()
except:
    print("failed to connect database")



class Patient:

    def __init__(self,name,phoneno,address,history,case):
        self.name = name
        self.phoneno = phoneno
        self.address = address
        self.history = history
        self.p_id = 0 
        self.case = case

    def insertPatient(self):
        try:    
            args = (self.name,self.phoneno,self.address,self.history)
            mycursor.callproc("insertPatient",args)
    

            mycursor.execute("SELECT MAX(patient_id) FROM patients")
            x = mycursor.fetchone()
            self.p_id = x[0] 
            self.insertCase()
            

        except:
            print("error")


    def insertCase(self):
        args = (self.p_id,date.today(),self.case)
        mycursor.callproc("insertCase",args)
        clinic_db.commit()

    
    def insertXray(self,address):    
        args = (self.p_id,address,date.today())
        mycursor.callproc("insertXray",args)
        clinic_db.commit()
        # except:
        #     print("error")


    @classmethod
    def getPatient(cls,id):
        mycursor.execute(f"SELECT * FROM patients WHERE patient_id = {id}")

        return mycursor.fetchone()

    
    
    def insertAppointment(self,date):
        try:    
            args = (self.p_id,date)
            mycursor.callproc("insertAppointment",args)
            clinic_db.commit()
        except:
            print("error")

    def createInvoice(self,consulting,paid,pending):
        args = (self.p_id,consulting,paid,pending)
        mycursor.callproc("createInvoice",args)
        clinic_db.commit()
    @classmethod
    def get_yearlyRevenue(cls):
        try:    
            mycursor.execute('SELECT * FROM yearly_revenue')
            return mycursor.fetchall()
            
        except:
            print("error")
            
    @classmethod
    def get_monthlyRevenue(cls):
        try:    
            mycursor.execute('SELECT * FROM monthly_revenue')
            result = mycursor.fetchall()
            return result
        except:
            print("error")

# def get_dailyRevenue():
#     try:    
#         mycursor.execute('SELECT * FROM daily_revenue')
#         result = mycursor.fetchall()
#         print(result)
#     except:
#         print("error")

