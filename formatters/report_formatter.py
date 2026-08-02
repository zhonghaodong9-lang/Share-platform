import datetime

def format_daily_report(market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping, ai_summary):
    """将所有市场数据与分析结果渲染为手机端极其清晰、直观、优雅的 A 股盘后智投日报"""
    today_str = datetime.datetime.now().strftime("%Y年%m月%d日")
    time_str = datetime.datetime.now().strftime("%H:%M")

    indexes = market_data.get("indexes", [])
    stats = market_data.get("stats", {})
    limit_info = market_data.get("limit_info", {})

    sector_inflow = money_flow_data.get("sector_flow", {}).get("inflow", [])
    indiv_inflow = money_flow_data.get("individual_flow", {}).get("inflow", [])
    longhu_list = money_flow_data.get("longhu_list", [])

    us_indexes = overseas_data.get("us_indexes", [])
    mapping_details = mapping.get("mapping_details", [])

    # 情绪进度条
    score = sentiment.get("score", 50.0)
    filled_blocks = int(score // 10)
    bar = "█" * filled_blocks + "░" * (10 - filled_blocks)

    md = f"""# 📈 A股盘后深度智投日报
📅 **{today_str}** | ⏰ **{time_str}**

==============================
⚡ **【1. 市场情绪与短线风向】**
------------------------------
• 🌡️ **情绪温度**：`[{bar}]` **{score} 分**
• 📌 **阶段评估**：**{sentiment.get('stage', '')}**
• 💰 **两市成交**：**{stats.get('total_volume', 0):.2f} 亿元**
• 📈 **上涨 / 下跌**：🔴 涨 **{stats.get('up_count', 0)}** 家 / 🟢 跌 **{stats.get('down_count', 0)}** 家 (平盘 {stats.get('flat_count', 0)} 家)
• 💥 **涨停 / 跌停**：🔥 涨停 **{limit_info.get('zt_count', 0)}** 家 / ❄️ 跌停 **{stats.get('down_limit_count', 0)}** 家
• ⚡ **炸板率**：**{limit_info.get('bomb_rate', 0)}%**
• 👑 **短线空间龙头**：🏆 **{limit_info.get('top_stock', '无')}**

💡 **操盘提醒**：{sentiment.get('advice', '')}

==============================
📊 **【2. 核心大盘指数】**
------------------------------
"""
    for idx in indexes:
        chg = idx.get("change_rate", 0.0)
        flag = "🔴" if chg > 0 else ("🟢" if chg < 0 else "⚪")
        md += f"• **{idx.get('name')}**：{idx.get('latest'):.2f} ({flag} **{chg:+.2f}%** | {idx.get('change_amount'):+.2f}) | 成交 **{idx.get('volume_amount'):.1f} 亿**\n"

    md += """
==============================
💰 **【3. 主力与机构资金流向】**
------------------------------
🔥 **领涨 / 主力资金净流入板块 Top 5**：
"""
    for i, sec in enumerate(sector_inflow[:5], 1):
        chg = sec.get("change_rate", 0.0)
        flag = "🔴" if chg > 0 else "🟢"
        md += f"{i}. **{sec.get('name')}** ({flag} {chg:+.2f}%) ➔ 领涨: **{sec.get('leader')}** ({sec.get('leader_change', 0):+.2f}%)\n"

    md += "\n💵 **个股主力净流入 Top 5**：\n"
    for i, ind in enumerate(indiv_inflow[:5], 1):
        chg = ind.get("change_rate", 0.0)
        flag = "🔴" if chg > 0 else "🟢"
        md += f"{i}. **{ind.get('name')}** (`{ind.get('code')}`)：{ind.get('latest'):.2f} ({flag} {chg:+.2f}%) ➔ 主力: **+{ind.get('net_inflow_amount', 0):.2f} 亿**\n"

    if longhu_list:
        md += "\n🐉 **龙虎榜机构/游资席位异动**：\n"
        for lhb in longhu_list[:4]:
            md += f"• **{lhb.get('name')}**：+{lhb.get('buy_amount', 0):.2f}万 ({lhb.get('reason')})\n"

    md += """
==============================
🌐 **【4. 中美板块逻辑映射比对】**
------------------------------
海外联动指标：
"""
    for us in us_indexes:
        chg = us.get("change_rate", 0.0)
        flag = "🔴" if chg > 0 else "🟢"
        md += f"• **{us.get('name')}**：{us.get('latest'):.2f} ({flag} {chg:+.2f}%)\n"

    cnh = overseas_data.get("cnh_rate", 7.18)
    a50 = overseas_data.get("a50_change", 0.0)
    flag_a50 = "🔴" if a50 > 0 else "🟢"
    md += f"• **富时中国 A50 期货**：{flag_a50} {a50:+.2f}%\n"
    md += f"• **离岸人民币 (USD/CNH)**：`{cnh:.4f}`\n\n"

    md += "🔗 **产业链逻辑传导比对**：\n"
    for m in mapping_details:
        md += f"• **{m.get('driver')}** ➔ **{m.get('hit_sectors')}** ({m.get('status')})\n  ↳ *逻辑*: {m.get('logic')}\n"

    md += """
==============================
📑 **【5. 投行与券商精选研报】**
------------------------------
"""
    for r in reports_data[:4]:
        md += f"• **{r.get('stock_name')}** ({r.get('institution')} | `{r.get('rating')}`)\n  ↳ *视点*: {r.get('title')}\n"

    md += """
==============================
🪜 **【6. 短线连板梯队分布】**
------------------------------
"""
    ladder = limit_info.get("ladder", {})
    if ladder:
        for height in sorted(ladder.keys(), reverse=True):
            stocks = "、".join(ladder[height])
            md += f"• **{height} 连板** ({len(ladder[height])}家)：{stocks}\n"
    else:
        md += "• 暂无高位连板数据\n"

    md += f"""
==============================
🤖 **【7. 首席智投策略分析】**
------------------------------
{ai_summary}

------------------------------
*免责声明：本报告由自动智能算法生成，仅供研究参考，不构成投资买卖建议。*
"""
    return md

if __name__ == "__main__":
    pass
