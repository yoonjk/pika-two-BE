from flask import request, jsonify
from flask_restx import Resource, Namespace
from src.service.company import *

Company = Namespace(
    name="Company",
    description="기업 상세 정보를 조회하기 위한 API,"
)

@Company.route('/')
class CompanySearch(Resource):
    def get(self):
        '''기업 검색(Get)'''
        com_keyword = request.args.get('keyword', default='', type=str)
        com_category = request.args.get('category', default='', type=str)
        com_type = request.args.get('type', default='', type=str)
        com_is_certified = request.args.get('is_certified', default=0, type=int)
        p_size = request.args.get('page_size', default='20', type=int)
        p_num = request.args.get('page_num', default='1', type=int)

        response = get_search_company(com_keyword, com_category, com_type, com_is_certified, p_size, p_num)

        return response

@Company.route('/<int:company_id>')
class CompanyDetail(Resource):
    def get(self, company_id):
        '''기업 상세 정보(Get)'''
        print(company_id)
        response = get_company_info(company_id)
        return jsonify({"code": 200,"data" : response})


@Company.route('/<int:company_id>/wage')
class CompanyWage(Resource):
    def get(self, company_id):
        '''직무,연차별 연봉 정보(Get)'''
        year = request.args.get('year', default='', type=int)
        pro = request.args.get('profession', default='', type=str)
        response = get_company_wage(company_id, year, pro)
        return jsonify({"code": 200, "data": response})
