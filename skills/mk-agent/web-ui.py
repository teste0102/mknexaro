#!/usr/bin/env python3
"""Web UI - Haiku + Qwen3"""
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>🎤 MK Agent</title>
    <style>
        body { font-family: Arial; margin: 0; background: #0E1430; color: white; }
        .container { max-width: 600px; margin: 50px auto; background: #1a2540; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
        h1 { color: #00d4ff; text-align: center; }
        .chat { height: 400px; overflow-y: auto; border: 2px solid #00d4ff; padding: 10px; margin: 20px 0; background: #0E1430; border-radius: 5px; }
        .msg { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #00d4ff; color: #0E1430; text-align: right; }
        .mk { background: #1abc9c; color: white; }
        .input-group { display: flex; gap: 10px; }
        input { flex: 1; padding: 10px; border: 2px solid #00d4ff; border-radius: 5px; background: #1a2540; color: white; }
        button { padding: 10px 20px; background: #00d4ff; color: #0E1430; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        button:hover { background: #1abc9c; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎤 MK Agent</h1>
        <div class="chat" id="chat"></div>
        <div class="input-group">
            <input type="text" id="input" placeholder="Fale com MK..." />
            <button onclick="enviar()">Enviar</button>
        </div>
    </div>
    <script>
        function enviar() {
            const texto = document.getElementById('input').value;
            if (!texto) return;
            
            addMsg('user', texto);
            document.getElementById('input').value = '';
            
            fetch('/falar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({texto: texto})
            })
            .then(r => r.json())
            .then(d => addMsg('mk', d.resposta));
        }
        
        function addMsg(tipo, texto) {
            const chat = document.getElementById('chat');
            const msg = document.createElement('div');
            msg.className = 'msg ' + tipo;
            msg.textContent = texto;
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/falar', methods=['POST'])
def falar():
    texto = request.json.get('texto', '')
    
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model":"qwen3:8b", "prompt":texto, "stream":False},
        timeout=120
    )
    resposta = resp.json()["response"]
    
    return jsonify({"resposta": resposta})

if __name__ == '__main__':
    app.run(port=5000, debug=False)

