from sqlalchemy import null
from src.database import db


class User(db.Model):
    __table_name__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    nickname = db.Column(db.String(256), unique=True)
    gender = db.Column(db.String(64), nullable=False)
    profession = db.Column(db.String(256), nullable=False)    # 직무, enum화 필요
    # applied_posts = db.relationship("JobPost", backref="id", lazy="select")
    cur_company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    # fav_companies = db.relationship("Company", backref="id", lazy="select")
    work_start_dt = db.Column(db.DateTime, nullable=False)
    account = db.Column(db.String(256), nullable=False)
    birth_yr = db.Column(db.Integer,nullable=False)
    created_dt = db.Column(db.DateTime, server_default=db.func.now())
    modified_dt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Company(db.Model):
    __table_name__ = "company"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)    
    name = db.Column(db.String(256), nullable=False)
    type = db.Column(db.String(100), nullable=False)    # 기업 타입, enum
    category = db.Column(db.String(100), nullable=False)    # 기업 유형, enum, ex) 유통업, 금융업 등
    is_certificated = db.Column(db.Boolean, nullable=False) # 기업 인증 유무
    created_dt = db.Column(db.DateTime, server_default=db.func.now())
    modified_dt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class FavoriteCompanies(db.Model):
    __table_name__ = "favorite_companies"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    # created_dt = db.Column(db.DateTime, server_default=db.func.now())
    # modified_dt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class JobPost(db.Model):
    __table_name__ = "job_post"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String(1024), nullable=False)
    start_dt = db.Column(db.DateTime, nullable=False)
    end_dt = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(100), nullable=False)    # 채용유형, ex) 공채, 수시
    company_id= db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    created_dt = db.Column(db.DateTime, server_default=db.func.now())
    modified_dt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Apply(db.Model):
    __table_name__ = "apply"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    job_post_id = db.Column(db.Integer, db.ForeignKey("job_post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(100), nullable=False)  # enum, ex) 작성중, 합격, 불합격 등
    created_dt = db.Column(db.DateTime, server_default=db.func.now())
    modified_dt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Deposit(db.Model):
    __table_name__ = "account"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    deposit_amount = db.Column(db.Integer)
    deposit_dt = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_dt = db.Column(db.DateTime, server_default=db.func.now())
    modified_dt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Wage(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    yr = db.Column(db.Integer)
    created_dt = db.Column(db.DateTime, server_default=db.func.now())
    modified_dt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    content = db.Column(db.String(1024), nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    created_dt = db.Column(db.DateTime, server_default=db.func.now())
    modified_dt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())