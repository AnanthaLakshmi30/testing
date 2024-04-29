from app import Flask_app
from config import db
from controllers.employeeController import *
from controllers.userController import *
from controllers.empProfileController import *
from controllers.templateController import *









# add admin
@Flask_app.route('/add_admin_details', methods=['POST'])
def add_admin():
    return addadmin()

# login
@Flask_app.route('/login', methods=['POST'])
def log_in():
    return login()

# generate otp and send to email
@Flask_app.route('/email', methods=['POST'])
def e_mail():
    print("sedfghjkl")
    return email()

# verify otp
@Flask_app.route('/verify', methods=['POST'])
def verif_y():
    print("sedfghjkl")
    return verify()

@Flask_app.route('/change_password', methods=['PUT'])
def change_password():
    print("sdtfyguio;")
    return changePassword()


# ////////////////employee////////
# add employee
@Flask_app.route('/add_emp_details', methods=['POST'])
def add_Employee():
    return addEmployee()
 
# add employees in bulk
@Flask_app.route('/add_emp_bulk', methods=['POST'])
def add_bulk():
    print("ghjkkljhgfgjhklkjhgfd")
    return addbulk()

# get all employees
@Flask_app.route('/get_emp_details', methods=['GET'])
def get_Employee():
    return getEmployee()

# get by employees id
@Flask_app.route('/get_emp_details/<int:id>', methods=['GET'])
def get_Employee_By_Id(id):
    return getEmployeeById(id)

# update employee details
@Flask_app.route('/update_emp/<id>', methods=['PUT'])
def update_emp(id):
    print("fdghjklkjhgfgojhb")
    return updateemp(id)

# delete employee
@Flask_app.route('/delete_data/<id>',methods=['DELETE'])
def delete_data(id):
    return deletedata(id)



# ////////////////////////////
# get all admins
@Flask_app.route('/get_admin_details', methods=['GET'])
def get_admin():
    return getadmin()

# get admin by id
@Flask_app.route('/get_admin_by_id/<id>', methods=['GET'])
def get_adminid(id):
    return getadmin_id(id)

# search
@Flask_app.route('/filterPersons/<search_data>', methods=['GET']) ##
def filter_Persons(search_data):
    return filterPersons(search_data)
 


# PUT/UPDATE Method


# update admin details
@Flask_app.route('/update_admindetails/<id>',methods=['PUT'])
def update_admindetails(id):
    return updateadmin_details(id)


# DELETE Method


# delete admin
@Flask_app.route('/delete_admin/<id>',methods=['DELETE'])
def delete_admin(id):
    return deleteadmin(id)

# /////////empProfile//////
# # add address
# @Flask_app.route('/add_address',methods=['POST'])
# def add_address():
#     return addaddress()

# add template
@Flask_app.route('/add_template',methods=['POST'])
def add_template():
    return addtemplate()

# retrieve template
@Flask_app.route('/retrieve_template/<string:Id>', methods=['GET'])
def retrieve_template(Id):
    print("sdfghjgvyvb")
    return temp(Id)
# convertpdf
@Flask_app.route('/convert_rtf/<string:Id>', methods=['GET'])
def convert_rtf(Id):
    print("sdfghjgvyvb")
    return convertrtf(Id)

# update template
@Flask_app.route('/update_temp/<string:Id>', methods=['PUT'])
def update_temp(Id):
    print("sdfghjgvyvb")
    return updatetemp(Id)


