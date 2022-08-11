from sqlalchemy.sql.expression import Delete, Insert, Select
from src.database import db

# 사용자 기본정보 등록
from src.model.models import User, FavoriteCompanies


def signup(input):
    print(input)
    newUser = User(nickname=input['nickname'], gender=input['gender'], email=input['email'])
    db.session.add(newUser)
    db.session.commit()


# 마이페이지 정보 조회
def get_my_page(user_id):
    print(user_id)
    user = User.query.get(user_id)
    wage = sorted(User.query.filter_by(user_id=user_id))

    prev_wage = wage[0]['amount']
    cur_wage = wage[1]['amount']
    response = {
        "id": user_id,
        "nickname": user['nickname'],
        "cur_company_id": user['cur_company_id'],
        "work_start_dt": user['cur_company_id'],
        "prev_wage": prev_wage,
        "cur_wage": cur_wage,
    }

    return response


# 찜목록
def get_fav_list(user_id):
    print(user_id)
    fav_list = User.query.get(user_id)['fav_companies']
    response = []
    for i in fav_list:
        res = {"id": i['id'], "name": i['name']}
        response.append(res)

    return response


# 찜등록
def post_fav_list(user_id, company_id):
    print(user_id)
    fav_company = FavoriteCompanies(user_id=user_id, company_id=company_id)
    db.session.add(fav_company)
    db.session.commit()


# 찜삭제
def delete_fav_list():
    print(user_id)
    request.get_json()
    return jsonify({"code": 200})


# 지원회사 목록
def get_applied_list():
    print(user_id)
    return jsonify({"code": 200})


# 계좌목록
def get_account_list():
    print(user_id)
    return jsonify({"code": 200})


# 급여계좌 등록
def post_account_list():
    print(user_id)
    request.get_json()
    return jsonify({"code": 200})


# 입금내역
def get_deposit_summary():
    print(user_id)
    print(account_id)
    return jsonify({"code": 200})


# 개인연봉 조회
def get_wage():
    print(user_id)
    return jsonify({"code": 200})
