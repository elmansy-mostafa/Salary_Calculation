from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from beanie import Document, PydanticObjectId


# User model
class User(BaseModel):
    email : EmailStr
    hashed_password : str
    
class UserInDB(User):
    id : PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")

    class Congig:
        orm_mode = True
    
        

#Adherance model
class Adherance(BaseModel):
    status : bool
    
# Appontments model
class Appointment(BaseModel):
    no_of_qualified_appointment : int
    no_of_not_qualified_appointment : int
    
#compension model
class Compensation(BaseModel):
    spiffs : float
    commissisons : float
    
# time extension model
class TimeExtension(BaseModel):
    has_time_extended : bool
    price : Optional[float] = None
    
# deduction model
class Deduction(BaseModel):
    deductions : float
    
# Employee model
class Employee(BaseModel):
    id : int
    name : str
    national_id : int
    company_id : int
    start_date : datetime
    end_date : Optional[datetime] = None
    position : str
    
# dailyreport model
class DailyReport(BaseModel):
    date : datetime
    employee_id : int
    adherance : Adherance
    appointment : Appointment
    compensation : Compensation
    time_extension : TimeExtension
    deductions : Deduction
    
# salary calculator service 
class SalaryCalculator:
    @staticmethod
    def calculate_salary(report:DailyReport) -> float:
        base_salary = 2000
        total_compensation = report.compensation.spiffs + report.compensation.commissisons
        total_deductions = report.deductions.deductions
        if report.time_extension.has_time_extended : 
            total_compensation += report.time_extension.price or 0
        return base_salary + total_compensation - total_deductions
        