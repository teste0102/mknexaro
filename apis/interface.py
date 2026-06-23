#!/usr/bin/env python3
from flask import Flask, render_template_string, jsonify, request
import requests

app = Flask(__name__)

HTML = '''<!DOCTYPE html><html><head><meta charset="utf-8"><title>MK Gerenciador</title><style>
*{margin:0;padding:0}body{background:#0E1430;color:white;font-family:Arial}
.header{background:#1a2540;padding:20px;text-align:center;border-bottom:2px solid #00d4ff}
h1{color:#00d4ff}.container{max-width:1000px;margin:20px auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px}
.card{background:#1a2540;padding:20px;border-radius:10px;border:2px solid #00d4ff}
.card h2{color:#00d4ff}.status-online{color:#1abc9c;font-weight:bold}
button{background:#00d4ff;color:#0E1430;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;font-weight:bold;margin-top:10px}
button:hover{background:#1abc9c}
</style></head><body>
<div class="header"><h1>🔗 MK Gerenciador Central</h1></div>
<div class="container">
<div class="card"><h2>📧 Email</h2><p class="status-online">✅ Online (8100)</p><button onclick="executar('email')">Abrir</button></div>
<div class="card"><h2>🏪 Loja</h2><p class="status-online">✅ Online (8101)</p><button onclick="executar('loja')">Abrir</button></div>
<div class="card"><h2>🐙 GitHub</h2><p class="status-online">✅ Online (8102)</p><button onclick="executar('github')">Abrir</button></div>
</div>
<script>function executar(tipo){alert('Clicou: ' + tipo)}</script>
</body></html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(port=9000, debug=False)

