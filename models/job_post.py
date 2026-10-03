from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import BaseModel


class JobPostModel(BaseModel):

    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    requirements = Column(Text, nullable=False)

    location = Column(String, nullable=False)

    job_type = Column(String, nullable=False)

    status = Column(String, nullable=False, default="active")

    posted_date = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    company_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    company = relationship(
        "UserModel",
        back_populates="job_posts"
    )

    applications = relationship(
        "ApplicationModel",
        back_populates="job_post"
    )