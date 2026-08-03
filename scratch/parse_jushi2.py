import requests
import json

url = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=5&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&secid=1.600176"

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

try:
    r = requests.get(url, proxies=p, timeout=5)
    data = r.json().get("data", {}).get("klines", [])
    print("=== 中国巨石 (600176) 最近 5 日大单与资金流向明细 ===")
    for k in data:
        parts = k.split(",")
        date = parts[0]
        main_net = float(parts[1]) / 10000.0  # 万元
        super_net = float(parts[2]) / 10000.0 # 万元
        big_net = float(parts[3]) / 10000.0   # 万元
        mid_net = float(parts[4]) / 10000.0   # 万元
        small_net = float(parts[5]) / 10000.0 # 万元
        print(f"[{date}] 主力净流入: {main_net:+.2f}万元 | 超大单: {super_net:+.2f}万元 | 大单: {big_net:+.2f}万元 | 中单: {mid_net:+.2f}万元 | 小单: {small_net:+.2f}万元")
except Exception as e:
    print("获取失败:", e)
