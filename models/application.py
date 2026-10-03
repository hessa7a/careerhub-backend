from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import BaseModel


class ApplicationModel(BaseModel):

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    status = Column(String, nullable=False, default="applied")

    applied_date = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    message = Column(Text, nullable=True)

    resume = Column(String, nullable=True)

    applicant_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    job_post_id = Column(
        Integer,
        ForeignKey("job_posts.id"),
        nullable=False
    )

    applicant = relationship(
        "UserModel",
        back_populates="applications"
    )

    job_post = relationship(
        "JobPostModel",
        back_populates="applications"
    )