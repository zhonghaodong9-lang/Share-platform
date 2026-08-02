import datetime
import logging

def format_daily_report(market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping, ai_summary):
    """将所有市场数据与分析结果渲染为美观、专业机构风采的 Markdown 盘后复盘日报"""
    today_str = datetime.datetime.now().strftime("%Y年%m月%d日")

    indexes = market_data.get("indexes", [])
    stats = market_data.get("stats", {})
    limit_info = market_data.get("limit_info", {})

    sector_inflow = money_flow_data.get("sector_flow", {}).get("inflow", [])
    indiv_inflow = money_flow_data.get("individual_flow", {}).get("inflow", [])
    longhu_list = money_flow_data.get("longhu_list", [])

    us_indexes = overseas_data.get("us_indexes", [])
    mapping_details = mapping.get("mapping_details", [])

    # 构建情绪温度 ProgressBar 图示
    score = sentiment.get("score", 50.0)
    filled_blocks = int(score // 10)
    bar = "█" * filled_blocks + "░" * (10 - filled_blocks)

    md = f"""# 📈 A股专业盘后智投与复盘日报 ({today_str})

> **生成时间**：{datetime.datetime.now().strftime("%H:%M:%S")} | **数据源**：AKShare / 新浪财经 / 深度智投引擎

---

## ⚡ 市场短线全景仪表盘

| 关键指标 | 表现 / 数值 | 说明 / 解读 |
| :--- | :--- | :--- |
| **市场情绪温度** | `[{bar}]` **{score} 分** | **{sentiment.get('stage', '')}** |
| **两市总成交额** | **{stats.get('total_volume', 0):.2f} 亿元** | 沪深京三市合计成交量能 |
| **全场上涨 / 下跌** | 🔴 涨 **{stats.get('up_count', 0)}** 家 / 🟢 跌 **{stats.get('down_count', 0)}** 家 | 平盘 {stats.get('flat_count', 0)} 家 |
| **涨停 / 跌停家数** | 🔥 涨停 **{limit_info.get('zt_count', 0)}** 家 / ❄️ 跌停 **{stats.get('down_limit_count', 0)}** 家 | 炸板率: **{limit_info.get('bomb_rate', 0)}%** |
| **连板最高高度** | 🏆 **{limit_info.get('top_stock', '无')}** | 全市场短线空间板龙头 |

> **💡 操盘策略提醒**：{sentiment.get('advice', '')}

---

## 📊 核心大盘指数表现

| 指数名称 | 代码 | 最新点位 | 涨跌额 | 涨跌幅 | 成交额 (亿元) |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

    for idx in indexes:
        chg = idx.get("change_rate", 0.0)
        flag = "🔴 " if chg > 0 else ("🟢 " if chg < 0 else "⚪ ")
        md += f"| **{idx.get('name')}** | `{idx.get('code')}` | {idx.get('latest'):.2f} | {idx.get('change_amount'):+.2f} | {flag}{chg:+.2f}% | {idx.get('volume_amount'):.2f} |\n"

    md += """
---

## 💰 资金量与主力/机构资金流向

### 1. 领涨/主力净流入行业板块 Top 5
| 板块名称 | 涨跌幅 | 领涨/领头个股 | 领涨股涨幅 |
| :--- | :--- | :--- | :--- |
"""
    for sec in sector_inflow[:5]:
        chg = sec.get("change_rate", 0.0)
        flag = "🔴 " if chg > 0 else "🟢 "
        md += f"| **{sec.get('name')}** | {flag}{chg:+.2f}% | {sec.get('leader')} | {sec.get('leader_change', 0):+.2f}% |\n"

    md += """
### 2. 个股主力资金净流入 TOP 5
| 股票名称 | 代码 | 最新价 | 今日涨跌幅 | 主力净流入 (亿元) |
| :--- | :--- | :--- | :--- | :--- |
"""
    for ind in indiv_inflow[:5]:
        chg = ind.get("change_rate", 0.0)
        flag = "🔴 " if chg > 0 else "🟢 "
        md += f"| **{ind.get('name')}** | `{ind.get('code')}` | {ind.get('latest'):.2f} | {flag}{chg:+.2f}% | **+{ind.get('net_inflow_amount', 0):.2f} 亿** |\n"

    md += """
### 3. 龙虎榜机构与游资异动明细
| 股票名称 | 代码 | 机构/游资净买入 (万元) | 上榜原因 / 席位解读 |
| :--- | :--- | :--- | :--- |
"""
    for lhb in longhu_list[:5]:
        md += f"| **{lhb.get('name')}** | `{lhb.get('code')}` | **+{lhb.get('buy_amount', 0):.2f} 万** | {lhb.get('reason')} |\n"

    md += """
---

## 🌐 海外市场与“中美板块映射”联动

### 1. 隔夜外资与全球宏观指标
| 市场 / 指标 | 最新点位 / 汇率 | 涨跌幅 |
| :--- | :--- | :--- |
"""
    for us in us_indexes:
        chg = us.get("change_rate", 0.0)
        flag = "🔴 " if chg > 0 else "🟢 "
        md += f"| **{us.get('name')}** | {us.get('latest'):.2f} | {flag}{chg:+.2f}% |\n"

    cnh = overseas_data.get("cnh_rate", 7.18)
    a50 = overseas_data.get("a50_change", 0.0)
    flag_a50 = "🔴 " if a50 > 0 else "🟢 "
    md += f"| **富时中国 A50 期货** | 期货联动 | {flag_a50}{a50:+.2f}% |\n"
    md += f"| **离岸人民币 (USD/CNH)** | {cnh:.4f} | 汇率参考 |\n"

    md += """
### 2. 中美板块逻辑映射比对
| 美股驱动源 | A股映射产业链 | 今日A股共振板块 | 映射状态与联动逻辑 |
| :--- | :--- | :--- | :--- |
"""
    for m in mapping_details:
        md += f"| **{m.get('driver')}** | {m.get('mapped_sectors')} | **{m.get('hit_sectors')}** | {m.get('status')}<br>*{m.get('logic')}* |\n"

    md += """
---

## 📑 投行与券商最新研报精选

| 证券/投行机构 | 看好标的 | 东财/机构评级 | 研报主题 / 核心视点 |
| :--- | :--- | :--- | :--- |
"""
    for r in reports_data[:5]:
        md += f"| **{r.get('institution')}** | **{r.get('stock_name')}** | `{r.get('rating')}` | {r.get('title')} |\n"

    md += f"""
---

## 🪜 短线连板梯队分布

"""
    ladder = limit_info.get("ladder", {})
    if ladder:
        for height in sorted(ladder.keys(), reverse=True):
            stocks = "、".join(ladder[height])
            md += f"- **{height} 连板** ({len(ladder[height])}家): {stocks}\n"
    else:
        md += "- 暂无高位连板数据\n"

    md += f"""
---

## 🤖 首席智投策略分析

{ai_summary}

---
*注：本复盘报告由 A股盘后自动化智投系统自动生成，仅供研究参考，不构成任何投资买卖建议。*
"""
    return md

if __name__ == "__main__":
    pass
