#!/usr/bin/env python3
"""MK Web UI - Haiku 4.5 Integrado"""
from flask import Flask, render_template_string, request, jsonify
import subprocess, whisper, anthropic, os, webbrowser, threading

# Carrega chave segura
with open(os.path.expanduser('~/.mk-api-key')) as f:
    api_key = f.read().strip()

app = Flask(__name__)
model = whisper.load_model("medium")
client = anthropic.Anthropic(api_key=api_key)

HTML = '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>MK Agent</title><style>
*{margin:0;padding:0}body{background:#0E1430;color:white;font-family:Arial;height:100vh}
.container{max-width:700px;height:100vh;display:flex;flex-direction:column;background:#0E1430}
header{background:#1a2540;padding:20px;text-align:center;border-bottom:2px solid #00d4ff}
h1{color:#00d4ff;font-size:28px}
.chat{flex:1;overflow-y:auto;padding:20px;background:#0E1430}
.msg{margin:15px 0;padding:15px;border-radius:8px;max-width:80%;word-wrap:break-word}
.user{background:#00d4ff;color:#0E1430;margin-left:auto;text-align:right}
.mk{background:#1abc9c;color:white}
footer{background:#1a2540;padding:20px;border-top:2px solid #00d4ff}
#btn{width:100%;padding:15px;background:#ff4444;color:white;border:none;border-radius:8px;cursor:pointer;font-size:16px;font-weight:bold}
#btn:hover{background:#ff6666}#btn.rec{background:#ffaa00}#status{text-align:center;color:#00d4ff;margin-bottom:10px;font-size:14px}
</style></head><body><div class="container"><header><h1>🎤 MK Agent - Haiku 4.5</h1></header>
<div class="chat" id="chat"></div><footer><div id="status">Pronto</div><button id="btn">🎤 HOLD TO TALK</button></footer></div>
<script>const btn=document.getElementById("btn");let rec=false;
btn.addEventListener("mousedown",()=>{rec=true;btn.classList.add("rec");btn.textContent="🔴 GRAVANDO";fetch("/start")});
btn.addEventListener("mouseup",()=>{rec=false;btn.classList.remove("rec");btn.textContent="🎤 HOLD TO TALK";
fetch("/stop").then(r=>r.json()).then(d=>{addMsg("user",d.texto);
fetch("/processar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({texto:d.texto})})
.then(r=>r.json()).then(d=>{addMsg("mk",d.resposta);document.getElementById("status").textContent="Pronto"})})});
function addMsg(t,m){const c=document.getElementById("chat"),e=document.createElement("div");e.className="msg "+t;
e.textContent=m;c.appendChild(e);c.scrollTop=c.scrollHeight}</script></body></html>'''

def open_browser():
    webbrowser.open('http://localhost:5000')

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/start')
def start():
    subprocess.Popen(['rec', '-r', '16000', '-c', '1', '-b', '16', '/tmp/mk.wav'])
    return jsonify({'ok': True})

@app.route('/stop')
def stop():
    os.system('pkill -f "rec.*mk.wav"')
    resultado = model.transcribe('/tmp/mk.wav', language='pt')
    return jsonify({'texto': resultado['text']})

@app.route('/processar', methods=['POST'])
def processar():
    texto = request.json.get('texto')
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role":"user","content":texto}]
    )
    resposta = msg.content[0].text
    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    timer = threading.Timer(1, open_browser)
    timer.daemon = True
    timer.start()
    app.run(port=5000, debug=False)

