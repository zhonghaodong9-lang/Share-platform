import datetime

def format_daily_report(market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping, ai_summary):
    """将所有市场数据与分析结果渲染为媲美原生 APP 的高颜值 HTML/CSS 移动端复盘 UI 界面"""
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

    # 情绪温度
    score = sentiment.get("score", 50.0)
    ai_summary_html = ai_summary.replace("\n", "<br>")
    
    # 构造 HTML 指数表格
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

    # 领涨板块 HTML Cards
    sector_cards_html = ""
    for i, sec in enumerate(sector_inflow[:5], 1):
        chg = sec.get("change_rate", 0.0)
        sector_cards_html += f"""
        <div style="background: #fff5f5; padding: 10px 12px; border-radius: 8px; margin-bottom: 6px; border-left: 4px solid #ef4444; display: table; width: 100%; box-sizing: border-box;">
            <div style="display: table-cell; font-size: 13px; font-weight: 700; color: #991b1b;">{i}. {sec.get('name')}</div>
            <div style="display: table-cell; text-align: right; font-size: 13px; font-weight: 800; color: #ef4444;">+{chg:.2f}%</div>
            <div style="display: table-cell; text-align: right; font-size: 11px; color: #64748b; padding-left: 10px;">领涨: {sec.get('leader')} ({sec.get('leader_change', 0):+.1f}%)</div>
        </div>
        """

    # 个股主力资金 HTML Cards
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

    # 中美板块逻辑映射 Cards
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

    # 连板梯队 HTML Badges
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

    html = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; padding: 12px; border-radius: 14px; box-sizing: border-box; max-width: 600px; margin: 0 auto;">
    
    <!-- 顶部 Banner 区域 -->
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; padding: 18px 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(15,23,42,0.25);">
        <div style="font-size: 21px; font-weight: 900; letter-spacing: 0.5px; color: #ffffff;">📈 A股盘后深度智投日报</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 6px;">📅 {today_str} | ⏰ {time_str} 发布</div>
    </div>

    <!-- 市场短线仪表盘卡片 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #ef4444; padding-left: 8px;">⚡ 市场短线风向标</div>
        
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
                </div>
                <div style="display: table-cell; background: #f8fafc; padding: 10px 4px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">上涨 / 下跌</div>
                    <div style="font-size: 13px; font-weight: 800; color: #ef4444; margin-top: 2px;">🔴{stats.get('up_count', 0)} / 🟢{stats.get('down_count', 0)}</div>
                </div>
                <div style="display: table-cell; background: #f8fafc; padding: 10px 4px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">涨停 / 跌停</div>
                    <div style="font-size: 13px; font-weight: 800; color: #ef4444; margin-top: 2px;">🔥{limit_info.get('zt_count', 0)} / ❄️{stats.get('down_limit_count', 0)}</div>
                </div>
            </div>
        </div>

        <div style="font-size: 11px; color: #334155; background: #fff7ed; padding: 10px; border-radius: 8px; margin-top: 8px; border-left: 3px solid #f97316;">
            💡 <b>操盘策略</b>：{sentiment.get('advice', '')}
        </div>
    </div>

    <!-- 核心大盘指数高颜值表格 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #3b82f6; padding-left: 8px;">📊 核心大盘指数表现</div>
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

    <!-- 领涨板块与主力资金 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #10b981; padding-left: 8px;">💰 领涨行业与个股主力流向</div>
        <div style="font-size: 12px; font-weight: 700; color: #475569; margin-bottom: 6px;">🔥 领涨板块 Top 5</div>
        {sector_cards_html}

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

    <!-- 连板龙头梯队分布 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #ec4899; padding-left: 8px;">🪜 空间高度与短线连板梯队</div>
        {ladder_html}
    </div>

    <!-- 首席智投策略建议 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #8b5cf6; padding-left: 8px;">🤖 首席智投策略总结</div>
        <div style="font-size: 12px; color: #334155; line-height: 1.6; background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;">
            {ai_summary_html}
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
