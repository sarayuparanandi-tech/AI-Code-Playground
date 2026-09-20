// Backend URL — same origin when served by Flask
const API = "";

const $ = (id) => document.getElementById(id);
const tabs = document.querySelectorAll(".tab");
const codes = { html: $("html"), css: $("css"), js: $("js") };

tabs.forEach(t => t.addEventListener("click", () => {
  tabs.forEach(x => x.classList.remove("active"));
  t.classList.add("active");
  document.querySelectorAll(".code").forEach(c => c.classList.remove("active"));
  codes[t.dataset.tab].classList.add("active");
}));

function buildDoc() {
  return `<!DOCTYPE html><html><head><style>${codes.css.value}</style></head>
  <body>${codes.html.value}
  <script>
    (function(){
      const log = (...a)=>parent.postMessage({type:'log',msg:a.join(' ')},'*');
      console.log = log; console.error = log;
      try { ${codes.js.value} } catch(e){ log('Error: '+e.message); }
    })();
  <\/script></body></html>`;
}

function run() {
  $("console").textContent = "";
  $("preview").srcdoc = buildDoc();
}
window.addEventListener("message", (e) => {
  if (e.data?.type === "log") {
    $("console").textContent += e.data.msg + "\n";
  }
});

$("runBtn").onclick = run;

function combinedCode() {
  return `<!-- HTML -->\n${codes.html.value}\n\n/* CSS */\n${codes.css.value}\n\n// JS\n${codes.js.value}`;
}

$("predictBtn").onclick = async () => {
  const box = $("prediction");
  box.textContent = "Analyzing with Naive Bayes model...";
  box.className = "card";
  try {
    const r = await fetch(API + "/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ code: combinedCode() })
    });
    const j = await r.json();
    const pct = (j.confidence * 100).toFixed(1);
    if (j.label === "clean") {
      box.className = "card ok";
      box.textContent = `✅ Error-Free Code (confidence ${pct}%)`;
    } else {
      box.className = "card err";
      box.textContent = `⚠ Code with Errors (confidence ${pct}%) — try AI Debug for suggestions.`;
    }
  } catch (e) {
    box.className = "card err";
    box.textContent = "Backend not reachable. Start the Flask server (see README).";
  }
};

$("debugBtn").onclick = async () => {
  const box = $("debug");
  box.textContent = "Asking the AI debugging assistant...";
  box.className = "card";
  try {
    const r = await fetch(API + "/debug", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ code: combinedCode() })
    });
    const j = await r.json();
    box.textContent = j.suggestion || "No suggestions returned.";
  } catch (e) {
    box.className = "card err";
    box.textContent = "Backend not reachable. Start the Flask server (see README).";
  }
};

// Initial render
run();
