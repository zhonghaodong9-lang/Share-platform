import datetime

def format_premarket_report(premarket_news, topic_analysis):
    """
    100% 参照【智能选】系统 UI 视觉规范设计的全量升级排版模版
    针对模块一、模块二、模块三深度优化：
    - 模块一：清晰结构化拆解（最强风口、外围传导、建议仓位、博弈纪律）
    - 模块二：标注利好/利空方向、影响程度与对应中军标的
    - 模块三：每条新闻均清晰列出利好/利空方向、影响程度与对应板块
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    weekday_str = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
    
    top_topics = topic_analysis.get("top_topics", [])
    strategy = topic_analysis.get("strategy", {})

    # 1. 模块一：核心盘前导向与博弈策略 (极简清晰卡片)
    strategy_html = f"""<div style="background:#ffffff;padding:12px;border-radius:8px;margin-top:8px;border:1px solid #e2e8f0;">
<div style="font-size:14px;font-weight:900;color:#0f172a;border-left:4px solid #dc2626;padding-left:8px;margin-bottom:10px;">📌 模块一：核心盘前导向与博弈策略</div>
<div style="display:flex;flex-direction:column;gap:6px;font-size:12px;color:#334155;">

<div style="background:#fff1f2;padding:8px 10px;border-radius:6px;border:1px solid #fecdd3;">
  <span style="background:#dc2626;color:#ffffff;padding:2px 6px;border-radius:4px;font-size:10px;margin-right:6px;"><b style="color:#ffffff;">🎯 最强风口</b></span>
  <b>{strategy.get('main_wind', '')}</b>
</div>

<div style="background:#f0f9ff;padding:8px 10px;border-radius:6px;border:1px solid #bae6fd;">
  <span style="background:#0284c7;color:#ffffff;padding:2px 6px;border-radius:4px;font-size:10px;margin-right:6px;"><b style="color:#ffffff;">🌐 外围传导</b></span>
  <b>{strategy.get('us_mapping', '')}</b>
</div>

<div style="background:#fefce8;padding:8px 10px;border-radius:6px;border:1px solid #fef08a;">
  <span style="background:#ca8a04;color:#ffffff;padding:2px 6px;border-radius:4px;font-size:10px;margin-right:6px;"><b style="color:#ffffff;">💰 建议仓位</b></span>
  <b>{strategy.get('position', '')}</b>
</div>

<div style="background:#f0fdf4;padding:8px 10px;border-radius:6px;border:1px solid #bbf7d0;">
  <span style="background:#16a34a;color:#ffffff;padding:2px 6px;border-radius:4px;font-size:10px;margin-right:6px;"><b style="color:#ffffff;">🛡️ 博弈纪律</b></span>
  <b>{strategy.get('discipline', '')}</b>
</div>

</div>
</div>"""

    # 2. 模块二：重点关注行业题材 TOP (明确标注利好/利空方向与程度)
    topics_html = ""
    for rank, topic in enumerate(top_topics, 1):
        ind_name = topic["industry"]
        direction_tag = topic.get("direction_tag", "🟢 重点利好")
        impact_degree = topic.get("impact_degree", "🔥🔥 强利好")
        leaders = topic["leaders"]
        news_cnt = topic["news_count"]
        
        dir_bg = "#dcfce7" if "利好" in direction_tag else "#fee2e2"
        dir_c = "#15803d" if "利好" in direction_tag else "#dc2626"
        
        # 催化条目
        catalysts_html = ""
        for n in topic["news_list"][:2]:
            src = n.get("source", "资讯")
            title = n.get("title", "")
            t_str = n.get("time", "")
            n_dir = n.get("direction", "🟢 利好")
            src_bg = "#e0f2fe" if "财联社" in src else ("#fef3c7" if "东方财富" in src else "#dcfce7")
            src_c = "#0369a1" if "财联社" in src else ("#b45309" if "东方财富" in src else "#15803d")
            
            catalysts_html += f"""<div style="margin-top:4px;font-size:11px;color:#334155;">
  • <span style="background:{src_bg};color:{src_c};padding:1px 4px;border-radius:3px;font-size:10px;"><b style="color:{src_c};">{src}</b></span> <span style="font-size:10px;margin-right:4px;">[{n_dir}]</span> <b>{title[:45]}</b> <span style="color:#94a3b8;font-size:10px;">({t_str})</span>
</div>"""

        topics_html += f"""<div style="background:#ffffff;padding:8px 10px;margin-bottom:8px;border:1px solid #e2e8f0;border-left:4px solid #f97316;border-radius:6px;font-size:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div style="color:#0f172a;"><span style="background:#f97316;color:#ffffff;padding:1px 5px;border-radius:3px;font-size:10px;margin-right:4px;"><b style="color:#ffffff;">TOP {rank}</b></span><b style="color:#0f172a;font-size:13px;">{ind_name}</b></div>
