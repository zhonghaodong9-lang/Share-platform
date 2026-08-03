import requests
from bs4 import BeautifulSoup
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://basic.10jqka.com.cn/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

url = "http://basic.10jqka.com.cn/600487/capital.html"
r = requests.get(url, headers=headers, proxies=p, timeout=5)
r.encoding = "gbk"

soup = BeautifulSoup(r.text, "html.parser")

# 1. 查找资金流向表格
tables = soup.find_all("table")
print(f"=== 同花顺 F10 (600487/capital.html) 找到 {len(tables)} 个表格 ===")

for idx, t in enumerate(tables, 1):
    rows = t.find_all("tr")
    if len(rows) > 1:
        print(f"\n--- 表格 No.{idx} ---")
        for row in rows[:6]:
            cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            print(cols)

# 2. 查找页面嵌入的 JSON 数据 (如 flashData / capitalData)
scripts = soup.find_all("script")
for s in scripts:
    if s.string and ("flashData" in s.string or "capital" in s.string or "json" in s.string):
        print("\n--- JS 引擎中发现的数据切片 ---")
        lines = [line.strip() for line in s.string.split("\n") if "flashData" in line or "data" in line]
        for l in lines[:5]:
            print(l[:200])
