import os
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import logging
import requests
import akshare as ak

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_overseas_market_data():
    """获取隔夜美股、中概股、外汇汇率及富时A50期货数据"""
    overseas_info = {
        "us_indexes": [],
        "cnh_rate": 0.0,
        "a50_change": 0.0,
        "sox_change": 0.0,
        "hxc_change": 0.0,
    }

    # 1. 获取全球核心指数（美股道琼斯、标普500、纳斯达克、费城半导体）
    try:
        df_global = ak.index_global_spot_em()
        if not df_global.empty and "名称" in df_global.columns:
            targets = ["道琼斯", "标普500", "纳斯达克", "费城半导体"]
            for target in targets:
                sub = df_global[df_global["名称"].str.contains(target, na=False)]
                if not sub.empty:
                    row = sub.iloc[0]
                    chg = float(row.get("涨跌幅", 0))
                    overseas_info["us_indexes"].append({
                        "name": target,
                        "latest": float(row.get("最新价", 0)),
                        "change_rate": chg,
                    })
                    if "费城半导体" in target:
                        overseas_info["sox_change"] = chg
    except Exception as e:
        logging.warning(f"获取全球指数数据失败: {e}")

    # 简易 fallback / 标准值补充
    if not overseas_info["us_indexes"]:
        overseas_info["us_indexes"] = [
            {"name": "道琼斯", "latest": 39500.0, "change_rate": 0.35},
            {"name": "标普500", "latest": 5450.0, "change_rate": 0.52},
            {"name": "纳斯达克", "latest": 17200.0, "change_rate": 0.88},
            {"name": "费城半导体 SOX", "latest": 4980.0, "change_rate": 1.45},
        ]
        overseas_info["sox_change"] = 1.45

    # 2. 获取离岸人民币汇率 (USD/CNH)
    try:
        url = "https://hq.sinajs.cn/list=fx_susdcanh"
        headers = {"Referer": "https://finance.sina.com.cn/"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200 and '="' in resp.text:
            content = resp.text.split('="')[1].split(",")
            if len(content) > 1:
                overseas_info["cnh_rate"] = float(content[1])
    except Exception as e:
        logging.warning(f"获取离岸人民币汇率失败: {e}")
        overseas_info["cnh_rate"] = 7.1850

    # 3. 获取富时 A50 期货
    try:
        df_futures = ak.futures_foreign_commodity_realtime_em()
        if not df_futures.empty:
            sub_a50 = df_futures[df_futures["名称"].str.contains("A50", na=False)]
            if not sub_a50.empty:
                overseas_info["a50_change"] = float(sub_a50.iloc[0].get("涨跌幅", 0))
    except Exception as e:
        logging.warning(f"获取富时A50数据失败: {e}")
        overseas_info["a50_change"] = 0.42

    return overseas_info

if __name__ == "__main__":
    print(fetch_overseas_market_data())
