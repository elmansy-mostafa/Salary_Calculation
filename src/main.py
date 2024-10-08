from fastapi import FastAPI, Depends
from modules.users import users_router
from modules.employees import employees_router
from modules.daily_reports import daily_reports_router
from modules.static_values import static_values_router
from modules.auth.authorizations import get_admin, get_superadmin
from services import exportPdf 


app = FastAPI()



app.include_router(users_router.router)
app.include_router(employees_router.router, dependencies=[Depends(get_admin)])
app.include_router(daily_reports_router.router, dependencies=[Depends(get_admin)])
app.include_router(static_values_router.router, dependencies=[Depends(get_superadmin)])
app.include_router(exportPdf.router,  dependencies=[Depends(get_admin)])

    
@app.get("/")
def read_root():
    return {"message": "Hello, salary_calculation!"}