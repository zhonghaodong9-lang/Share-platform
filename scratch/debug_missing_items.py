import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "http://quote.eastmoney.com/"
}

session = requests.Session()
session.trust_env = False

items = [
    ("上证指数", "1.000001"),
    ("深证成指", "0.399001"),
    ("创业板指", "0.399006"),
    ("科创50", "1.000688"),
    ("北证50", "0.899050"),
    ("科创50ETF华夏", "1.588000"),
    ("创业板人工智能ETF华宝", "0.159819"),
    ("半导体设备ETF国泰", "0.159516"),
    ("沪深300ETF华泰柏瑞", "1.510300"),
    ("科创半导体ETF华夏", "1.588200"),
    ("通信ETF国泰", "1.515880")
]

for name, secid in items:
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f57,f58,f43,f170,f168,f169,f171,f167,f162,f44,f45,f46,f47,f48,f60"
    try:
        r = session.get(url, headers=headers, timeout=3)
        data = r.json().get("data")
        if data:
            print(f"✅ {name} ({secid}): f43={data.get('f43')}, f48={data.get('f48')}")
        else:
            print(f"❌ {name} ({secid}): data is NULL!")
    except Exception as e:
        print(f"❌ {name} ({secid}): Exception {e}")
