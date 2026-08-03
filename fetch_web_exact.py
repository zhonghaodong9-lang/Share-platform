import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(k, None)

os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import requests
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

url = "http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=1&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&secid=1.600176"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://quote.eastmoney.com/"
}

session = requests.Session()
session.trust_env = False
session.proxies = {"http": None, "https": None}

try:
    r = session.get(url, headers=headers, timeout=5)
    data_raw = r.json()["data"]["klines"][-1].split(",")
    date = data_raw[0]
    main_net = float(data_raw[1]) / 1e8   # 主力净流入
    small_net = float(data_raw[2]) / 1e8  # 小单净流入
    mid_net = float(data_raw[3]) / 1e8    # 中单净流入
    large_net = float(data_raw[4]) / 1e8  # 大单净流入
    super_net = float(data_raw[5]) / 1e8  # 超大单净流入

    print("=== 东方财富网页端 (quote.eastmoney.com) 真实接口直连结果 ===")
    print("股票名称: 中国巨石 (600176) | 交易日期:", date)
    print(f"🔴 主力净流入: {main_net:+.2f} 亿元  (您截图权威显示: +19.02 亿)")
    print(f"🔴 超大单净流入: {super_net:+.2f} 亿元 (您截图权威显示: +20.60 亿)")
    print(f"🟢 大单净流入:   {large_net:+.2f} 亿元 (您截图权威显示: -1.58 亿)")
    print(f"🟢 中单净流入:   {mid_net:+.2f} 亿元 (您截图权威显示: -12.51 亿)")
    print(f"🟢 小单净流入:   {small_net:+.2f} 亿元 (您截图权威显示: -6.51 亿)")
except Exception as e:
    print("抓取失败:", e)
