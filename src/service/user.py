from src.database import db

# 사용자 기본정보 등록
from src.model.models import User
import logging

def signup(input):
    print(input)
    newUser = User(
        nickname=input['nickname'],
        gender=input['gender'],
        profession=input['profession'],
        cur_company_id=input['cur_company_id'],
        email=input['email'],
        work_start_dt=input['work_start_dt'],
        account=input['account'],
        birth_yr=input['birth_yr'],
    )
    db.session.add(newUser)
    db.session.commit()