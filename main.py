from fastapi import FastAPI
from Salary_Calculation.routers import endpoints
# from Salary_Calculation.database import init as init_db

app = FastAPI()
app.include_router(endpoints.router)

# # start event to initialize the database
# @app.on_event("startup")
# async def on_startup():
#     await init_db()
    
@app.get("/")
def read_root():
    return {"message: salary calculation system"}