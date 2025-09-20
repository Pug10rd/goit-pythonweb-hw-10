from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import String, create_engine, UniqueConstraint, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from pydantic import BaseModel, ConfigDict
import uvicorn
from datetime import datetime, timedelta

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"
    __table_args__ = (UniqueConstraint('id', name='student_uq_id'),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)   
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50) , unique=True) 
    phone_number: Mapped[str] = mapped_column(String(15))
    date_of_birth: Mapped[str] = mapped_column(String(10)) # Format: YYYY-MM-DD, example: 2024-06-01

    
    def __repr__(self) -> str:
        return f"Student(name={self.name!r}, surname={self.surname!r}, email={self.email!r}, phone_number={self.phone_number!r}, date_of_birth={self.date_of_birth!r})"

class StudentRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    surname: str
    email: str
    phone_number: str
    date_of_birth: str

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    surname: str
    email: str
    phone_number: str
    date_of_birth: str

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/hw8"

engine = create_engine(DATABASE_URL, echo=True)



app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

@app.post("/students/", response_model=StudentResponse)
async def create_student(student: StudentRequest):
    with Session(engine) as session:
        db_student = session.query(Student).filter(Student.email == student.email).first()
        if db_student is not None:
            raise HTTPException(status_code=400, detail="Student already exists")
        student_obj = Student(**student.model_dump())
        session.add(student_obj)
        session.commit()
        return StudentResponse.model_validate(student_obj)

@app.get("/students/{student_id}", response_model=StudentResponse)
async def read_student(student_id: int):
    with Session(engine) as session:
        student_obj = session.get(Student, student_id)
        if not student_obj:
            raise HTTPException(status_code=404, detail="Student not found")
        return StudentResponse.model_validate(student_obj)

@app.get("/students/", response_model=list[StudentResponse])
async def get_all_students():
    with Session(engine) as session:
        students = session.query(Student).all()
        return [StudentResponse.model_validate(student) for student in students]

@app.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student: StudentRequest):
    with Session(engine) as session:
        student_obj = session.get(Student, student_id)
        if not student_obj:
            raise HTTPException(status_code=404, detail="Student not found")
        student_obj.name = student.name
        student_obj.surname = student.surname
        student_obj.email = student.email
        student_obj.phone_number = student.phone_number
        student_obj.date_of_birth = student.date_of_birth
        session.commit()
        session.refresh(student_obj)
        return StudentResponse.model_validate(student_obj)
    
@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    with Session(engine) as session:
        student_obj = session.get(Student, student_id)
        if not student_obj:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(student_obj)
        session.commit()
        return {"detail": "Student deleted successfully"}
    

# UNCOMMENT TO ENABLE DELETE ALL STUDENTS, NEEDED FOR TESTING PURPOSES IF YOU WANT TO CLEAR THE DB!!!

# @app.delete("/students/")
# async def delete_all_students():
#     with Session(engine) as session:
#         num_deleted = session.query(Student).delete()
#         session.commit()
#         return {"detail": f"Deleted {num_deleted} students successfully"}
    
@app.get("/students/search/", response_model=list[StudentResponse])
async def search_students(
    name: str = Query(None),
    surname: str = Query(None),
    email: str = Query(None)
):
    with Session(engine) as session:
        query = session.query(Student)
        filters = []
        if name:
            filters.append(Student.name.ilike(f"%{name}%"))
        if surname:
            filters.append(Student.surname.ilike(f"%{surname}%"))
        if email:
            filters.append(Student.email.ilike(f"%{email}%"))
        if filters:
            query = query.filter(or_(*filters))
        students = query.all()
        return [StudentResponse.model_validate(student) for student in students]
    
@app.get("/students/upcoming_birthdays/", response_model=list[StudentResponse])
async def get_upcoming_birthdays():
    today = datetime.today()
    next_week = today + timedelta(days=7)
    with Session(engine) as session:
        students = session.query(Student).all()
        upcoming = []
        for student in students:
            try:
                dob = datetime.strptime(student.date_of_birth, "%Y-%m-%d")
                dob_this_year = dob.replace(year=today.year)
                if today <= dob_this_year <= next_week:
                    upcoming.append(student)
            except Exception:
                continue
        return [StudentResponse.model_validate(student) for student in upcoming]
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)