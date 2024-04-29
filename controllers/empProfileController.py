from base64 import encode
from datetime import timedelta
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from sqlalchemy import func
from flask import jsonify, request, session
from config import db
from Model.employeeData import *
from Model.userData import Admin
from Model.empProfile import *

# def addaddress():
#     try:
#         data = request.json
#         if not data:
#             return jsonify ({'error': 'data is required'}),400
        
#         details = Address(EMPLOYEE_ID
#                           ADDRESS_TYPE
#                           ADDRESS
#                           CITY
#                           STATE
#                           COUNTRY
#                           PIN_CODE
#                           DATE_FROM
#                           DATE_TO
#                           CREATED_BY
#                           LAST_UPDATED_BY)



