var APP = "ai-creative-studio";
var currentUser = "创作者";

// === Data Layer ===
function getData(key) {
  try { return JSON.parse(localStorage.getItem(APP + "_" + key)) || []; } catch(e) { return []; }
}
function setData(key, data) {
  localStorage.setItem(APP + "_" + key, JSON.stringify(data));
}

var scripts = getData("scripts");
var copyItems = getData("copyItems");
var materials = getData("materials");
var projects = getData("projects");
var settings = getData("settings") || {};

function saveAll() {
  setData("scripts", scripts);
  setData("copyItems", copyItems);
  setData("materials", materials);
  setData("projects", projects);
  setData("settings", settings);
  updateStats();
}

// === Navigation ===
document.querySelectorAll(".nav-item").forEach(function(el) {
  el.addEventListener("click", function() {
    document.querySelectorAll(".nav-item").forEach(function(n) { n.classList.remove("active"); });
    document.querySelectorAll(".tab-content").forEach(function(t) { t.classList.remove("active"); });
    el.classList.add("active");
    var tab = el.getAttribute("data-tab");
    document.getElementById("tab-" + tab).classList.add("active");
    document.getElementById("topbarTitle").textContent = el.textContent.trim();
    if (tab === "materials") renderMaterials();
    if (tab === "projects") renderProjects();
    if (tab === "copywriting") renderCopyList();
  });
});

// === Toast ===
function showToast(msg, type) {
  var t = document.getElementById("toast");
  t.textContent = msg;
  t.className = "toast show" + (type ? " " + type : "");
  clearTimeout(t._timer);
  t._timer = setTimeout(function() { t.classList.remove("show"); }, 3000);
}

// === Modal ===
function openModal(id) { document.getElementById(id).classList.add("active"); }
function closeModal(id) { document.getElementById(id).classList.remove("active"); }

// === Stats ===
function updateStats() {
  document.getElementById("statScripts").textContent = scripts.length;
  document.getElementById("statCopy").textContent = copyItems.length;
  document.getElementById("statMaterials").textContent = materials.length;
  document.getElementById("statProjects").textContent = projects.length;
}

// === Dashboard ===
function quickGenerate(type) {
  var topic = document.getElementById("quickTopic").value.trim();
  if (!topic) { showToast("请输入主题或关键词", "error"); return; }
  if (type === "script") {
    document.querySelector('[data-tab="script"]').click();
    document.getElementById("scriptTopic").value = topic;
    generateScript();
  } else {
    document.querySelector('[data-tab="copywriting"]').click();
    document.getElementById("copyTopic").value = topic;
    generateCopy();
  }
}

function renderRecentProjects() {
  var el = document.getElementById("recentProjects");
  if (projects.length === 0) {
    el.innerHTML = '<div class="empty-state"><p>暂无项目，开始创作吧！</p></div>';
    return;
  }
  var sorted = projects.slice().sort(function(a,b) { return b.updatedAt - a.updatedAt; }).slice(0,3);
  el.innerHTML = sorted.map(function(p) {
    var stageNames = {idea:"💡 创意",script:"📜 剧本",material:"📦 素材",copy:"✍️ 文案",production:"🎬 制作",done:"✅ 完成"};
    var progress = {idea:0,script:20,material:40,copy:60,production:80,done:100};
    return '<div class="project-card" onclick="openProject(\"' + p.id + '\")">' +
      '<div class="title">' + escapeHtml(p.name) + '</div>' +
      '<div class="meta">' + (stageNames[p.stage] || "创意") + ' · ' + new Date(p.updatedAt).toLocaleDateString() + '</div>' +
      '<div class="progress-bar"><div class="progress-fill" style="width:' + (progress[p.stage] || 0) + '%"></div></div></div>';
  }).join("");
}

