import os
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

def safe_fetch(url):
    for proxy_opt in [None, p]:
        for trust in [False, True]:
            try:
                s = requests.Session()
                s.trust_env = trust
                r = s.get(url, headers=headers, proxies=proxy_opt, timeout=2)
                if r.status_code == 200 and r.json().get("data"):
                    return r.json()["data"]
            except Exception:
                pass
    return None

print("=== 1. 测试 5 大指数完整抓取 ===")
idx_configs = [
    ("上证指数", "1.000001", "000001", 3809.66, -0.59, 9522.57, -2354.25, -19.8),
    ("深证成指", "0.399001", "399001", 13448.29, -0.96, 10451.29, -3091.38, -22.8),
    ("创业板指", "0.399006", "399006", 3302.55, -1.24, 4897.20, -1849.28, -27.4),
    ("科创50", "1.000688", "000688", 1552.89, -5.08, 1245.11, -384.65, -23.6),
    ("北证50", "0.899050", "899050", 1076.07, -0.66, 138.95, -42.47, -23.4)
]

for name, secid, code, default_price, default_pct, default_amt, default_diff, default_vol_pct in idx_configs:
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58,f43,f170,f168,f169,f171,f167,f162,f44,f45,f46,f47,f48,f60"
    data = safe_fetch(url)
    if data:
        price = data.get("f43", 0) / 100.0 if data.get("f43") else default_price
        pct = data.get("f170", 0) / 100.0 if data.get("f170") else default_pct
        amt = float(data.get("f48", 0)) / 1e8 if data.get("f48") else default_amt
        print(f"  ✅ [实时接口] {name} ({code}): 点位={price:.2f}, 涨跌={pct:+.2f}%, 成交={amt:.0f}亿")
    else:
        print(f"  ⚡ [保底兜底] {name} ({code}): 点位={default_price:.2f}, 涨跌={default_pct:+.2f}%, 成交={default_amt:.0f}亿")

print("\n=== 2. 测试 6 大 ETF 完整抓取 ===")
etf_configs = [
    ("科创50ETF华夏", "1.588000", "588000", 1.636, -5.32, 107.58, -47.13, -30.5),
    ("创业板人工智能ETF华宝", "0.159819", "159819", 1.721, -2.49, 5.03, -3.73, -42.6),
    ("半导体设备ETF国泰", "0.159516", "159516", 0.605, -9.70, 57.96, -17.03, -22.7),
    ("沪深300ETF华泰柏瑞", "1.510300", "510300", 4.599, -1.16, 42.70, -27.47, -39.1),
    ("科创半导体ETF华夏", "1.588200", "588200", 1.041, -6.64, 48.56, -17.37, -26.3),
    ("通信ETF国泰", "1.515880", "515880", 0.582, 0.00, 27.11, -29.03, -51.7)
]

for name, secid, code, default_price, default_pct, default_amt, default_diff, default_vol_pct in etf_configs:
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58,f43,f170,f168,f169,f171,f167,f162,f44,f45,f46,f47,f48,f60"
    data = safe_fetch(url)
    if data:
        price = data.get("f43", 0) / 1000.0 if data.get("f43") else default_price
        pct = data.get("f170", 0) / 100.0 if data.get("f170") else default_pct
        amt = float(data.get("f48", 0)) / 1e8 if data.get("f48") else default_amt
        print(f"  ✅ [实时接口] {name} ({code}): 最新={price:.3f}, 涨跌={pct:+.2f}%, 成交={amt:.2f}亿")
    else:
        print(f"  ⚡ [保底兜底] {name} ({code}): 最新={default_price:.3f}, 涨跌={default_pct:+.2f}%, 成交={default_amt:.2f}亿")
