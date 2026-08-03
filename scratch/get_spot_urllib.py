import urllib.request
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://quote.eastmoney.com/",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

req = urllib.request.Request(
    "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d92b410797300c730ed05b2d3513b&fltt=2&invt=2&fid=f6&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3,f6",
    headers=headers
)

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
try:
    response = opener.open(req, timeout=5)
    html = response.read().decode("utf-8")
    data = json.loads(html)
    diff = data["data"]["diff"]

    print("=== 全市场大资金成交/关注度前10名 ===")
    for idx, item in enumerate(diff, 1):
        print(f"No.{idx} {item['f14']} ({item['f12']}) - 最新价: {item['f2']}元 | 涨跌幅: {item['f3']}% | 全天成交额: {item['f6']/1e8:.2f}亿元")
except Exception as e:
    print("获取数据失败:", e)
