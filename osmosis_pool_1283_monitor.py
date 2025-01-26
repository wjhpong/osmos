import os
import requests
import time
from datetime import datetime

# 配置参数
OSMOSIS_POOL_ID = "1283"  # 监控的流动性池ID
STRIDE_REDEMPTION_API = "https://stride-lcd.polkachu.com/Stride-Labs/stride/stakeibc/redemption_rate/ATOM"
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")  # 从环境变量读取飞书Webhook URL
MIN_SPREAD_PERCENT = 1.5  # 最小套利价差率（%）

def get_osmosis_price(pool_id):
    """从Osmosis API获取stATOM/ATOM池的实时价格"""
    url = f"https://api-osmosis.imperator.co/pools/v2/{pool_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return float(response.json()["price"])
        else:
            print(f"Osmosis API请求失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"获取Osmosis价格异常：{str(e)}")
        return None

def get_stride_redemption_rate():
    """从Stride LCD获取stATOM赎回率"""
    try:
        response = requests.get(STRIDE_REDEMPTION_API, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return float(data["redemption_rate"])
        else:
            print(f"Stride API请求失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"获取Stride赎回率异常：{str(e)}")
        return None

def send_feishu_alert(spread_percent, osmosis_price, stride_rate):
    """发送飞书通知"""
    if not FEISHU_WEBHOOK_URL:
        print("飞书Webhook URL未配置！")
        return

    message = {
        "msg_type": "text",
        "content": {
            "text": (
                f"🚨 检测到套利机会！\n"
                f"- Osmosis价格: 1 stATOM = {osmosis_price:.4f} ATOM\n"
                f"- Stride赎回率: 1 stATOM = {stride_rate:.4f} ATOM\n"
                f"- 价差率: {spread_percent:.2f}%"
            )
        }
    }

    try:
        response = requests.post(FEISHU_WEBHOOK_URL, json=message, timeout=10)
        if response.status_code == 200:
            print("飞书通知发送成功")
        else:
            print(f"飞书通知发送失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"飞书通知异常：{str(e)}")

def main():
    """主监控逻辑"""
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} - 正在检查价差...")

        # 获取数据
        osmosis_price = get_osmosis_price(OSMOSIS_POOL_ID)
        stride_rate = get_stride_redemption_rate()

        if osmosis_price is None or stride_rate is None:
            print("数据获取失败，等待重试...")
            time.sleep(60)
            continue

        # 计算价差率
        spread = stride_rate - osmosis_price
        spread_percent = (spread / osmosis_price) * 100

        print(f"Osmosis价格: {osmosis_price:.4f} | Stride赎回率: {stride_rate:.4f} | 价差率: {spread_percent:.2f}%")

        # 触发通知
        if spread_percent >= MIN_SPREAD_PERCENT:
            send_feishu_alert(spread_percent, osmosis_price, stride_rate)

        # 间隔60秒
        time.sleep(60)

if __name__ == "__main__":
    main()