from datetime import datetime
from config import db
from app import Flask_app
from sqlalchemy.orm import relationship
# from sqlalchemy import DateTime,Foreignkey
from werkzeug.security import generate_password_hash,check_password_hash

    




class EMPLOYEE_DETAILS(db.Model):
   __tablename__ = "employeedetails"
 
 
 
   EMPLOYEE_ID = db.Column(db.Integer,autoincrement=True, primary_key=True)
   EMPLOYEE_NUMBER = db.Column(db.String(15),nullable=False)
   WORKER_TYPE = db.Column(db.String(15),nullable=False)
   FIRST_NAME = db.Column(db.String(150),nullable=False)
   MIDDLE_NAME = db.Column(db.String(150))
   LAST_NAME = db.Column(db.String(150),nullable=False)
   DATE_OF_JOINING = db.Column(db.Date,nullable = False)
   LOCATION = db.Column(db.String(150),nullable=False)
#    USER_ID = db.Column(db.Integer, db.ForeignKey('admindetails.USER_ID'), nullable=False)
   EMAIL_ID = db.Column(db.String(150),nullable=False)
   EFFECTIVE_START_DATE = db.Column(db.Date)
   EFFECTIVE_END_DATE = db.Column(db.Date)
   CREATED_BY = db.Column(db.String(150),nullable=False)
   LAST_UPDATED_BY = db.Column(db.String(150),nullable=False)
   CREATION_DATE = db.Column(db.DateTime, default=datetime.now)
   LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
   
 
 
   
   
 
   def serialize(self):
       return{
           "Employee_id" : self.EMPLOYEE_ID,
           "EMPLOYEE_NUMBER" : self.EMPLOYEE_NUMBER,
           "Employee_First_Name" : self.FIRST_NAME,
           "Middle_Name" : self.MIDDLE_NAME,
           "Last_Name" : self.LAST_NAME,
        #    'password' : self.password,
           "Date_of_Joining" : self.DATE_OF_JOINING,
           "EFFECTIVE_START_DATE" : self.EFFECTIVE_START_DATE,
           "EFFECTIVE_END_DATE" : self.EFFECTIVE_END_DATE,
           "WORKER_TYPE" : self.WORKER_TYPE,
           "Location" : self.LOCATION,
           "Email" : self.EMAIL_ID,
           "Creation_date" : self.CREATION_DATE,
           "Created_by" : self.CREATED_BY,
           "Last_Updated_Date" : self.LAST_UPDATED_DATE,
           "Last_Updated_by" : self.LAST_UPDATED_BY
       }

    



    
    