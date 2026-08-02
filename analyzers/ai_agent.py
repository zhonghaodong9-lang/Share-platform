import os
import logging
import requests
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_ai_analysis(market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping):
    """结合所有行情与研报数据，调用 AI 大模型或规则引擎生成高级盘后总结与明日展望"""
    
    # 提取关键量化指标
    idx_list = market_data.get("indexes", [])
    sh_index = next((i for i in idx_list if "000001" in i.get("code", "")), {})
    cyb_index = next((i for i in idx_list if "399006" in i.get("code", "")), {})
    
    sh_chg = sh_index.get("change_rate", 0.0)
    cyb_chg = cyb_index.get("change_rate", 0.0)
    total_vol = market_data.get("stats", {}).get("total_volume", 0.0)
    
    score = sentiment.get("score", 50.0)
    stage = sentiment.get("stage", "震荡期")
    top_stock = market_data.get("limit_info", {}).get("top_stock", "无")

    top_sectors = [s.get("name", "") for s in money_flow_data.get("sector_flow", {}).get("inflow", [])[:3]]
    top_sectors_str = "、".join(top_sectors) if top_sectors else "AI算力、半导体、机器人"

    # 如果配置了大模型 API Key
    if Config.AI_PROVIDER != "none" and Config.AI_API_KEY:
        try:
            prompt = f"""你是一名顶级 A 股量化交易员与机构策略首席分析师。请根据今日收盘全景数据，输出一份专业的【盘后智投精要与策略展望】：

【今日行情总结】
- 上证指数: {sh_chg}% | 创业板指: {cyb_chg}% | 两市总成交额: {total_vol:.2f} 亿元
- 短线情绪评分: {score} 分 ({stage}) | 全场最高高度板: {top_stock}
- 主力资金领涨板块: {top_sectors_str}
- 海外与映射: 隔夜SOX指数变动 {overseas_data.get('sox_change', 0)}%，富时A50变动 {overseas_data.get('a50_change', 0)}%，离岸人民币 {overseas_data.get('cnh_rate', 7.18)}

请写出：
1. 市场核心驱动力与主线逻辑分析（150字内）
2. 中美板块映射与资金博弈点评（150字内）
3. 次日操盘策略与防守关注（100字内）
"""
            url = f"{Config.AI_BASE_URL.rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {Config.AI_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": Config.AI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 800,
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                res_json = resp.json()
                content = res_json["choices"][0]["message"]["content"]
                return content
        except Exception as e:
            logging.warning(f"调用 AI 模型生成研报总结失败, 切换至内置规则智投引擎: {e}")

    # 规则引擎生成高质量结构化总结
    market_trend = "大盘放量反弹，市场信心明显修复" if sh_chg > 0.5 and total_vol > 15000 else "市场处于窄幅震荡结构性行情"
    
    analysis_text = f"""**【核心逻辑与大盘研判】**
今日 A 股呈现 {market_trend} 的格局。上证指数收盘涨跌幅 **{sh_chg}%**，创业板指涨跌幅 **{cyb_chg}%**，两市合计成交额达 **{total_vol:.2f} 亿元**。整体看，大盘在近期关键支撑位展现出较强抗跌性。

**【热点主线与资金流向】**
主力资金集中涌入 **{top_sectors_str}** 等硬科技与出海产业链板块。个股方面，全场最高高度板达到 **{top_stock}**，显示短线高标示范效应良好，短线博弈情绪回暖。

**【中美映射与海外传导】**
隔夜美股半导体 SOX 指数变动 **{overseas_data.get('sox_change', 0)}%**，直接形成对 A 股 CPO、算力及芯片产业链的强共振驱动；富时 A50 指数变动 **{overseas_data.get('a50_change', 0)}%**，外资环境总体平稳。

**【次日策略建议】**
当前情绪评分为 **{score} 分**（处于 *{stage}*）。操作策略上，建议顺应主线，逢回调关注具有中报高景气与投行研报看好的科技龙头，切忌在分歧高潮期盲目追高非主线跟风股。
"""
    return analysis_text

if __name__ == "__main__":
    print(generate_ai_analysis({}, {}, {}, {}, {"score": 72.5, "stage": "发酵期"}, {}))
