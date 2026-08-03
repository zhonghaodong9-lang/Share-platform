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
    "Referer": "https://quote.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

# 1. 指数 (Module 1)
secids_idx = "1.000001,0.399001,0.399006,1.000688,0.899050"
url_m1 = f"https://push2.eastmoney.com/api/qt/ulist/get?fltt=2&invt=2&fields=f2,f3,f4,f6,f12,f14&secids={secids_idx}"

# 2. 6 大指定 ETF (Module 2)
secids_etf = "1.588000,0.159819,0.159516,1.510300,1.588200,1.515880"
url_m2 = f"https://push2.eastmoney.com/api/qt/ulist/get?fltt=2&invt=2&fields=f2,f3,f6,f12,f14&secids={secids_etf}"

try:
    r1 = requests.get(url_m1, headers=headers, proxies=p, timeout=5)
    print("【模块一测试】: 指数 API 返回 Status:", r1.status_code)
    if r1.status_code == 200:
        data1 = r1.json()["data"]["diff"]
        tot = 0.0
        for item in data1:
            amt = float(item['f6']) / 1e8
            tot += amt
            print(f"   • [{item['f12']}] {item['f14']}: 点位 {item['f2']} ({item['f3']:+.2f}%) | 成交额: {amt:.2f} 亿")
        print(f"   👉 沪深京三市合计总成交额: {tot:.2f} 亿元 ({tot/10000:.4f} 万亿元)")
except Exception as e:
    print("模块一异常:", e)

try:
    r2 = requests.get(url_m2, headers=headers, proxies=p, timeout=5)
    print("\n【模块二测试】: 指定 6 大 ETF API 返回 Status:", r2.status_code)
    if r2.status_code == 200:
        data2 = r2.json()["data"]["diff"]
        for item in data2:
            amt = float(item['f6']) / 1e8
            print(f"   • [{item['f12']}] {item['f14']}: 净值 {item['f2']} ({item['f3']:+.2f}%) | 成交额: {amt:.2f} 亿")
except Exception as e:
    print("模块二异常:", e)
