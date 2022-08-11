import pandas as pd
import datetime
import xlrd
import os
from dateutil.relativedelta import relativedelta
from flask import current_app
import pandas as pd
import logging

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
    logging.info(f'BASEDIR={current_app.config.get("BASEDIR")}')
    data_dir = current_app.config.get("BASEDIR") + "/data/"
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
    data_dir = current_app.config.get("BASEDIR") + "/data/"
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


def get_deposit(user_id:int, account:str):
    """ 유저의 급여로 추정되는 입금내역 조회
    Args:
        user_id (int): 계좌내역을 조회할 user_id
        account (str): 급여계좌
    Returns:
        list: 계좌내역
    """
    statement = read_statement(user_id=user_id)
    salary_criteria = 500000
    if statement is None:
        # TODO: 급여 및 입금 내역 랜덤 생성 필요
        return []
    deposit_df = statement.loc[
        (statement["결제수단"]==account) \
        & (statement["금액"]>salary_criteria) \
        & (statement["날짜"] > datetime.datetime.now() - relativedelta(months=6))
    , ["날짜", "금액", "내용"]
    ]
    deposit_df["날짜"] = deposit_df["날짜"].apply(lambda x: x.strftime("%Y-%m-%d"))
    deposit_df.rename(columns={
        "날짜": "date",
        "금액": "amount",
        "내용": "comment",
    }, inplace=True)
    deposits = deposit_df.reset_index(drop=True).to_dict(orient="record")
    
    return deposits

def get_annual_salary(user_id:int, account:str, comments:list):
    """ 유저의 계좌내역 조회
    Args:
        user_id (int): 계좌내역을 조회할 user_id
        account (str): 급여계좌
        commnts (list): 급여에 해당하는 적요 리스트
    Returns:
        list: 계좌내역
    """
    statement = read_statement(user_id=user_id)
    if statement is None:
        # TODO: 급여 및 입금 내역 랜덤 생성 필요
        return []

    salary_df = statement.loc[
        (statement["결제수단"]==account) \
        & (statement["내용"].isin(comments))
    ]
    annual_income_dict = salary_df.groupby(salary_df["날짜"].map(lambda x: x.year)).sum().to_dict('index')
    annual_salaries = [{"year": key, "annual_salary": value["금액"]} for key, value in annual_income_dict.items()]
    return annual_salaries