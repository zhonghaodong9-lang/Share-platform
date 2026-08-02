import logging

# 中美板块映射规则库
MAPPING_DICTIONARY = [
    {
        "us_driver": "美股AI算力/半导体 (英伟达/SOX/博通)",
        "a_share_sectors": ["CPO概念", "算力概念", "PCB", "半导体", "集成电路"],
        "logic": "美股AI巨头资本开支强劲 → 驱动A股光模块(CPO)、印制电路板(PCB)与芯片封测算力链。"
    },
    {
        "us_driver": "美股特斯拉/智驾 (Tesla/自动驾驶)",
        "a_share_sectors": ["人形机器人", "智能驾驶", "汽车零部件", "减速器"],
        "logic": "特斯拉Robotaxi与FSD进展 → 映射A股机器人关节、智驾传感器与车路云产业链。"
    },
    {
        "us_driver": "美股医药生物 (礼来/诺和诺德/GLP-1)",
        "a_share_sectors": ["创新药", "CXO", "减肥药", "生物制品"],
        "logic": "海外重磅减肥药与慢病创新药业绩大超预期 → 驱动A股CXO代工与自主创新药标的估值修复。"
    },
    {
        "us_driver": "美股消费电子 (苹果/微软/Meta)",
        "a_share_sectors": ["果链概念", "消费电子", "智能穿戴", "眼镜概念"],
        "logic": "苹果AI智能硬件新品与Meta眼镜发布 → 带动A股消费电子零部件与组装龙头。"
    }
]

def analyze_us_china_mapping(overseas_data, money_flow_data):
    """分析隔夜美股热点与今日 A 股主线板块的映射传导逻辑"""
    sox_chg = overseas_data.get("sox_change", 0.0)
    inflow_sectors = money_flow_data.get("sector_flow", {}).get("inflow", [])
    top_sector_names = [s.get("name", "") for s in inflow_sectors]

    mapping_results = []

    for rule in MAPPING_DICTIONARY:
        driver = rule["us_driver"]
        mapped_a_sectors = rule["a_share_sectors"]
        
        hit_sectors = [s for s in mapped_a_sectors if any(s in top for top in top_sector_names)]
        
        if hit_sectors:
            status = "🔥 强共振联动（隔夜美股热点成功传导至 A 股主线）"
        elif "半导体" in driver and sox_chg > 1.0:
            status = "👀 溢出跟涨潜在标的（隔夜SOX走强，A股相关板块蓄势）"
        else:
            status = "⚖️ 结构性分化/独立走出自身节奏"

        mapping_results.append({
            "driver": driver,
            "mapped_sectors": "、".join(mapped_a_sectors),
            "hit_sectors": "、".join(hit_sectors) if hit_sectors else "无显现",
            "status": status,
            "logic": rule["logic"]
        })

    return {
        "sox_change": sox_chg,
        "a50_change": overseas_data.get("a50_change", 0.0),
        "cnh_rate": overseas_data.get("cnh_rate", 7.18),
        "mapping_details": mapping_results,
    }

if __name__ == "__main__":
    dummy_overseas = {"sox_change": 1.5, "a50_change": 0.4, "cnh_rate": 7.185}
    dummy_flow = {"sector_flow": {"inflow": [{"name": "CPO概念"}, {"name": "人形机器人"}]}}
    print(analyze_us_china_mapping(dummy_overseas, dummy_flow))
