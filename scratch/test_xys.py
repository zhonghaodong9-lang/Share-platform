import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(k, None)

import pywencai
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("=== 1. 查询同花顺问财: 300502 7月31日资金流向 ===")
try:
    res = pywencai.get(query="300502 7月31日资金流向")
    if isinstance(res, dict):
        print("同花顺问财抓取成功!")
        if "文本标题h1" in res:
            print("标题:", res["文本标题h1"])
        if "txt1" in res:
            print("摘要:", res["txt1"])
        if "资金流向" in res and "实时资金分布" in res["资金流向"]:
            print("\n资金分布表:")
            print(res["资金流向"]["实时资金分布"]["bar3"].to_string())
except Exception as e:
    print("失败:", e)
