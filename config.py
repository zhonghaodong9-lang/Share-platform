import os
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

class Config:
    # --- 消息推送配置 ---
    FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK", "")
    DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK", "")
    WECOM_WEBHOOK = os.getenv("WECOM_WEBHOOK", "")
    
    # 微信专用推送配置
    WXPUSHER_APP_TOKEN = os.getenv("WXPUSHER_APP_TOKEN", "AT_c90wajU5mczqv3HhaYe9RpopYDYHjGta")
    WXPUSHER_UIDS = os.getenv("WXPUSHER_UIDS", "UID_6KxduFL4ygE3cJVrgOfmzbrN4t8F")
    SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY", "")

    # --- AI 大模型智投引擎配置 ---
    AI_PROVIDER = os.getenv("AI_PROVIDER", "none")
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.deepseek.com")
    AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")

    # --- 输出路径配置 ---
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./reports")

    # --- 数据抓取阈值配置 ---
    MONEY_FLOW_TOP_N = int(os.getenv("MONEY_FLOW_TOP_N", "10"))
    LONGHU_TOP_N = int(os.getenv("LONGHU_TOP_N", "10"))
    REPORT_TOP_N = int(os.getenv("REPORT_TOP_N", "10"))

    @classmethod
    def validate(cls):
        """确保基础路径存在"""
        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR, exist_ok=True)

Config.validate()
