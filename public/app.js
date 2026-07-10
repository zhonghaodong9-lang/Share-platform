// === 全局配置 ===
const APP_NAME = "global_news_platform";
let currentUser = localStorage.getItem(APP_NAME + "_user") || "用户A";
let currentTab = "news";
let editingDocId = null;
let docList = [];
let libItems = [];
let newsCache = {};

// 获取存储数据
function getData(key) {
  try { return JSON.parse(localStorage.getItem(APP_NAME + "_" + key) || "null"); } catch(e) { return null; }
}
function setData(key, data) {
  localStorage.setItem(APP_NAME + "_" + key, JSON.stringify(data));
}

// === 初始化 ===
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("userName").value = currentUser;
  document.getElementById("userName").addEventListener("change", function() {
    currentUser = this.value || "匿名";
    localStorage.setItem(APP_NAME + "_user", currentUser);
    updateOnlineStatus();
  });

  // Tab 切换
  document.querySelectorAll(".nav-item").forEach(function(btn) {
    btn.addEventListener("click", function() {
      currentTab = this.getAttribute("data-tab");
      document.querySelectorAll(".nav-item").forEach(function(b) { b.classList.remove("active"); });
      document.querySelectorAll(".tab-content").forEach(function(t) { t.style.display = "none"; });
      this.classList.add("active");
      document.getElementById("tab-" + currentTab).style.display = "block";
      var titles = { news: "资讯速览", editor: "文稿编辑器", library: "素材库", reports: "资讯日报" };
      document.getElementById("pageTitle").textContent = titles[currentTab] || currentTab;
      if (currentTab === "library") renderLibrary();
      if (currentTab === "editor") renderDocList();
    });
  });

  // 新闻源选择
  document.querySelectorAll(".source-btn").forEach(function(btn) {
    btn.addEventListener("click", function() { this.classList.toggle("active"); });
  });

  // 获取新闻
  document.getElementById("fetchNewsBtn").addEventListener("click", fetchNewsFromBrowser);

  // 编辑器工具栏
  document.querySelectorAll(".editor-toolbar button").forEach(function(btn) {
    btn.addEventListener("click", function() {
      var cmd = this.getAttribute("data-cmd");
      var value = this.getAttribute("data-value");
      if (cmd === "createLink") {
        var url = prompt("输入链接地址:", "https://");
        if (url) document.execCommand(cmd, false, url);
      } else {
        document.execCommand(cmd, false, value || null);
      }
      document.getElementById("editorContent").focus();
      autoSaveDoc();
    });
  });

  // 编辑器自动保存
  var editorEl = document.getElementById("editorContent");
  var saveTimer = null;
  editorEl.addEventListener("input", function() {
    updateEditorStats();
    clearTimeout(saveTimer);
    saveTimer = setTimeout(autoSaveDoc, 2000);
  });
  document.getElementById("docTitle").addEventListener("input", function() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(autoSaveDoc, 2000);
  });

  // 文档操作
  document.getElementById("newDocBtn").addEventListener("click", createDocument);
  document.getElementById("saveDocBtn").addEventListener("click", function() {
    autoSaveDoc(true);
  });

  // 素材库
  document.getElementById("newLibItemBtn").addEventListener("click", function() { showLibModal(); });
  document.getElementById("modalSaveBtn").addEventListener("click", saveLibItem);
  document.getElementById("libSearch").addEventListener("input", renderLibrary);
  document.getElementById("libFilterTag").addEventListener("input", renderLibrary);

  // 加载数据
  docList = getData("documents") || [];
  libItems = getData("library") || [];
  newsCache = getData("news") || {};
  renderDocList();
  renderLibrary();
  updateOnlineStatus();

  // 显示协作指引
  showSyncGuide();
});

function showSyncGuide() {
  var grid = document.getElementById("newsGrid");
  if (!newsCache || Object.keys(newsCache).length === 0) {
    // Keep default message
  }
}

function updateOnlineStatus() {
  var area = document.getElementById("onlineUsers");
  area.innerHTML = "";
  var users = getData("users") || [currentUser];
  if (users.indexOf(currentUser) === -1) users.push(currentUser);
  setData("users", users);
  users.forEach(function(u) {
    var av = document.createElement("div");
    av.className = "user-avatar";
    av.textContent = u.charAt(0);
    av.title = u;
    av.style.background = "#" + hashCode(u).toString(16).slice(0, 6);
    area.appendChild(av);
  });
}

