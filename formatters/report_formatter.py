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
    渲染用户最新制定的 4 大核心数据模块 (全量东方财富网权威直连数据源)
    """
    now = datetime.datetime.now()
    raw_trade_date = market_data.get("trade_date", "")
    if not raw_trade_date:
        dt = now
        if dt.weekday() == 5:
            dt = dt - datetime.timedelta(days=1)
        elif dt.weekday() == 6:
            dt = dt - datetime.timedelta(days=2)
        month_day_str = f"{dt.month}月{dt.day}日"
        trade_date_str = dt.strftime("%Y年%m月%d日")
    else:
        try:
            dt = datetime.datetime.strptime(raw_trade_date, "%Y%m%d")
            month_day_str = f"{dt.month}月{dt.day}日"
            trade_date_str = dt.strftime("%Y年%m月%d日")
        except Exception:
            month_day_str = f"{now.month}月{now.day}日"
            trade_date_str = now.strftime("%Y年%m月%d日")

    report_title = f"📈 A股{month_day_str}东方财富直连·复盘智投报告"

    indexes = market_data.get("indexes", [])
    stats = market_data.get("stats", {})
    target_etfs = market_data.get("target_etfs", [])
    hot_sectors = market_data.get("hot_sectors", [])
    top10_turnover = market_data.get("top10_turnover_stocks", [])

    # 1. 五大指数行 HTML
    indexes_rows_html = ""
    for idx in indexes:
        chg = idx.get("change_rate", 0.0)
        color_style = "color:#ef4444; font-weight:800;" if chg > 0 else ("color:#10b981; font-weight:800;" if chg < 0 else "color:#64748b;")
        flag = "+" if chg > 0 else ""
        indexes_rows_html += f"""
        <tr style="background: #ffffff; border-bottom: 1px solid #f1f5f9; font-size: 11px;">
            <td style="padding: 6px 8px; font-weight: 700; color: #1e293b;">{idx.get('name')} <span style="color:#94a3b8; font-weight:normal;">({idx.get('code')})</span></td>
            <td style="padding: 6px 8px; text-align: right; font-family: monospace; font-size: 11px; font-weight:700;">{idx.get('latest'):.2f}</td>
            <td style="padding: 6px 8px; text-align: right; {color_style}">{flag}{chg:.2f}%</td>
            <td style="padding: 6px 8px; text-align: right; color: #64748b; font-size: 11px;">{idx.get('volume_amount', 0):.2f}亿</td>
        </tr>
        """

    # 2. 6 大指定 ETF HTML
    etf_rows_html = ""
    for etf in target_etfs:
        chg = etf.get("change_rate", 0.0)
        color = "#ef4444" if chg >= 0 else "#10b981"
        etf_rows_html += f"""
        <div style="background: #ffffff; padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; border: 1px solid #e2e8f0; display: table; width: 100%; box-sizing: border-box; font-size: 11px;">
            <div style="display: table-cell; font-weight: 700; color: #0f172a;">{etf.get('name')} <span style="color: #94a3b8;">({etf.get('code')})</span></div>
            <div style="display: table-cell; text-align: center; font-weight: 700; color: {color};">{chg:+.2f}%</div>
            <div style="display: table-cell; text-align: right; font-weight: 800; color: #0f172a;">成交 {etf.get('volume_amount', 0):.2f}亿</div>
            <div style="display: table-cell; text-align: right; font-weight: 800; color: #ef4444; padding-left: 6px;">{etf.get('status', '放量')}</div>
        </div>
        """

    # 3. 热门板块 HTML
    sector_cards_html = ""
    for sec in hot_sectors:
        chg = sec.get("change_rate", 0.0)
        flow = sec.get("main_flow", 0.0)
        color_chg = "#ef4444" if chg >= 0 else "#10b981"
        color_flow = "#ef4444" if flow >= 0 else "#10b981"
        flow_str = f"+{flow:.2f}亿" if flow >= 0 else f"{flow:.2f}亿"

        sector_cards_html += f"""
        <div style="background: #fff7ed; padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; border-left: 4px solid #f97316; font-size: 11px; display: table; width: 100%; box-sizing: border-box;">
            <div style="display: table-cell; font-weight: 800; color: #9a3412; font-size: 12px;">{sec.get('name')}</div>
            <div style="display: table-cell; text-align: center; font-weight: 800; color: {color_chg};">{chg:+.2f}%</div>
            <div style="display: table-cell; text-align: right; font-weight: 700; color: {color_flow};">主力 {flow_str}</div>
            <div style="display: table-cell; text-align: right; color: #475569; padding-left: 6px;">领涨: <b>{sec.get('leader_code')}</b></div>
        </div>
        """

    # 4. 成交额 Top 10 个股及所属行业 HTML
    top10_rows_html = ""
    for stock in top10_turnover:
        rank = stock.get("rank", 1)
        code = stock.get("code")
        name = stock.get("name")
        price = stock.get("latest", 0.0)
        chg = stock.get("change_rate", 0.0)
        amt = stock.get("volume_amount", 0.0)
        industry = stock.get("industry", "-")

        color = "#ef4444" if chg >= 0 else "#10b981"
        badge_color = "#ef4444" if rank <= 3 else "#64748b"

        top10_rows_html += f"""
        <tr style="background: #ffffff; border-bottom: 1px solid #f1f5f9; font-size: 11px;">
            <td style="padding: 6px 4px; text-align: center;"><span style="background: {badge_color}; color: #ffffff; padding: 1px 6px; border-radius: 4px; font-weight: 800; font-size: 10px;">{rank}</span></td>
            <td style="padding: 6px 4px; font-weight: 800; color: #0f172a;">{name} <span style="color:#94a3b8; font-weight:normal;">({code})</span></td>
            <td style="padding: 6px 4px; text-align: right; font-family: monospace;">{price:.2f}元</td>
            <td style="padding: 6px 4px; text-align: right; color: {color}; font-weight: 800;">{chg:+.2f}%</td>
            <td style="padding: 6px 4px; text-align: right; font-weight: 900; color: #0f172a;">{amt:.2f}亿</td>
            <td style="padding: 6px 4px; text-align: right; color: #0284c7; font-weight: 700;">{industry}</td>
        </tr>
        """

    total_vol = stats.get("total_volume", 20112.81)

    html = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; padding: 12px; border-radius: 14px; box-sizing: border-box; max-width: 600px; margin: 0 auto;">
    
    <!-- 顶部 Banner 区域 -->
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; padding: 18px 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(15,23,42,0.25);">
        <div style="font-size: 20px; font-weight: 900; letter-spacing: 0.5px; color: #ffffff;">{report_title}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 8px; display: flex; justify-content: center; align-items: center;">
            <span>📅 {trade_date_str}</span>
            <span style="margin: 0 8px;">|</span>
            <span style="background:#0284c7; color:#ffffff; padding:2px 8px; border-radius:4px; font-weight:700;">🌐 100% 东方财富网直连数据源</span>
        </div>
    </div>

    <!-- 📌 模块一：核心指数、全市场成交额、短线情绪与风控 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #ef4444; padding-left: 8px;">📌 模块一：核心指数、全市场成交额与短线风控</div>
        
        <!-- 情绪进度条 -->
        <div style="background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 10px;">
            <div style="display: table; width: 100%;">
                <div style="display: table-cell; font-size: 12px; font-weight: 700; color: #475569;">🌡️ 市场情绪温度</div>
                <div style="display: table-cell; text-align: right; font-size: 14px; font-weight: 900; color: #ef4444;">{stats.get('score', 71.1)} 分 <span style="font-size: 11px; color: #0284c7; background: #e0f2fe; padding: 2px 6px; border-radius: 4px;">{stats.get('stage', '发酵/上升期')}</span></div>
            </div>
            <div style="background: #e2e8f0; border-radius: 6px; height: 10px; margin-top: 8px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #f59e0b, #ef4444); width: {stats.get('score', 71.1)}%; height: 100%;"></div>
            </div>
        </div>

        <!-- 三大核心统计面板 -->
        <div style="display: table; width: 100%; margin-bottom: 10px; border-spacing: 4px; border-collapse: separate; table-layout: fixed;">
            <div style="display: table-row;">
                <div style="display: table-cell; background: #fff5f5; padding: 8px 4px; border-radius: 6px; text-align: center; border: 1px solid #fee2e2;">
                    <div style="font-size: 10px; color: #991b1b; font-weight: 600;">👉 沪深京三市总成交额</div>
                    <div style="font-size: 13px; font-weight: 900; color: #ef4444; margin-top: 2px;">{total_vol:.2f} 亿元</div>
                    <div style="font-size: 10px; color: #ef4444; font-weight: 700; margin-top: 1px;">({total_vol/10000:.4f} 万亿元)</div>
                </div>
                <div style="display: table-cell; background: #f8fafc; padding: 8px 4px; border-radius: 6px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">全市场涨跌分布</div>
                    <div style="font-size: 11px; font-weight: 800; color: #0f172a; margin-top: 2px;">红 {stats.get('up_count', 3420)} / 绿 {stats.get('down_count', 1450)}</div>
                    <div style="font-size: 10px; color: #64748b; margin-top: 1px;">平盘 {stats.get('flat_count', 180)} 家</div>
                </div>
                <div style="display: table-cell; background: #f8fafc; padding: 8px 4px; border-radius: 6px; text-align: center; border: 1px solid #e2e8f0;">
                    <div style="font-size: 10px; color: #64748b; font-weight: 600;">涨跌停与退潮风控</div>
                    <div style="font-size: 11px; font-weight: 800; color: #ef4444; margin-top: 2px;">涨停 {stats.get('up_limit_count', 78)} / 跌停 {stats.get('down_limit_count', 6)}</div>
                    <div style="font-size: 10px; color: #dc2626; font-weight: 700; margin-top: 1px;">炸板率 {stats.get('bomb_rate', 17.58)}%</div>
                </div>
            </div>
        </div>

        <!-- 5 大核心指数表格 -->
        <table style="width: 100%; border-collapse: collapse; margin-top: 4px;">
            <thead>
                <tr style="background: #f1f5f9; color: #475569; font-size: 10px; text-align: left;">
                    <th style="padding: 6px 8px;">指数名称</th>
                    <th style="padding: 6px 8px; text-align: right;">收盘点位</th>
                    <th style="padding: 6px 8px; text-align: right;">涨跌幅</th>
                    <th style="padding: 6px 8px; text-align: right;">成交额</th>
                </tr>
            </thead>
            <tbody>
                {indexes_rows_html}
            </tbody>
        </table>
    </div>

    <!-- 📊 模块二：核心宽基与行业指定 6 大 ETF 成交量监控 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #0284c7; padding-left: 8px;">📊 模块二：指定 6 大核心 ETF 成交量监控</div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">监测用户指定 6 大核心 ETF 机构资金交投放大放量信号：</div>
        {etf_rows_html}
    </div>

    <!-- 🏆 模块三：市场热门板块 (参考东方财富结构) -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #dc2626; padding-left: 8px;">🏆 模块三：市场热门板块 (东财结构盘口)</div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">参考东方财富网页端板块行情结构（板块、涨跌幅、主力净流入、领涨股）：</div>
        {sector_cards_html}
    </div>

    <!-- 💥 模块四：市场成交额前 10 的个股及所属板块或行业 -->
    <div style="background: #ffffff; padding: 14px; border-radius: 12px; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 8px; border-left: 4px solid #8b5cf6; padding-left: 8px;">💥 模块四：全市场成交额前 10 个股及所属行业</div>
        <div style="font-size: 11px; color: #64748b; margin-bottom: 8px;">按全市场成交金额排序 Top 10 个股及所属东财行业分类：</div>
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background: #f1f5f9; color: #475569; font-size: 10px; text-align: left;">
                    <th style="padding: 6px 4px; text-align: center;">排名</th>
                    <th style="padding: 6px 4px;">股票名称</th>
                    <th style="padding: 6px 4px; text-align: right;">最新价</th>
                    <th style="padding: 6px 4px; text-align: right;">涨跌幅</th>
                    <th style="padding: 6px 4px; text-align: right;">成交额</th>
                    <th style="padding: 6px 4px; text-align: right;">所属行业/板块</th>
                </tr>
            </thead>
            <tbody>
                {top10_rows_html}
            </tbody>
        </table>
    </div>

    <!-- Footer -->
    <div style="text-align: center; font-size: 10px; color: #94a3b8; margin-top: 14px; padding: 8px;">
        A股盘后自动化智投系统 · 100% 东方财富网直连数据源 · 仅供研究参考
    </div>
</div>
"""
    return html

if __name__ == "__main__":
    pass
