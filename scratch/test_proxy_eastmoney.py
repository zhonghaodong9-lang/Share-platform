import requests
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://quote.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

secids_idx = "1.000001,0.399001,0.399006,1.000688,0.899050"
url_idx = f"https://push2.eastmoney.com/api/qt/ulist/get?secids={secids_idx}&fields=f2,f3,f6,f12,f13,f14"

print("=== 测试代理模式 (7897) 批量调取 5 大指数 ===")
try:
    r = requests.get(url_idx, headers=headers, proxies=p, timeout=5)
    print("Status:", r.status_code)
    diff = r.json().get("data", {}).get("diff", [])
    for item in diff:
        print(f"  ✅ {item.get('f14')} ({item.get('f12')}): 点位={item.get('f2')}, 涨跌={item.get('f3')}%, 成交={float(item.get('f6',0))/1e8:.2f}亿")
except Exception as e:
    print("Proxy error:", e)
