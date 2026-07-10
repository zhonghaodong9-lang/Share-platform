// ===== 服务器同步层 =====
// 当应用通过服务器（node server.js）访问时，使用 API 替代 localStorage
const SERVER_API = window.location.origin;

// 检测是否运行在服务器模式（通过请求 /api/news/sources 验证）
let isServerMode = false;

function detectServer() {
  return fetch(SERVER_API + "/api/news/sources", { method: "GET", signal: AbortSignal.timeout(3000) })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      isServerMode = true;
      console.log("服务器模式已启用");
      return true;
    })
    .catch(function() {
      isServerMode = false;
      console.log("本地模式（使用 localStorage）");
      return false;
    });
}

// ===== 覆盖原有数据操作 =====

// 保留原有的 localStorage 函数
var origGetData = window.getData;
var origSetData = window.setData;

// 扩展 getData：先从 localStorage 加载，再从服务器同步
window.getData = function(key) {
  var local = origGetData ? origGetData(key) : null;
  return local;
};

// 扩展 setData：同时保存到 localStorage 和服务器
var saveTimer = null;
window.setData = function(key, data) {
  // 保存到 localStorage
  if (origSetData) origSetData(key, data);

  // 如果是服务器模式，同步到服务器
  if (isServerMode) {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function() {
      syncToServer(key, data);
    }, 1000);
  }
};

function syncToServer(key, data) {
  if (key === "documents") {
    // 对每个文档执行 PUT
    if (data && Array.isArray(data)) {
      data.forEach(function(doc) {
        fetch(SERVER_API + "/api/documents/" + doc.id, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            title: doc.title,
            content: doc.content,
            author: doc.author
          })
        }).catch(function() {});
      });
    }
  } else if (key === "library") {
    // 素材库的同步
    // 简单处理：对每个素材执行 POST
  }
}

// 在应用加载后尝试检测服务器
detectServer();

// 导出函数供调试
window.__isServerMode = function() { return isServerMode; };