// === AI Script ===
function generateScript() {
  var topic = document.getElementById("scriptTopic").value.trim();
  if (!topic) { showToast("请输入视频主题", "error"); return; }
  var duration = document.getElementById("scriptDuration").value;
  var audience = document.getElementById("scriptAudience").value || "大众";
  var style = document.getElementById("scriptStyle").value;
  var out = document.getElementById("scriptOutput");
  out.innerHTML = '<div style="text-align:center;padding:40px"><div class="spinner"></div><p style="margin-top:12px;color:var(--text-muted)">AI 正在创作剧本...</p></div>';
  
  var apiKey = (settings.apiKey || "").trim();
  if (apiKey) {
    fetch("/api/ai/generate", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({type:"script", topic:topic, duration:duration, audience:audience, style:style, apiKey:apiKey})
    }).then(function(r) { return r.json(); }).then(function(res) {
      if (res.success) {
        out.innerHTML = "<div class='fade-in'>" + res.data.replace(/\n/g, "<br>") + "</div>";
      } else {
        out.innerHTML = "<div class='placeholder'>生成失败: " + res.error + "</div>";
      }
    }).catch(function() {
      out.innerHTML = "<div class='placeholder'>请求失败，请检查设置中的 API Key</div>";
    });
  } else {
    out.innerHTML = '<div class="fade-in" style="color:var(--text-muted)">' +
      '请先告诉我主题，我帮你用 AI 生成剧本！' +
      '<br><br><button class="btn btn-primary btn-sm" onclick="insertDemoScript()">先看看示例剧本</button></div>';
  }
}

function insertDemoScript() {
  var topic = document.getElementById("scriptTopic").value || "AI改变生活";
  var out = document.getElementById("scriptOutput");
  var demo = "【" + topic + "】—— 3分钟短视频剧本\n\n"
    + "━━━ 开场（0:00-0:30）━━━\n"
    + "【画面】清晨城市街景，蒙太奇剪辑\n"
    + "【旁白】你有没有想过，未来的生活会是什么样子？\n\n"
    + "━━━ 主体（0:30-2:30）━━━\n"
    + "【场景1】智能家居展示\n"
    + "【画面】AI自动调节灯光、温度\n"
    + "【旁白】AI已经悄然改变了我们的日常\n\n"
    + "【场景2】AI工作助手\n"
    + "【画面】人物在电脑前用AI工具\n"
    + "【旁白】工作效率提升了10倍\n\n"
    + "━━━ 结尾（2:30-3:00）━━━\n"
    + "【画面】未来感城市俯瞰\n"
    + "【旁白】未来已来，你准备好了吗？\n\n"
    + "━━━ 自动匹配素材建议 ━━━\n"
    + "🎬 视频素材：城市航拍、科技产品特写\n"
    + "🎵 背景音乐：轻快电子风\n"
    + "🔊 音效：科技感UI音效";
  out.innerHTML = '<div class="fade-in" style="white-space:pre-wrap;line-height:1.8">' + demo.replace(/\n/g, "<br>") + '</div>';
}

function saveCurrentScript() {
  var out = document.getElementById("scriptOutput");
  var text = out.textContent || "";
  if (!text || text.includes("placeholder") || text.includes("请先告诉我")) {
    showToast("还没有生成的剧本", "error"); return;
  }
  scripts.push({
    id: "s_" + Date.now(),
    title: document.getElementById("scriptTopic").value || "未命名剧本",
    content: text,
    createdAt: Date.now()
  });
  saveAll();
  showToast("剧本已保存！");
}

