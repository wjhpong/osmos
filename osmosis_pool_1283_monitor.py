import os
import requests
import time
from datetime import datetime

# 配置参数
OSMOSIS_POOL_ID = "1283"  # 替换为有效 Pool ID
STRIDE_REDEMPTION_API = "https://stride-lcd.polkachu.com/Stride-Labs/stride/stakeibc/redemption_rate/ATOM"
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")
MIN_SPREAD_PERCENT = 1.5  # 目标价差率（%）

def get_osmosis_price(pool_id):
    """从 Osmosis 官方 LCD 获取池价格"""
    url = f"https://lcd.osmosis.zone/osmosis/gamm/v1beta1/pools/{pool_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            pool_data = response.json()["pool"]
            asset1 = pool_data["poolAssets"][0]
            asset2 = pool_data["poolAssets"][1]
            price = float(asset2["token"]["amount"]) / float(asset1["token"]["amount"])
            return price
        else:
            print(f"Osmosis API 请求失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"获取 Osmosis 价格异常：{str(e)}")
        return None

def get_stride_redemption_rate():
    """获取 Stride 赎回率"""
    try:
        response = requests.get(STRIDE_REDEMPTION_API, timeout=10)
        if response.status_code == 200:
            return float(response.json()["redemption_rate"])
        else:
            print(f"Stride API 请求失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"获取 Stride 赎回率异常：{str(e)}")
        return None

# ...（保持原有的 send_feishu_alert 和 main 函数不变）...