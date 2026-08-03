import os
import requests
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1. 亨通光电 (600487 -> secid=1.600487)
url = "http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=5&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&secid=1.600487"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://quote.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

try:
    r = requests.get(url, headers=headers, proxies=p, timeout=5)
    res_json = r.json()
    klines = res_json.get("data", {}).get("klines", [])
    print("=== 亨通光电 (600487) 东方财富网页端直连权威数据 ===")
    for line_str in klines:
        line = line_str.split(",")
        date = line[0]
        main_net = float(line[1]) / 10000.0   # 主力净流入 (万元)
        small_net = float(line[2]) / 10000.0  # 小单净流入 (万元)
        mid_net = float(line[3]) / 10000.0    # 中单净流入 (万元)
        large_net = float(line[4]) / 10000.0  # 大单净流入 (万元)
        super_net = float(line[5]) / 10000.0  # 超大单净流入 (万元)
        close = float(line[11])
        pct = float(line[12])

        print(f"\n【交易日期: {date}】 收盘价: {close}元 | 涨跌幅: {pct:+.2f}%")
        print(f"  🔴/🟢 主力资金净流入: {main_net:+.2f} 万元 ({main_net/10000:+.4f} 亿元)")
        print(f"  🔴 超大单净流入: {super_net:+.2f} 万元 ({super_net/10000:+.4f} 亿元)")
        print(f"  🟢 大单净流入:   {large_net:+.2f} 万元 ({large_net/10000:+.4f} 亿元)")
        print(f"  中单净流入:     {mid_net:+.2f} 万元 ({mid_net/10000:+.4f} 亿元)")
        print(f"  小单净流入:     {small_net:+.2f} 万元 ({small_net/10000:+.4f} 亿元)")
except Exception as e:
    print("失败:", e)