// === Copywriting ===
function generateCopy() {
  var topic = document.getElementById("copyTopic").value.trim();
  if (!topic) { showToast("请输入文案主题", "error"); return; }
  var type = document.getElementById("copyType").value;
  var tone = document.getElementById("copyTone").value;
  var out = document.getElementById("copyOutput");
  out.innerHTML = '<div style="text-align:center;padding:40px"><div class="spinner"></div><p style="margin-top:12px;color:var(--text-muted)">AI 正在生成文案...</p></div>';

  setTimeout(function() {
    var demos = {
      title: ["🔥 " + topic + "，看完惊呆了！", "⚡ " + topic + "的真相竟然是……", "💡 3分钟搞懂" + topic],
      description: [
        "本期视频带你深入了解" + topic + "，从入门到精通，全程干货！\n\n📌 时间轴：\n0:00 精彩开场\n1:30 核心内容\n3:00 深度解析",
        topic + "最全面的解读来了！\n\n👍 如果对你有帮助，记得点赞关注！"
      ],
      social: [
        "📢 " + topic + "\n\n这个话题最近太火了！\n你们怎么看？评论区聊聊 👇\n\n#自媒体 #" + topic.replace(/\s/g, ""),
        "💡 每日灵感 \n\n" + topic + "\n\n你觉得呢？\n\n#创作 #" + topic.replace(/\s/g, "")
      ],
      hashtags: "#" + topic.replace(/\s/g, "") + " #自媒体 #短视频 #AI创作 #热门话题 #内容创作 #涨知识 #干货分享",
      script_snippet: [
        "【开场】\n大家好，欢迎来到我的频道！\n今天我们来聊一聊" + topic + "。\n\n【正文】\n首先，什么是" + topic + "？\n简单来说就是...\n\n【结尾】\n如果你喜欢这期内容，别忘了点赞关注！"
      ]
    };
    var items = demos[type] || ["AI 生成的 " + topic + " 相关文案"];
    var html = items.map(function(t) {
      return '<div class="copy-card fade-in"><div class="content">' + t.replace(/\n/g, "<br>") + '</div>' +
        '<div class="actions"><button class="btn btn-sm btn-ghost" onclick="copyText(this)">📋 复制</button>' +
        '<button class="btn btn-sm btn-ghost" onclick="saveGeneratedCopy(\'' + escapeHtml(t) + '\')">💾 保存</button></div></div>';
    }).join("");
    out.innerHTML = html;
  }, 800);
}

function saveGeneratedCopy(text) {
  copyItems.push({ id:"c_" + Date.now(), title: document.getElementById("copyTopic").value || "文案", content: text, createdAt: Date.now() });
  saveAll();
  renderCopyList();
  showToast("文案已保存");
}

function copyText(btn) {
  var text = btn.parentElement.previousElementSibling.textContent;
  navigator.clipboard.writeText(text).then(function() { showToast("已复制"); });
}

function renderCopyList() {
  var el = document.getElementById("copyList");
  if (copyItems.length === 0) { el.innerHTML = '<div class="empty-state"><p>还没有保存的文案</p></div>'; return; }
  el.innerHTML = copyItems.slice().reverse().map(function(c) {
    return '<div class="copy-card fade-in"><div class="label">' + escapeHtml(c.title) + '</div>' +
      '<div class="content">' + (c.content || "").substring(0, 100) + '</div>' +
      '<div class="actions"><button class="btn btn-sm btn-danger" onclick="deleteCopy(\'' + c.id + '\')">删除</button></div></div>';
  }).join("");
}

function deleteCopy(id) {
  copyItems = copyItems.filter(function(c) { return c.id !== id; });
  saveAll(); renderCopyList(); showToast("已删除");
}

function showNewCopyModal() { openModal("copyModal"); }
function saveManualCopy() {
  var title = document.getElementById("copyManualTitle").value.trim();
  var content = document.getElementById("copyManualContent").value.trim();
  if (!title || !content) { showToast("请填写标题和内容", "error"); return; }
  copyItems.push({ id:"c_" + Date.now(), title: title, content: content, createdAt: Date.now() });
  saveAll();
  closeModal("copyModal");
  document.getElementById("copyManualTitle").value = "";
  document.getElementById("copyManualContent").value = "";
  renderCopyList();
  showToast("文案已保存");
}

