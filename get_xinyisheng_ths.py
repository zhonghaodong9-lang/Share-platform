import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(k, None)

import pywencai
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("=== 正在直连同花顺官网/问财引擎抓取: 新易盛 (300502) 资金数据 ===")
try:
    res = pywencai.get(query="新易盛 资金流向")
    if isinstance(res, dict) and "资金流向" in res:
        flow_data = res["资金流向"]
        print("\n【同花顺官方网页端 - 文本总结】:")
        if "文本标题h1" in res:
            print(res["文本标题h1"])
        if "txt1" in res:
            print(res["txt1"])

        if "实时资金分布" in flow_data and "bar3" in flow_data["实时资金分布"]:
            df_bar = flow_data["实时资金分布"]["bar3"]
            print("\n【同花顺官方网页端 - 07-31 四级资金分布明细】:")
            print(df_bar.to_string())

        if "多日资金流向" in flow_data and "line3" in flow_data["多日资金流向"]:
            df_multi = flow_data["多日资金流向"]["line3"]
            print("\n【同花顺官方网页端 - 多日资金积累走势】:")
            print(df_multi.tail(5).to_string())
    else:
        print("同花顺引擎返回结果:", res)
except Exception as e:
    print("同花顺官网抓取失败:", e)
