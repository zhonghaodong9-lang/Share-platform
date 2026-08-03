import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(k, None)

os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import requests
import json

session = requests.Session()
session.trust_env = False

# 1. 抓取东方财富网页版中国巨石(1.600176)个股资金流向接口
url_em = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=1&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&secid=1.600176"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://quote.eastmoney.com/"
}

try:
    r = session.get(url_em, headers=headers, timeout=5)
    res_json = r.json()
    klines = res_json.get("data", {}).get("klines", [])
    if klines:
        line = klines[-1].split(",")
        date = line[0]
        main_net = float(line[1]) / 1e8      # 主力净流入 (亿元)
        super_net = float(line[2]) / 1e8     # 超大单净流入 (亿元)
        large_net = float(line[3]) / 1e8     # 大单净流入 (亿元)
        middle_net = float(line[4]) / 1e8    # 中单净流入 (亿元)
        small_net = float(line[5]) / 1e8     # 小单净流入 (亿元)

        print(f"=== 东财 Web API 实测数据 (日期: {date}) ===")
        print(f"主力净流入: {main_net:+.2f} 亿")
        print(f"超大单净流入: {super_net:+.2f} 亿")
        print(f"大单净流入: {large_net:+.2f} 亿")
        print(f"中单净流入: {middle_net:+.2f} 亿")
        print(f"小单净流入: {small_net:+.2f} 亿")
    else:
        print("未获取到 klines 数据, Raw JSON:", res_json)
except Exception as e:
    print("东财 Web API 请求失败:", e)
