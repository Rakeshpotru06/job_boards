from pydantic import BaseModel
from typing import List


class UserData(BaseModel):
    id: int
    name: str
    email: str
    role: str

class UsersListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    users: List[UserData]


    class Config:
        orm_mode = True
        from_attributes = True
