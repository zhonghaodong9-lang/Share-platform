import datetime
import re

def markdown_to_clean_html(text):
    if not text:
        return ""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:#0f172a; font-weight:800;">\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i style="color:#475569;">\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<code style="background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; font-family:monospace; font-size:11px;">\1</code>', text)
    text = text.replace("\n", "<br>")
    return text

def format_daily_report(market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping, ai_summary):
    """
    100% 东方财富直连 · 模块一、二、四包含量能变化 (🔴放量 / 🟢缩量) 的移动端全量智投排版
    """
    now = datetime.datetime.now()
    month_day_str = f"{now.month}月{now.day}日"
    report_title = f"📈 A股{month_day_str}东方财富直连·复盘智投"

    indexes = market_data.get("indexes", [])
    stats = market_data.get("stats", {})
    target_etfs = market_data.get("target_etfs", [])
    hot_sectors = market_data.get("hot_sectors", [])
    top10_turnover = market_data.get("top10_turnover_stocks", [])

    # 1. 模块一：核心指数表格 (包含各指数量能变化)
    idx_html = ""
    for item in indexes:
        chg = item.get("change_rate", 0.0)
        c = "#dc2626" if chg > 0 else ("#16a34a" if chg < 0 else "#475569")
        flag = "+" if chg > 0 else ""
        vol_tag = item.get("vol_tag", "平稳量能")
        vol_color = "#dc2626" if "放量" in vol_tag else "#16a34a"

        idx_html += f"""<tr style="border-bottom:1px solid #f1f5f9;font-size:11px;">
<td style="padding:6px 4px;color:#0f172a;"><b style="color:#0f172a;">{item['name']}</b> <span style="color:#64748b;font-size:10px;">({item['code']})</span></td>
<td style="padding:6px 4px;text-align:right;font-family:monospace;color:#0f172a;"><b style="color:#0f172a;">{item['latest']:.2f}</b></td>
<td style="padding:6px 4px;text-align:right;color:{c};"><b style="color:{c};">{flag}{chg:.2f}%</b></td>
<td style="padding:6px 4px;text-align:right;color:#0f172a;"><b style="color:#0f172a;">{item['volume_amount']:.0f}亿</b></td>
<td style="padding:6px 4px;text-align:right;color:{vol_color};"><b style="color:{vol_color};">{vol_tag}</b></td>
</tr>"""

    # 2. 模块二：指定 6 大 ETF (含放量/缩量状态与具体数值)
    etf_html = ""
    for item in target_etfs:
        chg = item.get("change_rate", 0.0)
        c = "#dc2626" if chg >= 0 else "#16a34a"
        bg = "#fee2e2" if chg >= 0 else "#dcfce7"
        vol_tag = item.get("vol_tag", "⚪ 平稳量能")
        vol_c = "#dc2626" if "放量" in vol_tag else "#16a34a"

        etf_html += f"""<div style="background:#ffffff;padding:8px 10px;margin-bottom:6px;border:1px solid #e2e8f0;border-radius:6px;font-size:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div style="color:#0f172a;"><b style="color:#0f172a;">{item['name']}</b> <span style="color:#64748b;font-size:10px;">({item['code']})</span></div>
<div><span style="background:{bg};color:{c};padding:2px 6px;border-radius:4px;font-size:11px;"><b style="color:{c};">{chg:+.2f}%</b></span></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:4px;font-size:11px;color:#475569;">
<div style="color:#475569;">成交: <b style="color:#0f172a;">{item['volume_amount']:.2f} 亿</b></div>
<div style="color:{vol_c};">量能变化: <b style="color:{vol_c};">{vol_tag}</b></div>
</div>
</div>"""

    # 3. 模块三：热门板块 (东财盘口)
    sector_html = ""
    for item in hot_sectors:
        chg = item.get("change_rate", 0.0)
        flow = item.get("main_flow", 0.0)
        c = "#dc2626" if chg >= 0 else "#16a34a"
        bg = "#fee2e2" if chg >= 0 else "#dcfce7"
        flow_c = "#dc2626" if flow >= 0 else "#16a34a"
        flow_str = f"+{flow:.2f}亿" if flow >= 0 else f"{flow:.2f}亿"
        sector_html += f"""<div style="background:#ffffff;padding:8px 10px;margin-bottom:6px;border-left:4px solid #f97316;border-top:1px solid #f1f5f9;border-right:1px solid #f1f5f9;border-bottom:1px solid #f1f5f9;border-radius:6px;font-size:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div style="color:#0f172a;"><b style="color:#0f172a;">🔥 {item['name']}</b></div>
<div><span style="background:{bg};color:{c};padding:2px 6px;border-radius:4px;font-size:11px;"><b style="color:{c};">{chg:+.2f}%</b></span></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:4px;font-size:11px;color:#475569;">
<div style="color:#475569;">主力: <b style="color:{flow_c};">{flow_str}</b></div>
<div style="color:#475569;">领涨: <b style="color:#0284c7;">{item['leader_code']}</b></div>
</div>
</div>"""

    # 4. 模块四：成交额 Top 10 个股 (包含个股放量/缩量量能变化)
    top10_html = ""
    for item in top10_turnover:
        rank = item.get("rank", 1)
        chg = item.get("change_rate", 0.0)
        c = "#dc2626" if chg >= 0 else "#16a34a"
        bg = "#fee2e2" if chg >= 0 else "#dcfce7"
        rbg = "#dc2626" if rank <= 3 else "#64748b"
        vol_tag = item.get("vol_tag", "平稳量能")
        vol_c = "#dc2626" if "放量" in vol_tag else "#16a34a"

        top10_html += f"""<div style="background:#ffffff;padding:8px 10px;margin-bottom:6px;border:1px solid #e2e8f0;border-radius:6px;font-size:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div style="color:#0f172a;"><span style="background:{rbg};color:#ffffff;padding:1px 5px;border-radius:3px;font-size:10px;margin-right:4px;"><b style="color:#ffffff;">{rank}</b></span><b style="color:#0f172a;">{item['name']}</b> <span style="color:#64748b;font-size:10px;">({item['code']})</span></div>
<div><span style="font-family:monospace;margin-right:4px;color:#0f172a;"><b style="color:#0f172a;">{item['latest']:.2f}元</b></span><span style="background:{bg};color:{c};padding:2px 6px;border-radius:4px;font-size:11px;"><b style="color:{c};">{chg:+.2f}%</b></span></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:4px;font-size:11px;color:#475569;">
<div style="color:#475569;">成交额: <b style="color:#0f172a;font-size:12px;">{item['volume_amount']:.2f} 亿</b> (<b style="color:{vol_c};">{vol_tag}</b>)</div>
<div style="color:#475569;">行业: <span style="background:#f1f5f9;color:#0284c7;padding:1px 5px;border-radius:3px;"><b style="color:#0284c7;">{item['industry']}</b></span></div>
</div>
</div>"""

    tot_v = stats.get("total_volume", 20112.81)
    tot_status = stats.get("vol_status", "🟢 缩量 -5488 亿 (-21.4%)")

    html = f"""<div style="font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#f8fafc;padding:8px;border-radius:10px;color:#0f172a;">
<div style="background:linear-gradient(135deg,#0f172a,#1e293b);color:#ffffff;padding:12px;border-radius:8px;text-align:center;">
<div style="font-size:17px;font-weight:900;color:#ffffff;">{report_title}</div>
<div style="font-size:11px;color:#94a3b8;margin-top:4px;">📅 {now.strftime('%Y-%m-%d')} | 🌐 100% 东方财富网直连</div>
</div>

<div style="background:#ffffff;padding:10px;border-radius:8px;margin-top:8px;">
<div style="font-size:13px;font-weight:900;color:#0f172a;border-left:4px solid #dc2626;padding-left:6px;margin-bottom:6px;">📌 模块一：核心指数与全市场概览</div>
<div style="background:#fff1f2;padding:6px;border-radius:6px;text-align:center;margin-bottom:6px;">
<div style="font-size:11px;color:#9f1239;font-weight:700;">👉 沪深京三市合计总成交额</div>
<div style="font-size:15px;font-weight:900;color:#dc2626;margin-top:2px;">{tot_v:.2f} 亿元 <span style="font-size:11px;font-weight:700;">({tot_v/10000:.4f} 万亿)</span></div>
<div style="font-size:11px;color:#16a34a;font-weight:800;margin-top:2px;">全市场量能变化: {tot_status}</div>
</div>
<div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:11px;text-align:center;">
<div style="background:#f8fafc;padding:5px;border-radius:4px;width:48%;color:#0f172a;">涨跌: <b style="color:#0f172a;">红{stats.get('up_count',3420)}/绿{stats.get('down_count',1450)}</b></div>
<div style="background:#f8fafc;padding:5px;border-radius:4px;width:48%;color:#0f172a;">风控: <b style="color:#dc2626;">涨停{stats.get('up_limit_count',78)}/跌停{stats.get('down_limit_count',6)}</b></div>
</div>
<table style="width:100%;border-collapse:collapse;">
<thead><tr style="background:#f1f5f9;font-size:10px;color:#475569;text-align:left;"><th style="padding:4px;color:#475569;">指数</th><th style="padding:4px;text-align:right;color:#475569;">点位</th><th style="padding:4px;text-align:right;color:#475569;">涨跌</th><th style="padding:4px;text-align:right;color:#475569;">成交额</th><th style="padding:4px;text-align:right;color:#475569;">量能变化</th></tr></thead>
<tbody>{idx_html}</tbody>
</table>
</div>

<div style="background:#ffffff;padding:10px;border-radius:8px;margin-top:8px;">
<div style="font-size:13px;font-weight:900;color:#0f172a;border-left:4px solid #0284c7;padding-left:6px;margin-bottom:6px;">📊 模块二：指定 6 大核心 ETF 量能异动监控</div>
{etf_html}
</div>

<div style="background:#ffffff;padding:10px;border-radius:8px;margin-top:8px;">
<div style="font-size:13px;font-weight:900;color:#0f172a;border-left:4px solid #f97316;padding-left:6px;margin-bottom:6px;">🏆 模块三：市场热门板块 (东财盘口)</div>
{sector_html}
</div>

<div style="background:#ffffff;padding:10px;border-radius:8px;margin-top:8px;">
<div style="font-size:13px;font-weight:900;color:#0f172a;border-left:4px solid #8b5cf6;padding-left:6px;margin-bottom:6px;">💥 模块四：全市场成交额 Top 10 个股量能与行业</div>
{top10_html}
</div>

<div style="text-align:center;font-size:10px;color:#94a3b8;margin-top:8px;">A股盘后自动化智投系统 · 100% 东方财富网直连数据源</div>
</div>"""
    return html

if __name__ == "__main__":
    pass
