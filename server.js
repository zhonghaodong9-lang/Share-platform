const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");

const PORT = process.env.PORT || 3000;
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, "data");
const DOCS_DIR = path.join(DATA_DIR, "documents");
const LIB_DIR = path.join(DATA_DIR, "library");
const PUBLIC_DIR = path.join(__dirname, "public");

[DOCS_DIR, LIB_DIR].forEach(d => { try { fs.mkdirSync(d, { recursive: true }); } catch(e) {} });

const sseClients = new Map();
const MIME = { ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "application/javascript; charset=utf-8", ".json": "application/json; charset=utf-8", ".png": "image/png", ".svg": "image/svg+xml" };

function sendJSON(res, code, data) {
  res.writeHead(code, { "Content-Type": "application/json; charset=utf-8", "Access-Control-Allow-Origin": "*" });
  res.end(JSON.stringify(data));
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", c => body += c);
    req.on("end", () => { try { resolve(JSON.parse(body)); } catch(e) { reject(new Error("Invalid JSON")); } });
    req.on("error", reject);
  });
}

function sendSSE(docId, event, data) {
  const clients = sseClients.get(docId);
  if (!clients) return;
  const msg = "event: " + event + "\ndata: " + JSON.stringify(data) + "\n\n";
  clients.forEach(c => { try { c.write(msg); } catch(e) { clients.delete(c); } });
}

async function fetchRSS(feedUrl) {
  const resp = await fetch(feedUrl, { signal: AbortSignal.timeout(10000) });
  const xml = await resp.text();
  const items = [];
  const regex = /<item>([\s\S]*?)<\/item>/g;
  let m;
  while ((m = regex.exec(xml)) !== null) {
    const get = (tag) => {
      const r = new RegExp("<" + tag + "[^>]*>([\\s\\S]*?)<\\/" + tag + ">");
      const match = m[1].match(r);
      return match ? match[1].replace(/<!\[CDATA\[|\]\]>/g, "").trim() : "";
    };
    items.push({
      title: get("title").replace(/<!\[CDATA\[|\]\]>/g, ""),
      link: get("link"),
      pubDate: get("pubDate"),
      desc: get("description").replace(/<[^>]+>/g, "").slice(0, 200)
    });
  }
  return items.slice(0, 15);
}

const NEWS_FEEDS = {
  bbc: { url: "https://feeds.bbci.co.uk/news/rss.xml", name: "BBC News" },
  bbc_world: { url: "https://feeds.bbci.co.uk/news/world/rss.xml", name: "BBC World" },
  bbc_tech: { url: "https://feeds.bbci.co.uk/news/technology/rss.xml", name: "BBC Tech" },
  reuters: { url: "https://www.reutersagency.com/feed/", name: "Reuters" },
  techcrunch: { url: "https://techcrunch.com/feed/", name: "TechCrunch" },
  guardian: { url: "https://www.theguardian.com/world/rss", name: "Guardian" },
  nyt: { url: "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", name: "NY Times" },
  huanqiu: { url: "https://www.huanqiu.com/rss/international.xml", name: "环球网" }
};

