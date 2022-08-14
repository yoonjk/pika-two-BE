import pandas as pd
import datetime
import xlrd
import os
from dateutil.relativedelta import relativedelta
from flask import current_app
import pandas as pd
import logging
from src.database import db
from src.model.models import User, Memo, Company, Deposit, Wage
from sqlalchemy import func

ACCOUNT_BANK_MAP = {
    "KB나라사랑우대통장": "국민은행",
    "MY 입출금통장": "케이뱅크",
    "NH X 카카오페이통장(비대면실명확인)": "농협은행",
    "U드림 저축예금 (인터넷전용)": "신한은행",
    "Young 하나 통장": "하나은행",
    "세이프박스": "카카오뱅크",
    "입출금통장": "카카오뱅크",
    "자유저축예탁금": "지역농협",
    "첫급여우리 통장": "우리은행",
    "플러스박스": "케이뱅크",
}

def read_mydata(user_id:int) -> object:
    """ API나 파일을 통해 마이데이터 수집
    Args:
        user_id (int): 마이데이터를 수집할 user_id
    Returns:
        object: 엑셀 object
    """
    mydata_file = f"{user_id}.xlsx"
    mydata = None
    data_dir = current_app.config.get("DATADIR") + "/data/"
    if mydata_file in os.listdir(data_dir):
        try:
            mydata = xlrd.open_workbook(data_dir+mydata_file)
            mydata = mydata.sheet_by_index(0)
        except Exception as e:
            logging.error(f"[Error] {e}")
        
    return mydata

def read_statement(user_id:int) -> pd.DataFrame:
    """ 입출급내역 수집
    Args:
        user_id (int): 입출금내역을 수집할 user_id
    Returns:
        pd.DataFrame: 입출금내역
    """
    statement_file = f"{user_id}.xlsx"
    statement = None
    data_dir = current_app.config.get("DATADIR")
    if statement_file in os.listdir(data_dir):
        try:
            statement = pd.read_excel(data_dir+statement_file, sheet_name="가계부 내역")
        except Exception as e:
            logging.error(f"[ERror] {e}")
    return statement

def get_accounts(user_id:int) -> list:
    """ 유저의 계좌내역 조회
    Args:
        user_id (int): 계좌내역을 조회할 user_id
    Returns:
        list: 계좌내역
    """
    mydata = read_mydata(user_id=user_id)
    if mydata is None:
        # TODO: 계좌 랜덤 생성
        return []

    account_row_start = 0
    account_row_end = 0
    account_col = 0
    balance_col = 0
    for col_idx in range(mydata.ncols):
        for row_idx in range(mydata.nrows):
            cell_value = mydata.cell(row_idx, col_idx).value
            if cell_value == "자유입출금 자산":
                account_row_start = row_idx
                account_col = col_idx+1
            elif cell_value == "신탁 자산":
                account_row_end = row_idx
            elif cell_value == "금액":
                balance_col = col_idx
            else:
                continue
        if account_row_start and account_row_end and account_col and balance_col:
            break
    accounts = [{
        "bank": ACCOUNT_BANK_MAP[mydata.cell(row_idx, account_col).value],
        "account": mydata.cell(row_idx, account_col).value,
        "balance": int(mydata.cell(row_idx, balance_col).value),
    } for row_idx in range(account_row_start, account_row_end)]
    
    return accounts

def register_account(user_id:int, account:str) -> tuple:
    """ 유저의 급여계좌 정보 등록
    Args:
        user_id (int): 급여계좌를 등록할 user_id
        account (str): 급여계좌
    Returns:
        int: status_code
    """
    status_code = 200
    msg = account
    try:
        user = User.query.filter(User.id==user_id).first()
        user.account = account
        db.session.commit()
    except Exception as e:
        status_code = 404
        msg = str(e)
        logging.error(f"[ERROR] register_account - {e}")
        
    return (status_code, msg)

