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

def get_kline_volume_change_direct(secid):
    """直连模式获取近2日K线量能变化，绝不用死代理以免超时返回0"""
    url = f"http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&klt=101&fqt=1&lmt=2&end=20500101&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
    session = requests.Session()
    session.trust_env = False
    for p_opt in [None, {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}]:
        try:
            r = session.get(url, headers=headers, proxies=p_opt, timeout=3)
            if r.status_code == 200 and r.json().get("data"):
                klines = r.json()["data"].get("klines", [])
                if len(klines) >= 2:
                    prev_amt = float(klines[-2].split(",")[6]) / 1e8
                    curr_amt = float(klines[-1].split(",")[6]) / 1e8
                    diff_amt = curr_amt - prev_amt
                    diff_pct = (diff_amt / prev_amt * 100.0) if prev_amt > 0 else 0.0
                    return curr_amt, diff_amt, diff_pct
        except Exception:
            pass
    return 0.0, 0.0, 0.0

etfs = [
    ("科创50ETF华夏", "1.588000"),
    ("创业板人工智能ETF华宝", "0.159819"),
    ("半导体设备ETF国泰", "0.159516"),
    ("沪深300ETF华泰柏瑞", "1.510300"),
    ("科创半导体ETF华夏", "1.588200"),
    ("通信ETF国泰", "1.515880")
]

print("=== 直连测试指定 6 大 ETF 放量/缩量 ===")
for name, secid in etfs:
    curr, diff, pct = get_kline_volume_change_direct(secid)
    if diff > 0.01:
        tag = f"🔴 放量 +{diff:.2f}亿 (+{pct:.1f}%)"
    elif diff < -0.01:
        tag = f"🟢 缩量 {diff:.2f}亿 ({pct:.1f}%)"
    else:
        tag = "⚪ 平稳持平"
    print(f"  • {name} ({secid}): 今日 {curr:.2f}亿 | {tag}")
