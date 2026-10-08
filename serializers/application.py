from pydantic import BaseModel
from datetime import datetime

from serializers.user import UserSchema


class ApplicationCreateSchema(BaseModel):
    job_post_id: int
    message: str | None = None
    resume: str | None = None


class ApplicationUpdateSchema(BaseModel):
    status: str


class ApplicationSchema(BaseModel):
    id: int
    status: str
    applied_date: datetime
    message: str | None = None
    resume: str | None = None
    applicant_id: int
    job_post_id: int
    applicant: UserSchema

    model_config = {
    "from_attributes": True
}