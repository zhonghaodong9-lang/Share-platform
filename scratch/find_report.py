import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

import requests

session = requests.Session()
session.trust_env = False

reports = [
    "RPT_DATA_FUNDFLOW",
    "RPT_STOCK_FUNDFLOW",
    "RPT_ZJFL_STOCK",
    "RPTA_WEB_STOCK_FLOW",
    "RPT_DYZL_STOCK_FLOW",
    "RPT_MAIN_FUND_FLOW",
    "RPT_FLOW_STOCK",
    "RPT_GEGU_ZJLX"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for r_name in reports:
    url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TRADE_DATE&sortTypes=-1&pageSize=1&pageNumber=1&reportName={r_name}&columns=ALL"
    try:
        r = session.get(url, headers=headers, timeout=2)
        res = r.json()
        if res.get("success"):
            print("✅ 找到可用 ReportName:", r_name)
            data = res.get("result", {}).get("data", [])
            if data:
                print("示例列:", list(data[0].keys())[:10])
            break
        else:
            pass
    except Exception:
        pass