// === Materials ===
function renderMaterials() {
  var el = document.getElementById("materialGrid");
  var search = (document.getElementById("materialSearch").value || "").toLowerCase();
  var filter = document.getElementById("materialTypeFilter").value;
  var items = materials.filter(function(m) {
    if (filter !== "all" && m.type !== filter) return false;
    if (search && m.name.toLowerCase().indexOf(search) === -1 && (m.tags || "").toLowerCase().indexOf(search) === -1) return false;
    return true;
  });
  if (items.length === 0) { el.innerHTML = '<div class="empty-state"><div class="icon">📦</div><p>还没有素材，添加一些吧</p></div>'; return; }
  el.innerHTML = items.map(function(m) {
    return '<div class="material-item fade-in">' +
      '<span class="type-tag ' + m.type + '">' + {video:"🎬视频",image:"🖼️图片",audio:"🎵音频",text:"📝文本"}[m.type] + '</span>' +
      '<div class="title">' + escapeHtml(m.name) + '</div>' +
      '<div class="desc">' + escapeHtml((m.desc || "").substring(0, 60)) + '</div>' +
      '<div class="tags">' + (m.tags || "").split(",").map(function(t) { return t.trim() ? '<span class="tag">' + escapeHtml(t.trim()) + '</span>' : ""; }).join("") + '</div>' +
      '<button class="del-btn" onclick="deleteMaterial(\'' + m.id + '\')">✕</button></div>';
  }).join("");
}

function showNewMaterialModal() { openModal("materialModal"); }
function saveMaterial() {
  var name = document.getElementById("matName").value.trim();
  if (!name) { showToast("请输入素材名称", "error"); return; }
  materials.push({
    id: "m_" + Date.now(),
    name: name,
    type: document.getElementById("matType").value,
    tags: document.getElementById("matTags").value,
    desc: document.getElementById("matDesc").value,
    createdAt: Date.now()
  });
  saveAll();
  closeModal("materialModal");
  document.getElementById("matName").value = "";
  document.getElementById("matTags").value = "";
  document.getElementById("matDesc").value = "";
  renderMaterials();
  showToast("素材已添加");
}

function deleteMaterial(id) {
  materials = materials.filter(function(m) { return m.id !== id; });
  saveAll(); renderMaterials(); showToast("已删除");
}

// === Projects ===
function renderProjects() {
  var el = document.getElementById("projectList");
  if (projects.length === 0) { el.innerHTML = '<div class="empty-state"><div class="icon">🎯</div><p>还没有项目，新建一个吧！</p></div>'; return; }
  
  // Update pipeline counts
  document.querySelectorAll(".pipeline-stage").forEach(function(s) {
    var stage = s.getAttribute("data-stage");
    var count = projects.filter(function(p) { return p.stage === stage; }).length;
    s.querySelector(".stage-count").textContent = count + " 个";
  });
  
  el.innerHTML = projects.slice().reverse().map(function(p) {
    var stageNames = {idea:"💡 创意",script:"📜 剧本",material:"📦 素材",copy:"✍️ 文案",production:"🎬 制作",done:"✅ 完成"};
    var progress = {idea:0,script:20,material:40,copy:60,production:80,done:100};
    return '<div class="project-card fade-in">' +
      '<div class="title">' + escapeHtml(p.name) + '</div>' +
      '<div class="meta">' + (stageNames[p.stage] || "创意") + ' · ' + new Date(p.createdAt).toLocaleDateString() + '</div>' +
      '<div class="progress-bar"><div class="progress-fill" style="width:' + (progress[p.stage] || 0) + '%"></div></div>' +
      '<div style="margin-top:8px;display:flex;gap:4px">' +
      '<button class="btn btn-sm btn-ghost" onclick="advanceProjectStage(\'' + p.id + '\')">▶ 推进</button>' +
      '<button class="btn btn-sm btn-danger" onclick="deleteProject(\'' + p.id + '\')">删除</button></div></div>';
  }).join("");
}

function showNewProjectModal() { openModal("projectModal"); }
function saveProject() {
  var name = document.getElementById("projName").value.trim();
  if (!name) { showToast("请输入项目名称", "error"); return; }
  projects.push({
    id: "p_" + Date.now(),
    name: name,
    desc: document.getElementById("projDesc").value,
    stage: "idea",
    createdAt: Date.now(),
    updatedAt: Date.now()
  });
  saveAll();
  closeModal("projectModal");
  document.getElementById("projName").value = "";
  document.getElementById("projDesc").value = "";
  renderProjects();
  renderRecentProjects();
  showToast("项目已创建！🎉");
}

