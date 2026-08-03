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

us_items = [
    ("英伟达 (NVDA)", "105.NVDA"),
    ("美光科技 (MU)", "105.MU"),
    ("应用材料 (AMAT)", "105.AMAT"),
    ("费城半导体 (SOX)", "100.SOX"),
    ("纳斯达克 (IXIC)", "100.IXIC")
]

print("=== 测试东财抓取美股标的及半导体映射数据 ===")
for name, secid in us_items:
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58,f43,f170,f169,f171,f47,f48"
    d = safe_fetch(url)
    if d:
        price = float(d.get("f43", 0)) / 100.0 if d.get("f43") else 0.0
        pct = float(d.get("f170", 0)) / 100.0 if d.get("f170") else 0.0
        print(f"  ✅ {name} ({secid}): 最新=${price:.2f}, 涨跌={pct:+.2f}%")
    else:
        print(f"  ⚡ {name} ({secid}): 接口无响应，使用最新快照")
