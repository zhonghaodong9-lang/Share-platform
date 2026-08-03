import os
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import logging
import datetime
import requests
import re
from bs4 import BeautifulSoup

try:
    import akshare as ak
except ImportError:
    ak = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 核心行业热点关键词映射字典
INDUSTRY_KEYWORDS = {
    "AI与算力": ["AI", "算力", "大模型", "CPO", "光模块", "服务器", "芯片", "英伟达", "ChatGPT", "人工智能", "液冷", "Qwen"],
    "半导体与集成电路": ["半导体", "晶圆", "光刻机", "先进封装", "存储", "芯片", "中芯", "台积电", "ASML", "集成电路"],
    "机器人与具身智能": ["机器人", "人形机器人", "减速器", "丝杠", "伺服", "具身智能", "特斯拉Optimus"],
    "低空经济与飞行汽车": ["低空经济", "eVTOL", "无人机", "通航", "空域", "飞行汽车"],
    "新能源与电池": ["固态电池", "锂电池", "光伏", "风电", "储能", "钠电池", "特斯拉", "充电桩", "氢能", "电力", "电网"],
    "汽车与智慧出行": ["智能驾驶", "自动驾驶", "新能源汽车", "车联网", "华为智驾", "比亚迪", "小米汽车", "iPhone", "苹果"],
    "医药与创新药": ["创新药", "CXO", "减重药", "GLP-1", "医疗器械", "生物医药", "FDA", "肿瘤", "阿斯利康"],
    "军工与商业航天": ["商业航天", "卫星互联网", "千帆星座", "军工", "国防", "火箭", "低轨卫星", "美军", "月球"],
    "消费与电子": ["消费电子", "苹果", "折叠屏", "华为新机", "智能穿戴", "家电以旧换新", "消费"],
    "大金融与中字头": ["证券", "券商", "银行", "保险", "中字头", "国企改革", "央企", "互换便利", "分红", "国资委"]
}

POSITIVE_WORDS = ["突破", "大增", "新高", "印发", "规划", "上涨", "涨", "落地", "融资", "利好", "支持", "通过", "首构", "首发", "发布", "批准", "获批", "加码"]
NEGATIVE_WORDS = ["大跌", "跌", "下调", "警惕", "停职", "风险", "限缩", "亏损", "下滑", "受阻", "查处", "惩罚", "短缺", "严管", "关税", "禁令"]

def classify_industry(title_and_content: str):
    """根据关键词推断新闻所属的行业题材"""
    matched = []
    for ind, kw_list in INDUSTRY_KEYWORDS.items():
        for kw in kw_list:
            if kw.lower() in title_and_content.lower():
                matched.append(ind)
                break
    return matched if matched else ["宏观政策与综合行业"]

def analyze_news_sentiment(title_and_content: str):
    """分析新闻方向（利好/利空/中性）与影响程度"""
    pos_score = sum(1 for w in POSITIVE_WORDS if w in title_and_content)
    neg_score = sum(1 for w in NEGATIVE_WORDS if w in title_and_content)
    
    if pos_score > neg_score:
        direction = "🟢 利好"
    elif neg_score > pos_score:
        direction = "🔴 利空"
    else:
        direction = "⚪ 中性"

    # 判断影响程度
    if any(w in title_and_content for w in ["国务院", "工信部", "印发", "十五五", "重磅", "突破", "数亿元", "大跌", "涨近"]):
        degree = "🔥🔥🔥 极高"
    elif pos_score + neg_score >= 1:
        degree = "🔥🔥 高"
    else:
        degree = "⚡ 中"

    return direction, degree


def fetch_from_cls():
    """100% 调取 财联社 (https://www.cls.cn/) 真实数据"""
    cls_news = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.cls.cn/"
    }
    s = requests.Session()
    s.trust_env = False

    try:
        r_html = s.get("https://www.cls.cn/", headers=headers, timeout=6)
        r_html.encoding = "utf-8"
        soup = BeautifulSoup(r_html.text, "html.parser")
        for a in soup.find_all("a"):
            text = a.get_text(strip=True)
            href = a.get("href", "")
            if len(text) > 8 and ("/detail/" in href or "/telegraph" in href or "cls.cn" in href):
                if text not in [n["title"] for n in cls_news] and not any(kw in text for kw in ["APP", "关于我们", "下载"]):
                    full_url = href if href.startswith("http") else "https://www.cls.cn" + href
                    direction, degree = analyze_news_sentiment(text)
                    cls_news.append({
                        "title": text,
                        "content": text,
                        "time": datetime.datetime.now().strftime("%H:%M"),
                        "source": "财联社 (cls.cn)",
                        "url": full_url,
                        "industries": classify_industry(text),
                        "direction": direction,
                        "degree": degree
                    })
    except Exception as e:
        logging.warning(f"cls.cn HTML抓取: {e}")

    if ak is not None and len(cls_news) < 5:
        try:
            df_cls = ak.stock_info_global_cls()
            if df_cls is not None and not df_cls.empty:
                for idx, row in df_cls.head(15).iterrows():
                    content = str(row.get("内容", str(row.get("content", ""))))
                    time_str = str(row.get("发布时间", str(row.get("time", ""))))
                    title = content[:45] + "..." if len(content) > 45 else content
                    if content and title not in [n["title"] for n in cls_news]:
                        direction, degree = analyze_news_sentiment(content)
                        cls_news.append({
                            "title": title,
                            "content": content,
                            "time": time_str,
                            "source": "财联社 (cls.cn)",
                            "url": "https://www.cls.cn/telegraph",
                            "industries": classify_industry(content),
                            "direction": direction,
                            "degree": degree
                        })
        except Exception as e:
            logging.warning(f"cls.cn AkShare: {e}")

    logging.info(f"✅ [财联社 cls.cn] 成功调取 {len(cls_news)} 条真实新闻")
    return cls_news


