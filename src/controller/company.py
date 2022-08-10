from flask import jsonify, request, app
from flask_restx import Resource, Api


api = Api(app)


@api.route('/api/company')
class CompanySearch(Resource):

    #기업검색
    def get(self, user_id):
        print(user_id)
        return jsonify({"code": 200})


@api.route('/api/company<string:company_id>')
class CompanyDetail(Resource):

    #기업상세정보
    def get(self, company_id):
        print(company_id)
        return jsonify({"code": 200})


@api.route('/api/company<string:company_id>/wage')
class CompanyWage(Resource):

    #기업연봉정보
    def get(self, company_id):
        print(company_id)
        return jsonify({"code": 200})

