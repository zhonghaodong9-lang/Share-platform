import datetime
import re

def format_premarket_report(premarket_news, topic_analysis):
    """
    格式化生成《🌅 A股盘前行业热点与题材前瞻》 Markdown 与移动端排版报告
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    weekday_str = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
    
    top_topics = topic_analysis.get("top_topics", [])
    ai_insight = topic_analysis.get("ai_insight", "")
    total_cnt = topic_analysis.get("total_news_cnt", len(premarket_news))

    md_lines = []
    md_lines.append(f"# 🌅 A股盘前行业热点与题材前瞻 ({date_str} {weekday_str})")
    md_lines.append(f"> ⚡ **实时聚合**：隔夜及清晨重磅头条快讯 {total_cnt} 条 | **数据源**：新浪7x24 / 财联社 / 东方财富网\n")

    # 1. 盘前焦点与战略导向
    md_lines.append("## 核心盘前导向与博弈策略")
    md_lines.append(f"{ai_insight}\n")

    # 2. 重点关注行业题材 TOP
    md_lines.append("## 🔥 重点关注行业题材 TOP")
    for rank, topic in enumerate(top_topics, 1):
        ind_name = topic["industry"]
        impact = topic["impact_level"]
        leaders = topic["leaders"]
        news_cnt = topic["news_count"]
        
        md_lines.append(f"### {rank}. {impact} 【{ind_name}】 (聚合快讯 {news_cnt} 条)")
        md_lines.append(f"- 核心标的参考：`{leaders}`")
        md_lines.append("- 核心重磅催化：")
        for news in topic["news_list"][:2]:
            md_lines.append(f"  - [{news.get('source')}] **{news.get('title')}** ({news.get('time', '')})")
        md_lines.append("")

    # 3. 隔夜及清晨精选头条新闻
    md_lines.append("## 📰 隔夜与清晨重磅头条精选")
    for news in premarket_news[:10]:
        title = news.get("title", "")
        content = news.get("content", title)
        source = news.get("source", "7x24快讯")
        time_str = news.get("time", "")
        industries = " / ".join(news.get("industries", ["综合"]))
        
        md_lines.append(f"#### 🔹 [{source}] {title}")
        md_lines.append(f"*发布时间*: `{time_str}` | *关联行业*: `{industries}`")
        if content and len(content) > len(title):
            md_lines.append(f"> {content[:120]}...\n")
        else:
            md_lines.append("")

    # 4. 盘前风险提示
    md_lines.append("## ⚠️ 盘前操作与风控提醒")
    md_lines.append("1. **开盘竞价陷阱**：严防无业绩支撑概念股高开派发，避免在 09:25 开盘集合竞价盲目追高。")
    md_lines.append("2. **量能确认原则**：观察 09:30~10:00 早盘前 30 分钟量能，若大盘缩量冲高，需谨防冲高回落风险。")
    md_lines.append("3. **主线高低切换**：关注资金从高位连板妖股向有业绩支撑的趋势中军板块切换。")
    md_lines.append("\n---\n*免责声明：本报告由智能选盘前自动化系统采集生成，仅供研究参考，不构成任何买卖建议。*")

    return "\n".join(md_lines)

if __name__ == "__main__":
    test_news = [
        {"title": "工信部推动大模型在工业制造业深度落地", "content": "工信部印发指导意见推进 AI 算力与基础设施建设...", "source": "新浪7x24", "time": "07:30", "industries": ["AI与算力"]},
        {"title": "固态电池样品测试通过，车企拟装车测试", "content": "多家巨头全固态电池获得突破...", "source": "东方财富", "time": "08:00", "industries": ["新能源与电池"]}
    ]
    test_analysis = {"top_topics": [{"industry": "AI与算力", "impact_level": "🔥 强利好", "leaders": "中际旭创、新易盛", "news_count": 1, "news_list": test_news[:1]}], "ai_insight": "盘前AI算力表现强势。"}
    print(format_premarket_report(test_news, test_analysis))
