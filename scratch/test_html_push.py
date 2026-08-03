import os
import requests

os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

app_token = 'AT_c90wajU5mczqv3HhaYe9RpopYDYHjGta'
uid = 'UID_6KxduFL4ygE3cJVrgOfmzbrN4t8F'

html_content = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f1f5f9; padding: 12px; border-radius: 12px;">
    <!-- Header -->
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; padding: 16px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="font-size: 20px; font-weight: 800; letter-spacing: 0.5px;">📈 A股盘后深度智投日报</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">2026年08月02日 盘后专业复盘</div>
    </div>

    <!-- Metric Grid -->
    <div style="display: table; width: 100%; margin-top: 10px; border-spacing: 6px; border-collapse: separate;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 50%; background: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); text-align: center;">
                <div style="font-size: 11px; color: #64748b; font-weight: 600;">两市成交额</div>
                <div style="font-size: 16px; font-weight: 800; color: #0f172a; margin-top: 2px;">18,180 亿</div>
                <div style="font-size: 10px; color: #10b981; margin-top: 2px;">放量 +15.2%</div>
            </div>
            <div style="display: table-cell; width: 50%; background: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); text-align: center;">
                <div style="font-size: 11px; color: #64748b; font-weight: 600;">涨跌分布</div>
                <div style="font-size: 15px; font-weight: 800; color: #ef4444; margin-top: 2px;">3420 涨 / 1450 跌</div>
                <div style="font-size: 10px; color: #64748b; margin-top: 2px;">赚钱效应 70.2%</div>
            </div>
        </div>
    </div>

    <!-- Sentiment Card -->
    <div style="background: #ffffff; padding: 12px; border-radius: 10px; margin-top: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="display: table; width: 100%;">
            <div style="display: table-cell; text-align: left; font-size: 13px; font-weight: 700; color: #334155;">🌡️ 市场情绪温度</div>
            <div style="display: table-cell; text-align: right; font-size: 14px; font-weight: 800; color: #ef4444;">63.1 分 (发酵期)</div>
        </div>
        <div style="background: #e2e8f0; border-radius: 6px; height: 10px; margin-top: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #f59e0b, #ef4444); width: 63.1%; height: 100%;"></div>
        </div>
        <div style="font-size: 11px; color: #475569; background: #f8fafc; padding: 8px; border-radius: 6px; margin-top: 8px; border-left: 3px solid #ef4444;">
            💡 <b>操盘提醒</b>：市场赚钱效应良好，资金抱团主线板块，可顺势布局领涨龙头。
        </div>
    </div>

    <!-- Core Indices Table -->
    <div style="background: #ffffff; padding: 12px; border-radius: 10px; margin-top: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 8px;">📊 核心大盘指数</div>
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
            <thead>
                <tr style="background: #f1f5f9; color: #475569; text-align: left;">
                    <th style="padding: 6px 8px; border-radius: 4px 0 0 4px;">指数名称</th>
                    <th style="padding: 6px 8px; text-align: right;">最新点位</th>
                    <th style="padding: 6px 8px; text-align: right; border-radius: 0 4px 4px 0;">涨跌幅</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 8px; font-weight: 700; color: #1e293b;">上证指数</td>
                    <td style="padding: 8px; text-align: right; font-family: monospace;">3832.26</td>
                    <td style="padding: 8px; text-align: right; font-weight: 700; color: #ef4444;">+0.72%</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9; background: #fafafa;">
                    <td style="padding: 8px; font-weight: 700; color: #1e293b;">深证成指</td>
                    <td style="padding: 8px; text-align: right; font-family: monospace;">13578.93</td>
                    <td style="padding: 8px; text-align: right; font-weight: 700; color: #ef4444;">+2.21%</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 8px; font-weight: 700; color: #1e293b;">创业板指</td>
                    <td style="padding: 8px; text-align: right; font-family: monospace;">3343.96</td>
                    <td style="padding: 8px; text-align: right; font-weight: 700; color: #ef4444;">+3.06%</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: 700; color: #1e293b;">科创 50</td>
                    <td style="padding: 8px; text-align: right; font-family: monospace;">1635.96</td>
                    <td style="padding: 8px; text-align: right; font-weight: 700; color: #ef4444;">+2.99%</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Top Sectors & Money Flow Cards -->
    <div style="background: #ffffff; padding: 12px; border-radius: 10px; margin-top: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 8px;">💰 领涨/主力净流入行业板块 Top 5</div>
        
        <div style="background: #fff5f5; padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #ef4444; display: table; width: 100%;">
            <div style="display: table-cell; font-size: 12px; font-weight: 700; color: #991b1b;">1. CPO 概念</div>
            <div style="display: table-cell; text-align: right; font-size: 12px; font-weight: 800; color: #ef4444;">+4.52%</div>
        </div>
        <div style="background: #fff5f5; padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #ef4444; display: table; width: 100%;">
            <div style="display: table-cell; font-size: 12px; font-weight: 700; color: #991b1b;">2. 半导体</div>
            <div style="display: table-cell; text-align: right; font-size: 12px; font-weight: 800; color: #ef4444;">+3.85%</div>
        </div>
        <div style="background: #fff5f5; padding: 8px 10px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #ef4444; display: table; width: 100%;">
            <div style="display: table-cell; font-size: 12px; font-weight: 700; color: #991b1b;">3. 人形机器人</div>
            <div style="display: table-cell; text-align: right; font-size: 12px; font-weight: 800; color: #ef4444;">+3.12%</div>
        </div>
    </div>

    <!-- US-China Mapping Card -->
    <div style="background: #ffffff; padding: 12px; border-radius: 10px; margin-top: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 8px;">🌐 中美板块逻辑映射</div>
        <div style="background: #f0f9ff; padding: 8px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #0284c7; font-size: 11px;">
            <span style="font-weight: 700; color: #0369a1;">美股 AI算力 (英伟达/SOX)</span> ➔ 驱动 A股 <span style="background: #e0f2fe; color: #0369a1; padding: 2px 4px; border-radius: 4px; font-weight: 700;">CPO / 半导体</span> <span style="color: #ef4444; font-weight: 700;">(🔥 强共振)</span>
        </div>
        <div style="background: #f0f9ff; padding: 8px; border-radius: 6px; border-left: 3px solid #0284c7; font-size: 11px;">
            <span style="font-weight: 700; color: #0369a1;">美股 特斯拉 (Tesla/智驾)</span> ➔ 驱动 A股 <span style="background: #e0f2fe; color: #0369a1; padding: 2px 4px; border-radius: 4px; font-weight: 700;">人形机器人</span> <span style="color: #ef4444; font-weight: 700;">(🔥 强共振)</span>
        </div>
    </div>
</div>
"""

data = {
    'appToken': app_token,
    'uids': [uid],
    'content': html_content,
    'summary': 'A股盘后智投专业 UI 界面测试',
    'contentType': 2
}

r = requests.post('https://wxpusher.zjiecode.com/api/send/message', json=data)
print('HTML Push Status:', r.status_code, r.text)
