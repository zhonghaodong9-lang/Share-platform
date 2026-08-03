import socket
import json

ip = "183.232.229.21"
host = "push2.eastmoney.com"
path = "/api/qt/clist/get?pn=1&pz=10&po=1&np=1&ut=bd1d92b410797300c730ed05b2d3513b&fltt=2&invt=2&fid=f6&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3,f6"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((ip, 80))

    req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\nAccept: */*\r\nConnection: close\r\n\r\n"
    s.sendall(req.encode())

    resp = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        resp += data

    s.close()

    text = resp.decode("utf-8", errors="ignore")
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        json_str = text[start:end+1]
        res_json = json.loads(json_str)
        diff = res_json["data"]["diff"]

        print("=== 8月2日(周日) 17:14 实时最新全网排行榜 Top 10 ===")
        for idx, item in enumerate(diff, 1):
            print(f"No.{idx} {item['f14']} ({item['f12']}) - 最新价: {item['f2']}元 | 涨跌幅: {item['f3']}% | 全天成交额: {item['f6']/1e8:.2f}亿元")
    else:
        print("响应为空或未包含JSON:", text[:200])
except Exception as e:
    print("IP Socket 抓取失败:", e)
