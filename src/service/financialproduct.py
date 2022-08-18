from src.model.models import User, Wage
from src.service import mydata
from datetime import datetime
from flask import current_app
import requests
# from src.util.ml import *
import logging

def get_user_info(user_id):
    '''추천시스템으로 넘길 유저 사용자 정보 불러오기'''
    user = User.query.filter(User.id == user_id).first()
    wage = Wage.query.filter(Wage.user_id == user_id).first()
    wage_amount = mydata.get_annual_salary(user_id, year=datetime.today().year)["annual_salary"] if wage is None else wage.amount

    result = {
        "user_id" : user.id,
        "sexo": 'V' if user.gender == 'F' else 'H',
        "age" :  datetime.now().year - user.birth_yr,
        "wage" : wage_amount,
        "enter_dt" : user.work_start_dt.strftime('%Y-%m-%d')
    }

    return result

def read_finance_product(cluster_rank):
    '''클러스터 결과에 읽어오기'''
    product_file = "cluster_rank.csv"
    data_dir = current_app.config.get("DATADIR")

    f_read = open(data_dir+product_file, 'r')
    lines = f_read.readlines()

    return lines[int(cluster_rank)].rstrip('\n')

def find_finance_product(prod_ls):
    '''상품 찾아서 return 하기'''
    product_file = "financial_products.csv"
    data_dir = current_app.config.get("DATADIR")

    p_read = open(data_dir + product_file, 'r', encoding='UTF8')
    p_lines = p_read.readlines()
    p_lines = list(map(lambda s: s.strip(), p_lines))

    result = []

    for p in p_lines[1:]:
        if p.split('|')[4] in prod_ls:
            p_split = p.split('|')
            # print('한 줄씩 읽기 : ',p.split('|'))
            res = {
                "bank_name": p_split[0],
                "product_name": p_split[1],
                "description": p_split[2],
                "url": p_split[3],
                "code": p_split[4]
            }
            result.append(res)
    return result



def payload_make(_id,sexo,age,wage,enter_Dt,card1,card2,card3,card4,card5,deposit1,depoist2, deposit3, deposit4, deposit5, savings1, savings2, savings3, savings4, savings5,loan1, loan2, loan3, loan4, loan5, fund1, fund2, fund3, fund4, fund5):
    return [_id,sexo,age,wage,enter_Dt,card1,card2,card3,card4,card5,deposit1,depoist2, deposit3, deposit4, deposit5, savings1, savings2, savings3, savings4, savings5,loan1, loan2, loan3, loan4, loan5, fund1, fund2, fund3, fund4, fund5]


def ml(user_id):
    '''머신러닝 API 연결'''
    res = get_user_info(user_id)
    _id, _pick, _age, _wage, _date = res['user_id'], res['sexo'], res['age'], res['wage'], res['enter_dt']

    payload = {
        'input_data': [
            {'fields': ['id', 'sexo', 'age', 'wage', 'enter_dt', 'card1', 'card2', 'card3', 'card4', 'card5',
                        "deposit1", "deposit2", "deposit3", "deposit4", "deposit5", "savings1", "savings2",
                        "savings3", "savings4", "savings5", "loan1", "loan2", "loan3", "loan4", "loan5", "fund1",
                        "fund2", "fund3", 'fund4', 'fund5'],
                'values': [payload_make(*[_id, _pick, _age, _wage, _date, *[0] * 25])]
                }]
    }

    API_KEY = "nbaWdZ6hp9LfNnq9J83w7x5lzzSZw8uY-wrZfJ8uHsiD"
    token_url = 'https://iam.cloud.ibm.com/identity/token?grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=' + API_KEY
    res = requests.post(token_url)
    data = res.json()['access_token']
    header_token = f'Bearer {data}'
    headers = {'Content-Type': 'application/json; charset=utf-8',
               'Authorization': header_token
               }
    score_url = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d4c31800-dd3d-47e3-b0ac-1f1c25c052d3/predictions?version=2022-08-14"

    res2 = requests.post(score_url, headers=headers, json=payload)
    # print(res2.json()['predictions'][0]['values'][0][0][0], _pick, _age, _wage)

    cluster_rank = res2.json()['predictions'][0]['values'][0][0][0]
    result = read_finance_product(cluster_rank)

    print('result 결과 :: ',result.split(','))

    return find_finance_product(result.split(','))

