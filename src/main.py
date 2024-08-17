from fastapi import FastAPI, Depends
from modules.users import users_router
from modules.employees import employees_router
from modules.daily_reports import daily_reports_router
from modules.auth.authorizations import get_admin


app = FastAPI()



app.include_router(users_router.router)
app.include_router(employees_router.router, dependencies=[Depends(get_admin)])
app.include_router(daily_reports_router.router, dependencies=[Depends(get_admin)])

    
@app.get("/")
def read_root():
    return {"message": "Hello, salary_calculation!"}