from base64 import encode
from datetime import date, timedelta
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from sqlalchemy import func
from flask import jsonify, request, session
from config import db
from Model.employeeData import *
from Model.userData import Admin

# import bcrypt
from config import db, bcrypt
from werkzeug.security import generate_password_hash,check_password_hash
import re
import random
import smtplib
import ssl
from email.message import EmailMessage
import os

from sqlalchemy.exc import IntegrityError





    
# add employee details[POST Method]
def addEmployee():
    data = request.json
    e_id = data.get('Email_Id')
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, e_id):
        email = e_id
    else:
        return jsonify ({'error' : 'Invalid email'})
   
    existing_emp = EMPLOYEE_DETAILS.query.filter_by(EMAIL_ID = e_id).first()
    print("existing_emp",existing_emp)
    if existing_emp:
        return jsonify({'message':f'email {e_id} already exist '}), 400
   
    try:
       
        required_fields = ['Employee_Number','First_Name','Last_Name','Worker_Type','Effective_Start_Date','Date_Of_Joining','Location','Email_Id']
        returnData = []
        if not data:
            return jsonify ({'error': 'data is required'}),400
        for i in required_fields:
            print("a",i)
            if i not in data:
                returnData.append(f'{i} is required')
 
                print("returnData",returnData)
               
        if returnData:
            return jsonify({'message':returnData}),400
       
       
        details = EMPLOYEE_DETAILS(
           
                    EMPLOYEE_NUMBER = data['Employee_Number'],
                    FIRST_NAME = data['First_Name'],
                    MIDDLE_NAME = data['Middle_Name'],
                    LAST_NAME = data['Last_Name'],
                    WORKER_TYPE = data['Worker_Type'],
                    DATE_OF_JOINING = data['Date_Of_Joining'],
                    EFFECTIVE_START_DATE = data['Effective_Start_Date'],
                    EFFECTIVE_END_DATE = data['Effective_End_Date'] if data['Effective_End_Date'] else date(4712, 12, 31),
                    LOCATION = data['Location'],
                    EMAIL_ID =email,
                    CREATED_BY = 'HRName',
                    LAST_UPDATED_BY = "HRName")
 
        db.session.add(details)
        db.session.commit()
 
        return jsonify({'details': details.serialize()}), 201
           
    except Exception as e:
        return jsonify({'error':str(e)}),500


# add bulk employee details[POST Method]
def addbulk():
    try:
        excel = request.files['EXCEL']
        df = pd.read_excel(excel,sheet_name=0)
        print("df[Name]",df)
        # userEmail='sowmya@gmail.com'
        # print(userEmail)
        # user = Admin.query.filter_by(EMAIL_ID=userEmail).first()
        # user = Admin.query.get(1)
 
       
       
        returndata =[]
        for index,row in df.iterrows():
            e_id = row.get('Email_Id')
            e_no = row.get('Employee_Number')
 
            temp = row['Date_Of_Joining']
            print("row",temp)
 
            existing_emp = EMPLOYEE_DETAILS.query.filter_by(EMAIL_ID = e_id).all()
            emp_no = EMPLOYEE_DETAILS.query.filter_by(EMPLOYEE_NUMBER = e_no).all()
            print("existing_emp",existing_emp,emp_no)
            if existing_emp:
                return jsonify({'message':f'email {e_id} already exist '}), 400
            if emp_no:
                return jsonify({'message': f'employee number {e_no} already exist'}), 400
           
            if type(row.get('Middle_Name')) != float:
                middleName = row.get('Middle_Name')
 
            else:
                middleName = None
 
           
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern, row['Email_Id']):
                email = row['Email_Id']
            else:
                return jsonify ({'error' : 'Invalid email'})
           
            print("row['Effective_Start_Date']",row['Effective_Start_Date'])
            print("row['Date_Of_Joining']",row['Date_Of_Joining'])
           
   
            details = EMPLOYEE_DETAILS(EMPLOYEE_NUMBER = row['Employee_Number'],
                                       FIRST_NAME =row['First_Name'],
                                       MIDDLE_NAME = middleName,
                                       LAST_NAME =row['Last_Name'],
                                       DATE_OF_JOINING =row['Date_Of_Joining'],
                                       LOCATION =row['Location'],
                                       EFFECTIVE_START_DATE =row['Effective_Start_Date'],
                                       EFFECTIVE_END_DATE = '4712-12-31',
                                       WORKER_TYPE = row['Worker_Type'],
                                    #    USER_ID =user.USER_ID,
                                       EMAIL_ID =email,
                                       CREATED_BY = 'HR',
                                       LAST_UPDATED_BY = 'HR')
            print("sdvjvosvkm")
            print("details['EFFECTIVE_START_DATE']",details.EFFECTIVE_START_DATE.strftime('%Y-%m-%d'))
            temp = {
                "Employee_id" : details.EMPLOYEE_ID,
                "Employee_Number" : details.EMPLOYEE_NUMBER,
                "Employee_First_Name" : details.FIRST_NAME,
                "Middle_Name" : details.MIDDLE_NAME,
                "Last_Name" : details.LAST_NAME,
                "Date_of_Joining" : details.DATE_OF_JOINING.strftime('%Y-%m-%d'),
                "EFFECTIVE_START_DATE" : details.EFFECTIVE_START_DATE.strftime('%Y-%m-%d'),
                "EFFECTIVE_END_DATE" : details.EFFECTIVE_END_DATE,
                "Location" : details.LOCATION,
                "Email" : details.EMAIL_ID
            }
            details.EFFECTIVE_START_DATE = details.EFFECTIVE_START_DATE.strftime('%Y-%m-%d')
            # details['EFFECTIVE_START_DATE']=details['EFFECTIVE_START_DATE'].
            returndata.append(temp)
            # break
 
            db.session.add(details)
            print("asdfghj")
        db.session.commit()
        print("returndata",returndata)
        return jsonify({"message":"Bulk Upload Successfully",'details': returndata}), 201
           
    # except IntegrityError as e:
    #     return jsonify({'error': 'Unique key violation. This operation would result in duplicate data.'}), 400
    except Exception as e:
        return jsonify({'error':str(e)}),500


