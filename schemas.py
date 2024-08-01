from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# user model schemas 

class UserCreate(BaseModel):
    email : EmailStr
    password : str
    

    
class Token(BaseModel):
    access_token : str
    token_type : str
    
class TokenData(BaseModel):
    email : Optional[str] = None

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
class EmployeeBase(BaseModel):
    id : int
    name : str
    national_id : int
    company_id : int
    start_date : datetime
    end_date : Optional[datetime] = None
    position : str
    
class EmployeeCreate(EmployeeBase):
    id : int
    
class EmployeeUpdate(EmployeeBase):
    pass 

class EmployeeInDB(EmployeeBase):
    id : int
    
class EmployeeResponse(EmployeeInDB):
    pass 

    
# Employee list response schema
class EmployeeListResponse(BaseModel):
    employee : list[EmployeeResponse]
    

# dailyreport model
class DailyReportBase(BaseModel):
    date : datetime
    employee_id : int
    adherance : Adherance
    appointment : Appointment
    compensation : Compensation
    time_extension : TimeExtension
    deductions : Deduction
    
class DailyReportCreate(DailyReportBase):
    pass 
class DailyReportUpdate(DailyReportBase):
    pass 
class DailyReportResponse(DailyReportBase):
    pass 
class DailyReportRequest(BaseModel):
    employee_id: int
    report_date : datetime

    