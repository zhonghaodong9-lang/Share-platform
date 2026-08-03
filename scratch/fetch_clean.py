import urllib.request
import json
import os

os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

url = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d92b410797300c730ed05b2d3513b&fltt=2&invt=2&fid=f6&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3,f6"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    # Use explicit empty proxy dictionary
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    res = opener.open(req, timeout=5)
    data = json.loads(res.read().decode("utf-8"))
    diff = data["data"]["diff"]
    print("=== 8月2日(周日) 17:14 实时最新排序 Top 10 ===")
    for i, item in enumerate(diff, 1):
        print(f"No.{i} {item['f14']} ({item['f12']}) - 最新价: {item['f2']}元 | 涨跌幅: {item['f3']}% | 成交额: {item['f6']/1e8:.2f}亿")
except Exception as e:
    print("错误:", e)