function hashCode(str) {
  var hash = 0;
  for (var i = 0; i < str.length; i++) { hash = ((hash << 5) - hash) + str.charCodeAt(i); hash |= 0; }
  return Math.abs(hash);
}

// === 新闻获取（通过浏览器）===
function fetchNewsFromBrowser() {
  var selected = [];
  document.querySelectorAll(".source-btn.active").forEach(function(btn) {
    selected.push(btn.getAttribute("data-source"));
  });
  if (selected.length === 0) { document.getElementById("fetchStatus").textContent = "请至少选择一个新闻来源"; return; }

  document.getElementById("fetchStatus").textContent = "提示: 你可以告诉我「帮我获取这些新闻源的资讯」，我会用浏览器帮你抓取后填入";

  // Try to use cached news first
  if (Object.keys(newsCache).length > 0) {
    renderNews(newsCache);
    document.getElementById("fetchStatus").textContent = "显示缓存资讯（点击「刷新」获取最新）";
  }
}

// 这个方法被 Codex 调用，从浏览器获取新闻后填入
function updateNewsFromCodex(data) {
  newsCache = data;
  setData("news", data);
  renderNews(data);
  document.getElementById("fetchStatus").textContent = "已更新 " + new Date().toLocaleTimeString("zh-CN");
  // Also add to library
  var count = 0;
  for (var src in data) {
    var items = data[src];
    if (!items || !items.length) continue;
    items.forEach(function(item) {
      if (!item.title) return;
      addToLibraryAuto(item.title, item.link || "", src, item.desc || "");
      count++;
    });
  }
  document.getElementById("fetchStatus").textContent += "，已自动收藏 " + count + " 条到素材库";
}

function renderNews(data) {
  var grid = document.getElementById("newsGrid");
  grid.innerHTML = "";
  var count = 0;
  var sourceNames = { bbc: "BBC News", bbc_world: "BBC World", bbc_tech: "BBC Tech", reuters: "Reuters", techcrunch: "TechCrunch", guardian: "The Guardian", nyt: "NY Times", google: "Google News", ars: "Ars Technica", huanqiu: "环球网" };

  for (var src in data) {
    var items = data[src];
    if (!items || !items.length || items.error) continue;
    items.forEach(function(item) {
      if (!item.title) return;
      count++;
      var card = document.createElement("div");
      card.className = "news-card";
      card.innerHTML =
        '<div class="source-tag">' + (sourceNames[src] || src) + '</div>' +
        '<h3>' + escapeHtml(item.title) + '</h3>' +
        (item.desc ? '<p>' + escapeHtml(item.desc).slice(0, 150) + '</p>' : "") +
        '<div class="card-footer">' +
        '<span>' + (item.pubDate || "") + '</span>' +
        '<div class="card-actions">' +
        (item.link ? '<button onclick="window.open(\'' + item.link + '\',\'_blank\')">打开</button>' : "") +
        '<button onclick="addToLibraryAuto(\'' + escapeHtml(item.title).replace(/\'/g, "\\'") + '\',\'' + (item.link || "") + '\',\'' + (sourceNames[src] || src) + '\',\'' + escapeHtml(item.desc || "").replace(/\'/g, "\\'").slice(0, 100) + '\')">收藏</button>' +
        '</div></div>';
      grid.appendChild(card);
    });
  }

  if (count === 0) {
    grid.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-secondary);"><div style="font-size:48px;margin-bottom:16px;">📰</div><p>还没有资讯数据。你可以对我说：<br><br>"帮我获取 BBC、TechCrunch 和环球网的今日新闻"</p><p style="font-size:13px;margin-top:12px;color:var(--primary);">我会用浏览器帮你抓取并填入这里</p></div>';
  }
}

// === 文档管理 ===
function createDocument() {
  var title = document.getElementById("docTitle").value.trim() || "新文档_" + Date.now();
  var id = "doc_" + Date.now();
  var doc = { id: id, title: title, content: "", author: currentUser, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), collaborators: [currentUser] };
  docList.push(doc);
  setData("documents", docList);
  editingDocId = id;
  document.getElementById("currentDocId").textContent = id;
  document.getElementById("editorContent").innerHTML = "";
  updateEditorStats();
  document.getElementById("editorStatus").textContent = "已创建: " + title;
  renderDocList();
}

