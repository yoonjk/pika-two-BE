from sqlalchemy import or_, and_, func, text
from src.database import db
from src.model.models import Company, JobPost
from datetime import datetime

now = datetime.now()


def get_main_page_jobposts():

    now_dt = datetime.now().date()

    job_post = JobPost.query.filter(db.func.date(JobPost.start_dt) <= now_dt, db.func.date(JobPost.end_dt) >= now_dt)

    job_posts = []
    for job_p in job_post:
        com = Company.query.filter(job_p.company_id == Company.id).first()
        res = {
            "company_id": com.id,
            "company_name": com.name,
            "type": com.type,
            "post_id": job_p.id,
            "post_title": job_p.title,
            "start_dt": job_p.start_dt.strftime('%Y-%m-%d'),
            "end_dt": job_p.end_dt.strftime('%Y-%m-%d'),
        }
        job_posts.append(res)

    return job_posts
