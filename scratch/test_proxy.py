import requests

url = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d92b410797300c730ed05b2d3513b&fltt=2&invt=2&fid=f6&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3,f6"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "http://quote.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
r = requests.get(url, headers=headers, proxies=p, timeout=5)
data = r.json()["data"]["diff"]

print("=== 8月2日(周日) 17:14 实时最新全网排行榜 Top 10 ===")
for i, item in enumerate(data, 1):
    print(f"No.{i} {item['f14']} ({item['f12']}) - 最新价: {item['f2']}元 | 涨跌: {item['f3']}% | 成交额: {item['f6']/1e8:.2f}亿")
