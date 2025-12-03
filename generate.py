from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean, Float
import os

fake = Faker('en_NG')  # Nigerian names, phones, addresses

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    department = Column(String)
    position = Column(String)
    salary_ngn = Column(Float)
    city = Column(String)
    hire_date = Column(Date)
    is_active = Column(Boolean)

# Use SQLite for demo (change to PostgreSQL URL when deploying)
engine = create_engine("sqlite:///naija_employees.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

departments = ["IT", "HR", "Finance", "Marketing", "Operations", "Sales", "Engineering"]
positions = ["Intern", "Junior", "Mid-level", "Senior", "Manager", "Director"]
cities = ["Lagos", "Abuja", "Port Harcourt", "Ibadan", "Kano", "Enugu"]

print("Generating 100,000 Nigerian employees...")

for i in range(1, 100001):
    emp = Employee(
        name=fake.name(),
        email=fake.unique.email(),
        phone=fake.phone_number(),
        department=random.choice(departments),
        position=random.choice(positions),
        salary_ngn=round(random.uniform(300000, 5000000), 2),
        city=random.choice(cities),
        hire_date=fake.date_between(start_date='-5y', end_date='today'),
        is_active=random.choice([True, True, True, False])  # 75% active
    )
    session.add(emp)
    
    if i % 10000 == 0:
        session.commit()
        print(f"{i:,} employees created...")

session.commit()
print("100,000 Nigerian employees generated!")
