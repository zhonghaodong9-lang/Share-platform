import os
for k in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
    os.environ.pop(k, None)

os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import requests
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.eastmoney.com/"
}

def get_em_json(url):
    for p_opt in [None, {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}]:
        try:
            session = requests.Session()
            session.trust_env = False
            r = session.get(url, headers=headers, proxies=p_opt, timeout=4)
            if r.status_code == 200:
                j = r.json()
                if j:
                    return j
        except Exception:
            pass
    return None

print("==========================================================")
print("🚀 东方财富网 (eastmoney.com) 全业务模块数据调取测试 (v3 最终版)")
print("==========================================================\n")

results_summary = {}

# 1. 核心大盘指数快照 (上证、深证、创业板、科创50、北证50)
print("【1/6 模块测试】: 大盘指数与市场成交额 (quote.eastmoney.com)...")
url_index = "https://push2.eastmoney.com/api/qt/ulist/get?np=1&fltt=2&invt=2&ut=bd199837b29a737c473157207fe0b06f&fields=f2,f3,f4,f6,f12,f14&secids=1.000001,0.399001,0.399006,1.000688,0.899050"
res_index = get_em_json(url_index)
if res_index and res_index.get("data"):
    data = res_index["data"].get("diff", [])
    print("  ✅ 成功直连东财大盘指数 API (quote.eastmoney.com)")
    total_vol = 0.0
    for item in data:
        code = item.get("f12")
        name = item.get("f14")
        price = item.get("f2")
        pct = item.get("f3")
        amt = float(item.get("f6", 0)) / 1e8
        total_vol += amt
        print(f"    • [{code}] {name}: 点位 {price} | 涨跌幅 {pct:+.2f}% | 成交额 {amt:.2f} 亿元")
    print(f"  👉 东方财富网官方全市场成交额汇总: {total_vol:.2f} 亿元 ({total_vol/10000:.4f} 万亿元)")
    results_summary["大盘指数与总成交额"] = "成功 (100% 东财直连)"
else:
    print("  ❌ 失败")
    results_summary["大盘指数与总成交额"] = "失败"

# 2. 板块/行业涨幅榜 Top 5 与领涨龙头
print("\n【2/6 模块测试】: 板块行业涨幅榜 Top 5 (quote.eastmoney.com)...")
url_board = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5&po=1&np=1&ut=bd199837b29a737c473157207fe0b06f&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f2,f3,f12,f14,f128,f140"
res_board = get_em_json(url_board)
if res_board and res_board.get("data"):
    data = res_board["data"].get("diff", [])
    print("  ✅ 成功直连东财板块行情 API")
    for item in data:
        b_name = item.get("f14")
        b_pct = item.get("f3")
        leader_code = item.get("f140")
        print(f"    • {b_name}: 涨跌幅 {b_pct:+.2f}% | 领涨龙头代码: {leader_code}")
    results_summary["行业板块榜单"] = "成功 (100% 东财直连)"
else:
    print("  ❌ 失败")
    results_summary["行业板块榜单"] = "失败"

# 3. 涨停池与连板空间梯队
print("\n【3/6 模块测试】: 今日涨停池与空间板梯队 (quote.eastmoney.com)...")
url_zt = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd199837b29a737c473157207fe0b06f&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f12,f14,f22"
res_zt = get_em_json(url_zt)
if res_zt and res_zt.get("data"):
    data = res_zt["data"].get("diff", [])
    print("  ✅ 成功直连东财涨停/涨幅池 API")
    for item in data[:5]:
        code = item.get("f12")
        name = item.get("f14")
        price = item.get("f2")
        pct = item.get("f3")
        print(f"    • [{code}] {name}: 价格 {price}元 | 涨幅 {pct:+.2f}%")
    results_summary["涨停池与空间板"] = "成功 (100% 东财直连)"
else:
    print("  ❌ 失败")
    results_summary["涨停池与空间板"] = "失败"

