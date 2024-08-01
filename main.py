from fastapi import FastAPI, Depends
from Salary_Calculation.routers import auth, endpoints
# from Salary_Calculation.database import init as init_db

app = FastAPI()

# protect endpoints with authentication



app.include_router(auth.router)
app.include_router(endpoints.router, dependencies=[Depends(auth.get_current_user)])

# # start event to initialize the database
# @app.on_event("startup")
# async def on_startup():
#     await init_db()
    
@app.get("/")
def read_root():
    return {"message: salary calculation system"}