<div><span style="background:{dir_bg};color:{dir_c};padding:2px 6px;border-radius:4px;font-size:11px;"><b style="color:{dir_c};">{direction_tag} · {impact_degree}</b></span></div>
</div>
<div style="margin-top:6px;font-size:11px;color:#475569;">
<div>中军核心标的: <span style="background:#f1f5f9;color:#0284c7;padding:1px 5px;border-radius:3px;"><b style="color:#0284c7;">{leaders}</b></span></div>
<div style="margin-top:4px;font-weight:700;color:#0f172a;">重磅催化事件:</div>
{catalysts_html}
</div>
</div>"""

    # 3. 模块三：三大官方网站热点新闻 TOP 20 (清晰标注方向、程度、对应板块)
    news_top20_html = ""
    for idx, news in enumerate(premarket_news[:20], 1):
        title = news.get("title", "")
        content = news.get("content", title)
        source = news.get("source", "综合资讯")
        time_str = news.get("time", "")
        industries = " / ".join(news.get("industries", ["综合"]))
        direction = news.get("direction", "🟢 利好")
        degree = news.get("degree", "🔥🔥 高")

        src_bg = "#e0f2fe" if "财联社" in source else ("#fef3c7" if "东方财富" in source else "#dcfce7")
        src_c = "#0369a1" if "财联社" in source else ("#b45309" if "东方财富" in source else "#15803d")
        rank_bg = "#dc2626" if idx <= 3 else "#64748b"
        
        dir_bg = "#dcfce7" if "利好" in direction else ("#fee2e2" if "利空" in direction else "#f1f5f9")
        dir_c = "#15803d" if "利好" in direction else ("#dc2626" if "利空" in direction else "#475569")

        digest = f"<div style=\"color:#64748b;font-size:11px;margin-top:4px;line-height:1.4;background:#f8fafc;padding:4px 6px;border-radius:4px;\">{content[:120]}...</div>" if content and len(content) > len(title) and content != title else ""

        news_top20_html += f"""<div style="background:#ffffff;padding:8px 10px;margin-bottom:6px;border:1px solid #e2e8f0;border-radius:6px;font-size:12px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div style="color:#0f172a;"><span style="background:{rank_bg};color:#ffffff;padding:1px 5px;border-radius:3px;font-size:10px;margin-right:4px;"><b style="color:#ffffff;">{idx}</b></span><b style="color:#0f172a;">{title}</b></div>
<div><span style="background:{dir_bg};color:{dir_c};padding:2px 5px;border-radius:3px;font-size:10px;"><b style="color:{dir_c};">{direction} ({degree})</b></span></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:4px;font-size:10px;color:#64748b;">
<div><span style="background:{src_bg};color:{src_c};padding:1px 4px;border-radius:3px;"><b style="color:{src_c};">{source}</b></span> · 对应板块: <span style="background:#e0f2fe;color:#0284c7;padding:1px 4px;border-radius:3px;"><b style="color:#0284c7;">{industries}</b></span></div>
<div>时间: <b>{time_str}</b></div>
</div>
{digest}
</div>"""

    # 全量 HTML 报告模版
    html_report = f"""<div style="font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#f8fafc;padding:8px;border-radius:10px;color:#0f172a;">
<div style="background:linear-gradient(135deg,#0f172a,#1e293b);color:#ffffff;padding:12px;border-radius:8px;text-align:center;">
<div style="font-size:18px;font-weight:900;color:#ffffff;letter-spacing:1px;">🔥 热点资讯前瞻</div>
<div style="font-size:11px;color:#94a3b8;margin-top:4px;">📅 {date_str} {weekday_str} | 🌐 财联社 · 东方财富 · 同花顺 直连</div>
</div>

{strategy_html}

<div style="background:#ffffff;padding:10px;border-radius:8px;margin-top:8px;border:1px solid #e2e8f0;">
<div style="font-size:13px;font-weight:900;color:#0f172a;border-left:4px solid #f97316;padding-left:6px;margin-bottom:6px;">🔥 模块二：重点关注行业题材 TOP (含方向与程度)</div>
{topics_html}
</div>

<div style="background:#ffffff;padding:10px;border-radius:8px;margin-top:8px;border:1px solid #e2e8f0;">
<div style="font-size:13px;font-weight:900;color:#0f172a;border-left:4px solid #0284c7;padding-left:6px;margin-bottom:6px;">📰 模块三：三大官方网站盘前热点新闻 TOP 20 (含利好利空/程度/对应板块)</div>
{news_top20_html}
</div>

<div style="background:#ffffff;padding:10px;border-radius:8px;margin-top:8px;border:1px solid #e2e8f0;">
<div style="font-size:13px;font-weight:900;color:#0f172a;border-left:4px solid #059669;padding-left:6px;margin-bottom:6px;">⚠️ 模块四：盘前风控与交易纪律提醒</div>
<div style="font-size:11px;color:#475569;line-height:1.6;">
1. <b>竞价博弈纪律</b>：严禁在 09:25 盲目挂高价追高，防范无基本面题材高开低走开盘派发陷阱。<br>
2. <b>量能确认原则</b>：观察 09:30~10:00 前 30 分钟大盘成交量，放量拉升方可确认真突破。<br>
3. <b>主线高低切换</b>：关注资金从高位连板情绪妖股向有业绩支撑的行业中军板块切换。
</div>
</div>

<div style="text-align:center;font-size:10px;color:#94a3b8;margin-top:8px;">A股盘前自动化智投系统 · 财联社 · 东方财富 · 同花顺 100% 真实直连数据源</div>
</div>"""

    return html_report

if __name__ == "__main__":
    pass
