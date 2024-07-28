from pydantic import BaseModel
from typing import Optional
from datetime import date

#Adherance model
class Adherance(BaseModel):
    is_full_time : bool
    is_part_time : bool
    status = bool
    
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
    start_date : date
    end_date : Optional[date] = None
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
    date : date
    employee : EmployeeResponse
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

    