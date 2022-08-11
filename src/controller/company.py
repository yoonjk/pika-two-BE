from flask import request, jsonify
from flask_restx import Resource, Namespace

Company = Namespace(
    name="Company",
    description="기업 상세 정보를 조회하기 위한 API,"
)

parser = Company.parser()
parser.add_argument('keyword', location='args', help='검색하고자 하는 키워드')
parser.add_argument('category',location='args',help="회사 업종")
parser.add_argument('type',location='args',help='회사 유형')
parser.add_argument('is_certified',location='args',help='인증된 기업')
parser.add_argument('page_size',location='args', default=20,type=int, help='페이지 사이즈')
parser.add_argument('page_num',location='args', default=1,type=int, help='페이지 번호')


@Company.route('/')
class CompanySearch(Resource):
    @Company.expect(parser)
    def get(self):
        '''기업 검색(Get)'''
        s_keyword = request.args.get('keyword', default='', type=str)
        com_category = request.args.get('category', default='', type=str)
        com_type = request.args.get('type', default='', type=str)
        com_is_certified = request.args.get('is_certified', default='false', type=bool)
        page_size = request.args.get('page_size', default='20', type=int)
        page_num = request.args.get('page_num', default='1', type=int)

        return jsonify({"code": 200})


@Company.route('/<int:company_id>')
class CompanyDetail(Resource):
    def get(self):
        '''기업 상세 정보(Get)'''
        return jsonify({"code": 200})


parser1 = Company.parser()
parser1.add_argument('year', location='args', help='검색하고자 하는 키워드')
parser1.add_argument('profession',location='args',help="회사 업종")

@Company.route('/<int:company_id>/wage')
class CompanyWage(Resource):
    @Company.expect(parser1)
    def get(self):
        '''직무,연차별 연봉 정보(Get)'''
        year = request.args.get('year', default='', type=int)
        profession = request.args.get('profession', default='', type=str)
        return jsonify({"code": 200})
