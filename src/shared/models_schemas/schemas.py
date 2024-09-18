from pydantic import BaseModel, EmailStr
from typing import Dict, Optional, List
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
    

# Static values model
class StaticValuesBase(BaseModel):
    id : int
    tier_base_salary: Dict[str,float]
    cad: float
    kpis: float
    butter_up: float
    allowance: Dict[str,float]
    hour_price: Dict[str,float]
    no_of_qulified_appt_tier_setter : Dict[str,float]
    no_of_qulified_appt_tier_fronter : Dict[str,float]
    # saturdays_price: float
    

class StaticValuesCreate(StaticValuesBase):
    pass

class StaticValuesResponse(StaticValuesBase):
    pass

# Daily report model
class DailyReportBase(BaseModel):
    date: datetime
    employee_id: int
    appointment: Appointment
    compensation: Compensation
    deductions: Deduction
    allowance: AdditionalAllowance
    adherence_status: bool
    total_salary: float = None
    is_saturday: bool
    working_hours: float

    # def calculate_total_salary(self, static_values:StaticValuesBase, employee:EmployeeBase):
    #     if employee.tier_type == "C" and employee.employee_type.is_appointment_serrer == True:
    #         if self.appointment.no_of_qualified_appointment >= 3 :
    #             kpis = self.compensation.kpis * static_values.kpis 
    #         else:
    #             kpis = 0
    #     elif employee.tier_type == "B" and employee.employee_type.is_appointment_serrer == True:
    #         if self.appointment.no_of_qualified_appointment >= 4 :
    #             kpis = self.compensation.kpis * static_values.kpis 
    #         else:
    #             kpis = 0
    #     elif employee.tier_type == "A" and employee.employee_type.is_appointment_serrer == True:
    #         if self.appointment.no_of_qualified_appointment >= 6 :
    #             kpis = self.compensation.kpis * static_values.kpis 
    #         else:
    #             kpis = 0
    #     elif employee.tier_type == "C" and employee.employee_type.is_appointment_serrer == False:
    #         if self.appointment.no_of_qualified_appointment >= 7 :
    #             kpis = self.compensation.kpis * static_values.kpis 
    #         else:
    #             kpis = 0
    #     elif employee.tier_type == "B" and employee.employee_type.is_appointment_serrer == False:
    #         if self.appointment.no_of_qualified_appointment >= 6 :
    #             kpis = self.compensation.kpis * static_values.kpis 
    #         else:
    #             kpis = 0
    #     elif employee.tier_type == "A" and employee.employee_type.is_appointment_serrer == False:
    #         if self.appointment.no_of_qualified_appointment >= 6 :
    #             kpis = self.compensation.kpis * static_values.kpis 
    #         else:
    #             kpis = 0
                
    #     if self.is_saturday:
    #         saturdays = self.working_hours * static_values.hour_price[employee.tier_type]
    #     else:
    #         saturdays = 0
                    
    #     # Calculate compensation, allowance, and deductions
    #     spiffs = self.compensation.spiffs * static_values.cad
    #     butter_up = self.compensation.butter_up * static_values.butter_up
        
    #     compensation = spiffs + kpis + butter_up
    #     allowance = self.allowance.allowance_value
    #     deductions = self.deductions.deductions

    #     if self.working_hours != 9 and self.working_hours != 0:
    #         # Calculate the value based on working hours
    #         hours_value = (self.working_hours - 9) * static_values.hour_price[employee.tier_type]
    #     else:
    #         hours_value = 0
        
    #     # Total salary calculation
    #     total_salary = compensation + allowance + saturdays + hours_value - deductions
    #     return total_salary
    
    
class DailyReportCreate(DailyReportBase):
    pass 

class DailyReportUpdate(DailyReportBase):
    pass 

class DailyReportResponse(DailyReportBase):
    pass 

class DailyReportRequest(BaseModel):
    employee_id: int
    report_date : datetime




