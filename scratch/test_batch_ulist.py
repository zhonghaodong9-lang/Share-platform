import requests
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://quote.eastmoney.com/"
}

session = requests.Session()
session.trust_env = False

# 1. 批量一次性调取 5 大指数
secids_idx = "1.000001,0.399001,0.399006,1.000688,0.899050"
url_idx = f"http://push2.eastmoney.com/api/qt/ulist/get?secids={secids_idx}&fields=f2,f3,f6,f12,f13,f14"

print("=== 1. 批量调取 5 大指数 ===")
r = session.get(url_idx, headers=headers, timeout=4)
diff = r.json().get("data", {}).get("diff", [])
for item in diff:
    print(f"  ✅ {item.get('f14')} ({item.get('f12')}): 点位={float(item.get('f2',0))/100.0 if item.get('f12') in ['000001','399001','399006','000688','899050'] else item.get('f2')}, 涨跌={item.get('f3')}%, 成交={float(item.get('f6',0))/1e8:.2f}亿")

# 2. 批量一次性调取 6 大指定 ETF
secids_etf = "1.588000,0.159819,0.159516,1.510300,1.588200,0.1515880"
url_etf = f"http://push2.eastmoney.com/api/qt/ulist/get?secids={secids_etf}&fields=f2,f3,f6,f12,f13,f14"

print("\n=== 2. 批量调取 6 大 ETF ===")
r2 = session.get(url_etf, headers=headers, timeout=4)
diff2 = r2.json().get("data", {}).get("diff", [])
for item in diff2:
    print(f"  ✅ {item.get('f14')} ({item.get('f12')}): 最新={item.get('f2')}, 涨跌={item.get('f3')}%, 成交={float(item.get('f6',0))/1e8:.2f}亿")
