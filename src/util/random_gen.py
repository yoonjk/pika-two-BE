import json, requests
import random
from src.model.models import User, Company, Memo
from datetime import date
import pandas as pd
from flask import current_app
import os



BANK_ACCOUNTS = {
    "국민은행": ["KB나라사랑우대통장", "KB Star*t통장"],
    "케이뱅크": ["MY 입출금통장", "플러스박스"],
    "농협은행": ["NH X 카카오페이통장(비대면실명확인)", "NH주거래우대통장"],
    "신한은행": ["U드림 저축예금 (인터넷전용)"],
    "하나은행": ["Young 하나 통장", "하나멤버스 주거래통장"],
    "카카오뱅크": ["세이프박스", "입출금통장"],
    "지역농협": ["자유저축예탁금"],
    "우리은행": ["첫급여우리 통장", "위비모바일통장", "저축예금"],
    "토스뱅크": ["토스뱅크"],
}
DEPOSIT_MEMOS = {
    "홍길동": (500, 2000),
    "환불대금": (500, 1000),
    "적금만기": (1200,24000),
    "김국민": (500, 1500),
    "로또 당첨금": (1, 1),
}
SALARY_MEMOS = ["월정급여", "급여", "정기급여"]

def nick_gen(p):
    params = {
        'format':'json',
        'count': p
    }
    url = 'https://nickname.hwanmoo.kr/'
    response = requests.get(url, params=params)
    json_data = json.loads(response.text)['words']

    return ','.join(json_data)

def account_list_gen():
    account_list = []
    for bank, accounts in BANK_ACCOUNTS.items():
        if bank == "국민은행":
            account_list.append({            
                "bank": "국민은행",
                "account": "KB마이핏통장",
                "balance": 15000000
            })
        else:
            if random.random()>=0.5:
                account = random.choice(accounts)
                account_list.append({            
                    "bank": bank,
                    "account": account,
                    "balance": random.randint(0, 100)*1000,
                })
    return account_list

def deposit_list_gen(user_id, period=12, salary_day=21):
    csv_path = f'{current_app.config.get("DATADIR")}{user_id}_deposit.csv'
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path).to_dict(orient="record")
    user = User.query.filter(User.id==user_id).first()
    company_name = Company.query.get(user.cur_company_id).name
    salary_memos = SALARY_MEMOS + [company_name]
    salary_memo = random.choice(salary_memos)
    today = date.today()
    year = today.year
    m = today.month
    standard_salary = int(abs(random.gauss(3000, 200)))
    deposit_list = []
    for month in range(m, m-period,-1):
        yr, month = (year, month) if month > 0 else (year-1, month+12)
        salary_dt = "{}-{:02d}-{:02d}".format(yr, month, salary_day)
        salary_amount = int(abs(random.gauss(standard_salary, 5)))*1000
        deposit_list.append({
            "date": salary_dt,
            "amount": salary_amount,
            "memo": salary_memo,
        })
        if random.random() < 0.2:
            day = random.randrange(1, salary_day-1)
            deposit_memo = random.choice(list(DEPOSIT_MEMOS.keys()))
            start, end = DEPOSIT_MEMOS[deposit_memo]
            rand_amount = max(int(random.expovariate(start)*1000) if deposit_memo == "로또 당첨금" else random.randrange(start, end), 500)*1000
            deposit_list.append({
                "date": "{}-{:02d}-{:02d}".format(yr, month, day),
                "amount": rand_amount,
                "memo": deposit_memo,
            })
    pd.DataFrame(deposit_list).to_csv(csv_path, index=False)
    return deposit_list

def salary_history_gen(user_id, memos):
    deposit_df = pd.read_csv(f'{current_app.config.get("DATADIR")}{user_id}_deposit.csv')
    salary_df = deposit_df.loc[
        (deposit_df["memo"].isin(memos))
    ]
    salary_df["date"] = salary_df["date"]
    salary_df.rename(columns={
        "date": "deposit_dt",
        "amount": "deposit_amount",
        "memo": "memo"
    }, inplace=True)
    salary_history = salary_df.to_dict(orient="records")
    return salary_history
