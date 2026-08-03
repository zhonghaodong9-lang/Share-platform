import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://quote.eastmoney.com/"
}

def fetch_single_with_retry(secid):
    """加 3 次自动重试与间隔，防止东财 API 频繁拒绝连接"""
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58,f43,f170,f168,f169,f171,f167,f162,f44,f45,f46,f47,f48,f60"
    for attempt in range(3):
        try:
            session = requests.Session()
            session.trust_env = False
            r = session.get(url, headers=headers, timeout=3)
            if r.status_code == 200 and r.json().get("data"):
                return r.json()["data"]
        except Exception:
            time.sleep(0.2)
    return None

items = [
    ("上证指数", "1.000001"),
    ("深证成指", "0.399001"),
    ("创业板指", "0.399006"),
    ("科创50", "1.000688"),
    ("北证50", "0.899050"),
    ("科创50ETF华夏", "1.588000"),
    ("创业板人工智能ETF华宝", "0.159819"),
    ("半导体设备ETF国泰", "0.159516"),
    ("沪深300ETF华泰柏瑞", "1.510300"),
    ("科创半导体ETF华夏", "1.588200"),
    ("通信ETF国泰", "1.515880")
]

print("=== 带重试机制测试全量 5 大指数与 6 大 ETF ===")
for name, secid in items:
    d = fetch_single_with_retry(secid)
    if d:
        print(f"  ✅ [成功] {name} ({secid}): 最新={d.get('f43')}, 成交={d.get('f48')}")
    else:
        print(f"  ❌ [失败] {name} ({secid})")
