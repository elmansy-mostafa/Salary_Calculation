from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# User model
class User(BaseModel):
    name : str
    email : EmailStr
    hashed_password : str
    role : str
    is_verified : bool = False
        
    class Config:
        orm_mode = True
        


class Login(BaseModel):
    username : str
    password : str

    
# saturdays model
class Saturdays(BaseModel):
    saturdays : int        


# Appontments model
class Appointment(BaseModel):
    no_of_qualified_appointment : int
    no_of_not_qualified_appointment : int
    
#compension model
class Compensation(BaseModel):
    spiffs : float
    kpis : float
    butter_up : float

    
# deduction model
class Deduction(BaseModel):
    deductions : float
    reason : str

# Additional allowance model
class AdditionalAllowance(BaseModel):
    allowance_type : str
    allowance_value : float
    
# EmployeeType model
class EmployeeType(BaseModel):
    is_appointment_serrer : bool
    is_full_time : bool

# Employee model
class Employee(BaseModel):
    id : int
    name : str
    national_id : int
    company_id : int
    start_date : datetime
    end_date : Optional[datetime] = None
    reason_of_leaving : Optional[str] = None
    position : str
    tier_type : str
    is_onsite : bool
    has_insurance : bool
    employee_type : EmployeeType
    
# dailyreport model
class DailyReport(BaseModel):
    date : datetime
    employee_id : int
    appointment : Appointment
    compensation : Compensation
    deductions : Deduction
    allowance : AdditionalAllowance
    adherence_status : bool
    total_salary : float
    is_saturday : bool
    working_hours : float
    

class Static_values(BaseModel):
    tier_appointment_setter_base_salary : object
    tier_fronter_base_salary : object
    spiffs : float
    kpis : float
    butter_up : float
    allowance : object
    hour_price : float
    saturdays_price : float
    




# # salary calculator service 
# class SalaryCalculator:
#     @staticmethod
#     def calculate_salary(report:DailyReport) -> float:
#         base_salary = 2000
#         total_compensation = report.compensation.spiffs + report.compensation.commissisons
#         total_deductions = report.deductions.deductions
#         if report.time_extension.has_time_extended : 
#             total_compensation += report.time_extension.price or 0
#         return base_salary + total_compensation - total_deductions
        
        