# get all employees[GET Method]
def getEmployee():
    try:
        get=EMPLOYEE_DETAILS.query.all()
        returndata=[]
        if not get:
            return jsonify({'message': f'person {id} not found'}),404
        for i in get:
            returndata.append(i.serialize())
        return jsonify({'data': returndata}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

# get employee by id[GET Method]
def getEmployeeById(id):
    try:
        person =EMPLOYEE_DETAILS.query.get(id)
        print('person',person)
        if not person:
            return jsonify({'message': f'person {id} not found'}),404
        print("person.serialize()",person.serialize())
        return jsonify({'data' : person.serialize()}),200
    except Exception as e:
        return jsonify({'error':str(e)}),500
    
# update employee details by id[PUT Method]
def updateemp(id):
    try:
        data = request.json
        e_id = data.get('Email_Id')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, data['Email_Id']):
                email = data.get('Email_Id')
 
        dbdata = EMPLOYEE_DETAILS.query.get(id)
       
        # existing_emp = EMPLOYEE_DETAILS.query.filter_by(EMPLOYEE_NO =data.get('Employee_No')).first()
        print("existing_emp",dbdata)
        if  dbdata.EMAIL_ID == e_id and dbdata.EMPLOYEE_NUMBER == data.get('Employee_Number'):
            # return jsonify({"message":"email already exist"})
       
            print("data",data)
            # email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            # if re.match(email_pattern, data['Email_Id']):
            #     email = data.get('Email_Id')
           
            dbdata = EMPLOYEE_DETAILS.query.get(id)
            Datedb = str(data['Effective_Start_Date'])
            Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
            date = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
       
            if date <= Datedb and data.get('Employee_Number').startswith('C'):
               
                print("dfghj",data.get('Employee_Number').startswith('C'))
                for i in data:
                    print("i",i)
                    cap = i.upper()
                    new_value = data.get(i)
                    print("new_value",new_value)
                    if getattr(dbdata,cap) != new_value:
                        print("new_value",new_value)
                        setattr(dbdata,cap,new_value)
                db.session.commit()
                return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
           
            if not data.get('Employee_Number').startswith('C') and dbdata.EMPLOYEE_NUMBER == data.get('Employee_Number'):
                Datedb = str(data['Effective_Start_Date'])
                Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                date = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                if date == Datedb:
                    print("dfgdghjjkkhj")
                    for i in data:
                        print("i",i)
                        cap = i.upper()
                        new_value = data.get(i)
                        print("new_value",new_value)
                        if getattr(dbdata,cap) != new_value:
                            print("new_value",new_value)
                            setattr(dbdata,cap,new_value)
                    db.session.commit()
                    return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
 
            if not data.get('Employee_Number').startswith('C'):
 
                Datedb = str(data['Effective_Start_Date'])
                print("Datedb",Datedb)
                # Convert Date_Of_Joining to a datetime object
                Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                # Subtract one day from the Date_Of_Joining
                # if data.get('Employee_No').startswith('C'):
                #     dbdata.EFFECTIVE_END_DATE = dbdata.EFFECTIVE_START_DATE
                # else:
                #     PrevEED = Datedb - timedelta(days=1)
                #     dbdata.EFFECTIVE_END_DATE = PrevEED
                PrevEED = Datedb - timedelta(days=1)
                dbdata.EFFECTIVE_END_DATE = PrevEED
 
 
                print("dbdata.EMPLOYEE_NUMBER",dbdata.EMPLOYEE_NUMBER)
 
                details = EMPLOYEE_DETAILS(
                   
                            EMPLOYEE_NUMBER = data.get('Employee_Number') if data.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                            FIRST_NAME = data.get('First_Name') if data.get('First_Name') else dbdata.FIRST_NAME,
                            MIDDLE_NAME = data.get('Middle_Name') if data.get('Middle_Name') else dbdata.MIDDLE_NAME,
                            LAST_NAME = data.get('Last_Name') if data.get('Last_Name') else dbdata.LAST_NAME,
                            WORKER_TYPE = data.get('Worker_Type') if data.get('Worker_Type') else dbdata.WORKER_TYPE,
                            DATE_OF_JOINING = data.get('Date_Of_Joining') if data.get('Date_Of_Joining') else dbdata.DATE_OF_JOINING,
                            EFFECTIVE_START_DATE =  data['Effective_Start_Date'] if data['Effective_Start_Date'] else date.today(),
                            EFFECTIVE_END_DATE = data.get('Effective_End_Date') if data.get('Effective_End_Date') else date(4712, 12, 31),
                            LOCATION = data.get('Location')if data.get('Location') else dbdata.LOCATION,
                            EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                            CREATED_BY = 'HRName',
                            LAST_UPDATED_BY = "HRName")
               
                db.session.add(details)
                db.session.commit()
                return jsonify({"message":f"{data.get('Employee_Number')} newrecord added successfully", "data":details.serialize()}),201
            else:
                for i in data:
                    print("i",i)
                    cap = i.upper()
                    new_value = data.get(i)
                    print("new_value",new_value)
                    if getattr(dbdata,cap) != new_value:
                        print("new_value",new_value)
                        setattr(dbdata,cap,new_value)
                db.session.commit()
                return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
        else:
            existing_email = EMPLOYEE_DETAILS.query.filter_by(EMAIL_ID = e_id).first()
            print("existing_email",existing_email)
            if existing_email:
                return jsonify({"message":"email already exist"})
            else:
                dbdata = EMPLOYEE_DETAILS.query.get(id)
                print("dbdata.EFFECTIVE_START_DATE",type(dbdata.EFFECTIVE_START_DATE))
                print("data['Effective_Start_Date']",type(data['Effective_Start_Date']))
                Datedb = str(data['Effective_Start_Date'])
                print("Datedb",Datedb)
                # Convert Date_Of_Joining to a datetime object
                Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                print("Datedb",type(Datedb))
                date = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                print("date",type(date))
                if date <= Datedb and data.get('Employee_Number').startswith('C'):
                   
                    print("dfghj",data.get('Employee_Number').startswith('C'))
                    for i in data:
                        print("i",i)
                        cap = i.upper()
                        new_value = data.get(i)
                        print("new_value",new_value)
                        if getattr(dbdata,cap) != new_value:
                            print("new_value",new_value)
                            setattr(dbdata,cap,new_value)
                    db.session.commit()
                    return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
 
                # if not data.get('Employee_No').startswith('C'):
                if not data.get('Employee_Number').startswith('C') and dbdata.EMPLOYEE_NUMBER == data.get('Employee_Number'):
                    Datedb = str(data['Effective_Start_Date'])
                    Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                    date = datetime.strptime(str(dbdata.EFFECTIVE_START_DATE), "%Y-%m-%d")
                    if date == Datedb:
                        print("dfgdghjjkkhj")
                        for i in data:
                            print("i",i)
                            cap = i.upper()
                            new_value = data.get(i)
                            print("new_value",new_value)
                            if getattr(dbdata,cap) != new_value:
                                print("new_value",new_value)
                                setattr(dbdata,cap,new_value)
                        db.session.commit()
                        return jsonify({"message": "update existing record", "data":dbdata.serialize()}),200
 
                Datedb = str(data['Effective_Start_Date'])
                print("Datedb",Datedb)
                # Convert Date_Of_Joining to a datetime object
                Datedb = datetime.strptime(Datedb, "%Y-%m-%d")
                # Subtract one day from the Date_Of_Joining
                # if data.get('Employee_No').startswith('C'):
                #     dbdata.EFFECTIVE_END_DATE = dbdata.EFFECTIVE_START_DATE
                # else:
                #     PrevEED = Datedb - timedelta(days=1)
                #     dbdata.EFFECTIVE_END_DATE = PrevEED
                PrevEED = Datedb - timedelta(days=1)
                dbdata.EFFECTIVE_END_DATE = PrevEED
 
                print("dbdata.Employee_Number",dbdata.EMPLOYEE_NUMBER)
 
                details = EMPLOYEE_DETAILS(
                   
                            EMPLOYEE_NUMBER = data.get('Employee_Number') if data.get('Employee_Number') else dbdata.EMPLOYEE_NUMBER,
                            FIRST_NAME = data.get('First_Name') if data.get('First_Name') else dbdata.FIRST_NAME,
                            MIDDLE_NAME = data.get('Middle_Name') if data.get('Middle_Name') else dbdata.MIDDLE_NAME,
                            LAST_NAME = data.get('Last_Name') if data.get('Last_Name') else dbdata.LAST_NAME,
                            WORKER_TYPE = data.get('Worker_Type') if data.get('Worker_Type') else dbdata.WORKER_TYPE,
                            DATE_OF_JOINING = data.get('Date_Of_Joining') if data.get('Date_Of_Joining') else dbdata.DATE_OF_JOINING,
                            EFFECTIVE_START_DATE =  data.get('Effective_Start_Date') if data.get('Effective_Start_Date') else date.today(),
                            EFFECTIVE_END_DATE = data.get('Effective_End_Date') if data.get('Effective_End_Date') else date(4712, 12, 31),
                            LOCATION = data.get('Location')if data.get('Location') else dbdata.LOCATION,
                            EMAIL_ID =email  if email else dbdata.EMAIL_ID,
                            CREATED_BY = 'HRName',
                            LAST_UPDATED_BY = "HRName")
               
                db.session.add(details)
                db.session.commit()
                return jsonify({"message":f"{data.get('Employee_Number')} newrecord added successfully", "data":details.serialize()}),201
 
    except Exception as e:
        return jsonify({'error':str(e)}),500
