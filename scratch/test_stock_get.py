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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://quote.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

def get_single_em(secid):
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58,f43,f170,f168,f169,f171,f167,f162,f44,f45,f46,f47,f48,f60,f116"
    for proxy_opt in [p, None]:
        try:
            r = requests.get(url, headers=headers, proxies=proxy_opt, timeout=3)
            if r.status_code == 200 and r.json().get("data"):
                return r.json()["data"]
        except Exception:
            pass
    return None

print("=== 1. 测试东财单只大盘指数直连接口 ===")
indexes = [
    ("上证指数", "1.000001"),
    ("深证成指", "0.399001"),
    ("创业板指", "0.399006"),
    ("科创50", "1.000688"),
    ("北证50", "0.899050")
]

tot_vol = 0.0
for name, secid in indexes:
    d = get_single_em(secid)
    if d:
        code = d.get("f57")
        price = d.get("f43", 0) / 100.0 if d.get("f43") else 0
        pct = d.get("f170", 0) / 100.0 if d.get("f170") else 0
        amt = float(d.get("f48", 0)) / 1e8  # 成交额 (亿元)
        tot_vol += amt
        print(f"  ✅ [{code}] {name}: 点位 {price:.2f} ({pct:+.2f}%) | 成交额: {amt:.2f} 亿元")

print(f"\n👉 沪深京三市合计总成交额: {tot_vol:.2f} 亿元 ({tot_vol/10000:.4f} 万亿元)")

print("\n=== 2. 测试东财指定 6 大 ETF 直连接口 ===")
etfs = [
    ("科创50ETF华夏", "1.588000"),
    ("创业板人工智能ETF华宝", "0.159819"),
    ("半导体设备ETF国泰", "0.159516"),
    ("沪深300ETF华泰柏瑞", "1.510300"),
    ("科创半导体ETF华夏", "1.588200"),
    ("通信ETF国泰", "1.515880")
]

for name, secid in etfs:
    d = get_single_em(secid)
    if d:
        code = d.get("f57")
        price = d.get("f43", 0) / 1000.0 if d.get("f43") else 0
        pct = d.get("f170", 0) / 100.0 if d.get("f170") else 0
        amt = float(d.get("f48", 0)) / 1e8
        print(f"  ✅ [{code}] {name}: 净值 {price:.3f} ({pct:+.2f}%) | 成交额: {amt:.2f} 亿元")
