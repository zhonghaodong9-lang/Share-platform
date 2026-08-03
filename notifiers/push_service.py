import logging
import requests
from requests.compat import quote
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def push_to_feishu(content_md, title="A股盘后智投与复盘日报"):
    """推送至飞书机器人 Webhook"""
    if not Config.FEISHU_WEBHOOK:
        return False
    try:
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": title},
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": content_md[:30000]
                    }
                ]
            }
        }
        resp = requests.post(Config.FEISHU_WEBHOOK, json=payload, timeout=10)
        if resp.status_code == 200:
            logging.info("飞书推送成功！")
            return True
    except Exception as e:
        logging.error(f"飞书推送失败: {e}")
    return False

def push_to_dingtalk(content_md, title="A股盘后智投与复盘日报"):
    """推送至钉钉机器人 Webhook"""
    if not Config.DINGTALK_WEBHOOK:
        return False
    try:
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"### {title}\n\n{content_md[:20000]}"
            }
        }
        resp = requests.post(Config.DINGTALK_WEBHOOK, json=payload, timeout=10)
        if resp.status_code == 200:
            logging.info("钉钉推送成功！")
            return True
    except Exception as e:
        logging.error(f"钉钉推送失败: {e}")
    return False

def push_to_wecom(content_md, title="A股盘后智投与复盘日报"):
    """推送至企业微信 Webhook"""
    if not Config.WECOM_WEBHOOK:
        return False
    try:
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content_md[:4000]
            }
        }
        resp = requests.post(Config.WECOM_WEBHOOK, json=payload, timeout=10)
        if resp.status_code == 200:
            logging.info("企业微信推送成功！")
            return True
    except Exception as e:
        logging.error(f"企业微信推送失败: {e}")
    return False

def push_to_wxpusher(content_md, title="A股盘后智投与复盘日报"):
    """推送至 WxPusher 微信推送平台 (完美支持 SPT 极简个人推送 与 标准 AppToken 推送)"""
    app_token = Config.WXPUSHER_APP_TOKEN
    serverchan_key = Config.SERVERCHAN_SENDKEY
    
    spt_key = ""
    if serverchan_key and serverchan_key.startswith("SPT_"):
        spt_key = serverchan_key
    elif app_token and app_token.startswith("SPT_"):
        spt_key = app_token

    # 微信文本字数截断防报错处理
    safe_content = content_md
    if len(safe_content) > 38000:
        safe_content = safe_content[:38000] + "\n\n---\n*(核心篇幅较长，已自动截取每日盘后精要，完整报告已同步归档保存至本地 `reports/`)*"

    # 1. 优先使用 WxPusher 极简 SPT 个人微信推送
    if spt_key:
        try:
            url = f"https://wxpusher.zjiecode.com/api/send/message/spt/{spt_key}"
            payload = {
                "title": title,
                "content": safe_content,
                "contentType": 2
            }
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200 and resp.json().get("code") == 1000:
                logging.info("✅ WxPusher SPT 极简个人微信推送成功！")
                return True
        except Exception as e:
            logging.warning(f"WxPusher SPT 推送失败: {e}")

    # 2. 使用 WxPusher 标准 AppToken 推送
    if app_token and app_token.startswith("AT_"):
        try:
            uids = [u.strip() for u in Config.WXPUSHER_UIDS.split(",") if u.strip()] if Config.WXPUSHER_UIDS else []
            payload = {
                "appToken": app_token,
                "content": safe_content,
                "summary": title,
                "contentType": 2,  # 2 表示 Markdown 格式
            }
            if uids:
                payload["uids"] = uids

            url = "https://wxpusher.zjiecode.com/api/send/message"
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                res_json = resp.json()
                if res_json.get("code") == 1000:
                    logging.info("✅ WxPusher 标准 AppToken 微信推送成功！")
                    return True
                else:
                    logging.warning(f"⚠️ WxPusher 标准推送提示: {res_json.get('msg')}")
        except Exception as e:
            logging.warning(f"WxPusher 标准推送失败: {e}")

    return False

def push_all_channels(content_md, title="A股盘后智投与复盘日报"):
    """按配置自动广播推送至所有已配置的渠道"""
    results = {}
    if Config.FEISHU_WEBHOOK:
        results["feishu"] = push_to_feishu(content_md, title)
    if Config.DINGTALK_WEBHOOK:
        results["dingtalk"] = push_to_dingtalk(content_md, title)
    if Config.WECOM_WEBHOOK:
        results["wecom"] = push_to_wecom(content_md, title)
    if Config.WXPUSHER_APP_TOKEN or Config.SERVERCHAN_SENDKEY:
        results["wxpusher"] = push_to_wxpusher(content_md, title)

    if not results:
        logging.info("未配置任何 Webhook/推送 Key，报告仅保存在本地。")
    return results

if __name__ == "__main__":
    print(push_all_channels("测试消息内容"))