function openDocument(id) {
  var doc = null;
  for (var i = 0; i < docList.length; i++) {
    if (docList[i].id === id) { doc = docList[i]; break; }
  }
  if (!doc) return;
  editingDocId = id;
  document.getElementById("currentDocId").textContent = id;
  document.getElementById("docTitle").value = doc.title || "无标题";
  document.getElementById("editorContent").innerHTML = doc.content || "";
  document.getElementById("editorStatus").textContent = "已打开: " + doc.title;
  updateEditorStats();
}

function autoSaveDoc(force) {
  if (!editingDocId) return;
  var title = document.getElementById("docTitle").value.trim() || "无标题";
  var content = document.getElementById("editorContent").innerHTML;

  for (var i = 0; i < docList.length; i++) {
    if (docList[i].id === editingDocId) {
      docList[i].title = title;
      docList[i].content = content;
      docList[i].updatedAt = new Date().toISOString();
      docList[i].author = currentUser;
      if (docList[i].collaborators.indexOf(currentUser) === -1) docList[i].collaborators.push(currentUser);
      break;
    }
  }
  setData("documents", docList);

  // Broadcast to other tabs on same machine
  try {
    var bc = new BroadcastChannel(APP_NAME);
    bc.postMessage({ type: "doc-update", id: editingDocId, user: currentUser });
    bc.close();
  } catch(e) {}

  if (force) {
    document.getElementById("editorStatus").textContent = "已保存 " + new Date().toLocaleTimeString("zh-CN");
    renderDocList();
  }
}

function renderDocList() {
  var list = document.getElementById("docList");
  list.innerHTML = '<span style="font-size:13px;color:var(--text-secondary);padding:4px 0;white-space:nowrap;">文档:</span>';
  if (docList.length === 0) {
    list.innerHTML += '<span style="font-size:13px;color:var(--text-secondary);">（暂无文档，点击"新建文档"）</span>';
    return;
  }
  docList.forEach(function(doc) {
    var btn = document.createElement("button");
    btn.style.cssText = "padding:4px 12px;border:1px solid var(--border);border-radius:4px;cursor:pointer;font-size:13px;background:" + (editingDocId === doc.id ? "var(--accent)" : "var(--surface)") + ";";
    btn.textContent = doc.title + (doc.collaborators && doc.collaborators.length > 1 ? " 👥" : "");
    btn.title = "最后编辑: " + (doc.updatedAt || "");
    btn.addEventListener("click", function() { openDocument(doc.id); });
    list.appendChild(btn);
  });
}

// === 素材库 ===
function addToLibraryAuto(title, source, sourceName, desc) {
  var exists = libItems.some(function(item) { return item.title === title && item.source === source; });
  if (exists) return;

  var id = "lib_" + Date.now() + "_" + Math.random().toString(36).slice(2, 6);
  libItems.push({
    id: id,
    title: title,
    content: desc || "",
    tags: [sourceName || "资讯"],
    source: source,
    author: currentUser,
    createdAt: new Date().toISOString()
  });
  setData("library", libItems);
  document.getElementById("libCount").textContent = libItems.length;
}

function renderLibrary() {
  var search = (document.getElementById("libSearch").value || "").toLowerCase();
  var tagFilter = (document.getElementById("libFilterTag").value || "").toLowerCase();
  var grid = document.getElementById("libraryGrid");
  grid.innerHTML = "";

  var filtered = libItems.filter(function(item) {
    var ms = !search || item.title.toLowerCase().includes(search) || (item.content || "").toLowerCase().includes(search);
    var mt = !tagFilter || (item.tags || []).some(function(t) { return t.toLowerCase().includes(tagFilter); });
    return ms && mt;
  });

  if (filtered.length === 0) {
    grid.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-secondary);grid-column:1/-1;"><p>没有匹配的素材</p><p style="font-size:13px;margin-top:8px;">从资讯速览收藏或手动添加</p></div>';
    return;
  }

  filtered.forEach(function(item) {
    var div = document.createElement("div");
    div.className = "library-item";
    div.innerHTML =
      '<div style="display:flex;justify-content:space-between;align-items:start;">' +
      '<h3>' + escapeHtml(item.title) + '</h3>' +
      '<button onclick="deleteLibItem(\'' + item.id + '\')" style="border:none;background:none;cursor:pointer;color:var(--danger);font-size:18px;padding:0 4px;">×</button>' +
      '</div>' +
      (item.tags && item.tags.length ? '<div class="tags">' + item.tags.map(function(t) { return '<span class="tag">' + escapeHtml(t) + '</span>'; }).join("") + '</div>' : "") +
      (item.source ? '<div class="meta">来源: ' + escapeHtml(item.source) + '</div>' : "") +
      '<div class="meta">' + escapeHtml(item.author) + " · " + (item.createdAt ? new Date(item.createdAt).toLocaleString("zh-CN") : "") + '</div>' +
      (item.content ? '<div class="preview">' + stripHtml(item.content).slice(0, 120) + '</div>' : "");
    div.addEventListener("dblclick", function() {
      showLibModal(item.title, item.source, "", item.content, item.tags);
    });
    grid.appendChild(div);
  });
}

