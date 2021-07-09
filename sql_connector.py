from datetime import date
import mysql.connector  
from pandas import read_sql_query, DataFrame

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
            
    

def get_dailyRevenue():
    try:    
        mycursor.execute('SELECT * FROM daily_revenue')
        result = mycursor.fetchall()
        print(result)
    except:
        print("error")

class GetRevenue:
    @classmethod
    def get_monthlyRevenue(cls):
        try:    
            sql_query = read_sql_query("SELECT * FROM monthly_revenue",clinic_db) 

            fileName = "monthlyRevenue" + date.today().strftime("%d%m%Y")               

            df = DataFrame(sql_query)
            df.to_csv(f"C:/Users/ASUS/Documents/LabVIEW Data/{fileName}.csv", index = False)   # change the path at last
        except:
            print("error")

    @classmethod
    def get_dailyRevenue(cls):
        try:    
            sql_query = read_sql_query("SELECT * FROM daily_revenue",clinic_db) 

            fileName = "dailyRevenue" + date.today().strftime("%d%m%Y")               

            df = DataFrame(sql_query)
            df.to_csv(f"C:/Users/ASUS/Documents/LabVIEW Data/{fileName}.csv", index = False)   # change the path at last
        except:
            print("error")

    @classmethod
    def get_yearlyRevenue(cls):
        try:    
            sql_query = read_sql_query("SELECT * FROM yearly_revenue",clinic_db) 

            fileName = "yearlyRevenue" + date.today().strftime("%d%m%Y")               

            df = DataFrame(sql_query)
            df.to_csv(f"C:/Users/ASUS/Documents/LabVIEW Data/{fileName}.csv", index = False)   # change the path at last
        except:
            print("error")

    @classmethod
    def custom(cls,date1,date2):
           
        sql_query = read_sql_query(f'''SELECT i.invoice_id,p.name,i.payment_date,i.payment AS payment_amount FROM invoices i INNER JOIN patients p ON p.patient_id = i.patient_id WHERE i.payment_date BETWEEN {date1} AND {date2}''',clinic_db) 

        fileName = "customRevenue" + date.today().strftime("%d%m%Y")        #date1 + to + date2 + date.today().strftime("%d%m%Y")              

        df = DataFrame(sql_query)
        df.to_csv(f"C:/Users/ASUS/Documents/LabVIEW Data/{fileName}.csv", index = False)   # change the path at last
        

        