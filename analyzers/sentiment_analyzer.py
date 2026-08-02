import logging

def analyze_sentiment(base_data):
    """计算短线情绪温度与判定情绪周期"""
    stats = base_data.get("stats", {})
    limit_info = base_data.get("limit_info", {})

    up_count = stats.get("up_count", 0)
    down_count = stats.get("down_count", 0)
    total_stocks = up_count + down_count + stats.get("flat_count", 0)
    
    up_ratio = (up_count / total_stocks * 100) if total_stocks > 0 else 50.0
    bomb_rate = limit_info.get("bomb_rate", 20.0)
    max_height = limit_info.get("max_height", 1)
    zt_count = limit_info.get("zt_count", 0)
    dt_count = stats.get("down_limit_count", 0)

    # 综合情绪打分 (0 ~ 100)
    score = 50.0
    # 上涨比例贡献 (-20 ~ +20)
    score += (up_ratio - 50) * 0.4
    # 涨停家数贡献
    score += min(zt_count * 0.3, 20)
    # 炸板率扣分
    score -= min(bomb_rate * 0.4, 15)
    # 跌停扣分
    score -= min(dt_count * 1.5, 20)
    # 连板高度加分
    score += min(max_height * 2.0, 10)

    sentiment_score = max(0.0, min(100.0, round(score, 1)))

    # 情绪周期阶段判定
    if sentiment_score >= 80:
        stage = "高潮期 (注意情绪高位分歧风险)"
        advice = "市场情绪极其高涨，跟风追高需谨慎，防范次日冲高回落分歧。"
    elif sentiment_score >= 60:
        stage = "发酵/上升期 (主线轮动做多)"
        advice = "市场赚钱效应良好，资金抱团主线板块，可顺势布局领涨龙头。"
    elif sentiment_score >= 40:
        stage = "分歧/震荡期 (结构性行情)"
        advice = "多空博弈激烈，热点切换频繁，建议收缩仓位，低吸高抛。"
    elif sentiment_score >= 20:
        stage = "修复/试错期 (等待止跌信号)"
        advice = "市场处于冰点后的修复试错阶段，密切关注率先反弹的先锋板块。"
    else:
        stage = "冰点期 (杀跌情绪出清)"
        advice = "恐慌盘加速出清，防守为主，等待市场底部企稳与量能释放。"

    return {
        "score": sentiment_score,
        "stage": stage,
        "advice": advice,
        "up_ratio": round(up_ratio, 1),
        "bomb_rate": bomb_rate,
        "max_height": max_height,
    }

if __name__ == "__main__":
    dummy_data = {
        "stats": {"up_count": 3200, "down_count": 1500, "flat_count": 200, "down_limit_count": 3},
        "limit_info": {"zt_count": 65, "bomb_rate": 14.5, "max_height": 5}
    }
    print(analyze_sentiment(dummy_data))
