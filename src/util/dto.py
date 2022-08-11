from flask_restx import Namespace,fields

class MydataDto:
    api = Namespace("Mydata", description="마이데이터 조회 및 연동 API")

    account = api.model('Account', {
        "bank": fields.String(description="은행"),
        "account": fields.String(desciption="상품명"),
        "balance": fields.Integer(description="잔액"),
    })

    deposit = api.model("Deposit", {
        "date": fields.Date(description="입금일자"),
        "amount": fields.Integer(description="입금액"),
        "comment": fields.String(description="적요"),
    })

    annual_salary = api.model("AnnulSalary", {
        "year": fields.Integer(description="연도"),
        "annual_salary": fields.Integer(description="연봉"),
    })

    response_accounts = api.model('response_accounts',{
        'status' : fields.Integer(description="상태코드"),
        'data' : fields.List(fields.Nested(account,description="데이터 집합")),
        'message' : fields.String(description="상태 메시지"),
    })

    response_deposits = api.model('response_deposits',{
        'status' : fields.Integer(description="상태코드"),
        'data' : fields.List(fields.Nested(deposit, description="데이터 집합")),
        'message' : fields.String(description="상태 메시지"),
    })

    response_annual_salaries = api.model('response_annual_salaries',{
        'status' : fields.Integer(description="상태코드"),
        'data' : fields.List(fields.Nested(annual_salary, description="데이터 집합")),
        'message' : fields.String(description="상태 메시지"),
    })