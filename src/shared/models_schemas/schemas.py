from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# user model schemas 
class UserBase(BaseModel):
    name : str
    email : EmailStr
    role : str

class UserCreate(UserBase):
    password : str

class UserInDB(UserBase):
    hashed_password : str
    is_verified :bool = False


class Token(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str
    
class TokenRefresh(BaseModel):
    refresh_token : str


class TokenData(BaseModel):
    email : Optional[str] = None
    role : Optional[str] = None
    
class SignupResponse(BaseModel):
    msg :str


    
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
class EmployeeBase(BaseModel):
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
    employee : List[EmployeeResponse]
    

# dailyreport model
class DailyReportBase(BaseModel):
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
    
class DailyReportCreate(DailyReportBase):
    pass 

class DailyReportUpdate(DailyReportBase):
    pass 

class DailyReportResponse(DailyReportBase):
    pass 

class DailyReportRequest(BaseModel):
    employee_id: int
    report_date : datetime


