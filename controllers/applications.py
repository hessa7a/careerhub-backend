# controllers/applications.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.application import ApplicationModel
from models.job_post import JobPostModel
from models.user import UserModel
from serializers.application import ApplicationCreateSchema, ApplicationUpdateSchema, ApplicationSchema
from database import get_db
from dependencies.get_current_user import get_current_user


router = APIRouter()


@router.post("/applications", response_model=ApplicationSchema, status_code=201)
def create_application(
    application: ApplicationCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "applicant":
        raise HTTPException(status_code=403, detail="Only applicants can apply for jobs")

    job = db.query(JobPostModel).filter(
        JobPostModel.id == application.job_post_id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing_application = db.query(ApplicationModel).filter(
        ApplicationModel.applicant_id == current_user.id,
        ApplicationModel.job_post_id == application.job_post_id
    ).first()

    if existing_application:
        raise HTTPException(status_code=409, detail="You already applied for this job")

    new_application = ApplicationModel(
        message=application.message,
        resume=application.resume,
        applicant_id=current_user.id,
        job_post_id=application.job_post_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@router.get("/applications/my", response_model=list[ApplicationSchema])
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "applicant":
        raise HTTPException(status_code=403, detail="Only applicants can view their applications")

    applications = db.query(ApplicationModel).filter(
        ApplicationModel.applicant_id == current_user.id
    ).all()

    return applications


@router.get("/jobs/{job_id}/applications", response_model=list[ApplicationSchema])
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    job = db.query(JobPostModel).filter(
        JobPostModel.id == job_id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot view applications for this job")

    applications = db.query(ApplicationModel).filter(
        ApplicationModel.job_post_id == job_id
    ).all()

    return applications


@router.put("/applications/{application_id}", response_model=ApplicationSchema)
def update_application_status(
    application_id: int,
    application_data: ApplicationUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    application = db.query(ApplicationModel).filter(
        ApplicationModel.id == application_id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    job = db.query(JobPostModel).filter(
        JobPostModel.id == application.job_post_id
    ).first()

    if job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot update this application")

    application.status = application_data.status

    db.commit()
    db.refresh(application)

    return application