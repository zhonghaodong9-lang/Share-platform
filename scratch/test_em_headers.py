import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(k, None)

import requests
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://quote.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

print("=== 正在带东财官方 Referer 验证 6 大核心业务模块 ===")

# 1. 大盘指数
url1 = "https://push2.eastmoney.com/api/qt/ulist/get?np=1&fltt=2&invt=2&fields=f2,f3,f4,f6,f12,f14&secids=1.000001,0.399001,0.399006,1.000688,0.899050"
try:
    r1 = requests.get(url1, headers=headers, proxies=p, timeout=5)
    if r1.status_code == 200 and r1.json().get("data"):
        data1 = r1.json()["data"]["diff"]
        print("\n✅ 1. 东财大盘指数与总成交额:")
        tot = 0.0
        for item in data1:
            amt = float(item['f6'])/1e8
            tot += amt
            print(f"   • [{item['f12']}] {item['f14']}: 点位 {item['f2']} ({item['f3']:+.2f}%) | 成交额: {amt:.2f} 亿")
        print(f"   👉 东方财富全市场成交额算术总和: {tot:.2f} 亿元 ({tot/10000:.4f} 万亿元)")
except Exception as e:
    print("1. 失败:", e)

# 2. 行业板块
url2 = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5&po=1&np=1&ut=bd199837b29a737c473157207fe0b06f&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f2,f3,f12,f14,f128,f140"
try:
    r2 = requests.get(url2, headers=headers, proxies=p, timeout=5)
    if r2.status_code == 200 and r2.json().get("data"):
        data2 = r2.json()["data"]["diff"]
        print("\n✅ 2. 东财行业板块 Top 5:")
        for item in data2:
            print(f"   • {item['f14']}: 涨跌幅 {item['f3']:+.2f}%")
except Exception as e:
    print("2. 失败:", e)

# 3. 涨停池
url3 = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5&po=1&np=1&ut=bd199837b29a737c473157207fe0b06f&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f12,f14,f22"
try:
    r3 = requests.get(url3, headers=headers, proxies=p, timeout=5)
    if r3.status_code == 200 and r3.json().get("data"):
        data3 = r3.json()["data"]["diff"]
        print("\n✅ 3. 东财涨停/涨幅池 Top 5:")
        for item in data3:
            print(f"   • [{item['f12']}] {item['f14']}: 价格 {item['f2']}元 | 涨幅 {item['f3']:+.2f}%")
except Exception as e:
    print("3. 失败:", e)

# 4. 宽基 ETF
url4 = "https://push2.eastmoney.com/api/qt/ulist/get?np=1&fltt=2&invt=2&fields=f2,f3,f6,f12,f14&secids=1.510300,0.159919,0.512100,1.159845,0.159915,1.588000,1.510500"
try:
    r4 = requests.get(url4, headers=headers, proxies=p, timeout=5)
    if r4.status_code == 200 and r4.json().get("data"):
        data4 = r4.json()["data"]["diff"]
        print("\n✅ 4. 东财宽基 ETF 盘口:")
        for item in data4:
            print(f"   • [{item['f12']}] {item['f14']}: 净值 {item['f2']} | 涨跌幅 {item['f3']:+.2f}% | 成交额: {float(item['f6'])/1e8:.2f} 亿")
except Exception as e:
    print("4. 失败:", e)

# 5. 单股资金流向 (中国巨石、亨通光电、中际旭创)
print("\n✅ 5. 东财单股主力与大单资金流向:")
for name, secid in [("中国巨石", "1.600176"), ("亨通光电", "1.600487"), ("中际旭创", "0.300308")]:
    url5 = f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=1&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&secid={secid}"
    try:
        r5 = requests.get(url5, headers=headers, proxies=p, timeout=5)
        if r5.status_code == 200 and r5.json().get("data"):
            line = r5.json()["data"]["klines"][-1].split(",")
            print(f"   • [{name}] {line[0]}: 主力 {float(line[1])/1e8:+.2f}亿 | 超大单 {float(line[5])/1e8:+.2f}亿 | 大单 {float(line[4])/1e8:+.2f}亿 | 中单 {float(line[3])/1e8:+.2f}亿 | 小单 {float(line[2])/1e8:+.2f}亿")
    except Exception as e:
        print(f"   • [{name}] 失败:", e)

# 6. 券商研报中心
url6 = "https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_WEB_NREPORT&columns=ALL&pageNumber=1&pageSize=5&sortColumns=PUBLISH_DATE&sortTypes=-1"
try:
    r6 = requests.get(url6, headers=headers, proxies=p, timeout=5)
    if r6.status_code == 200 and r6.json().get("result"):
        data6 = r6.json()["result"]["data"]
        print("\n✅ 6. 东财数据中心券商研报:")
        for item in data6[:3]:
            print(f"   • [{str(item.get('PUBLISH_DATE'))[:10]}] {item.get('ORG_NAME')} -> 《{item.get('TITLE')}》")
except Exception as e:
    print("\n6. 研报失败:", e)
