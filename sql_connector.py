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

            args = (self.p_id,date.today(),self.case)
            mycursor.callproc("insertCase",args)
            clinic_db.commit()

        except:
            print("error")

    @classmethod
    def getPatient(cls,id):
        mycursor.execute("SELECT name,phoneno,address FROM patients WHERE patient_id = %s",(id,))
        
        return mycursor.fetchone()

# def insertAppointment(id,date):
#     try:    
#         args = (id,date)
#         mycursor.callproc("insertAppointment",args)
#         clinic_db.commit()
#     except:
#         print("error")

# def get_yearlyRevenue():
#     try:    
#         mycursor.execute('SELECT * FROM yearly_revenue')
#         result = mycursor.fetchall()
#         print(result)
#     except:
#         print("error")

# def get_monthlyRevenue():
#     try:    
#         mycursor.execute('SELECT * FROM monthly_revenue')
#         result = mycursor.fetchall()
#         print(result)
#     except:
#         print("error")

# def get_dailyRevenue():
#     try:    
#         mycursor.execute('SELECT * FROM daily_revenue')
#         result = mycursor.fetchall()
#         print(result)
#     except:
#         print("error")

