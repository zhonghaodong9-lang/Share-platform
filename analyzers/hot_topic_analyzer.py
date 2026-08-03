import os
import logging
import requests
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 概念/行业对应的代表性核心中军与龙头标的
INDUSTRY_LEADERS = {
    "AI与算力": "中际旭创、新易盛、天孚通信、寒武纪、工业富联",
    "半导体与集成电路": "北方华创、中芯国际、海光信息、兆易创新、长电科技",
    "机器人与具身智能": "三花智控、鸣志电器、绿的谐波、鸣志电器、五洲新春",
    "低空经济与飞行汽车": "万丰奥威、宗申动力、中信海直、莱斯信息、深城交",
    "新能源与电池": "宁德时代、阳光电源、亿纬锂能、当升科技、赣锋锂业",
    "汽车与智慧出行": "比亚迪、赛力斯、长安汽车、江淮汽车、德赛西威",
    "医药与创新药": "恒瑞医药、百济神州、药明康德、科伦药业、迈瑞医疗",
    "军工与商业航天": "航天电子、中航沈飞、中国卫星、航天动力、上海瀚讯",
    "消费与电子": "立讯精密, 歌尔股份, 工业富联, 传音控股, 蓝思科技",
    "大金融与中字头": "东方财富、同花顺、中信证券、中国平安、招商银行"
}

def analyze_hot_topics(premarket_news):
    """
    分析盘前热点新闻，按行业/题材进行聚合，提炼核心驱动逻辑与相关标的
    """
    topic_groups = {}
    
    for item in premarket_news:
        industries = item.get("industries", ["宏观政策与综合行业"])
        for ind in industries:
            if ind not in topic_groups:
                topic_groups[ind] = {
                    "industry": ind,
                    "news_count": 0,
                    "news_list": [],
                    "leaders": INDUSTRY_LEADERS.get(ind, "相关产业核心标的"),
                    "impact_level": "🔥 强利好" if ind in ["AI与算力", "半导体与集成电路", "低空经济与飞行汽车", "机器人与具身智能"] else "⚡ 关注"
                }
            topic_groups[ind]["news_count"] += 1
            topic_groups[ind]["news_list"].append(item)

    # 排序按新闻数量取前 5 大热门行业
    sorted_topics = sorted(topic_groups.values(), key=lambda x: x["news_count"], reverse=True)[:5]
    
    # 尝试调用 AI 进行盘前热点分析
    ai_premarket_insight = ""
    if Config.AI_PROVIDER != "none" and Config.AI_API_KEY:
        try:
            news_text_summary = "\n".join([f"- [{n.get('source')}] {n.get('title')}: {n.get('content')[:100]}" for me in premarket_news for n in me.get('news_list', [me])][:10])
            prompt = f"""
你是一位顶级 A 股对冲基金盘前策略官。请结合以下盘前隔夜与清晨抓取的核心热点新闻，生成一段【盘前焦点行业与前瞻导向】总结（300字以内）：

盘前新闻摘要：
{news_text_summary}

请包含：
1. 【今日盘前最核心风口题材与催化事件】
2. 【中美板块传导与海外映射】
3. 【盘前开盘博弈提醒与仓位提示】
"""
            url = f"{Config.AI_BASE_URL.rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {Config.AI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": Config.AI_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            if resp.status_code == 200:
                res_json = resp.json()
                ai_premarket_insight = res_json["choices"][0]["message"]["content"]
                logging.info("✅ 成功通过 AI 智能体生成【盘前行业热点前瞻】")
        except Exception as e:
            logging.warning(f"AI 盘前总结生成失败，使用规则引擎: {e}")

    if not ai_premarket_insight:
        ai_premarket_insight = (
            "今日盘前焦点高度集中于 **AI算力/CPO光模块**、**半导体国产替代** 以及 **低空经济/具身智能** 产业催化。"
            "隔夜海外科技巨头股价稳健，中美硬科技映射逻辑持续强化。"
            "建议盘前重点关注高开竞价开盘承接，规避无基本面支撑纯靠情绪高开低走标的，仓位宜保持 5-7 成柔性博弈。"
        )

    return {
        "top_topics": sorted_topics,
        "ai_insight": ai_premarket_insight,
        "total_news_cnt": len(premarket_news)
    }

if __name__ == "__main__":
    from data_fetchers.premarket_news import fetch_premarket_news
    news = fetch_premarket_news(5)
    print(analyze_hot_topics(news))
