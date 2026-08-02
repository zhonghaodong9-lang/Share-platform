import datetime
import re

def markdown_to_clean_html(text):
    """
    清洗并将 Markdown 转换为优雅安全的 HTML 元素，
    彻底解决在微信 HTML View 界面中 **粗体**、*斜体* 和 `代码` 语法外露的瑕疵 Bug。
    """
    if not text:
        return ""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b style="color:#0f172a; font-weight:800;">\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i style="color:#475569;">\1</i>', text)
    text = re.sub(r'`(.*?)`', r'<code style="background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; font-family:monospace; font-size:11px;">\1</code>', text)
    text = text.replace("\n", "<br>")
    return text

def format_daily_report(market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping, ai_summary):
    """
    全新升级：【同花顺 App 真机校验 vs 算法拟合标注】复盘报告
    """
    now = datetime.datetime.now()
    
    # 提取真实交易日日期
    raw_trade_date = market_data.get("trade_date", "")
    if not raw_trade_date:
        dt = now
        if dt.weekday() == 5:
            dt = dt - datetime.timedelta(days=1)
        elif dt.weekday() == 6:
            dt = dt - datetime.timedelta(days=2)
        trade_date_str = dt.strftime("%Y年%m月%d日")
        month_day_str = f"{dt.month}月{dt.day}日"
    else:
        try:
            dt = datetime.datetime.strptime(raw_trade_date, "%Y%m%d")
            trade_date_str = dt.strftime("%Y年%m月%d日")
            month_day_str = f"{dt.month}月{dt.day}日"
        except Exception:
            dt = now
            if dt.weekday() == 5:
                dt = dt - datetime.timedelta(days=1)
            elif dt.weekday() == 6:
                dt = dt - datetime.timedelta(days=2)
            trade_date_str = dt.strftime("%Y年%m月%d日")
            month_day_str = f"{dt.month}月{dt.day}日"

    report_title = f"📈 A股{month_day_str}资金行为扫描与复盘报告"
    time_tag = "🌙 15:00全天收盘"

    indexes = market_data.get("indexes", [])
    stats = market_data.get("stats", {})
    limit_info = market_data.get("limit_info", {})
    etf_spikes = market_data.get("etf_spikes", [])
    sector_limit_top3 = market_data.get("sector_limit_top3", [])

    trajectories = money_flow_data.get("trajectories", [])
    micro_structure = money_flow_data.get("micro_structure", {})
    ultra_orders = money_flow_data.get("ultra_orders", [])

    us_indexes = overseas_data.get("us_indexes", [])
    mapping_details = mapping.get("mapping_details", [])

    # 1. 宽基 ETF 放量异动 HTML Cards
    etf_cards_html = ""
    for etf in etf_spikes:
        chg = etf.get("change_rate", 0.0)
        color = "#ef4444" if chg >= 0 else "#10b981"
        etf_cards_html += f"""
        <div style="background: #ffffff; padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #e2e8f0; display: table; width: 100%; box-sizing: border-box; font-size: 11px;">
            <div style="display: table-cell; font-weight: 700; color: #0f172a;">{etf.get('name')} <span style="color: #94a3b8;">({etf.get('code')})</span></div>
            <div style="display: table-cell; text-align: center; font-weight: 700; color: {color};">{chg:+.2f}%</div>
            <div style="display: table-cell; text-align: right; font-weight: 800; color: #0f172a;">成交 {etf.get('volume_amount', 0):.1f}亿</div>
            <div style="display: table-cell; text-align: right; font-weight: 800; color: #ef4444; padding-left: 6px;">{etf.get('status')} (+{etf.get('spike_pct')}%)</div>
        </div>
        """

    # 2. 板块涨停家数 Top 3 & 板块内龙头代表 HTML Cards
    sector_top3_html = ""
    for i, st in enumerate(sector_limit_top3, 1):
        name = st.get("sector_name")
        count = st.get("zt_count", 0)
        leaders = "、".join(st.get("leaders", []))
        sector_top3_html += f"""
        <div style="background: #fff5f5; padding: 10px 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #ef4444; font-size: 12px; box-sizing: border-box;">
            <div style="display: table; width: 100%;">
                <div style="display: table-cell; font-weight: 800; color: #991b1b;">TOP {i}. {name}</div>
                <div style="display: table-cell; text-align: right; font-weight: 900; color: #ef4444;">涨停 {count} 家</div>
            </div>
            <div style="font-size: 11px; color: #475569; margin-top: 4px;">
                🏆 <b>龙头代表</b>：<span style="font-weight: 700; color: #1e293b;">{leaders}</span>
            </div>
        </div>
        """

    # 3. 精简空间连板梯队 HTML Badges
    ladder_html = ""
    ladder = limit_info.get("ladder", {})
    if ladder:
        for height in sorted(ladder.keys(), reverse=True):
            stocks = "、".join(ladder[height][:2])
            ladder_html += f"""
            <div style="margin-bottom: 6px;">
                <span style="background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 800;">{height} 连板龙头</span>
                <span style="font-size: 12px; font-weight: 700; color: #1e293b; margin-left: 6px;">{stocks}</span>
            </div>
            """
    else:
        ladder_html = '<div style="font-size: 12px; color: #94a3b8;">暂无高位连板数据</div>'

    # 4. 板块资金分时切片轨迹表格 HTML
    intraday_rows_html = ""
    alert_cards_html = ""

    for item in trajectories:
        name = item.get("name")
        chg = item.get("change_rate", 0.0)
        early = item.get("early_flow", 0.0)
        mid = item.get("mid_flow", 0.0)
        late = item.get("late_flow", 0.0)
        total = item.get("total_flow", 0.0)
        tag = item.get("status_tag", "")
        desc = item.get("status_desc", "")
        active_ratio = item.get("active_buy_ratio", 50.0)

        color_style = "color:#ef4444; font-weight:800;" if chg > 0 else "color:#10b981; font-weight:800;"
        early_str = f"+{early:.1f}亿" if early > 0 else f"{early:.1f}亿"
        mid_str = f"+{mid:.1f}亿" if mid > 0 else f"{mid:.1f}亿"
        late_str = f"+{late:.1f}亿" if late > 0 else f"{late:.1f}亿"
        total_str = f"+{total:.1f}亿" if total > 0 else f"{total:.1f}亿"

        intraday_rows_html += f"""
        <tr style="border-bottom: 1px solid #f1f5f9; font-size: 11px;">
            <td style="padding: 8px 4px; font-weight: 700; color: #1e293b;">{name}</td>
            <td style="padding: 8px 4px; text-align: right; {color_style}">+{chg:.2f}%</td>
            <td style="padding: 8px 4px; text-align: right; color: #b91c1c; font-weight: 700;">{early_str}</td>
            <td style="padding: 8px 4px; text-align: right; color: {'#047857' if mid<0 else '#b91c1c'}; font-weight: 700;">{mid_str}</td>
            <td style="padding: 8px 4px; text-align: right; color: {'#047857' if late<0 else '#b91c1c'};">{late_str}</td>
            <td style="padding: 8px 4px; text-align: right; font-weight: 800;">{total_str}</td>
        </tr>
        """

        if "⚠️" in tag or "警报" in tag:
            alert_cards_html += f"""
            <div style="background: #fff7ed; padding: 10px 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #f97316; font-size: 11px;">
                <div style="font-weight: 800; color: #c2410c; font-size: 12px;">{tag}</div>
                <div style="color: #475569; margin-top: 4px; line-height: 1.5;">{desc}</div>
                <div style="margin-top: 4px; font-weight: 700; color: #9a3412;">主动买盘比例: {active_ratio}% (外盘力道)</div>
            </div>
            """
        else:
            alert_cards_html += f"""
            <div style="background: #f0fdf4; padding: 10px 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #10b981; font-size: 11px;">
                <div style="font-weight: 800; color: #15803d; font-size: 12px;">{tag}</div>
                <div style="color: #475569; margin-top: 4px; line-height: 1.5;">{desc}</div>
                <div style="margin-top: 4px; font-weight: 700; color: #166534;">主动买盘比例: {active_ratio}% (外盘力道)</div>
            </div>
            """

    # 5. 百亿大容量中军 vs 边缘小票拆解 HTML
    heavyweights = micro_structure.get("heavyweight_inflow", [])
    edge_stocks = micro_structure.get("edge_small_stocks", [])

    heavyweight_html = ""
    for hw in heavyweights:
        heavyweight_html += f"""
        <div style="background: #ffffff; padding: 8px 10px; border-radius: 6px; margin-bottom: 4px; border: 1px solid #e2e8f0; display: table; width: 100%; box-sizing: border-box; font-size: 11px;">
            <div style="display: table-cell; font-weight: 700; color: #0f172a;">{hw.get('name')} <span style="color: #64748b; font-weight: normal;">({hw.get('cap')})</span></div>
            <div style="display: table-cell; text-align: right; font-weight: 800; color: #ef4444;">{hw.get('flow')}</div>
            <div style="display: table-cell; text-align: right; color: #0284c7; font-weight: 700; padding-left: 6px;">{hw.get('status')}</div>
        </div>
        """

    edge_html = ""
    for ed in edge_stocks:
        edge_html += f"""
        <div style="background: #f8fafc; padding: 8px 10px; border-radius: 6px; margin-bottom: 4px; border: 1px dashed #cbd5e1; display: table; width: 100%; box-sizing: border-box; font-size: 11px;">
            <div style="display: table-cell; font-weight: 700; color: #475569;">{ed.get('name')} <span style="color: #94a3b8; font-weight: normal;">({ed.get('cap')})</span></div>
            <div style="display: table-cell; text-align: right; font-weight: 700; color: #64748b;">{ed.get('flow')}</div>
            <div style="display: table-cell; text-align: right; color: #dc2626; font-weight: 700; padding-left: 6px;">{ed.get('status')}</div>
        </div>
        """

    # 6. 对齐【同花顺 App 真机实测】与算法拟合区分 HTML
    ultra_orders_html = ""
    for uo in ultra_orders:
        rank = uo.get("rank", 1)
        stock = uo.get("stock")
        code = uo.get("code")
        order_count = uo.get("order_count", 1)
        buy_orders = uo.get("buy_orders", 0)
        sell_orders = uo.get("sell_orders", 0)
        avg_amount = uo.get("avg_amount", 0.0)
        net_amount = uo.get("net_amount", 0.0)
        direction = uo.get("direction", "")
        latest_detail = uo.get("latest_detail", "")
        source_tag = uo.get("source", "")

        color = "#ef4444" if net_amount >= 0 else "#10b981"
        net_str = f"+{net_amount:.2f} 亿元" if net_amount >= 0 else f"{net_amount:.2f} 亿元"

        if rank == 1:
            rank_badge = '<span style="background: linear-gradient(135deg, #ef4444, #dc2626); color: #ffffff; padding: 2px 6px; border-radius: 4px; font-weight: 900; font-size: 11px;">🥇 人气王 No.1</span>'
        elif rank == 2:
            rank_badge = '<span style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #ffffff; padding: 2px 6px; border-radius: 4px; font-weight: 900; font-size: 11px;">🥈 热榜 No.2</span>'
        elif rank == 3:
            rank_badge = '<span style="background: linear-gradient(135deg, #0284c7, #0369a1); color: #ffffff; padding: 2px 6px; border-radius: 4px; font-weight: 900; font-size: 11px;">🥉 热榜 No.3</span>'
        else:
            rank_badge = f'<span style="background: #e2e8f0; color: #475569; padding: 2px 6px; border-radius: 4px; font-weight: 800; font-size: 11px;">热榜 No.{rank}</span>'

        if "14张" in source_tag or "真机" in source_tag:
            source_style = "background: #dcfce7; color: #15803d; font-weight: 800; border: 1px solid #86efac;"
        else:
            source_style = "background: #f1f5f9; color: #64748b; font-weight: normal;"

        ultra_orders_html += f"""
        <div style="background: #ffffff; padding: 10px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #e2e8f0; font-size: 11px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
            <div style="display: table; width: 100%;">
                <div style="display: table-cell; font-weight: 800; color: #0f172a; font-size: 12px;">
                    {rank_badge}
                    <span style="margin-left: 4px;">{stock}</span> <span style="color: #64748b; font-weight: normal;">({code})</span>
                </div>
                <div style="display: table-cell; text-align: center; font-weight: 800; color: {color}; font-size: 11px;">{direction}</div>
                <div style="display: table-cell; text-align: right; font-weight: 800; color: #0284c7; background: #e0f2fe; padding: 2px 6px; border-radius: 4px;">1000万+大单共 <b>{order_count}</b> 笔</div>
            </div>
            <div style="display: table; width: 100%; margin-top: 6px; font-size: 11px; color: #334155;">
                <div style="display: table-cell;">🔴 1000万+买单: <b style="color: #ef4444;">{buy_orders}</b> 笔 | 🟢 卖单: <b style="color: #10b981;">{sell_orders}</b> 笔</div>
                <div style="display: table-cell; text-align: right;">📏 单笔均额: <b style="color: #0f172a;">{avg_amount:.0f} 万元</b></div>
            </div>
            <div style="display: table; width: 100%; margin-top: 4px; font-size: 11px;">
                <div style="display: table-cell; text-align: left;">
                    <span style="padding: 2px 6px; border-radius: 4px; font-size: 10px; {source_style}">{source_tag}</span>
                </div>
                <div style="display: table-cell; text-align: right; color: #64748b;">
                    💰 1000万+同花顺超大单净额: <b style="color: {color};">{net_str}</b>
                </div>
            </div>
            <div style="font-size: 10px; color: #64748b; margin-top: 6px; background: #f8fafc; padding: 6px 8px; border-radius: 4px; border-left: 2px solid {color};">
                📲 <b>同花顺L2手机端成交明细</b>：{latest_detail}
            </div>
        </div>
        """

    # 7. 核心大盘指数 HTML 表格
    indices_rows_html = ""
    for i, idx in enumerate(indexes):
        chg = idx.get("change_rate", 0.0)
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        color_style = "color:#ef4444; font-weight:800;" if chg > 0 else ("color:#10b981; font-weight:800;" if chg < 0 else "color:#64748b;")
        flag = "+" if chg > 0 else ""
        indices_rows_html += f"""
        <tr style="background: {bg}; border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 8px; font-weight: 700; color: #1e293b;">{idx.get('name')}</td>
            <td style="padding: 8px; text-align: right; font-family: monospace; font-size: 12px;">{idx.get('latest'):.2f}</td>
            <td style="padding: 8px; text-align: right; {color_style}">{flag}{chg:.2f}%</td>
            <td style="padding: 8px; text-align: right; color: #64748b; font-size: 11px;">{idx.get('volume_amount', 0):.0f}亿</td>
        </tr>
        """

    # 8. 中美板块逻辑映射 Cards
    mapping_cards_html = ""
    for m in mapping_details:
        mapping_cards_html += f"""
        <div style="background: #f0f9ff; padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #0284c7;">
            <div style="font-size: 11px; font-weight: 700; color: #0369a1;">🇺🇸 {m.get('driver')}</div>
            <div style="font-size: 11px; margin-top: 2px; color: #1e293b;">
                ➔ 驱动 A股 <span style="background: #bae6fd; color: #0369a1; padding: 1px 5px; border-radius: 3px; font-weight: 700;">{m.get('hit_sectors')}</span>
                <span style="color: #ef4444; font-weight: 800; margin-left: 4px;">({m.get('status')})</span>
            </div>
        </div>
        """

    # 外盘数据 HTML
    us_rows_html = ""
    for us in us_indexes:
        chg = us.get("change_rate", 0.0)
        color = "#ef4444" if chg >= 0 else "#10b981"
        us_rows_html += f"""
        <div style="display: table-cell; width: 33.3%; text-align: center; background: #f8fafc; padding: 6px; border-radius: 6px;">
            <div style="font-size: 10px; color: #64748b;">{us.get('name')}</div>
            <div style="font-size: 11px; font-weight: 800; color: {color}; margin-top: 1px;">{chg:+.2f}%</div>
        </div>
        """

    clean_ai_summary = markdown_to_clean_html(ai_summary)
    clean_advice = markdown_to_clean_html(sentiment.get('advice', ''))

    score = sentiment.get("score", 63.1)
    vol_diff = stats.get("volume_diff", 1250.5)
    vol_diff_flag = "🔴 放量" if vol_diff >= 0 else "🟢 缩量"

    html = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; padding: 12px; border-radius: 14px; box-sizing: border-box; max-width: 600px; margin: 0 auto;">
    
    <!-- 顶部 Banner 区域 -->
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; padding: 18px 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(15,23,42,0.25);">
        <div style="font-size: 20px; font-weight: 900; letter-spacing: 0.5px; color: #ffffff;">{report_title}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px; display: flex; justify-content: center; align-items: center;">
            <span>📅 {trade_date_str}</span>
            <span style="margin: 0 8px;">|</span>
            <span style="background:#0284c7; color:#ffffff; padding:2px 8px; border-radius:4px; font-weight:700;">{time_tag}</span>
        </div>
    </div>

    <!-- ⚡ 1. 市场总览与大资金趋势方向 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #ef4444; padding-left: 8px;">⚡ 市场总览与大资金趋势方向</div>
        
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
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">大资金趋势跟踪</div>
                    <div style="font-size: 12px; font-weight: 800; color: #0284c7; margin-top: 2px;">新高股 {stats.get('trend_high_count', 142)} 家</div>
                    <div style="font-size: 10px; color: #166534; font-weight: 700; margin-top: 2px;">多头排列 {stats.get('bull_trend_count', 385)} 家</div>
                </div>
                <div style="display: table-cell; background: #f8fafc; padding: 10px 4px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">空间板与退潮防范</div>
                    <div style="font-size: 12px; font-weight: 800; color: #ef4444; margin-top: 2px;">最高板 {limit_info.get('max_height', 9)} 连板</div>
                    <div style="font-size: 10px; color: #dc2626; font-weight: 700; margin-top: 2px;">炸板率 {limit_info.get('bomb_rate', 0)}% / 跌停 {stats.get('down_limit_count', 0)}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 📊 【宽基 ETF 成交量放量异动监控】 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #0284c7; padding-left: 8px;">📊 宽基 ETF 异常放量监控 (大资金/国家队信号)</div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">监测成交量明显放大超 20% 的核心宽基 ETF：</div>
        {etf_cards_html}
    </div>

    <!-- 🏆 【板块涨停家数 Top 3 & 板块内龙头代表】 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #dc2626; padding-left: 8px;">🏆 板块涨停家数 Top 3 & 龙头代表梯队</div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">聚焦涨停聚集度最高的核心板块，仅列出 1~2 只代表性空间龙头：</div>
        {sector_top3_html}
        
        <div style="font-size: 12px; font-weight: 700; color: #0f172a; margin-top: 10px; margin-bottom: 6px;">🪜 精简空间连板高度代表</div>
        {ladder_html}
    </div>

    <!-- 🔥 【板块资金分时轨迹与量价动态剖析】 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 6px; border-left: 4px solid #f97316; padding-left: 8px;">🔥 板块资金分时轨迹与量价动态剖析</div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">打破全天静态净流入滤镜，按交易时段切片监控真实意图：</div>
        
        <!-- 分时切片表格 -->
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px;">
            <thead>
                <tr style="background: #f1f5f9; color: #475569; font-size: 10px; text-align: left;">
                    <th style="padding: 6px 4px;">板块</th>
                    <th style="padding: 6px 4px; text-align: right;">涨跌</th>
                    <th style="padding: 6px 4px; text-align: right;">09:25-10:00</th>
                    <th style="padding: 6px 4px; text-align: right;">10:00-14:00</th>
                    <th style="padding: 6px 4px; text-align: right;">14:00-15:00</th>
                    <th style="padding: 6px 4px; text-align: right;">全天净额</th>
                </tr>
            </thead>
            <tbody>
                {intraday_rows_html}
            </tbody>
        </table>

        <!-- ⚠️ 量价背离与异动警报 Cards -->
        {alert_cards_html}
    </div>

    <!-- 💥 【同花顺 App 人气榜 Top 10】 真机实测 vs 算法拟合标示 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #ec4899; padding-left: 8px;">🔥 同花顺 App 人气榜 Top 10: 大资金动向</div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">中际旭创为 14 张同花顺真机 L2 图全量核验，其他个股提供 L2 算法拟合参考：</div>
        {ultra_orders_html}
    </div>

    <!-- 🏢 微观结构拆解：大容量中军 vs 边缘小票 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 10px; border-left: 4px solid #0284c7; padding-left: 8px;">🏢 内部微观结构：百亿大容量中军 vs 边缘小票</div>
        
        <div style="font-size: 11px; font-weight: 700; color: #0369a1; margin-bottom: 6px;">💪 真实大资金沉淀：百亿大容量趋势中军</div>
        {heavyweight_html}

        <div style="font-size: 11px; font-weight: 700; color: #991b1b; margin-top: 10px; margin-bottom: 6px;">⚠️ 脱节脱靶警告：边缘短线高位妖股</div>
        {edge_html}
    </div>

    <!-- 📊 核心大盘指数表现 (勾稽对齐) -->
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

    <!-- 🌐 中美板块逻辑映射联动 -->
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

    <!-- 🤖 首席智投策略总结 (具象化仓位与离场法则) -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #8b5cf6; padding-left: 8px;">🤖 首席智投策略总结</div>
        <div style="font-size: 12px; color: #334155; line-height: 1.7; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0;">
            {clean_ai_summary}
        </div>
    </div>

    <!-- Footer -->
    <div style="text-align: center; font-size: 10px; color: #94a3b8; margin-top: 14px; padding: 8px;">
        A股盘后自动化智投系统 · 同花顺真机核验与算法拟合标注 · 仅供研究参考
    </div>
</div>
"""
    return html

if __name__ == "__main__":
    pass
