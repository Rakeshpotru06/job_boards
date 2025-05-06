from pydantic import BaseModel, EmailStr

class Usersdata(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
        from_attributes = True
