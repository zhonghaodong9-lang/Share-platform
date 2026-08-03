import os
import logging
import requests
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

INDUSTRY_LEADERS = {
    "AI与算力": "中际旭创、新易盛、天孚通信、寒武纪、工业富联",
    "半导体与集成电路": "北方华创、中芯国际、海光信息、兆易创新、长电科技",
    "机器人与具身智能": "三花智控、鸣志电器、绿的谐波、五洲新春",
    "低空经济与飞行汽车": "万丰奥威、宗申动力、中信海直、莱斯信息、深城交",
    "新能源与电池": "宁德时代、阳光电源、亿纬锂能、当升科技、赣锋锂业",
    "汽车与智慧出行": "比亚迪、赛力斯、长安汽车、江淮汽车、德赛西威",
    "医药与创新药": "恒瑞医药、百济神州、药明康德、科伦药业、迈瑞医疗",
    "军工与商业航天": "航天电子、中航沈飞、中国卫星、航天动力、上海瀚讯",
    "消费与电子": "立讯精密、歌尔股份、工业富联、传音控股、蓝思科技",
    "大金融与中字头": "东方财富、同花顺、中信证券、中国平安、招商银行"
}

def analyze_hot_topics(premarket_news):
    """
    分析盘前热点新闻，按行业/题材进行聚合，提炼利好/利空方向、影响程度与代表标的
    """
    topic_groups = {}
    
    for item in premarket_news:
        industries = item.get("industries", ["宏观政策与综合行业"])
        direction = item.get("direction", "🟢 利好")
        degree = item.get("degree", "🔥🔥 高")

        for ind in industries:
            if ind not in topic_groups:
                topic_groups[ind] = {
                    "industry": ind,
                    "news_count": 0,
                    "news_list": [],
                    "leaders": INDUSTRY_LEADERS.get(ind, "相关产业核心标的"),
                    "pos_cnt": 0,
                    "neg_cnt": 0,
                }
            topic_groups[ind]["news_count"] += 1
            topic_groups[ind]["news_list"].append(item)
            if "利好" in direction:
                topic_groups[ind]["pos_cnt"] += 1
            elif "利空" in direction:
                topic_groups[ind]["neg_cnt"] += 1

    # 判定各板块整体利好/利空方向与程度
    for ind, data in topic_groups.items():
        if data["pos_cnt"] >= data["neg_cnt"]:
            data["direction_tag"] = "🟢 重点利好"
            if data["news_count"] >= 3:
                data["impact_degree"] = "🔥🔥🔥 重大利好"
            else:
                data["impact_degree"] = "🔥🔥 强利好"
        else:
            data["direction_tag"] = "🔴 情绪防守/利空"
            data["impact_degree"] = "🔴 承压防守"

    # 排序按新闻数量取前 5 大热门行业
    sorted_topics = sorted(topic_groups.values(), key=lambda x: x["news_count"], reverse=True)[:5]
    
    # 提炼模块一的核心策略结构 (清晰结构化)
    top_ind_names = "、".join([t["industry"] for t in sorted_topics[:3]])
    
    structured_strategy = {
        "main_wind": f"**{top_ind_names}** 产业链获密集重磅催化，关注资金高低切换与核心中军动向。",
        "us_mapping": "隔夜美股与中概股科技板块表现强劲，中美硬科技映射传导逻辑持续强化。",
        "position": "建议保持 **5 ~ 7 成柔性仓位**，聚焦有业绩支撑的趋势中军，避免满仓赌博。",
        "discipline": "09:25 开盘集合竞价切忌盲目追高；观察 09:30~10:00 前 30 分钟成交量，放量承接方可确认真突破。"
    }

    return {
        "top_topics": sorted_topics,
        "strategy": structured_strategy,
        "total_news_cnt": len(premarket_news)
    }

if __name__ == "__main__":
    pass
