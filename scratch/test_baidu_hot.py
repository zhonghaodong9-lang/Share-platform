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

print("=== 尝试百度/股吧全网热门个股热榜 ===")
url = "https://gbapi.eastmoney.com/apijson/hotstock/gethotstocklist"
try:
    r = session.get(url, timeout=5)
    data = r.json().get("re", [])
    for idx, item in enumerate(data[:10], 1):
        print(f"No.{idx} {item.get('name')} ({item.get('code')}) - 热度: {item.get('hot')}")
except Exception as e:
    print("热榜接口异常:", e)
