import requests

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "http://quote.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

# 测试 159819 (创业板人工智能ETF华宝) 的 K 线数据
secid = "0.159819"
url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&klt=101&fqt=1&lmt=5&end=20500101&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"

r = requests.get(url, headers=headers, timeout=5)
print("Return JSON:", r.json())
