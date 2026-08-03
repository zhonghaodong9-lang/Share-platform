import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(k, None)

import requests
from bs4 import BeautifulSoup
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://stockpage.10jqka.com.cn/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

url = "http://stockpage.10jqka.com.cn/300502/money-flow/"
r = requests.get(url, headers=headers, proxies=p, timeout=5)
r.encoding = "utf-8"

print("=== 解析同花顺官网新易盛 (300502) Next.js 页面结构 ===")

# 正则寻找所有包含资金流向及具体数字的文本段落与 JSON 节点
matches = re.findall(r'self\.__next_f\.push\((.*?)\)', r.text)

for idx, m in enumerate(matches, 1):
    if "净流入" in m or "大单" in m or "主力" in m or "流入" in m or "流出" in m:
        print(f"\n--- 匹配段落 No.{idx} ---")
        # 清理转义字符
        clean_text = m.replace('\\"', '"').replace('\\\\', '\\')
        # 寻找“净流入”、“大单”、“超大单”关键字及数字
        found_lines = re.findall(r'[^"\\]*(?:净流入|超大单|大单|中单|小单|主力)[^"\\]*', clean_text)
        for line in found_lines[:15]:
            if len(line.strip()) > 3:
                print(line.strip())
