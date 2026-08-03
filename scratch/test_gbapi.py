import requests

url = "https://gbapi.eastmoney.com/apijson/hotstock/gethotstocklist"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://guba.eastmoney.com/"
}

p = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
try:
    r = requests.get(url, headers=headers, proxies=p, timeout=5)
    print("Status:", r.status_code)
    print("Content:", r.text[:300])
except Exception as e:
    print("Error:", e)
