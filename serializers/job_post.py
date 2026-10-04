from pydantic import BaseModel
from datetime import datetime


class JobPostCreateSchema(BaseModel):
    title: str
    description: str
    requirements: str
    location: str
    job_type: str


class JobPostUpdateSchema(BaseModel):
    title: str
    description: str
    requirements: str
    location: str
    job_type: str
    status: str


class JobPostSchema(BaseModel):
    id: int
    title: str
    description: str
    requirements: str
    location: str
    job_type: str
    status: str
    posted_date: datetime
    company_id: int

    class Config:
        orm_mode = True