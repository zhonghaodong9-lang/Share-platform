import os
# 全局防代理异常配置
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import argparse
import datetime
import logging

from config import Config
from data_fetchers import (
    fetch_market_overview,
    fetch_money_flow_data,
    fetch_overseas_market_data,
    fetch_research_reports,
)
from analyzers import (
    analyze_sentiment,
    analyze_us_china_mapping,
    generate_ai_analysis,
)
from formatters import format_daily_report
from notifiers import push_all_channels

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_daily_review(should_save=True, should_push=True):
    """每日盘后复盘主任务流"""
    logging.info("🚀 启动 A股每日盘后自动化复盘智投系统...")

    # 1. 抓取各维数据
    logging.info("1/4 [数据采集] 正在获取大盘概览、资金流向、海外联动及券商研报...")
    market_data = fetch_market_overview()
    money_flow_data = fetch_money_flow_data()
    overseas_data = fetch_overseas_market_data()
    reports_data = fetch_research_reports()

    # 2. 规则与逻辑分析
    logging.info("2/4 [智投分析] 正在计算短线情绪温度、情绪周期及中美板块映射...")
    sentiment = analyze_sentiment(market_data)
    mapping = analyze_us_china_mapping(overseas_data, money_flow_data)

    # 3. AI / 智投引擎总结
    logging.info("3/4 [策略总结] 正在调用 AI/智投引擎生成复盘精要与操盘展望...")
    ai_summary = generate_ai_analysis(
        market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping
    )

    # 4. 格式化排版
    logging.info("4/4 [报告排版] 正在渲染机构风采 Markdown 复盘日报...")
    report_md = format_daily_report(
        market_data, money_flow_data, overseas_data, reports_data, sentiment, mapping, ai_summary
    )

    # 保存本地
    if should_save:
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        filepath = os.path.join(Config.OUTPUT_DIR, f"daily_review_{today_str}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report_md)
        logging.info(f"✅ 复盘日报已成功保存至本地文件: {filepath}")

    # 推送广播
    if should_push:
        logging.info("📡 正在广播推送至消息渠道...")
        push_results = push_all_channels(report_md)
        logging.info(f"推送完成: {push_results}")

    logging.info("🎉 每日盘后复盘任务执行结束！")
    return report_md

def main():
    parser = argparse.ArgumentParser(description="A股每日盘后自动化复盘与智投系统")
    parser.add_argument("--save", action="store_true", default=True, help="保存报告至本地")
    parser.add_argument("--push", action="store_true", default=True, help="推送到 Webhook/微信 渠道")
    parser.add_argument("--test", action="store_true", help="测试运行（仅打印报告预览）")

    args = parser.parse_args()

    if args.test:
        report = run_daily_review(should_save=False, should_push=False)
        print("\n================== 报告预览 ==================\n")
        print(report[:1500])
        print("\n=============================================\n")
    else:
        run_daily_review(should_save=args.save, should_push=args.push)

if __name__ == "__main__":
    main()
