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

    def __init__(self,name,phoneno,address,history):
        self.name = name
        self.phoneno = phoneno
        self.address = address
        self.history = history


    def insertPatient(self):
        try:    
            args = (self.name,self.phoneno,self.address,self.history)
            mycursor.callproc("insertPatient",args)
            clinic_db.commit()
        except:
            print("error")

    def insertCase(id,date,case):
        try:    
            args = (id,date,case)
            mycursor.callproc("insertCase",args)
            clinic_db.commit()
        except:
            print("error")

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