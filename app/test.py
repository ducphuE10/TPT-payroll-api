from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Database setup
DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    companies = relationship("Company", back_populates="owner")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    employees = relationship("Employee", back_populates="company")
    owner = relationship("User", back_populates="companies")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="employees")


Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

# Authentication setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
users_db = {"admin": {"username": "admin", "password": "secret"}}


def fake_hash_password(password: str):
    return f"hashed-{password}"


def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return user
    return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = users_db.get(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Schemas
class CompanyCreate(BaseModel):
    name: str


class EmployeeCreate(BaseModel):
    name: str


class EmployeeOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CompanyOut(BaseModel):
    id: int
    name: str
    employees: List[EmployeeOut]

    class Config:
        orm_mode = True


# Routes
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user["username"], "token_type": "bearer"}


@app.get("/companies", response_model=List[CompanyOut])
def get_companies(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    companies = (
        db.query(Company).filter(Company.owner_id == current_user["username"]).all()
    )
    return companies


@app.post("/companies", response_model=CompanyOut)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_company = Company(name=company.name, owner_id=current_user["username"])
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@app.post("/companies/{company_id}/employees", response_model=EmployeeOut)
def create_employee(
    company_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_company = (
        db.query(Company)
        .filter(Company.id == company_id, Company.owner_id == current_user["username"])
        .first()
    )
    if not db_company:
        raise HTTPException(
            status_code=404, detail="Company not found or not owned by you"
        )

    db_employee = Employee(name=employee.name, company_id=company_id)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.get("/companies/{company_id}/employees", response_model=List[EmployeeOut])
def get_employees(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_company = (
        db.query(Company)
        .filter(Company.id == company_id, Company.owner_id == current_user["username"])
        .first()
    )
    if not db_company:
        raise HTTPException(
            status_code=404, detail="Company not found or not owned by you"
        )

    employees = db.query(Employee).filter(Employee.company_id == company_id).all()
    return employees
