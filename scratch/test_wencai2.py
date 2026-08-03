import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import pywencai

print("=== 测试 pywencai 成交额前10名 ===")
try:
    df = pywencai.get(query="成交额前10名")
    if df is not None:
        print("成功获取数据，列名如下:")
        print(list(df.columns)[:10])
        cols = [c for c in df.columns if "股票" in c or "名称" in c or "代码" in c or "成交" in c]
        print(df[cols].head(10))
except Exception as e:
    print("抓取失败:", e)
