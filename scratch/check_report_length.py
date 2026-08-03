import sys
sys.path.insert(0, ".")

from data_fetchers import fetch_market_overview, fetch_money_flow_data, fetch_overseas_market_data, fetch_research_reports
from analyzers import analyze_sentiment, analyze_us_china_mapping, generate_ai_analysis
from formatters import format_daily_report

m = fetch_market_overview()
f = fetch_money_flow_data()
o = fetch_overseas_market_data()
r = fetch_research_reports()
s = analyze_sentiment(m)
mp = analyze_us_china_mapping(o, f)
ai = generate_ai_analysis(m, f, o, r, s, mp)

html = format_daily_report(m, f, o, r, s, mp, ai)
print("HTML 报告总字符长度:", len(html))
print("HTML 报告总字节数:", len(html.encode('utf-8')))

idx4 = html.find("💥 模块四")
print("模块四起始字符位置:", idx4)
