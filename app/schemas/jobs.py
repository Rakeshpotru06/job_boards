from pydantic import BaseModel
from typing import List


class JobsData(BaseModel):
    id: int
    title: str
    company: str
    location: str

class JobsListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    jobs: List[JobsData]


    class Config:
        orm_mode = True
        from_attributes = True
