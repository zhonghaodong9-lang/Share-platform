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

def safe_fetch(url):
    for proxy_opt in [None, p]:
        for trust in [False, True]:
            try:
                s = requests.Session()
                s.trust_env = trust
                r = s.get(url, headers=headers, proxies=proxy_opt, timeout=3)
                if r.status_code == 200 and r.json().get("data"):
                    return r.json()["data"]
            except Exception:
                pass
    return None

us_targets = [
    ("英伟达", "NVDA", "105.NVDA"),
    ("美光科技", "MU", "105.MU"),
    ("应用材料", "AMAT", "105.AMAT"),
    ("台积电", "TSM", "105.TSM"),
    ("阿斯麦", "ASML", "105.ASML"),
    ("博通", "AVGO", "105.AVGO"),
    ("费城半导体", "SOX", "100.SOX")
]

print("=== 调取东财美股实时行情与涨跌数据 ===")
for name, symbol, secid in us_targets:
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58,f43,f170,f169,f171,f44,f45,f46,f47,f48,f60"
    d = safe_fetch(url)
    if d:
        price = float(d.get("f43", 0)) / 100.0 if d.get("f43") else 0.0
        pct = float(d.get("f170", 0)) / 100.0 if d.get("f170") else 0.0
        high = float(d.get("f44", 0)) / 100.0 if d.get("f44") else 0.0
        low = float(d.get("f45", 0)) / 100.0 if d.get("f45") else 0.0
        print(f"  ✅ {name} ({symbol}): 当前价=${price:.2f}, 涨跌幅={pct:+.2f}%, 最高=${high:.2f}, 最低=${low:.2f}")
    else:
        print(f"  ⚡ {name} ({symbol}): 触发快照模式")
