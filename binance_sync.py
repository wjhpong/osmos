import requests
import hmac
import hashlib
import time

# 币安 API 配置
API_KEY = 'XK7eCSnoHc2CMAqFa9Hyo8HXTWudcglQ0O5fWt0oI09z255qODGayavPowX79OF6'
API_SECRET = '5vmi7ecji7Q6WNiLUWPpNRnBu7g5Hn8MiQgCVxnWtSMUBEBVd8VVN8N9AV6O37UV'
BASE_URL = 'https://api.binance.com'

def get_margin_account():
    """获取保证金账户信息"""
    endpoint = '/sapi/v1/margin/account'
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp
    }
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    response = requests.get(BASE_URL + endpoint, headers=headers, params={**params, 'signature': signature})
    return response.json()

def get_vip_loan_info():
    """获取 VIP 借币信息"""
    endpoint = '/sapi/v1/loan/vip/ongoing/orders'  # 使用正确的 VIP 借币接口
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'loanCoin': 'ATOM',
        'limit': 100,  # 设置较大的限制以获取所有订单
        'current': 1   # 从第一页开始
    }
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    response = requests.get(BASE_URL + endpoint, headers=headers, params={**params, 'signature': signature})
    print("API 响应:", response.text)
    return response.json()

def get_atom_vip_debt():
    """获取 ATOM 的 VIP 借币负债总额"""
    loan_info = get_vip_loan_info()
    total_debt = 0.0
    
    print("数据类型:", type(loan_info))
    print("数据内容:", loan_info)
    
    # 根据新的数据结构修改处理逻辑
    if isinstance(loan_info, dict) and 'rows' in loan_info:
        for loan in loan_info['rows']:
            if loan.get('loanCoin') == 'ATOM':
                total_debt += float(loan.get('totalDebt', 0))
    
    return total_debt

# 获取并打印结果
atom_debt = get_atom_vip_debt()
print(f"ATOM VIP借币负债总额: {atom_debt}")
