import requests
from api_key import API_KEY

def get_balance():
    url = "https://api.deepseek.com/user/balance"

    payload={}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response
    
def is_available():
    re = get_balance()
    return re['is_available']

def balance_num():
    re = get_balance()
    return re['balance_infos'][0]["total_balance"]

