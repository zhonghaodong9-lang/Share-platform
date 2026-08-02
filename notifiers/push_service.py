import logging
import requests
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
                        "content": content_md
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
                "text": f"### {title}\n\n{content_md}"
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
                "content": content_md
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
    """推送至 WxPusher 微信推送平台"""
    token = Config.WXPUSHER_APP_TOKEN or Config.SERVERCHAN_SENDKEY
    if not token:
        return False
    
    uids = [u.strip() for u in Config.WXPUSHER_UIDS.split(",") if u.strip()] if Config.WXPUSHER_UIDS else []
    payload = {
        "appToken": token,
        "content": content_md,
        "summary": title,
        "contentType": 2,  # 2 表示 Markdown 格式
    }
    if uids:
        payload["uids"] = uids

    urls = [
        "https://wxpusher.com/api/send/message",
        "https://wxpusher.zhengxianliang.com/api/send/message",
    ]

    for url in urls:
        try:
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                res_json = resp.json()
                code = res_json.get("code")
                msg = res_json.get("msg")
                logging.info(f"WxPusher API ({url}) 响应: code={code}, msg={msg}")
                if code == 1000:
                    logging.info("✅ WxPusher 微信推送成功！")
                    return True
                else:
                    logging.warning(f"⚠️ WxPusher 提示: {msg}")
        except Exception as e:
            logging.warning(f"WxPusher 连接 {url} 失败: {e}")

    return False

def push_to_serverchan(content_md, title="A股盘后智投与复盘日报"):
    """推送至 Server酱 / 方糖 微信"""
    sendkey = Config.SERVERCHAN_SENDKEY or Config.WXPUSHER_APP_TOKEN
    if not sendkey:
        return False
    
    urls = [
        f"https://sctapi.ftqq.com/{sendkey}.send",
        f"https://push.ftqq.com/{sendkey}.send",
    ]
    for url in urls:
        try:
            payload = {"title": title, "desp": content_md}
            resp = requests.post(url, data=payload, timeout=10)
            if resp.status_code == 200:
                res_json = resp.json()
                logging.info(f"Server酱 API ({url}) 响应: {res_json}")
                if res_json.get("code") == 0 or res_json.get("errno") == 0:
                    logging.info("✅ Server酱 微信推送成功！")
                    return True
        except Exception as e:
            logging.warning(f"Server酱 请求 {url} 异常: {e}")
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
    if Config.WXPUSHER_APP_TOKEN or Config.WXPUSHER_UIDS:
        results["wxpusher"] = push_to_wxpusher(content_md, title)
    if Config.SERVERCHAN_SENDKEY or (Config.WXPUSHER_APP_TOKEN and Config.WXPUSHER_APP_TOKEN.startswith("SPT_")):
        results["serverchan"] = push_to_serverchan(content_md, title)

    if not results:
        logging.info("未配置任何 Webhook/推送 Key，报告仅保存在本地。")
    return results

if __name__ == "__main__":
    print(push_all_channels("测试消息内容"))
