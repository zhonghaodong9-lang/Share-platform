import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import pywencai

print("=== 1. 查询同花顺问财网页端: 同花顺个股热榜前10名 ===")
try:
    res = pywencai.get(query="同花顺热榜前10名", query_type="stock")
    print(res)
except Exception as e:
    print("查询1异常:", e)

print("\n=== 2. 查询同花顺问财网页端: 今日主力资金净流入前10名 ===")
try:
    res2 = pywencai.get(query="今日主力资金净流入前10名", query_type="stock")
    print(res2)
except Exception as e:
    print("查询2异常:", e)
