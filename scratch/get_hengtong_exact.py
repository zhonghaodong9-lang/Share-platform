import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(k, None)

os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import subprocess
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1. 拉取亨通光电 (1.600487) 东方财富网页端日线资金流向接口
cmd_flow = [
    "curl.exe", "--noproxy", "*", "-s",
    "http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=5&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&secid=1.600487"
]

# 2. 拉取亨通光电行情快照接口
cmd_quote = [
    "curl.exe", "--noproxy", "*", "-s",
    "http://push2.eastmoney.com/api/qt/stock/get?secid=1.600487&fields=f57,f58,f43,f170,f168,f169,f171,f167,f162"
]

try:
    out_flow = subprocess.check_output(cmd_flow).decode("utf-8")
    res_flow = json.loads(out_flow)
    klines = res_flow["data"]["klines"]
    
    print("=== 亨通光电 (600487) 东方财富网页端直连抓取数据 ===")
    for line_str in klines:
        line = line_str.split(",")
        date = line[0]
        main_net = float(line[1]) / 1e8   # 主力净流入 (亿元)
        small_net = float(line[2]) / 1e8  # 小单净流入 (亿元)
        mid_net = float(line[3]) / 1e8    # 中单净流入 (亿元)
        large_net = float(line[4]) / 1e8  # 大单净流入 (亿元)
        super_net = float(line[5]) / 1e8  # 超大单净流入 (亿元)
        close_price = float(line[11])
        change_pct = float(line[12])

        print(f"\n【日期: {date}】 收盘价: {close_price}元 | 涨跌幅: {change_pct:+.2f}%")
        print(f"  主力资金净流入: {main_net:+.2f} 万元 ({main_net/10000:+.4f} 亿元)" if abs(main_net)<1 else f"  主力资金净流入: {main_net:+.2f} 亿元")
        print(f"  🔴 超大单净流入: {super_net:+.2f} 亿元 ({super_net*10000:+.2f} 万元)")
        print(f"  🟢 大单净流入:   {large_net:+.2f} 亿元 ({large_net*10000:+.2f} 万元)")
        print(f"  中单净流入:     {mid_net:+.2f} 亿元 ({mid_net*10000:+.2f} 万元)")
        print(f"  小单净流入:     {small_net:+.2f} 亿元 ({small_net*10000:+.2f} 万元)")

except Exception as e:
    print("抓取失败:", e)
