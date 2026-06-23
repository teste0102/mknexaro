#!/usr/bin/env python3
"""MK Web - Whisper + Haiku"""
from flask import Flask, render_template_string, request, jsonify
import whisper, anthropic, os

app = Flask(__name__)
client = anthropic.Anthropic()
model_whisper = whisper.load_model("medium")

HTML = '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>MK Agent</title><style>body{font-family:Arial;margin:0;background:#0E1430;color:white}.container{max-width:600px;margin:50px auto;background:#1a2540;padding:30px;border-radius:10px}h1{color:#00d4ff;text-align:center}.chat{height:400px;overflow-y:auto;border:2px solid #00d4ff;padding:10px;margin:20px 0;background:#0E1430;border-radius:5px}.msg{margin:10px 0;padding:10px;border-radius:5px}.user{background:#00d4ff;color:#0E1430;text-align:right}.mk{background:#1abc9c}#mic-btn{padding:15px 40px;background:#ff4444;color:white;border:none;border-radius:50px;cursor:pointer;font-size:16px;font-weight:bold;width:100%;margin:10px 0}#mic-btn.recording{background:#ffaa00}</style></head><body><div class="container"><h1>🎤 MK Agent</h1><div class="chat" id="chat"></div><button id="mic-btn">🎤 HOLD TO TALK</button></div><script>let mediaRecorder,audioChunks=[];const btn=document.getElementById("mic-btn");btn.addEventListener("mousedown",iniciar);btn.addEventListener("mouseup",parar);async function iniciar(){audioChunks=[];const stream=await navigator.mediaDevices.getUserMedia({audio:true});mediaRecorder=new MediaRecorder(stream);btn.classList.add("recording");btn.textContent="🔴 GRAVANDO";mediaRecorder.ondataavailable=e=>audioChunks.push(e.data);mediaRecorder.start()}async function parar(){btn.classList.remove("recording");btn.textContent="🎤 HOLD TO TALK";mediaRecorder.stop();mediaRecorder.onstop=async()=>{const blob=new Blob(audioChunks,{type:"audio/wav"}),fd=new FormData();fd.append("audio",blob);const r=await fetch("/processar",{method:"POST",body:fd}).then(x=>x.json());addMsg("user",r.texto);const r2=await fetch("/responder",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({texto:r.texto})}).then(x=>x.json());addMsg("mk",r2.resposta)}}function addMsg(t,m){const c=document.getElementById("chat"),d=document.createElement("div");d.className="msg "+t;d.textContent=m;c.appendChild(d);c.scrollTop=c.scrollHeight}</script></body></html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/processar', methods=['POST'])
def processar():
    audio = request.files.get('audio')
    audio.save('/tmp/mk_audio.wav')
    resultado = model_whisper.transcribe('/tmp/mk_audio.wav', language='pt')
    return jsonify({'texto': resultado['text']})

@app.route('/responder', methods=['POST'])
def responder():
    texto = request.json.get('texto')
    msg = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=300,
        messages=[{'role':'user','content':texto}]
    )
    return jsonify({'resposta': msg.content[0].text})

if __name__ == '__main__':
    app.run(port=5000, debug=False)

