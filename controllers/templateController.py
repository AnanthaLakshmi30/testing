import mimetypes
from sqlalchemy import func
from flask import jsonify, request, send_file, session
from config import db
from Model.employeeData import *
from Model.userData import Admin
from Model.template import *
from io import BytesIO
import pandas as pd
import re
import pythoncom
import os
import win32com.client
from mimetypes import guess_type
# import magic
# from pyRTF import *


def addtemplate():
    try:
        file = request.files['TEMPLATE']
        temp = file.read()
        print(temp)
        temp_name = request.form['letterType']
        dbdata = Template.query.filter_by(TEMPLATE_NAME = temp_name ).first()
        if dbdata:
            dbdata.TEMPLATE_ID = dbdata.TEMPLATE_ID
            dbdata.TEMPLATE_NAME = dbdata.TEMPLATE_NAME
            dbdata.TEMPLATE_TYPE = file.mimetype
            dbdata.TEMPLATE_SIZE = len(temp)
            dbdata.TEMPLATE = temp
            dbdata.LAST_UPDATED_BY = 'HR'
            db.session.commit()
 
            return jsonify(f'{dbdata.TEMPLATE_NAME} template updated successfully'), 200
 
        details = Template(
            TEMPLATE_ID = request.form['letterId'],
            TEMPLATE_NAME = request.form['letterType'],
            TEMPLATE_TYPE = file.mimetype,
            TEMPLATE_SIZE = len(temp),
            TEMPLATE = temp,
            CREATED_BY = 'HR',
            LAST_UPDATED_BY = 'HR'
        )
        db.session.add(details)
        db.session.commit()
 
        return jsonify('template added successfully'),201
   
    except Exception as e:
        return jsonify({'error':str(e)}),500
 

def temp(TEMPLATE_ID):
    try:
        # temp = Template.query.filter_by(Template_name = Template_name).first()
        temp = Template.query.get(TEMPLATE_ID)
        print("Template_name",temp)

        file_obj = BytesIO(temp.TEMPLATE)
        
 
    # Return the file as a response
        return send_file(file_obj, mimetype=temp.TEMPLATE_TYPE)
    except Exception as e: 
        return jsonify({'error':str(e)}),500
    
def convertrtf(TEMPLATE_ID):
    try:
        temp = Template.query.filter(Template.TEMPLATE_ID==TEMPLATE_ID).one()
        print("temp",temp)
        x = temp.TEMPLATE
        print("x",x)
        

        file_obj = BytesIO(x)

        rtf_file_name = 'rtffile.rtf'
        pdf_file_name = 'pdffile.pdf'
        rtf_file_path = os.path.join(os.getcwd(), rtf_file_name)
        print("rtf_file_path",rtf_file_path)
        with open(rtf_file_path, 'wb') as file:
                file.write(file_obj.read())
        

        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(rtf_file_path)
        
        pdfpath = os.path.join(os.getcwd(), pdf_file_name)
        doc.SaveAs(pdfpath, FileFormat=17)
        print("pdfpath",pdfpath)
        doc.Close()
        word.Quit()
        pythoncom.CoUninitialize()
        os.remove(rtf_file_path)

        with open ('C:\\Angular\\HRIT- Project\\pdffile.pdf','rb') as file:
            a = file.read()

        file_obj = BytesIO(a)
        mimetype = mimetypes.MimeTypes().guess_type(pdf_file_name)[0]
        os.remove(pdfpath)
    # Return the file as a response
        return send_file(file_obj, mimetype=mimetype)    
    except Exception as e: 
        return jsonify({'error':str(e)}),500




def updatetemp(id):
    try:
        update = Template.query.get(id)
        data = request.files['TEMPLATE']
        temp = data.read()
       
        update.TEMPLATE = temp
        db.session.commit()
        return jsonify({'message': 'template changed successfully'}),200

    except Exception as e:
        return jsonify ({'error':str(e)}),500





