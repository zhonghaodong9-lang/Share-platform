import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(k, None)

import pywencai
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("=== 展开同花顺问财亨通光电 (600487) 详细资金表格 ===")
res = pywencai.get(query="亨通光电 资金流向")

if isinstance(res, dict) and "资金流向" in res:
    flow_data = res["资金流向"]
    print("资金流向包含子项:", list(flow_data.keys()))
    for k, v in flow_data.items():
        print(f"\n--- 子项: {k} ---")
        if isinstance(v, dict):
            for k2, v2 in v.items():
                print(f"[{k2}]")
                if hasattr(v2, "to_string"):
                    print(v2.to_string())
                else:
                    print(v2)
