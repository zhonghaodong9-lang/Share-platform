import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(k, None)

import requests
from bs4 import BeautifulSoup
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://basic.10jqka.com.cn/600487/capital.html"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

# 1. 抓取同花顺 F10 资金流向页面 (http://basic.10jqka.com.cn/600487/capital.html)
url_ths_f10 = "http://basic.10jqka.com.cn/600487/capital.html"
try:
    r = requests.get(url_ths_f10, headers=headers, proxies=p, timeout=5)
    r.encoding = "gbk"
    print("=== 1. 同花顺 F10 网页 (basic.10jqka.com.cn) 响应测试 ===")
    print("状态码:", r.status_code)
    if "flashData" in r.text or "大单" in r.text or "主力" in r.text:
        print("页面包含资金流向文本关键字")
except Exception as e:
    print("F10 抓取异常:", e)

# 2. 抓取同花顺数据中心动态接口 (http://data.10jqka.com.cn/funds/ggzjl/)
url_ths_datacenter = "http://data.10jqka.com.cn/funds/ggzjl/field/zjl/order/desc/page/1/ajax/1/"
headers_dc = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "http://data.10jqka.com.cn/funds/ggzjl/",
    "X-Requested-With": "XMLHttpRequest"
}
try:
    r_dc = requests.get(url_ths_datacenter, headers=headers_dc, proxies=p, timeout=5)
    r_dc.encoding = "gbk"
    soup = BeautifulSoup(r_dc.text, "html.parser")
    table = soup.find("table", class_="m-table")
    if table:
        for row in table.find_all("tr"):
            text = row.get_text(strip=True)
            if "600487" in text or "亨通光电" in text:
                cols = [td.get_text(strip=True) for td in row.find_all("td")]
                print("\n=== 同花顺数据中心 (data.10jqka.com.cn) 亨通光电数据 ===")
                print(cols)
except Exception as e:
    print("数据中心抓取异常:", e)
