import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import pywencai

print("=== 尝试问财多组热榜关键词 ===")
queries = [
    "人气排名前10",
    "热度排名前10的股票",
    "同花顺热股前10名",
    "主力资金净流入前10名"
]

for q in queries:
    try:
        res = pywencai.get(query=q)
        if res is not None and hasattr(res, "head"):
            print(f"\n✅ 关键词 '{q}' 成功获取 {len(res)} 条结果:")
            print(res.head(10)[["股票代码", "股票简称"] if "股票简称" in res.columns else res.columns[:3]])
    except Exception as e:
        print(f"❌ 关键词 '{q}' 异常: {e}")