def get_deposit(user_id:int)->list:
    """ 유저의 급여로 추정되는 입금내역 조회
    Args:
        user_id (int): 입금내역을 조회할 user_id
    Returns:
        list: 입금 내역
    """
    statement = read_statement(user_id=user_id)
    account = User.query.filter(User.id==user_id).first().account
    salary_criteria = 500000
    if statement is None:
        # TODO: 급여 및 입금 내역 랜덤 생성 필요
        return []
    deposit_df = statement.loc[
        (statement["결제수단"]==account) \
        & (statement["금액"] > salary_criteria) \
        & (statement["날짜"] > datetime.datetime.now() - relativedelta(months=6))
    , ["날짜", "금액", "내용"]
    ]
    deposit_df["날짜"] = deposit_df["날짜"].apply(lambda x: x.strftime("%Y-%m-%d"))
    deposit_df.rename(columns={
        "날짜": "date",
        "금액": "amount",
        "내용": "memo",
    }, inplace=True)
    deposits = deposit_df.reset_index(drop=True).to_dict(orient="record")
    
    return deposits

def add_memos(user_id:int, memos:list) -> tuple:
    """ 유저의 급여 적요 등록
    Args:
        user_id (int): 계좌내역을 조회할 user_id
        memos (list): 급여에 해당하는 적요 리스트
    Returns:
        tuple: (상태코드, 메세지)
    """
    status_code = 200
    msg = memos
    registered_memos = [m.memo for m in Memo.query.filter(Memo.user_id==user_id).all()]
    try:
        # TODO: memo 테이블에서 없는 memo만 등록
        for memo in memos:
            if memo not in registered_memos:
                new_memo = Memo(
                    user_id=user_id,
                    memo=memo,
                )
                db.session.add(new_memo)
        db.session.commit()

        # 메모 기반으로 급여내역 등록
        status_code = add_salary_history(user_id)

        msg = f"{user_id}의 급여계좌 등록이 완료되었습니다"

    except Exception as e:
        status_code = 404
        msg = f"{user_id}의 급여계좌 등록 중 에러가 발생하였습니다 - {e}"
        logging.error(msg)

    return (status_code, msg)

def get_salary_history_from_mydata(user_id:int) -> list:
    """ 마이데이터에서 유저의 급여내역 조회
    Args:
        user_id (int): 급여내역을 조회할 user_id
    Returns:
        list: 급여내역
    """
    statement = read_statement(user_id=user_id)
    user = User.query.filter(User.id==user_id).first()
    account = user.account
    memos = [memo.memo for memo in Memo.query.filter(Memo.user_id==user_id).all()]
    if statement is None:
        # TODO: 급여 및 입금 내역 랜덤 생성 필요
        return []

    salary_df = statement.loc[
        (statement["결제수단"]==account) \
        & (statement["내용"].isin(memos))
    , ["날짜", "내용", "금액"]]
    salary_df["날짜"] = salary_df["날짜"].apply(lambda x: x.strftime("%Y-%m-%d"))
    salary_df.rename(columns={
        "날짜": "deposit_dt",
        "금액": "deposit_amount",
        "내용": "memo",
    }, inplace=True)
    salary_history = salary_df.to_dict(orient="records")
    return salary_history


def add_salary_history(user_id:int) -> tuple:
    """ 유저의 급여 입금내역 추가
    Args:
        user_id (int): 급여내역을 추가할 user_id
    """
    status_code = 200
    try:
        salary_history = get_salary_history_from_mydata(user_id)
        for salary in salary_history:
            if Deposit.query.filter((Deposit.user_id==user_id) & (Deposit.deposit_dt==salary["deposit_dt"]) & (Deposit.deposit_amount==salary["deposit_amount"]) & (Deposit.memo==salary["memo"])).count() == 0:
                new_salary = Deposit(
                    deposit_amount=salary["deposit_amount"],
                    deposit_dt=salary["deposit_dt"],
                    user_id=user_id,
                    memo=salary["memo"],
                )
                db.session.add(new_salary)
        db.session.commit()

        # 연봉정보 등록
        status_code = add_annual_salary(user_id)

        logging.info(f"{user_id}의 급여내역이 추가되었습니다.")
        return status_code
    except Exception as e:
        logging.error(f"{user_id}의 급여내역 추가 중 오류가 발생하였습니다 - {e}")
        raise Exception(e)