function advanceProjectStage(id) {
  var stages = ["idea","script","material","copy","production","done"];
  var p = projects.find(function(p) { return p.id === id; });
  if (!p) return;
  var idx = stages.indexOf(p.stage);
  if (idx < stages.length - 1) { p.stage = stages[idx + 1]; p.updatedAt = Date.now(); }
  saveAll();
  renderProjects();
  renderRecentProjects();
  showToast("项目已推进到下一阶段！");
}

function deleteProject(id) {
  if (!confirm("确定删除此项目？")) return;
  projects = projects.filter(function(p) { return p.id !== id; });
  saveAll(); renderProjects(); renderRecentProjects(); showToast("已删除");
}

function openProject(id) {
  var p = projects.find(function(p) { return p.id === id; });
  if (!p) return;
  document.querySelector('[data-tab="script"]').click();
  document.getElementById("scriptTopic").value = p.name;
}

// === Settings ===
function updateSettings() {
  settings.name = document.getElementById("settingsName").value;
  settings.apiKey = document.getElementById("settingsApiKey").value;
  settings.duration = document.getElementById("settingsDuration").value;
  saveAll();
  currentUser = settings.name;
  document.getElementById("sidebarUser").textContent = currentUser;
}

// === Export/Import ===
function exportAllData() {
  var data = { scripts:scripts, copyItems:copyItems, materials:materials, projects:projects, settings:settings, exportedAt:new Date().toISOString() };
  var blob = new Blob([JSON.stringify(data, null, 2)], {type:"application/json"});
  var a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "ai-creative-studio-backup.json";
  a.click();
  showToast("数据已导出");
}

function importAllData(event) {
  var file = event.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var data = JSON.parse(e.target.result);
      if (data.scripts) { scripts = data.scripts; setData("scripts", scripts); }
      if (data.copyItems) { copyItems = data.copyItems; setData("copyItems", copyItems); }
      if (data.materials) { materials = data.materials; setData("materials", materials); }
      if (data.projects) { projects = data.projects; setData("projects", projects); }
      if (data.settings) { settings = data.settings; setData("settings", settings); }
      saveAll();
      renderMaterials();
      renderProjects();
      renderCopyList();
      renderRecentProjects();
      showToast("数据导入成功！");
    } catch(err) { showToast("导入失败: " + err.message, "error"); }
  };
  reader.readAsText(file);
  event.target.value = "";
}

// === Init ===
function init() {
  if (settings.name) { currentUser = settings.name; document.getElementById("sidebarUser").textContent = currentUser; }
  if (settings.apiKey) document.getElementById("settingsApiKey").value = settings.apiKey;
  if (settings.duration) document.getElementById("settingsDuration").value = settings.duration;
  document.getElementById("settingsName").value = currentUser;
  updateStats();
  renderRecentProjects();
  renderMaterials();
  renderProjects();
  renderCopyList();
  updateStats();
  console.log("AI 创作工坊已加载");
}

// === Utils ===
function escapeHtml(str) {
  if (!str) return "";
  return String(str).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");
}

// === Expose for inline use ===
window.quickGenerate = quickGenerate;
window.generateScript = generateScript;
window.insertDemoScript = insertDemoScript;
window.saveCurrentScript = saveCurrentScript;
window.generateCopy = generateCopy;
window.saveGeneratedCopy = saveGeneratedCopy;
window.copyText = copyText;
window.renderCopyList = renderCopyList;
window.deleteCopy = deleteCopy;
window.showNewCopyModal = showNewCopyModal;
window.saveManualCopy = saveManualCopy;
window.renderMaterials = renderMaterials;
window.showNewMaterialModal = showNewMaterialModal;
window.saveMaterial = saveMaterial;
window.deleteMaterial = deleteMaterial;
window.renderProjects = renderProjects;
window.showNewProjectModal = showNewProjectModal;
window.saveProject = saveProject;
window.advanceProjectStage = advanceProjectStage;
window.deleteProject = deleteProject;
window.openProject = openProject;
window.updateSettings = updateSettings;
window.exportAllData = exportAllData;
window.importAllData = importAllData;
window.closeModal = closeModal;
window.openModal = openModal;

document.addEventListener("DOMContentLoaded", init);
