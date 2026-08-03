import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(k, None)

import requests
from bs4 import BeautifulSoup
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://stockpage.10jqka.com.cn/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

url = "http://stockpage.10jqka.com.cn/300502/money-flow/"
print(f"=== 正在拉取同花顺官网资金流向页面 ({url}) ===")

try:
    r = requests.get(url, headers=headers, proxies=p, timeout=5)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    print("页面状态码:", r.status_code)
    print("页面 Title:", soup.title.string if soup.title else "无标题")

    # 提取页面里的 JSON 或数据节点
    scripts = soup.find_all("script")
    found_data = False
    for s in scripts:
        if s.string and ("flashData" in s.string or "money" in s.string or "capital" in s.string or "bar" in s.string):
            print("\n--- 提取到页面内嵌数据切片 ---")
            lines = [l.strip() for l in s.string.split("\n") if "Data" in l or "val" in l or "flow" in l]
            for l in lines[:10]:
                print(l[:250])
            found_data = True
            break
    if not found_data:
        print("未找到内嵌脚本数据，查看文本摘要:")
        text = soup.get_text()
        print("\n".join([line.strip() for line in text.split("\n") if "净流入" in line or "大单" in line or "主力" in line][:10]))
except Exception as e:
    print("拉取同花顺网页失败:", e)
