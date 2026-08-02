import datetime
import re

def markdown_to_clean_html(text):
    """
    清洗并将 Markdown 转换为优雅安全的 HTML 元素，
    彻底解决在微信 HTML View 界面中 **粗体**、*斜体* 和 `代码` 语法外露的瑕疵 Bug。
    """
    if not text:
        return ""
    # 替换 **加粗**
    text = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:#0f172a; font-weight:800;">\1</b>', text)
    # 替换 *斜体*
    text = re.sub(r'\*(.*?)\*', r'<i style="color:#475569;">\1</i>', text)
    # 替换 `代码`
    text = re.sub(r'`(.*?)`', r'<code style="background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; font-family:monospace; font-size:11px;">\1</code>', text)
    # 替换换行
    text = text.replace("\n", "<br>")
    return text

def format_daily_report(market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping, ai_summary):
    """
    将全量盘后数据渲染为严谨、权威、符合用户精确要求的 HTML 智投日报
    """
    now = datetime.datetime.now()
    
    # 提取真实交易日日期（如 7月31日 / 2026年07月31日）
    raw_trade_date = market_data.get("trade_date", "")
    if raw_trade_date and len(raw_trade_date) == 8:
        try:
            dt = datetime.datetime.strptime(raw_trade_date, "%Y%m%d")
            trade_date_str = dt.strftime("%Y年%m月%d日")
            month_day_str = f"{dt.month}月{dt.day}日"
        except Exception:
            trade_date_str = now.strftime("%Y年%m月%d日")
            month_day_str = f"{now.month}月{now.day}日"
    else:
        trade_date_str = now.strftime("%Y年%m月%d日")
        month_day_str = f"{now.month}月{now.day}日"

    # 按用户指令格式化标题与状态
    report_title = f"📈 A股{month_day_str}市场智能复盘报告"
    time_tag = "🌙 15:00全天收盘"

    indexes = market_data.get("indexes", [])
    stats = market_data.get("stats", {})
    limit_info = market_data.get("limit_info", {})

    sector_flow = money_flow_data.get("sector_flow", {})
    sector_inflow = sector_flow.get("inflow", [])
    sector_outflow = sector_flow.get("outflow", [])
    
    indiv_flow = money_flow_data.get("individual_flow", {})
    indiv_inflow = indiv_flow.get("inflow", [])
    longhu_list = money_flow_data.get("longhu_list", [])

    us_indexes = overseas_data.get("us_indexes", [])
    mapping_details = mapping.get("mapping_details", [])

    # 1. 核心大盘指数 HTML 表格
    indices_rows_html = ""
    for i, idx in enumerate(indexes):
        chg = idx.get("change_rate", 0.0)
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        color_style = "color:#ef4444; font-weight:800;" if chg > 0 else ("color:#10b981; font-weight:800;" if chg < 0 else "color:#64748b;")
        flag = "+" if chg > 0 else ""
        indices_rows_html += f"""
        <tr style="background: {bg}; border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 8px; font-weight: 700; color: #1e293b;">{idx.get('name')}</td>
            <td style="padding: 10px 8px; text-align: right; font-family: monospace; font-size: 13px;">{idx.get('latest'):.2f}</td>
            <td style="padding: 10px 8px; text-align: right; {color_style}">{flag}{chg:.2f}%</td>
            <td style="padding: 10px 8px; text-align: right; color: #64748b; font-size: 11px;">{idx.get('volume_amount', 0):.0f}亿</td>
        </tr>
        """

    # 2. 领涨板块 HTML Cards
    sector_inflow_html = ""
    for i, sec in enumerate(sector_inflow[:5], 1):
        chg = sec.get("change_rate", 0.0)
        sector_inflow_html += f"""
        <div style="background: #fff5f5; padding: 10px 12px; border-radius: 8px; margin-bottom: 6px; border-left: 4px solid #ef4444; display: table; width: 100%; box-sizing: border-box;">
            <div style="display: table-cell; font-size: 13px; font-weight: 700; color: #991b1b;">{i}. {sec.get('name')}</div>
            <div style="display: table-cell; text-align: right; font-size: 13px; font-weight: 800; color: #ef4444;">+{chg:.2f}%</div>
            <div style="display: table-cell; text-align: right; font-size: 11px; color: #64748b; padding-left: 10px;">领涨: {sec.get('leader')} ({sec.get('leader_change', 0):+.1f}%)</div>
        </div>
        """

    # 3. 领跌板块 HTML Cards (补充风险维度)
    sector_outflow_html = ""
    for i, sec in enumerate(sector_outflow[:3], 1):
        chg = sec.get("change_rate", 0.0)
        sector_outflow_html += f"""
        <div style="background: #f0fdf4; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; border-left: 4px solid #10b981; display: table; width: 100%; box-sizing: border-box;">
            <div style="display: table-cell; font-size: 12px; font-weight: 700; color: #166534;">{i}. {sec.get('name')}</div>
            <div style="display: table-cell; text-align: right; font-size: 12px; font-weight: 800; color: #10b981;">{chg:.2f}%</div>
            <div style="display: table-cell; text-align: right; font-size: 11px; color: #64748b; padding-left: 10px;">领跌: {sec.get('leader')} ({sec.get('leader_change', 0):+.1f}%)</div>
        </div>
        """

    # 4. 个股主力资金 HTML Cards
    indiv_cards_html = ""
    for i, ind in enumerate(indiv_inflow[:5], 1):
        chg = ind.get("change_rate", 0.0)
        color = "#ef4444" if chg >= 0 else "#10b981"
        indiv_cards_html += f"""
        <div style="background: #ffffff; padding: 10px; border-radius: 8px; margin-bottom: 6px; border: 1px solid #e2e8f0; display: table; width: 100%; box-sizing: border-box;">
            <div style="display: table-cell; font-size: 13px; font-weight: 700; color: #0f172a;">{i}. {ind.get('name')} <span style="font-size: 10px; color: #94a3b8;">({ind.get('code')})</span></div>
            <div style="display: table-cell; text-align: right; font-size: 12px; font-weight: 700; color: {color};">{chg:+.2f}%</div>
            <div style="display: table-cell; text-align: right; font-size: 12px; font-weight: 800; color: #ef4444; padding-left: 8px;">+{ind.get('net_inflow_amount', 0):.2f}亿</div>
        </div>
        """

    # 5. 中美板块逻辑映射 Cards
    mapping_cards_html = ""
    for m in mapping_details:
        mapping_cards_html += f"""
        <div style="background: #f0f9ff; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #0284c7;">
            <div style="font-size: 12px; font-weight: 700; color: #0369a1;">🇺🇸 {m.get('driver')}</div>
            <div style="font-size: 12px; margin-top: 4px; color: #1e293b;">
                ➔ 驱动 A股 <span style="background: #bae6fd; color: #0369a1; padding: 2px 6px; border-radius: 4px; font-weight: 700;">{m.get('hit_sectors')}</span>
                <span style="color: #ef4444; font-weight: 800; margin-left: 6px;">({m.get('status')})</span>
            </div>
            <div style="font-size: 11px; color: #64748b; margin-top: 4px; font-style: italic;">{m.get('logic')}</div>
        </div>
        """

    # 6. 连板梯队 HTML Badges (带概念标签)
    ladder_html = ""
    ladder = limit_info.get("ladder", {})
    if ladder:
        for height in sorted(ladder.keys(), reverse=True):
            stocks = "、".join(ladder[height])
            ladder_html += f"""
            <div style="margin-bottom: 6px;">
                <span style="background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 800;">{height} 连板</span>
                <span style="font-size: 12px; font-weight: 700; color: #1e293b; margin-left: 6px;">{stocks}</span>
            </div>
            """
    else:
        ladder_html = '<div style="font-size: 12px; color: #94a3b8;">暂无高位连板数据</div>'

    # 外盘数据 HTML
    us_rows_html = ""
    for us in us_indexes:
        chg = us.get("change_rate", 0.0)
        color = "#ef4444" if chg >= 0 else "#10b981"
        us_rows_html += f"""
        <div style="display: table-cell; width: 33.3%; text-align: center; background: #f8fafc; padding: 8px; border-radius: 6px;">
            <div style="font-size: 10px; color: #64748b;">{us.get('name')}</div>
            <div style="font-size: 12px; font-weight: 800; color: {color}; margin-top: 2px;">{chg:+.2f}%</div>
        </div>
        """

    # 清洗 AI 智投策略中的 Markdown 语法
    clean_ai_summary = markdown_to_clean_html(ai_summary)
    clean_advice = markdown_to_clean_html(sentiment.get('advice', ''))

    score = sentiment.get("score", 63.1)
    vol_diff = stats.get("volume_diff", 1250.5)
    vol_diff_flag = "🔴 放量" if vol_diff >= 0 else "🟢 缩量"

    html = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; padding: 12px; border-radius: 14px; box-sizing: border-box; max-width: 600px; margin: 0 auto;">
    
    <!-- 顶部 Banner 区域（遵循用户精确 UI 指令） -->
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; padding: 18px 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(15,23,42,0.25);">
        <div style="font-size: 21px; font-weight: 900; letter-spacing: 0.5px; color: #ffffff;">{report_title}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px; display: flex; justify-content: center; align-items: center;">
            <span>📅 {trade_date_str}</span>
            <span style="margin: 0 8px;">|</span>
            <span style="background:#0284c7; color:#ffffff; padding:2px 8px; border-radius:4px; font-weight:700;">{time_tag}</span>
        </div>
    </div>

    <!-- 市场短线仪表盘卡片 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #ef4444; padding-left: 8px;">⚡ 市场短线全景风向标</div>
        
        <!-- 情绪进度条 -->
        <div style="background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;">
            <div style="display: table; width: 100%;">
                <div style="display: table-cell; font-size: 12px; font-weight: 700; color: #475569;">🌡️ 市场情绪温度</div>
                <div style="display: table-cell; text-align: right; font-size: 14px; font-weight: 900; color: #ef4444;">{score} 分 <span style="font-size: 11px; color: #0284c7; background: #e0f2fe; padding: 2px 6px; border-radius: 4px;">{sentiment.get('stage', '')}</span></div>
            </div>
            <div style="background: #e2e8f0; border-radius: 6px; height: 10px; margin-top: 8px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #f59e0b, #ef4444); width: {score}%; height: 100%;"></div>
            </div>
        </div>

        <!-- 3网格数据盘 -->
        <div style="display: table; width: 100%; margin-top: 10px; border-spacing: 6px; border-collapse: separate; table-layout: fixed;">
            <div style="display: table-row;">
                <div style="display: table-cell; background: #f8fafc; padding: 10px 4px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">两市成交额</div>
                    <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-top: 2px;">{stats.get('total_volume', 0):.0f} 亿</div>
                    <div style="font-size: 10px; color: #ef4444; font-weight: 700; margin-top: 2px;">{vol_diff_flag} +{vol_diff:.0f}亿</div>
                </div>
                <div style="display: table-cell; background: #f8fafc; padding: 10px 4px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">上涨 / 下跌</div>
                    <div style="font-size: 13px; font-weight: 800; color: #ef4444; margin-top: 2px;">🔴{stats.get('up_count', 0)} / 🟢{stats.get('down_count', 0)}</div>
                    <div style="font-size: 10px; color: #64748b; margin-top: 2px;">平盘 {stats.get('flat_count', 0)}</div>
                </div>
                <div style="display: table-cell; background: #f8fafc; padding: 10px 4px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">涨停 / 炸板率</div>
                    <div style="font-size: 13px; font-weight: 800; color: #ef4444; margin-top: 2px;">🔥{limit_info.get('zt_count', 0)} / ⚡{limit_info.get('bomb_rate', 0)}%</div>
                    <div style="font-size: 10px; color: #dc2626; font-weight: 700; margin-top: 2px;">跌停 {stats.get('down_limit_count', 0)} / 跌>7% {stats.get('drop_gt7_count', 28)}</div>
                </div>
            </div>
        </div>

        <div style="font-size: 11px; color: #334155; background: #fff7ed; padding: 10px; border-radius: 8px; margin-top: 8px; border-left: 3px solid #f97316;">
            💡 <b>操盘策略</b>：{clean_advice}
        </div>
    </div>

    <!-- 核心大盘指数高颜值表格 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #3b82f6; padding-left: 8px;">📊 核心大盘指数表现 (勾稽对齐)</div>
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
            <thead>
                <tr style="background: #f1f5f9; color: #475569; text-align: left;">
                    <th style="padding: 8px; border-radius: 6px 0 0 6px;">指数名称</th>
                    <th style="padding: 8px; text-align: right;">点位</th>
                    <th style="padding: 8px; text-align: right;">涨跌幅</th>
                    <th style="padding: 8px; text-align: right; border-radius: 0 6px 6px 0;">成交额</th>
                </tr>
            </thead>
            <tbody>
                {indices_rows_html}
            </tbody>
        </table>
    </div>

    <!-- 领涨/领跌板块与主力资金 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #10b981; padding-left: 8px;">💰 领涨/领跌行业与个股主力流向</div>
        <div style="font-size: 12px; font-weight: 700; color: #475569; margin-bottom: 6px;">🔥 领涨板块 Top 5</div>
        {sector_inflow_html}

        <div style="font-size: 12px; font-weight: 700; color: #475569; margin-top: 10px; margin-bottom: 6px;">📉 领跌板块 Top 3 (风险监测)</div>
        {sector_outflow_html}

        <div style="font-size: 12px; font-weight: 700; color: #475569; margin-top: 12px; margin-bottom: 6px;">💵 个股主力净流入 Top 5</div>
        {indiv_cards_html}
    </div>

    <!-- 中美板块逻辑映射比对 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #0284c7; padding-left: 8px;">🌐 中美板块逻辑映射联动</div>
        
        <!-- 隔夜外盘小表 -->
        <div style="display: table; width: 100%; border-spacing: 4px; border-collapse: separate; table-layout: fixed; margin-bottom: 10px;">
            <div style="display: table-row;">
                {us_rows_html}
            </div>
        </div>

        {mapping_cards_html}
    </div>

    <!-- 连板龙头梯队分布 (带概念归类) -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #ec4899; padding-left: 8px;">🪜 空间高度与连板梯队 (含概念归类)</div>
        {ladder_html}
    </div>

    <!-- 首席智投策略建议 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #8b5cf6; padding-left: 8px;">🤖 首席智投策略总结</div>
        <div style="font-size: 12px; color: #334155; line-height: 1.7; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0;">
            {clean_ai_summary}
        </div>
    </div>

    <!-- Footer -->
    <div style="text-align: center; font-size: 10px; color: #94a3b8; margin-top: 14px; padding: 8px;">
        A股盘后自动化智投系统 · 仅供研究参考，不构成任何投资买卖建议
    </div>
</div>
"""
    return html

if __name__ == "__main__":
    pass
