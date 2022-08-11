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

deposit_parser = reqparse.RequestParser()
deposit_parser.add_argument('account', required=True, help='입금내역을 조회하려는 계좌')

@api.route('/<int:user_id>/account', methods=["GET", "POST"], doc={"description": """ 유저 계좌내역
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

    @api.expect(deposit_parser)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    def post(self, user_id:int):
        """
        유저 데이터에 급여계좌 정보 추가
        """
        args = deposit_parser.parse_args()
        account = args['account']
        status_code, msg = mydata.register_account(user_id, account)
        if status_code == 200:
            response = {
            'status': status_code,
            'data': msg,
            'message': 'Success to register account'
        }

        else:
            response = {
            'status': status_code,
            'data': msg,
            'message': 'Fail to register account'
        }
    
        return response


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
annual_salary_parser.add_argument('memos', action="split", required=True, help='급여에 해당하는 적요 리스트')
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
        memos = args["memos"]
        annaul_salarys = mydata.get_annual_salary(user_id, account, memos)
        return {
            'status': 200,
            'data': annaul_salarys,
            'message': f'input: user_id={user_id}, account={account}, memos={memos}',
        }
