from src.database import db
from src.model.models import User, FavoriteCompanies, Wage, Apply, JobPost, Company
from src.service.nickname_gen import nick_gen
from src.service.company import get_or_create_company
import logging


def signup(input):
    logging.info(f"signup - {input}")
    randNickname = nick_gen(1)
    cur_company_id = get_or_create_company(input['company_name'])
    if User.query.filter(User.email==input["email"]).count() == 0:
        newUser = User(
            nickname=randNickname,
            gender=input['gender'],
            profession="IT",
            cur_company_id=cur_company_id,
            email=input['email'],
            work_start_dt= f'{input["work_start_dt"]}-01-01',
            account="",
            # work_start_dt = int(input['work_start_dt']),
            birth_yr= int(input['birth_yr'])
            # birth_yr = int(input['birth_yr'])
        )
        db.session.add(newUser)
        db.session.commit()
        return {
            "user_id": newUser.id,
            "nickname": randNickname,
            "profession": newUser.profession,
            "gender": newUser.gender,
            "email": newUser.email,
            "work_start_dt": newUser.work_start_dt,
            "applied_list": [],
            "acccount": newUser.account,
            "birth_yr": newUser.birth_yr,
            "cur_company_id": newUser.cur_company_id,
        }
    user = User.query.filter(User.email==input["email"]).first()
    applied_list = [post.job_post_id for post in Apply.query.filter(Apply.user_id==user.id).all()]
    return {
        "user_id": user.id,
        "nickname": user.nickname,
        "profession": user.profession,
        "gender": user.gender,
        "email": user.email,
        "work_start_dt": user.work_start_dt,
        "applied_list": applied_list,
        "acccount": user.account,
        "birth_yr": user.birth_yr,
        "cur_company_id": user.cur_company_id,
    }


# 마이페이지 정보 조회
def get_my_page(user_id):
    print(user_id)
    user = User.query.get(user_id)
    wage = sorted(Wage.query.filter(Wage.user_id == user_id).all(), key=lambda x: x.yr)

    prev_wage = 0
    cur_wage = 0
    if len(wage) > 0:
        if len(wage) < 2:
            cur_wage = wage[0].amount
        else:
            prev_wage = wage[0].amount
            cur_wage = wage[1].amount

    response = {
        "id": user_id,
        "nickname": user.nickname,
        "cur_company_id": user.cur_company_id,
        "work_start_dt": user.cur_company_id,
        "prev_wage": prev_wage,
        "cur_wage": cur_wage,
    }

    return response


# 찜목록
def get_fav_list(user_id):
    print(user_id)
    fav_list = FavoriteCompanies.query.filter(FavoriteCompanies.user_id == user_id).all()
    response = []
    print(fav_list)
    for i in fav_list:
        company = Company.query.get(i.company_id)
        res = {"fav_company_id": i.id, "id": company.id, "name": company.name}
        response.append(res)

    return response


# 찜등록
def post_fav_list(user_id, company_id):
    print(user_id)
    fav_company = FavoriteCompanies(user_id=user_id, company_id=company_id)
    db.session.add(fav_company)
    db.session.commit()


# 찜삭제
def delete_fav_list(fav_company_id):
    FavoriteCompanies.query.get(fav_company_id).delete()
    db.session.commit()


# 지원회사 목록
def get_applied_posts(user_id):
    print(user_id)
    app_list = Apply.query.filter_by(user_id=user_id).all()
    response = []
    for i in app_list:
        jobPost = JobPost.query.get(i.job_post_id)
        company = Company.query.get(jobPost.company_id)
        res = {
            "apply_id": i.id,
            "post_id": jobPost.id,
            "post_title": jobPost.title,
            "start_dt": jobPost.start_dt,
            "end_dt": jobPost.end_dt,
            "company_id": jobPost.company_id,
            "company_name": company.name,
        }
        response.append(res)

    return response


# 지원하기
def post_applied_posts(user_id, post_id):
    print(user_id)
    app_company = Apply(user_id=user_id, job_post_id=post_id, status='진행중')
    db.session.add(app_company)
    db.session.commit()


# 지원상태 수정
def update_applied_posts(user_id, apply_id, status):
    print(user_id)
    Apply.query.filter_by(id=apply_id).update({'status': status})
    db.session.commit()


# 지원공고 삭제
def delete_applied_posts(apply_id):
    Apply.query.get(apply_id).delete()
    db.session.commit()
