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
print("=== 头部 500 字符 ===")
print(html[:500])
print("\n=== 19000~21000 字符 (模块四所在区域) ===")
print(html[19000:21000])
print("\n=== 尾部 500 字符 ===")
print(html[-500:])
