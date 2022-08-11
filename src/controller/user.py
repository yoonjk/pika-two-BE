from flask import jsonify, request
from flask_restx import Resource, Namespace
from src.service.user import signup, get_my_page, get_fav_list

User = Namespace('User')


@User.route('/signup')
class Signup(Resource):

    #사용자 기본정보 등록
    def post(self):
        signup(dict(request.get_json()))
        return jsonify({"code": 200})


@User.route('/<string:user_id>')
class MyPage(Resource):

    #마이페이지 정보 조회
    def get(self, user_id):
        print(user_id)
        response = get_my_page(user_id)
        return jsonify({"code": 200, "data": response})


@User.route('/<string:user_id>/fav-posts')
class FavList(Resource):

    #찜목록
    def get(self, user_id):
        print(user_id)
        response = get_fav_list(user_id)
        return jsonify({"code": 200, "data": response})

    #찜등록
    def post(self, user_id):
        print(user_id)
        request.get_json()['company_id']
        return jsonify({"code": 200})

    #찜삭제
    def delete(self, user_id):
        print(user_id)
        request.get_json()
        return jsonify({"code": 200})


@User.route('/<string:user_id>/applied-posts')
class AppliedList(Resource):

    #지원회사 목록
    def get(self, user_id):
        print(user_id)
        return jsonify({"code": 200})


@User.route('/<string:user_id>/account')
class AccountList(Resource):

    #계좌목록
    def get(self, user_id):
        print(user_id)
        return jsonify({"code": 200})

    #급여계좌 등록
    def post(self, user_id):
        print(user_id)
        request.get_json()
        return jsonify({"code": 200})


@User.route('/<string:user_id>/<string:account_id>/summary')
class DepositSummary(Resource):

    #입금내역
    def get(self, user_id, account_id):
        print(user_id)
        print(account_id)
        return jsonify({"code": 200})


@User.route('/<string:user_id>/wage')
class Wage(Resource):

    #개인연봉 조회
    def get(self, user_id):
        print(user_id)
        return jsonify({"code": 200})

