import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(k, None)

import pywencai
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

res = pywencai.get(query="新易盛资金流向")
if isinstance(res, dict) and "资金流向" in res:
    print("=== 同花顺官方网页端 (stockpage.10jqka.com.cn / iwencai) 新易盛 (300502) 数据 ===")
    if "文本标题h1" in res:
        print("【文字总结】:", res["文本标题h1"])
    print("\n【资金分布明细表】:")
    df_bar = res["资金流向"]["实时资金分布"]["bar3"]
    print(df_bar.to_string())
else:
    print("同花顺抓取结果:", res)
