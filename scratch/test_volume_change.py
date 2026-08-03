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

def get_kline_2days(secid):
    """获取标的近 2 日日K数据，计算精确的放量/缩量数值与比例"""
    url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&klt=101&fqt=1&lmt=2&end=20500101&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
    for proxy_opt in [p, None]:
        try:
            session = requests.Session()
            session.trust_env = False
            r = session.get(url, headers=headers, proxies=proxy_opt, timeout=3)
            if r.status_code == 200 and r.json().get("data"):
                klines = r.json()["data"].get("klines", [])
                if len(klines) >= 2:
                    # kline format: date, open, close, high, low, volume, amount, amplitude, pct, change, turn
                    prev_parts = klines[-2].split(",")
                    curr_parts = klines[-1].split(",")
                    prev_amt = float(prev_parts[6]) / 1e8  # 亿元
                    curr_amt = float(curr_parts[6]) / 1e8  # 亿元
                    diff_amt = curr_amt - prev_amt
                    diff_pct = (diff_amt / prev_amt * 100.0) if prev_amt > 0 else 0.0
                    return curr_amt, diff_amt, diff_pct
                elif len(klines) == 1:
                    curr_parts = klines[0].split(",")
                    curr_amt = float(curr_parts[6]) / 1e8
                    return curr_amt, 0.0, 0.0
        except Exception:
            pass
    return 0.0, 0.0, 0.0

print("=== 1. 验证模块一 (指数) 放量/缩量 ===")
indexes = [
    ("上证指数", "1.000001"),
    ("深证成指", "0.399001"),
    ("创业板指", "0.399006"),
    ("科创50", "1.000688"),
    ("北证50", "0.899050")
]

for name, secid in indexes:
    curr, diff, pct = get_kline_2days(secid)
    tag = f"🔴 放量 +{diff:.2f}亿 (+{pct:.1f}%)" if diff >= 0 else f"🟢 缩量 {diff:.2f}亿 ({pct:.1f}%)"
    print(f"  • {name}: 今日 {curr:.2f}亿 | {tag}")

print("\n=== 2. 验证模块二 (6 大指定 ETF) 放量/缩量 ===")
etfs = [
    ("科创50ETF华夏", "1.588000"),
    ("创业板人工智能ETF华宝", "0.159819"),
    ("半导体设备ETF国泰", "0.159516"),
    ("沪深300ETF华泰柏瑞", "1.510300"),
    ("科创半导体ETF华夏", "1.588200"),
    ("通信ETF国泰", "1.515880")
]

for name, secid in etfs:
    curr, diff, pct = get_kline_2days(secid)
    tag = f"🔴 放量 +{diff:.2f}亿 (+{pct:.1f}%)" if diff >= 0 else f"🟢 缩量 {diff:.2f}亿 ({pct:.1f}%)"
    print(f"  • {name}: 今日 {curr:.2f}亿 | {tag}")

print("\n=== 3. 验证模块四 (成交额 Top 10 个股) 放量/缩量 ===")
stocks = [
    ("长鑫科技", "1.688825"),
    ("中际旭创", "0.300308"),
    ("兆易创新", "1.603986"),
    ("新易盛", "0.300502"),
    ("寒武纪", "1.688256")
]

for name, secid in stocks:
    curr, diff, pct = get_kline_2days(secid)
    tag = f"🔴 放量 +{diff:.2f}亿 (+{pct:.1f}%)" if diff >= 0 else f"🟢 缩量 {diff:.2f}亿 ({pct:.1f}%)"
    print(f"  • {name}: 今日 {curr:.2f}亿 | {tag}")
