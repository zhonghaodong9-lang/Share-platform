# 全球资讯素材平台 - 在线协作版

## 项目简介
一个支持多人实时协作的全球新闻采集与文稿编辑平台。你和你的同事可以同时在线上浏览新闻、编辑文稿、管理素材。

## 功能
- 📰 全球新闻聚合（BBC、Reuters、TechCrunch、环球网等）
- 📝 实时协作文稿编辑器
- 📚 素材库管理
- 🔄 SSE 实时同步

## 快速部署（二选一）

### 方式一：Render.com（推荐，免费）

1. 打开 https://dashboard.render.com 注册账号
2. 点击 "New +" → "Web Service"
3. 选择 "Deploy from GitHub"（先把本项目上传到 GitHub）
4. 连接你的 GitHub 仓库
5. Render 会自动识别 `render.yaml` 配置
6. 点击 "Deploy"，等待 2-3 分钟
7. 部署完成会得到一个永久网址

### 方式二：Railway.app（免费）

1. 打开 https://railway.app 注册
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 连接项目仓库
4. 部署完成即获得域名

## 本地开发

需要 Node.js 18+：

```bash
npm install
npm start
```

访问 http://localhost:3000

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| PORT | 端口号 | 3000 |
| DATA_DIR | 数据存储路径 | ./data |

## 项目结构

```
├─ server.js          # 后端服务器
├─ package.json       # 依赖配置
├─ render.yaml        # Render.com 部署配置
├─ .env.example       # 环境变量示例
├─ public/
│  └─ index.html      # 前端页面
└─ data/              # 数据存储（自动创建）
   ├─ documents/
   └─ library/
```
