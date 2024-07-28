from fastapi import FastAPI
from Salary_Calculation.routers import endpoints

app = FastAPI()
app.include_router(endpoints.router)

@app.get("/")
def read_root():
    return {"message: salary calculation system"}