const server = http.createServer(async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.writeHead(204); res.end(); return; }

  const pn = url.parse(req.url).pathname;
  const method = req.method;

  try {
    // ===== News API =====
    if (pn === "/api/news/sources" && method === "GET") {
      const list = Object.keys(NEWS_FEEDS).map(k => ({ id: k, name: NEWS_FEEDS[k].name }));
      return sendJSON(res, 200, { success: true, data: list });
    }

    if (pn === "/api/news/fetch" && method === "POST") {
      const body = await parseBody(req);
      const sources = body.sources || ["bbc"];
      const results = {};
      for (const src of sources) {
        const feed = NEWS_FEEDS[src];
        if (!feed) { results[src] = []; continue; }
        try { results[src] = await fetchRSS(feed.url); }
        catch(e) { results[src] = []; }
      }
      return sendJSON(res, 200, { success: true, data: results });
    }

    // ===== Documents API =====
    if (pn === "/api/documents" && method === "GET") {
      const files = fs.readdirSync(DOCS_DIR).filter(f => f.endsWith(".json"));
      const docs = files.map(f => {
        const d = JSON.parse(fs.readFileSync(path.join(DOCS_DIR, f), "utf-8"));
        return { id: d.id, title: d.title, updatedAt: d.updatedAt, author: d.author, collaborators: d.collaborators || [] };
      });
      docs.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
      return sendJSON(res, 200, { success: true, data: docs });
    }

    if (pn === "/api/documents" && method === "POST") {
      const body = await parseBody(req);
      const id = "doc_" + Date.now();
      const doc = { id, title: body.title || "新文档", content: body.content || "", author: body.author || "用户", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), collaborators: [body.author || "用户"] };
      fs.writeFileSync(path.join(DOCS_DIR, id + ".json"), JSON.stringify(doc, null, 2), "utf-8");
      return sendJSON(res, 200, { success: true, data: doc });
    }

    const docMatch = pn.match(/^\/api\/documents\/([^\/]+)/);
    if (docMatch) {
      const id = docMatch[1];
      const fp = path.join(DOCS_DIR, id + ".json");

      if (method === "GET" && !pn.endsWith("/events")) {
        if (!fs.existsSync(fp)) return sendJSON(res, 404, { error: "Not found" });
        return sendJSON(res, 200, { success: true, data: JSON.parse(fs.readFileSync(fp, "utf-8")) });
      }

      if (method === "PUT") {
        const body = await parseBody(req);
        let doc;
        try { doc = JSON.parse(fs.readFileSync(fp, "utf-8")); } catch(e) { doc = { id, collaborators: [] }; }
        if (body.title !== undefined) doc.title = body.title;
        if (body.content !== undefined) doc.content = body.content;
        doc.updatedAt = new Date().toISOString();
        if (body.author && !doc.collaborators.includes(body.author)) doc.collaborators.push(body.author);
        doc.author = body.author || doc.author;
        fs.writeFileSync(fp, JSON.stringify(doc, null, 2), "utf-8");
        sendSSE(id, "content-update", { content: doc.content, author: doc.author });
        return sendJSON(res, 200, { success: true, data: doc });
      }

      if (method === "DELETE") {
        try { fs.unlinkSync(fp); } catch(e) {}
        return sendJSON(res, 200, { success: true });
      }

      // SSE for real-time collaboration
      if (pn.endsWith("/events") && method === "GET") {
        res.writeHead(200, { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", "Connection": "keep-alive", "Access-Control-Allow-Origin": "*" });
        res.write("event: connected\ndata: {}\n\n");
        if (!sseClients.has(id)) sseClients.set(id, new Set());
        sseClients.get(id).add(res);
        req.on("close", () => {
          const set = sseClients.get(id);
          if (set) { set.delete(res); if (set.size === 0) sseClients.delete(id); }
        });
        return;
      }
    }

    // ===== Library API =====
    if (pn === "/api/library" && method === "GET") {
      const files = fs.readdirSync(LIB_DIR).filter(f => f.endsWith(".json"));
      const items = files.map(f => JSON.parse(fs.readFileSync(path.join(LIB_DIR, f), "utf-8")));
      return sendJSON(res, 200, { success: true, data: items });
    }

    if (pn === "/api/library" && method === "POST") {
      const body = await parseBody(req);
      const id = "lib_" + Date.now();
      const item = { id, title: body.title || "素材", content: body.content || "", tags: body.tags || [], source: body.source || "", author: body.author || "用户", createdAt: new Date().toISOString() };
      fs.writeFileSync(path.join(LIB_DIR, id + ".json"), JSON.stringify(item, null, 2), "utf-8");
      return sendJSON(res, 200, { success: true, data: item });
    }

    if (pn.startsWith("/api/library/") && method === "DELETE") {
      const id = pn.split("/")[3];
      try { fs.unlinkSync(path.join(LIB_DIR, id + ".json")); } catch(e) {}
      return sendJSON(res, 200, { success: true });
    }

    // ===== Static files =====
    let filePath = path.join(PUBLIC_DIR, pn === "/" ? "index.html" : pn);
    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
      const ext = path.extname(filePath);
      res.writeHead(200, { "Content-Type": MIME[ext] || "application/octet-stream" });
      res.end(fs.readFileSync(filePath));
    } else {
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(fs.readFileSync(path.join(PUBLIC_DIR, "index.html")));
    }

  } catch(e) {
    if (!res.headersSent) sendJSON(res, 500, { error: e.message });
  }
});

server.listen(PORT, "0.0.0.0", () => {
  console.log("=== 全球资讯素材平台 ===");
  console.log("本地访问: http://localhost:" + PORT);
  console.log("数据目录: " + DATA_DIR);
});
