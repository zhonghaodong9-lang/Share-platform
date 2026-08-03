import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

import requests

session = requests.Session()
session.trust_env = False

url = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TRADE_DATE&sortTypes=-1&pageSize=5&pageNumber=1&reportName=RPT_DYZL_STOCK&columns=ALL"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://data.eastmoney.com/"
}

try:
    r = session.get("https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TRADE_DATE&sortTypes=-1&pageSize=1&pageNumber=1&reportName=RPT_MF_STOCK_DFLOW&columns=ALL", headers=headers, timeout=5)
    print("Raw text:", r.text[:300])
except Exception as e:
    print("失败:", e)
