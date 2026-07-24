from typing import Optional
from pydantic import(BaseModel, Field, EmailStr, ValidationError, field_validator, StrictInt)

class Address(BaseModel):
    city: str
    state: str

class Student(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    age: int = Field(ge=0, le=30)
    email: EmailStr
    course: str = "Python"
    phone: Optional[str] = None
    address: Address

    @field_validator("age")
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Age must be at least 18")
        return value

address = Address(city="Srinagar", state="j&k")

student = Student(name="Amarah", age="24",email="amarah@gmail.com", phone="1234567890", address=address)
print(student)
print(student.name)
print(student.model_dump())
print(student.model_dump_json(indent=4))

try:
    student = Student(name = "A", age=15, email="wrong", address=address)
except ValidationError as e:
    print(e)

class Account(BaseModel):
    id: StrictInt