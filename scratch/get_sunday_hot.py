import urllib.request
import json
import os

print("=== 正在抓取 8月2日(周日) 17:14 实时全网热搜/人气热榜 Top 10 ===")

# 1. 抓取实时全网人气热榜
url = "http://emappdata.eastmoney.com/stockrank/getAllList"
payload = json.dumps({"appId": "appId01", "globalId": "7862440156941131", "pageNo": 1, "pageSize": 10}).encode("utf-8")

req = urllib.request.Request(
    url,
    data=payload,
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
)

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
try:
    resp = opener.open(req, timeout=5)
    data = json.loads(resp.read().decode("utf-8"))
    stock_list = data.get("data", [])
    if stock_list:
        print("✅ 成功拉取 Sunday 17:14 实时人气榜 Top 10:")
        for idx, item in enumerate(stock_list[:10], 1):
            sc = item.get("srcSecurityCode", "")
            code = sc[2:] if len(sc) > 2 else sc
            print(f"No.{idx} {item.get('name', '')} ({code}) - 实时人气排名: {item.get('rank', idx)}")
    else:
        print("未获取到列表:", data)
except Exception as e:
    print("方式1失败:", e)

# 2. 备用接口：同花顺/东财热股 API
url2 = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d92b410797300c730ed05b2d3513b&fltt=2&invt=2&fid=f26&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3,f6"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0", "Referer": "http://quote.eastmoney.com/"})
try:
    resp2 = opener.open(req2, timeout=5)
    data2 = json.loads(resp2.read().decode("utf-8"))
    diff = data2.get("data", {}).get("diff", [])
    if diff:
        print("\n✅ 方式2 实时热度榜:")
        for idx, item in enumerate(diff[:10], 1):
            print(f"No.{idx} {item.get('f14')} ({item.get('f12')})")
except Exception as e:
    print("方式2失败:", e)
