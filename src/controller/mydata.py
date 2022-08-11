from flask_restx import Resource, reqparse
from src.service import mydata
from src.util.dto import MydataDto

api = MydataDto.api

_account_model = MydataDto.account
_deposit_model = MydataDto.deposit
_annual_salary_model = MydataDto.annual_salary

_response_account = MydataDto.response_accounts
_response_deposits = MydataDto.response_deposits
_response_annual_salaries = MydataDto.response_annual_salaries

@api.route('/<int:user_id>/account', methods=["GET"], doc={"description": """ 유저 계좌내역
"""})
class Account(Resource):
    @api.response(200, 'Success', _account_model)
    @api.response(400, 'Bad Request')
    @api.marshal_with(_response_account)
    def get(self, user_id:int):
        """
        유저 계좌내역 조회
        """
        accounts = mydata.get_accounts(user_id=user_id)
        return {
            'status': 200,
            'data': accounts,
            'message': f'input: user_id={user_id}',
        }


deposit_parser = reqparse.RequestParser()
deposit_parser.add_argument('account', required=True, help='입금내역을 조회하려는 계좌')
@api.route('/<int:user_id>/deposit', methods=["GET"], doc={"description": """ 급여로 추정되는 입금내역 API
"""})
class Deposit(Resource):
    @api.expect(deposit_parser)
    @api.response(200, 'Success', _deposit_model)
    @api.response(400, 'Bad Request')
    @api.marshal_with(_response_deposits)
    def get(self, user_id:int):
        """
        급여로 추정되는 입금내역 조회
        """
        args = deposit_parser.parse_args()
        account = args['account']
        deposits = mydata.get_deposit(user_id, account)
        return {
            'status': 200,
            'data': deposits,
            'message': f'input: user_id={user_id}, account={account}',
        }

annual_salary_parser = reqparse.RequestParser()
annual_salary_parser.add_argument('account', type=str, required=True, help='입금내역을 조회하려는 계좌')
annual_salary_parser.add_argument('comments', action="split", required=True, help='급여에 해당하는 적요 리스트')
@api.route('/<int:user_id>/annual-salary', methods=["GET"], doc={"description": """ 유저 세후 연봉조회 API
"""})
class AnnualSalary(Resource):
    @api.expect(annual_salary_parser)
    @api.response(200, 'Success', _annual_salary_model)
    @api.response(400, 'Bad Request')
    @api.marshal_with(_response_annual_salaries)
    def get(self, user_id:int):
        """
        유저 세후 연봉조회
        """
        args = annual_salary_parser.parse_args()
        account = args["account"]
        comments = args["comments"]
        annaul_salarys = mydata.get_annual_salary(user_id, account, comments)
        return {
            'status': 200,
            'data': annaul_salarys,
            'message': f'input: user_id={user_id}, account={account}, comments={comments}',
        }