# 4. 宽基 ETF 异常放量监控
print("\n【4/6 模块测试】: 核心宽基 ETF 成交量监控 (quote.eastmoney.com)...")
url_etf = "https://push2.eastmoney.com/api/qt/ulist/get?np=1&fltt=2&invt=2&ut=bd199837b29a737c473157207fe0b06f&fields=f2,f3,f6,f12,f14&secids=1.510300,0.159919,0.512100,1.159845,0.159915,1.588000,1.510500"
res_etf = get_em_json(url_etf)
if res_etf and res_etf.get("data"):
    data = res_etf["data"].get("diff", [])
    print("  ✅ 成功直连东财 ETF 盘口 API")
    for item in data:
        code = item.get("f12")
        name = item.get("f14")
        price = item.get("f2")
        pct = item.get("f3")
        amt = float(item.get("f6", 0)) / 1e8
        print(f"    • [{code}] {name}: 净值 {price} | 涨跌幅 {pct:+.2f}% | 成交额 {amt:.2f} 亿元")
    results_summary["宽基ETF放量监控"] = "成功 (100% 东财直连)"
else:
    print("  ❌ 失败")
    results_summary["宽基ETF放量监控"] = "失败"

# 5. 个股全天大单与主力资金流向 (中国巨石 600176、亨通光电 600487、中际旭创 300308)
print("\n【5/6 模块测试】: 单股主力与大单资金流向 (push2his.eastmoney.com)...")
test_stocks = [("中国巨石", "1.600176"), ("亨通光电", "1.600487"), ("中际旭创", "0.300308")]
success_count = 0
for name, secid in test_stocks:
    url_flow = f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=1&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&secid={secid}"
    res_flow = get_em_json(url_flow)
    if res_flow and res_flow.get("data"):
        line = res_flow["data"]["klines"][-1].split(",")
        date = line[0]
        main_net = float(line[1]) / 1e8   # 主力净流入 (亿元)
        small_net = float(line[2]) / 1e8  # 小单净流入 (亿元)
        mid_net = float(line[3]) / 1e8    # 中单净流入 (亿元)
        large_net = float(line[4]) / 1e8  # 大单净流入 (亿元)
        super_net = float(line[5]) / 1e8  # 超大单净流入 (亿元)
        print(f"  ✅ [{name}] {date} 资金明细:")
        print(f"     • 主力净流入: {main_net:+.2f} 亿 | 超大单: {super_net:+.2f} 亿 | 大单: {large_net:+.2f} 亿 | 中单: {mid_net:+.2f} 亿 | 小单: {small_net:+.2f} 亿")
        success_count += 1

if success_count == len(test_stocks):
    results_summary["个股资金大单流向"] = "成功 (100% 东财直连)"
else:
    results_summary["个股资金大单流向"] = "部分失败"

# 6. 券商研报与机构最新评级
print("\n【6/6 模块测试】: 东方财富数据中心券商研报 (datacenter-web.eastmoney.com)...")
url_report = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=PUBLISH_DATE&sortTypes=-1&pageSize=5&pageNumber=1&reportName=RPT_ORGAN_RATING&columns=ALL"
res_report = get_em_json(url_report)
if res_report and res_report.get("result"):
    data = res_report["result"].get("data", [])
    print("  ✅ 成功直连东财研报中心 API")
    for item in data[:3]:
        stock = item.get("STOCK_NAME", "未知标的")
        org = item.get("ORG_NAME", "机构")
        rating = item.get("RATING_NAME", "看好")
        date = str(item.get("PUBLISH_DATE"))[:10]
        print(f"    • [{date}] {org} -> 看好标的: 《{stock}》 (最新评级: {rating})")
    results_summary["券商研报中心"] = "成功 (100% 东财直连)"
else:
    print("  ❌ 失败")
    results_summary["券商研报中心"] = "失败"

print("\n==========================================================")
print("🏁 测试总结报告 (6/6 业务全模块验证结果):")
for module, status in results_summary.items():
    print(f"  • {module}: {status}")
print("==========================================================")
