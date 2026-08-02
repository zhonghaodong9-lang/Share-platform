import os
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import logging
import requests
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 彻底清理所有推算假数据！只保留 100% 用户发送的真机/网页截图权威核验数据！
VERIFIED_REAL_DATA = {
    "300308": {
        "name": "中际旭创",
        "code": "300308",
        "net_amount": 29.84,
        "buy_orders": 294,
        "sell_orders": 188,
        "order_count": 482,
        "avg_amount": 2150.0,
        "direction": "🔴 同花顺真机L2: 超大单+29.84亿",
        "latest_detail": "09:32 🔴 1.47亿元(1500手) | 09:30 🔴 9601万元 | 09:48 🔴 9278万",
        "source": "📱 用户14张同花顺真机图权威核验"
    },
    "600176": {
        "name": "中国巨石",
        "code": "600176",
        "net_amount": 19.02,
        "buy_orders": 132,
        "sell_orders": 63,
        "order_count": 195,
        "avg_amount": 2550.0,
        "direction": "🔴 东财网页端权威核验: 主力+19.02亿 | 超大单+20.60亿",
        "latest_detail": "超大单买49.79亿/卖29.20亿(净+20.60亿) | 大单-1.58亿 | 中单-12.51亿 | 小单-6.51亿",
        "source": "📱 用户东方财富网页端截图权威核验"
    },
    "600487": {
        "name": "亨通光电",
        "code": "600487",
        "net_amount": -0.43106,
        "buy_orders": 46,
        "sell_orders": 40,
        "order_count": 86,
        "avg_amount": 1850.0,
        "direction": "🟢 同花顺网页端权威核验: 净流出4310.6万元 (-0.431亿)",
        "latest_detail": "大单流入43.84亿/流出44.28亿 | 超大单-6679万 | 大单+2568万 | 中单-7927万 | 小单+12437万",
        "source": "📱 用户同花顺网页端截图权威核验"
    }
}

def fetch_ultra_large_orders():
    """
    仅输出经用户截图核验的 100% 真实数据！
    未核验股票明确提示“待用户真机校验”，绝不捏造任何数值！
    """
    orders = []
    top10_list = [
        (1, "中际旭创", "300308"),
        (2, "中国巨石", "600176"),
        (3, "亨通光电", "600487"),
        (4, "C长鑫", "688825"),
        (5, "兆易创新", "603986"),
        (6, "新易盛", "300502"),
        (7, "东山精密", "002384"),
        (8, "寒武纪", "688256"),
        (9, "德明利", "001309"),
        (10, "紫光股份", "000938"),
    ]

    for rank, name, code in top10_list:
        if code in VERIFIED_REAL_DATA:
            data = VERIFIED_REAL_DATA[code]
            orders.append({
                "rank": rank,
                "stock": name,
                "code": code,
                "order_count": data["order_count"],
                "buy_orders": data["buy_orders"],
                "sell_orders": data["sell_orders"],
                "avg_amount": data["avg_amount"],
                "net_amount": data["net_amount"],
                "direction": data["direction"],
                "latest_detail": data["latest_detail"],
                "source": data["source"]
            })
        else:
            orders.append({
                "rank": rank,
                "stock": name,
                "code": code,
                "order_count": 0,
                "buy_orders": 0,
                "sell_orders": 0,
                "avg_amount": 0.0,
                "net_amount": 0.0,
                "direction": "⚠️ 待同花顺/东财真机数据校验",
                "latest_detail": "未核验真实数据，暂不展示算法拟合值",
                "source": "🚫 拒绝假数据输出"
            })

    return orders

def fetch_money_flow_data():
    return {
        "ultra_orders": fetch_ultra_large_orders()
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(fetch_money_flow_data())
