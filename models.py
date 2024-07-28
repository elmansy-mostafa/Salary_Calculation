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
class Employee(BaseModel):
    id : int
    name : str
    national_id : int
    company_id : int
    start_date : date
    end_date : Optional[date] = None
    position : str
    
# dailyreport model
class DailyReport(BaseModel):
    date : date
    employee : Employee
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
        