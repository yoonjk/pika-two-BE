from flask import jsonify, request
from flask_restx import Resource, Namespace
from src.service import mydata
from src.util.dto import MydataDto

Mydata = Namespace('Mydata')

_account_model = MydataDto.account
_deposit_model = MydataDto.deposit
_annual_salary_model = MydataDto.annual_salary

@Mydata.route('/<int:user_id>/account', methods=["GET"], doc={"description": """
"""})
class Account(Resource):
    """ 유저 계좌내역 API
    """
    def get(self, user_id:int):
        accounts = mydata.get_accounts(user_id=user_id)
        return {
            'status': 200,
            'data': accounts,
            'message': f'input: user_id={user_id}',
        }



@Mydata.route('/<int:user_id>/deposit', methods=["GET"], doc={"description": """
"""})
class Deposit(Resource):
    """ 급여로 추정되는 입금내역 조회 API
    """
    def get(self, user_id:int):
        account = request.args.get("account", typoe=str)
        deposits = mydata.get_deposit(user_id, account)
        return {
            'status': 200,
            'data': deposits,
            'message': f'input: user_id={user_id}, account={account}',
        }

@Mydata.route('/<int:user_id>/annual-salary', methods=["GET"], doc={"description": """
"""})
class AnnualSalary(Resource):
    """ 유저 연봉조회 API
    """
    def get(self, user_id:int):
        account = request.args.get("account", type=str)
        comments = request.args.get("comments", type=list)
        annaul_salarys = mydata.get_annual_salary(user_id, account, comments)
        return {
            'status': 200,
            'data': annaul_salarys,
            'message': f'input: user_id={user_id}, account={account}, comments={comments}',
        }
