from datetime import datetime
from config import db
from app import Flask_app
from sqlalchemy.orm import relationship


class Address(db.Model):
   __tablename__ = "addressdetails"


   ADDRESS_ID = db.Column(db.Integer, autoincrement=True, primary_key=True)               		
   EMPLOYEE_ID = db.Column(db.Integer, db.ForeignKey('employeedetails.EMPLOYEE_ID'))	
   ADDRESS_TYPE	= db.Column(db.String(15))		
   ADDRESS = db.Column(db.String(15),nullable=False)	
   CITY	= db.Column(db.String(15),nullable=False)
   STATE = db.Column(db.String(15),nullable=False)					
   COUNTRY = db.Column(db.String(15),nullable=False)			
   PIN_CODE	= db.Column(db.String(15),nullable=False)			
   DATE_FROM = db.Column(db.Date,nullable = False)			
   DATE_TO = db.Column(db.Date)				
   CREATED_BY = db.Column(db.String(150))
   LAST_UPDATED_BY = db.Column(db.String(150))
   CREATION_DATE = db.Column(db.DateTime, default=datetime.now)
   LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)