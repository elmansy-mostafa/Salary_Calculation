from fastapi import FastAPI, Depends
from Salary_Calculation.modules.users import users_router
from Salary_Calculation.modules.employees import employees_router
from Salary_Calculation.modules.daily_reports import daily_reports_router
from Salary_Calculation.modules.auth.authorizations import get_admin


app = FastAPI()



app.include_router(users_router.router)
app.include_router(employees_router.router, dependencies=[Depends(get_admin)])
app.include_router(daily_reports_router.router, dependencies=[Depends(get_admin)])

    
@app.get("/")
def read_root():
    return {"message: salary calculation system"}