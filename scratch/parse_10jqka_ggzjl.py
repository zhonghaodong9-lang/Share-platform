import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://data.10jqka.com.cn/funds/ggzjl/",
    "X-Requested-With": "XMLHttpRequest"
}

url = "http://data.10jqka.com.cn/funds/ggzjl/field/zjl/order/desc/page/1/ajax/1/"
try:
    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = "gbk"
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", class_="m-table")
    if table:
        print("=== 同花顺网页版(http://data.10jqka.com.cn) 实时大资金流向榜前十名 ===")
        rows = table.find_all("tr")[1:11]
        for idx, row in enumerate(rows, 1):
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) >= 5:
                print(f"No.{idx} 代码: {cols[1]} | 股票: {cols[2]} | 最新价: {cols[3]}元 | 涨跌幅: {cols[4]}% | 换手率: {cols[5]}% | 资金净流入: {cols[6]}万元")
    else:
        print("AJAX 响应片段长度:", len(r.text))
        print("前 200 字:", r.text[:200])
except Exception as e:
    print("解析异常:", e)
