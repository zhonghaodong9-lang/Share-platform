import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(k, None)

os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import requests
import json
import akshare as ak
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("=== 正在直连东财/新浪/AkShare 验证 2026-08-03 今天两市真实成交额 ===")

# 1. 新浪全市场成交额接口
url_sina = "http://hq.sinajs.cn/list=sh000001,sz399001,sz399006,bj899050"
headers = {"Referer": "http://finance.sina.com.cn"}

try:
    r = requests.get(url_sina, headers=headers, timeout=5)
    text = r.text
    print("\n--- 新浪行情快照 ---")
    lines = text.strip().split("\n")
    sh_amount = 0
    sz_amount = 0
    bj_amount = 0
    for line in lines:
        if "sh000001" in line:
            parts = line.split(",")
            sh_amount = float(parts[9]) / 1e8 if len(parts) > 9 else 0 # 亿元
            print(f"上证指数 (000001) 收盘价: {parts[3]} | 成交额: {sh_amount:.2f} 亿元")
        elif "sz399001" in line:
            parts = line.split(",")
            sz_amount = float(parts[9]) / 1e8 if len(parts) > 9 else 0 # 亿元
            print(f"深证成指 (399001) 收盘价: {parts[3]} | 成交额: {sz_amount:.2f} 亿元")
        elif "bj899050" in line:
            parts = line.split(",")
            bj_amount = float(parts[9]) / 1e8 if len(parts) > 9 else 0 # 亿元
            print(f"北证50 (899050) 收盘价: {parts[3]} | 成交额: {bj_amount:.2f} 亿元")

    total_amount = sh_amount + sz_amount + bj_amount
    print(f"\n👉 新浪权威计算 today 全市场总成交额: {total_amount:.2f} 亿元 (沪深京合集: {total_amount/10000:.4f} 万亿元)")

except Exception as e:
    print("新浪接口异常:", e)

# 2. 东财大盘快照接口
url_em = "http://push2.eastmoney.com/api/qt/ulist/get?fltt=2&invt=2&fields=f2,f3,f12,f14,f6&secids=1.000001,0.399001,0.399006,0.899050"
try:
    r_em = requests.get(url_em, timeout=5)
    data = r_em.json().get("data", {}).get("diff", [])
    print("\n--- 东方财富官方大盘接口 ---")
    em_total = 0
    for item in data:
        code = item.get("f12")
        name = item.get("f14")
        amount = float(item.get("f6", 0)) / 1e8
        em_total += amount
        print(f"[{code}] {name}: 成交额 {amount:.2f} 亿元")
    print(f"\n👉 东方财富权威计算 today 全市场总成交额: {em_total:.2f} 亿元 ({em_total/10000:.4f} 万亿元)")
except Exception as e:
    print("东财接口异常:", e)
