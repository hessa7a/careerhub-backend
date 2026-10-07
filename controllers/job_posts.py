# controllers/job_posts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.job_post import JobPostModel
from models.user import UserModel
from serializers.job_post import JobPostCreateSchema, JobPostUpdateSchema, JobPostSchema
from database import get_db
from dependencies.get_current_user import get_current_user


router = APIRouter()


@router.get("/jobs", response_model=list[JobPostSchema])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobPostModel).all()

    return jobs


@router.get("/jobs/{job_id}", response_model=JobPostSchema)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobPostModel).filter(JobPostModel.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.post("/jobs", response_model=JobPostSchema, status_code=201)
def create_job(
    job: JobPostCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "company":
        raise HTTPException(status_code=403, detail="Only companies can create jobs")

    new_job = JobPostModel(
        title=job.title,
        description=job.description,
        requirements=job.requirements,
        location=job.location,
        job_type=job.job_type,
        company_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.put("/jobs/{job_id}", response_model=JobPostSchema)
def update_job(
    job_id: int,
    job_data: JobPostUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    job = db.query(JobPostModel).filter(JobPostModel.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot update this job")

    job.title = job_data.title
    job.description = job_data.description
    job.requirements = job_data.requirements
    job.location = job_data.location
    job.job_type = job_data.job_type

    if job_data.status:
        job.status = job_data.status

    db.commit()
    db.refresh(job)

    return job


@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    job = db.query(JobPostModel).filter(JobPostModel.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot delete this job")

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}