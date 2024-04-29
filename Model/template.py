from datetime import datetime
from config import db
from app import Flask_app
from sqlalchemy import Column, Integer, String, DateTime






class Template(db.Model):
   __tablename__ = 'templatedb'

   TEMPLATE_ID = db.Column(db.String(15),primary_key=True)
   TEMPLATE_NAME = db.Column(db.String(150),nullable = False)
   TEMPLATE = db.Column(db.LargeBinary(length=20 * (1024 * 1024)))
   TEMPLATE_SIZE = db.Column(db.Integer)
   TEMPLATE_TYPE = db.Column(db.String(150))
   CREATED_BY = db.Column(db.String(150))
   LAST_UPDATED_BY = db.Column(db.String(150))
   CREATION_DATE = db.Column(db.DateTime, default=datetime.now)
   LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


   def serialize(self):
        return{
            'TEMPLATE_ID' : self.TEMPLATE_ID,
            'TEMPLATE_NAME' : self.TEMPLATE_NAME,
            'TEMPLATE' : self.TEMPLATE,
            'TEMPLATE_TYPE' :self.TEMPLATE_TYPE,
            'CREATED_BY' : self.CREATED_BY,
            'CREATED_AT' : self.CREATED_AT,
            'LAST_UPDATED_BY' : self.LAST_UPDATED_BY,
            'UPDATED_AT' : self.UPDATED_AT
        }
   