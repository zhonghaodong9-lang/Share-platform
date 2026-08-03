import requests

# 1.600176 represents Shanghai stock 600176 (China Jushi)
url = "http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=1&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&secid=1.600176"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "http://quote.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
try:
    r = requests.get(url, headers=headers, proxies=p, timeout=5)
    data = r.json().get("data", {}).get("klines", [])
    if data:
        line = data[-1].split(",")
        print("=== 中国巨石 (600176) 07-31 全天资金流向明细 ===")
        print("日期:", line[0])
        print("主力净流入 (超大单+大单):", f"{float(line[1])/10000:.2f}", "万元")
        print("超大单净流入:", f"{float(line[2])/10000:.2f}", "万元")
        print("大单净流入:", f"{float(line[3])/10000:.2f}", "万元")
        print("中单净流入:", f"{float(line[4])/10000:.2f}", "万元")
        print("小单净流入:", f"{float(line[5])/10000:.2f}", "万元")
    else:
        print("无数据:", r.text)
except Exception as e:
    print("错误:", e)
