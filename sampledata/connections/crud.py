""" import modules """
from sqlalchemy.orm import Session
from connections import schema

import models


def get_user_by_username(db_data:Session,username:str):
    """ get employee by username"""
    user_data = db_data.query(models.Employee).filter(models.Employee.username == username).first()
    return user_data

def get_user_by_email(db_data:Session,email:str):
    """ get employee with given email"""
    user_data = db_data.query(models.Employee).filter(models.Employee.email == email).first()
    return user_data

def get_user_by_phonenumber(db_data:Session,phonenumber:str):
    """ get employee by phonenumber """
    user_data = db_data.query(models.Employee).filter(models.Employee.phonenumber == phonenumber).first()
    return user_data


def create_employee(db_data:Session,emp:schema.EmployeeData):
    """ create new employee """
    new_employee = models.Employee(
            username = emp.username,
            email = emp.email,
            password = emp.password,
            phonenumber = emp.phonenumber,
            role = emp.role
    )
    db_data.add(new_employee)
    db_data.commit()
    return new_employee

def verify_emp_by_email_password(db_data: Session,email:str,password:str):
    user_data = db_data.query(models.Employee).filter(models.Employee.email==email,models.Employee.password==password).first()
    return user_data