# delete employee
def deletedata(id):
    try:
        data = EMPLOYEE_DETAILS.query.get(id)
        
        if not data:
            return jsonify({'message': 'person not found'}),404
        print("data.serialize()",data.serialize())
        db.session.delete(data)
        db.session.commit()
        return jsonify({'data' : data.serialize()}),200
        
    except Exception as e:
        return jsonify({'error':str(e)}),500  
        


    
# search employee[GET Method]
def filterPersons(search_data):
   
    search_data = search_data
    print('type(search_data)',type(search_data))
    person_list = []
    # Use filter and filter conditions for efficient querying
    today = date.today()
    persons = EMPLOYEE_DETAILS.query.filter((
        (EMPLOYEE_DETAILS.EMPLOYEE_NO == search_data) |
        (func.lower(EMPLOYEE_DETAILS.FIRST_NAME).startswith(search_data.lower()))) &
        # | (func.lower(Fields.location).startswith(search_data.lower()))
       
        # | (Fields.LAST_NAME.startswith(search_data))
        #| (PersonData.DATE_OF_BIRTH.contains(search_data))
        (EMPLOYEE_DETAILS.EFFECTIVE_START_DATE <= today) &
    (today <= EMPLOYEE_DETAILS.EFFECTIVE_END_DATE)
    ).all()
   
    for person in persons:
            person_dict = person.serialize()
            person_list.append(person_dict)
    return jsonify(person_list), 200

# delete employee by id[DELETE Method]




    # try:
    #         a = Fields.query.get(id)
    #         if not a:
    #             return jsonify({'message': f'Person with id {id} not found'}), 404
            
    #         data = request.json
    #         print("data", data)

    #         updateData = {}
    #         for key in ['MIDDLE_NAME', 'LAST_NAME', 'DATE_OF_JOINING', 'LOCATION', 'EMAIL', 'CREATED_BY', 'LAST_UPDATED_BY']:
    #             if key in data:
    #                 updateData[key] = data[key]
            
    #         print("update", a.serialize())

    #         for key, value in updateData.items():
    #             setattr(a, key, value)

    #         db.session.commit()
    #         return jsonify({'data': a.serialize()}), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500    



