import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import pywencai

queries = [
    "个股人气排名前10名",
    "热度最高股票前10名",
    "同花顺概念板块净流入前5名"
]

for q in queries:
    try:
        res = pywencai.get(query=q)
        if res is not None:
            print(f"\n=== 查询 '{q}' 成功 ===")
            print(res.head(10))
    except Exception as e:
        print(f"\n查询 '{q}' 异常:", e)
