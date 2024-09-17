from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, Dict
from datetime import datetime



# User model
class User(BaseModel):
    name : str
    email : EmailStr
    hashed_password : str
    role : str
    is_verified : bool = False
        
    model_config = ConfigDict(from_attributes=True)
        


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
    

# Static values model
class StaticValues(BaseModel):
    id : int
    tier_base_salary: Dict[str,float]
    spiffs: float
    kpis: float
    butter_up: float
    allowance: Dict[str,float]
    hour_price: Dict[str,float]
    # saturdays_price: float

# Daily report model
class DailyReport(BaseModel):
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

    def calculate_total_salary(self, static_values:StaticValues, employee:Employee):
        if employee.tier_type == "C" and employee.employee_type.is_appointment_serrer == True:
            if self.appointment.no_of_qualified_appointment >= 3 :
                kpis = self.compensation.kpis * static_values.kpis 
            else:
                kpis = 0
        elif employee.tier_type == "B" and employee.employee_type.is_appointment_serrer == True:
            if self.appointment.no_of_qualified_appointment >= 4 :
                kpis = self.compensation.kpis * static_values.kpis 
            else:
                kpis = 0
        elif employee.tier_type == "A" and employee.employee_type.is_appointment_serrer == True:
            if self.appointment.no_of_qualified_appointment >= 6 :
                kpis = self.compensation.kpis * static_values.kpis 
            else:
                kpis = 0
        elif employee.tier_type == "C" and employee.employee_type.is_appointment_serrer == False:
            if self.appointment.no_of_qualified_appointment >= 7 :
                kpis = self.compensation.kpis * static_values.kpis 
            else:
                kpis = 0
        elif employee.tier_type == "B" and employee.employee_type.is_appointment_serrer == False:
            if self.appointment.no_of_qualified_appointment >= 6 :
                kpis = self.compensation.kpis * static_values.kpis 
            else:
                kpis = 0
        elif employee.tier_type == "A" and employee.employee_type.is_appointment_serrer == False:
            if self.appointment.no_of_qualified_appointment >= 6 :
                kpis = self.compensation.kpis * static_values.kpis 
            else:
                kpis = 0
                
        if self.is_saturday:
            saturdays = self.working_hours * static_values.hour_price[employee.tier_type]
        else:
            saturdays = 0
        # Calculate compensation, allowance, and deductions
        spiffs = self.compensation.spiffs * static_values.spiffs
        butter_up = self.compensation.butter_up * static_values.butter_up
        
        compensation = spiffs + kpis + butter_up
        allowance = self.allowance.allowance_value
        deductions = self.deductions.deductions

        if self.working_hours != 9 :
            # Calculate the value based on working hours
            hours_value = (self.working_hours - 9) * static_values.hour_price[employee.tier_type]
        else:
            hours_value = 0
        
        # Total salary calculation
        total_salary = compensation + allowance + saturdays + hours_value - deductions
        return total_salary


    

        
        