def fetch_from_eastmoney():
    """100% 调取 东方财富网 (https://www.eastmoney.com/default.html) 真实数据"""
    em_news = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.eastmoney.com/default.html"
    }
    s = requests.Session()
    s.trust_env = False

    try:
        r_em = s.get("https://www.eastmoney.com/default.html", headers=headers, timeout=6)
        r_em.encoding = "utf-8"
        soup_em = BeautifulSoup(r_em.text, "html.parser")
        
        for a in soup_em.find_all("a", href=re.compile(r"eastmoney\.com/a/\d+")):
            title = a.get_text(strip=True)
            href = a.get("href", "")
            if len(title) > 8 and title not in [n["title"] for n in em_news]:
                direction, degree = analyze_news_sentiment(title)
                em_news.append({
                    "title": title,
                    "content": title,
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "source": "东方财富网 (eastmoney.com)",
                    "url": href,
                    "industries": classify_industry(title),
                    "direction": direction,
                    "degree": degree
                })

        if len(em_news) < 10:
            em_api = "https://np-fastnews.eastmoney.com/api/Client/GetNewsList?limit=20&page=1&type=0"
            r_api = s.get(em_api, headers=headers, timeout=6)
            if r_api.status_code == 200:
                res_data = r_api.json()
                items = res_data.get("data", {}).get("news_list", []) or res_data.get("data", [])
                for item in items:
                    t = item.get("title", "") or item.get("digest", "")
                    show_time = item.get("show_time", "")
                    if t and t not in [n["title"] for n in em_news]:
                        direction, degree = analyze_news_sentiment(t + item.get("digest", ""))
                        em_news.append({
                            "title": t,
                            "content": item.get("digest", t),
                            "time": show_time,
                            "source": "东方财富网 (eastmoney.com)",
                            "url": "https://kuaixun.eastmoney.com/",
                            "industries": classify_industry(t),
                            "direction": direction,
                            "degree": degree
                        })
    except Exception as e:
        logging.warning(f"eastmoney.com 抓取异常: {e}")

    logging.info(f"✅ [东方财富网 eastmoney.com] 成功调取 {len(em_news)} 条真实新闻")
    return em_news


def fetch_from_10jqka():
    """100% 调取 同花顺 (https://www.10jqka.com.cn/) 真实数据"""
    ths_news = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.10jqka.com.cn/"
    }
    s = requests.Session()
    s.trust_env = False

    try:
        r_ths = s.get("https://news.10jqka.com.cn/", headers=headers, timeout=6)
        content_text = r_ths.content.decode("gbk", errors="ignore")
        soup_ths = BeautifulSoup(content_text, "html.parser")
        
        for a in soup_ths.find_all("a", href=re.compile(r"10jqka\.com\.cn/\d+/\w+")):
            title = a.get_text(strip=True)
            href = a.get("href", "")
            if len(title) > 8 and not any(kw in title for kw in ["登录", "注册", "软件", "App", "同花顺", "首页", "服务", "下载"]):
                if title not in [n["title"] for n in ths_news]:
                    direction, degree = analyze_news_sentiment(title)
                    ths_news.append({
                        "title": title,
                        "content": title,
                        "time": datetime.datetime.now().strftime("%H:%M"),
                        "source": "同花顺 (10jqka.com.cn)",
                        "url": href,
                        "industries": classify_industry(title),
                        "direction": direction,
                        "degree": degree
                    })
    except Exception as e:
        logging.warning(f"10jqka.com.cn 抓取异常: {e}")

    logging.info(f"✅ [同花顺 10jqka.com.cn] 成功调取 {len(ths_news)} 条真实新闻")
    return ths_news


def fetch_premarket_news(top_n=20):
    """
    综合三大网站（财联社、东方财富、同花顺）资讯，通过交叉交错混合算法生成前 20 条热点新闻列表
    """
    logging.info("🌐 正在从 [财联社 cls.cn]、[东方财富 eastmoney.com]、[同花顺 10jqka.com.cn] 三大网站交叉抓取综合资讯...")
    
    cls_data = fetch_from_cls()
    em_data = fetch_from_eastmoney()
    ths_data = fetch_from_10jqka()

    combined_news = []
    seen_titles = set()
    max_len = max(len(cls_data), len(em_data), len(ths_data))

    for i in range(max_len):
        for data_source in [cls_data, em_data, ths_data]:
            if i < len(data_source):
                item = data_source[i]
                clean_title = re.sub(r'[^\w\u4e00-\u9fa5]', '', item['title'][:25])
                if clean_title not in seen_titles and len(clean_title) > 5:
                    seen_titles.add(clean_title)
                    combined_news.append(item)
                    if len(combined_news) >= top_n:
                        break
        if len(combined_news) >= top_n:
            break

    logging.info(f"🎉 已成功综合三大网站资讯，精选输出 TOP {len(combined_news[:top_n])} 盘前热点新闻！")
    return combined_news[:top_n]


if __name__ == "__main__":
    import pprint
    pprint.pprint(fetch_premarket_news(20))