def add_annual_salary(user_id:int) -> tuple:
    """ 유저의 연봉 데이터 추가
    Args:
        user_id (int): 급여내역을 추가할 user_id
    """
    user = User.query.filter(User.id==user_id).first()
    company_id = user.cur_company_id
    annual_salaries = db.session.query(func.sum(Deposit.deposit_amount).label("annual_salary"), func.year(Deposit.deposit_dt).label("year")).filter(Deposit.user_id==1).group_by(func.year(Deposit.deposit_dt)).all()
    status_code = 200

    try:
        for salary in annual_salaries:
            career_yr = salary.year - user.work_start_dt.year
            registered_wage = Wage.query.filter((Wage.user_id==user_id) & (Wage.yr==career_yr) & (Wage.company_id==company_id)).first()
            if registered_wage is None:
                new_wage = Wage(
                    amount=salary.annual_salary,
                    user_id=user_id,
                    company_id=company_id,
                    yr=career_yr,
                )
                db.session.add(new_wage)
            else:
                if registered_wage.amount != salary.annual_salary:
                    registered_wage.amount = salary.annual_salary
        db.session.commit()
        logging.info(f"{user_id}의 연봉정보가 등록되었습니다.")
        return status_code
    except Exception as e:
        logging.error(f"{user_id}의 연봉정보 등록 중 오류가 발생하였습니다 - {e}")
        raise Exception(e)


def update_annual_salary(user_id:int, year:int) -> tuple:
    """ 유저의 연봉 업데이트
    Args:
        user_id (int): 급여내역을 추가할 user_id
        year (int): 연봉을 업데이트 하려는 연도
    Returns:
        int: 상태코드
    """
    status_code=200
    annual_salary=None
    try:
        user = User.query.filter(User.id==user_id).first()
        annual_salary = db.session.query(func.sum(Deposit.deposit_amount).label("annual_salary"), func.year(Deposit.deposit_dt).label("year")).filter((Deposit.user_id==user_id)&(func.year(Deposit.deposit_dt)==year)).group_by(func.year(Deposit.deposit_dt)).first().annual_salary  # {user_id}의 {year}연도의 급여 총합
        career_yr = year - user.work_start_dt.year
        wage = Wage.query.filter((Wage.user_id==user_id)&(Wage.yr==career_yr))
        wage.amount = annual_salary
        db.session.commit()
        logging.info(f"{user_id}의 {year}년 연봉 정보를 업데이트하였습니다")
    except Exception as e:
        status_code=404
        logging.error(f"{user_id}의 {year}년 연봉 정보를 업데이트하던 중 오류가 발생하였습니다 - {e}")
    
    return status_code, annual_salary

def get_annual_salary(user_id:int, year:int) -> list:
    """ 유저의 연봉내역 조회
    Args:
        user_id (int): 연봉내역을 조회할 user_id
        year (int): 연봉을 조회하려는 연도
    Returns:
        list: 연봉내역
    """
    user = User.query.filter(User.id==user_id).first()
    career_yr = year-user.work_start_dt.year
    company_name = Company.query.filter(Company.id==user.cur_company_id).first().name
    annual_salary = {
        "year": career_yr,
        "annual_salary": Wage.query.filter(
            (Wage.user_id==user_id) &
            (Wage.yr==career_yr)
        ).first().amount,
        "company": company_name,
    }
        
    return annual_salary