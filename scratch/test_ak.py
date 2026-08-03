import os
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import akshare as ak

print("=== 尝试 AKShare 600176 资金流向 ===")
try:
    df = ak.stock_individual_fund_flow(stock="600176", market="sh")
    print(df.tail(5))
except Exception as e:
    print("失败:", e)
