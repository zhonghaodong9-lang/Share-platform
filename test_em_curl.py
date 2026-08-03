import subprocess
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

cmd_index = [
    "curl.exe", "-k", "-s",
    "https://push2.eastmoney.com/api/qt/ulist/get?fltt=2&invt=2&fields=f2,f3,f4,f6,f12,f14&secids=1.000001,0.399001,0.399006,1.000688,0.899050"
]

cmd_report = [
    "curl.exe", "-k", "-s",
    "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=PUBLISH_DATE&sortTypes=-1&pageSize=5&pageNumber=1&reportName=RPT_WEB_NREPORT&columns=ALL"
]

try:
    print("=== 1. 测试 curl.exe 抓取东财大盘指数 (ulist) ===")
    out_idx = subprocess.check_output(cmd_index).decode("utf-8")
    j_idx = json.loads(out_idx)
    print("大盘指数返回成功:", len(j_idx.get("data", {}).get("diff", [])))
    for item in j_idx["data"]["diff"]:
        print(f"  • [{item['f12']}] {item['f14']}: 点位 {item['f2']} | 成交额 {float(item['f6'])/1e8:.2f} 亿")
except Exception as e:
    print("指数抓取失败:", e)

try:
    print("\n=== 2. 测试 curl.exe 抓取东财券商研报中心 ===")
    out_rpt = subprocess.check_output(cmd_report).decode("utf-8")
    j_rpt = json.loads(out_rpt)
    print("研报中心返回成功:", len(j_rpt.get("result", {}).get("data", [])))
    for item in j_rpt["result"]["data"][:3]:
        print(f"  • [{item.get('PUBLISH_DATE')[:10]}] {item.get('ORG_NAME')} -> 《{item.get('TITLE')}》")
except Exception as e:
    print("研报抓取失败:", e)
