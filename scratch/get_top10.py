import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import requests

session = requests.Session()
session.trust_env = False
session.proxies = {"http": None, "https": None}

print("=== 1. 全市场成交额 Top 10 个股 (大资金博弈最集中) ===")
url_vol = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d92b410797300c730ed05b2d3513b&fltt=2&invt=2&fid=f6&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3,f6"
try:
    r = session.get(url_vol, timeout=5)
    data = r.json().get("data", {}).get("diff", [])
    for idx, item in enumerate(data, 1):
        print(f"No.{idx} {item.get('f14')} ({item.get('f12')}) - 最新价: {item.get('f2')} - 涨跌幅: {item.get('f3')}% - 成交额: {item.get('f6')/1e8:.2f}亿")
except Exception as e:
    print("成交额接口异常:", e)

print("\n=== 2. 全市场涨幅榜 Top 10 个股 (短线最高人气情绪连板) ===")
url_hot = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d92b410797300c730ed05b2d3513b&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3,f6"
try:
    r = session.get(url_hot, timeout=5)
    data = r.json().get("data", {}).get("diff", [])
    for idx, item in enumerate(data, 1):
        print(f"No.{idx} {item.get('f14')} ({item.get('f12')}) - 最新价: {item.get('f2')} - 涨跌幅: {item.get('f3')}% - 成交额: {item.get('f6')/1e8:.2f}亿")
except Exception as e:
    print("涨幅榜接口异常:", e)
