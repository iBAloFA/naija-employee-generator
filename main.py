from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

app = FastAPI(title="Naija Employee Generator API", description="100k realistic Nigerian employees")

# Change this to your PostgreSQL URL when deploying
engine = create_engine("sqlite:///naija_employees.db")

@app.get("/")
def home():
    return {"message": "Welcome to Naija Employee API – 100k records ready!", "docs": "/docs"}

@app.get("/employees")
def get_employees(
    department: str = Query(None),
    city: str = Query(None),
    limit: int = Query(50, le=1000)
):
    query = "SELECT * FROM employees"
    conditions = []
    if department:
        conditions.append(f"department = '{department}'")
    if city:
        conditions.append(f"city = '{city}'")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += f" LIMIT {limit}"
    
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")