function showLibModal(title, source, sourceName, content, tags) {
  document.getElementById("modal").style.display = "flex";
  document.getElementById("modalTitle").textContent = "新增素材";
  document.getElementById("modalLibTitle").value = title || "";
  document.getElementById("modalLibSource").value = source || (sourceName || "");
  document.getElementById("modalLibTags").value = (tags || []).join(", ");
  document.getElementById("modalLibContent").value = content || "";
}

function saveLibItem() {
  var title = document.getElementById("modalLibTitle").value.trim();
  if (!title) { alert("请输入标题"); return; }
  var tags = document.getElementById("modalLibTags").value.split(",").map(function(t) { return t.trim(); }).filter(Boolean);
  var id = "lib_" + Date.now() + "_" + Math.random().toString(36).slice(2, 6);
  libItems.push({
    id: id,
    title: title,
    content: document.getElementById("modalLibContent").value,
    tags: tags,
    source: document.getElementById("modalLibSource").value,
    author: currentUser,
    createdAt: new Date().toISOString()
  });
  setData("library", libItems);
  document.getElementById("modal").style.display = "none";
  document.getElementById("libCount").textContent = libItems.length;
  renderLibrary();
}

function deleteLibItem(id) {
  if (!confirm("确定删除此素材？")) return;
  libItems = libItems.filter(function(item) { return item.id !== id; });
  setData("library", libItems);
  document.getElementById("libCount").textContent = libItems.length;
  renderLibrary();
}

// === 数据导入导出 ===
function exportData() {
  var data = {
    documents: docList,
    library: libItems,
    news: newsCache,
    exportedAt: new Date().toISOString(),
    exportedBy: currentUser
  };
  var blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  a.href = url;
  a.download = "资讯素材库_备份_" + new Date().toISOString().slice(0, 10) + ".json";
  a.click();
  URL.revokeObjectURL(url);
}

function importData(jsonText) {
  try {
    var data = JSON.parse(jsonText);
    if (data.documents) { docList = data.documents; setData("documents", docList); }
    if (data.library) { libItems = data.library; setData("library", libItems); document.getElementById("libCount").textContent = libItems.length; }
    if (data.news) { newsCache = data.news; setData("news", newsCache); }
    renderDocList();
    renderLibrary();
    alert("数据导入成功！共导入 " + (data.documents ? data.documents.length : 0) + " 个文档、" + (data.library ? data.library.length : 0) + " 条素材");
  } catch(e) {
    alert("导入失败: " + e.message);
  }
}

// 监听其他标签页的更新
try {
  var bc = new BroadcastChannel(APP_NAME);
  bc.onmessage = function(e) {
    if (e.data && e.data.type === "doc-update") {
      docList = getData("documents") || [];
      renderDocList();
      document.getElementById("editorStatus").textContent = "另一设备更新了文档";
    }
  };
} catch(e) {}

// === 工具函数 ===
function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function stripHtml(str) {
  if (!str) return "";
  var tmp = document.createElement("div");
  tmp.innerHTML = str;
  return tmp.textContent || tmp.innerText || "";
}

function updateEditorStats() {
  var editor = document.getElementById("editorContent");
  var text = editor.textContent || "";
  document.getElementById("editorChars").textContent = text.length + " 字";
}

// 导出更新函数，供 Codex 调用
window.updateNewsFromCodex = updateNewsFromCodex;
window.exportData = exportData;
window.importData = importData;

console.log("全球资讯素材平台已加载，用户: " + currentUser);
