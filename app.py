"""
AI-Powered Online Code Playground - Backend
Flask API serving:
  POST /predict  -> Naive Bayes error prediction
  POST /debug    -> Generative AI debugging suggestions
"""
import os, pickle, re, json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

BASE = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE / "ML" / "saved_model" / "model.pkl"
FRONTEND = BASE / "Frontend"

app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")
CORS(app)

# ---- Load ML model ----
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ---- GenAI debugging ----
def llm_debug(code: str) -> str:
    """Call an LLM to get debugging suggestions. Falls back to rule-based hints."""
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("LOVABLE_API_KEY")
    if api_key:
        try:
            import requests
            base = "https://ai.gateway.lovable.dev/v1" if os.environ.get("LOVABLE_API_KEY") else "https://api.openai.com/v1"
            headers = {"Content-Type": "application/json"}
            if os.environ.get("LOVABLE_API_KEY"):
                headers["Lovable-API-Key"] = api_key
                model_name = "google/gemini-3-flash-preview"
            else:
                headers["Authorization"] = f"Bearer {api_key}"
                model_name = "gpt-4o-mini"
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "You are a helpful code debugging assistant for HTML, CSS, and JavaScript. Identify errors and suggest concise fixes."},
                    {"role": "user", "content": f"Analyze this code and suggest fixes:\n\n{code}"}
                ],
                "temperature": 0.2
            }
            r = requests.post(f"{base}/chat/completions", headers=headers, json=payload, timeout=30)
            if r.ok:
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("LLM error:", e)
    # ---- Fallback rule-based debugger ----
    hints = []
    # Unclosed HTML tags
    opens = re.findall(r"<([a-zA-Z][a-zA-Z0-9]*)\b[^/>]*>", code)
    closes = re.findall(r"</([a-zA-Z][a-zA-Z0-9]*)\s*>", code)
    self_closing = {"br","img","input","hr","meta","link"}
    for tag in opens:
        if tag.lower() in self_closing: continue
        if opens.count(tag) > closes.count(tag):
            hints.append(f"The <{tag}> tag is not closed. Add </{tag}> to fix the issue.")
            break
    # Bracket balance
    for op, cl, name in [("(",")","parenthesis"),("{","}","brace"),("[","]","bracket")]:
        if code.count(op) > code.count(cl):
            hints.append(f"Missing closing {name} '{cl}'. Add it where the block ends.")
        elif code.count(cl) > code.count(op):
            hints.append(f"Extra closing {name} '{cl}'. Remove the unmatched one.")
    # JS missing semicolons (very loose hint)
    js_lines = [l.strip() for l in code.split("\n") if l.strip()]
    for l in js_lines:
        if re.match(r"^(let|const|var|return)\b.*[^;{}\s]$", l) and not l.endswith(("{","}")):
            hints.append(f"Statement `{l}` may be missing a semicolon `;`.")
            break
    # Unclosed string
    if (code.count("'") % 2) or (code.count('"') % 2):
        hints.append("Unclosed string literal — make sure every quote has a matching pair.")
    if not hints:
        return "No obvious issues detected. The code looks syntactically reasonable."
    return "\n".join(f"• {h}" for h in hints)

# ---- Routes ----
@app.route("/")
def index():
    return send_from_directory(str(FRONTEND), "index.html")

@app.post("/predict")
def predict():
    data = request.get_json(force=True)
    code = data.get("code", "")
    if not code.strip():
        return jsonify({"label": "clean", "confidence": 0.0})
    pred = model.predict([code])[0]
    proba = model.predict_proba([code])[0]
    classes = list(model.classes_)
    conf = float(proba[classes.index(pred)])
    return jsonify({"label": pred, "confidence": round(conf, 3)})

@app.post("/debug")
def debug():
    data = request.get_json(force=True)
    code = data.get("code", "")
    if not code.strip():
        return jsonify({"suggestion": "Please enter some code first."})
    return jsonify({"suggestion": llm_debug(code)})

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
