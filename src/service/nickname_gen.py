import json, requests


def nick_gen(p):
    params = {
        'format':'json',
        'count': p
    }
    url = 'https://nickname.hwanmoo.kr/'
    response = requests.get(url, params=params)
    json_data = json.loads(response.text)['words']

    return ','.join(json_data)
    # return json_data
