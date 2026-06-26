#!/usr/bin/env python3
"""API para conectar Claude com MK"""
from flask import Flask, request, jsonify
import requests, json, os

app = Flask(__name__)

@app.route('/mk/falar', methods=['POST'])
def mk_falar():
    try:
        dados = request.json
        texto = dados.get('texto', '')
        
        # Qwen3.5 processa
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model":"qwen3.5:9b", "prompt":texto, "stream":False},
            timeout=120
        )
        resposta = resp.json()["response"]
        
        return jsonify({"resposta": resposta})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=False)
