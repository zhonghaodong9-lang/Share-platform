# 📈 A股专业级每日盘后自动复盘与智投系统

一个高度可定制、功能全面的 **A股每日盘后自动化复盘与智投分析系统**。系统不仅涵盖行情基本面与短线情绪，还深度融合了**微观资金流向（主力/机构/龙虎榜）**、**投行券商研报情报**以及**海外市场（美股/中概/汇率/A50）与中美板块映射关系**，支持通过飞书、钉钉、企业微信机器人及微信 WxPusher 广播推送报告。

---

## ✨ 核心特色与功能列表

1. **⚡ 全景数据采集**
   - **大盘指数与量能**：抓取上证、深证、创业板、科创50收盘价、涨跌幅及三市成交额对比。
   - **市场全景分布**：全场上涨/下跌家数、涨停/跌停家数及炸板率。
2. **💰 资金量与资金流向**
   - **主力资金板块 TOP**：领涨/主力资金净流入前 5 板块与个股。
   - **机构/游资龙虎榜**：机构买入额及知名游资席位异动明细。
3. **🌐 海外市场与中美板块映射**
   - **隔夜外资走势**：道琼斯、纳斯达克、标普500、费城半导体 SOX、富时 A50 与离岸人民币汇率。
   - **中美映射逻辑引擎**：比对美股英伟达/特斯拉/礼来/苹果大涨对 A 股算力、智驾、创新药、果链的实际驱动传导效应。
4. **📑 投行与券商研报精选**
   - 抓取头部券商（中信、中金、招商等）每日最新研报与机构评级变动。
5. **🪜 短线情绪周期与梯队状态机**
   - 计算 0~100 市场情绪温度得分，判定处于“发酵、高潮、分歧、修复或冰点”阶段。
   - 输出完整连板高度梯队。
6. **🤖 AI / 智投策略总结**
   - 支持接入 **DeepSeek** / OpenAI / 兼容 OpenAI 格式的大模型生成精炼研报，未配置 Key 时自动启用结构化智投规则引擎。
7. **📡 云端定时无服务器运行**
   - 配置 GitHub Actions 工作流，交易日北京时间 **15:30** 自动免费运行并发送报告。

---

## 🛠️ 快速开始与本地运行

### 1. 安装依赖
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. 配置环境变量 (可选)
复制环境变量模版并修改：
```bash
cp .env.example .env
```
根据需求填入消息推送 Webhook（飞书、钉钉、企微或 WxPusher）或 DeepSeek API Key。

### 3. 执行测试/复盘
- **本地测试预览**：
  ```bash
  python main.py --test
  ```
- **生成报告并触发推送**：
  ```bash
  python main.py --save --push
  ```
  生成的复盘报告将自动保存在 `./reports/daily_review_YYYYMMDD.md`。

---

## ☁️ 部署至 GitHub Actions 实现每日无感推送

1. 将本项目推送至你的 GitHub 仓库。
2. 进入 GitHub 仓库设置：`Settings` $\rightarrow$ `Secrets and variables` $\rightarrow$ `Actions`.
3. 添加 Secrets 密钥（如 `FEISHU_WEBHOOK`、`DINGTALK_WEBHOOK` 或 `AI_API_KEY`）。
4. 系统将在每交易日北京时间 **15:30** 自动触发，全自动发送每日盘后复盘！

---

## 📂 项目目录架构

```
智能选/
├── config.py                 # 系统配置管理
├── .env.example              # 环境变量示例
├── requirements.txt          # 项目依赖定义
├── main.py                   # 启动主程序
├── data_fetchers/            # 数据采集模块
│   ├── base_market.py        # 大盘行情、成交额、涨跌分布、连板梯队
│   ├── money_flow.py         # 资金量、主力流向、机构/游资龙虎榜
│   ├── overseas_market.py    # 美股SOX/中概/离岸人民币/A50
│   └── research_reports.py   # 投行券商研报、机构评级
├── analyzers/                # 逻辑与 AI 分析引擎
│   ├── sentiment_analyzer.py # 情绪温度评分与情绪周期状态机
│   ├── mapping_analyzer.py   # 中美板块映射驱动分析
│   └── ai_agent.py           # DeepSeek/规则智投策略总结
├── formatters/               # 报告排版
│   └── report_formatter.py   # 渲染机构风采 Markdown
├── notifiers/                # 消息推送服务
│   └── push_service.py       # 飞书、钉钉、企微、WxPusher
└── .github/workflows/        # 自动化工作流
    └── daily_review.yml      # 交易日 15:30 自动触发
```

---

*免责声明：本项目包含的所有行情分析、机构研报及 AI 预测内容仅供量化选股与技术研究参考，不构成任何形式的投资建议或买卖依据。*
