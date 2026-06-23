#!/usr/bin/env python3
"""Integrador Central - Unifica todas as APIs"""
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

APIS = {
    'email': 'http://localhost:8100',
    'loja': 'http://localhost:8101',
    'github': 'http://localhost:8102'
}

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'integrador': 'central',
        'porta': 8110,
        'apis_conectadas': APIS
    })

@app.route('/executar', methods=['POST'])
def executar():
    """Haiku chama isso para gerenciar tudo"""
    dados = request.json
    comando = dados.get('comando', '').lower()
    
    if 'email' in comando:
        resp = requests.get(f"{APIS['email']}/status")
        return jsonify({'tipo': 'email', 'resultado': resp.json()})
    
    elif 'loja' in comando or 'os' in comando:
        resp = requests.get(f"{APIS['loja']}/os")
        return jsonify({'tipo': 'loja', 'resultado': resp.json()})
    
    elif 'github' in comando or 'repo' in comando:
        resp = requests.get(f"{APIS['github']}/repos")
        return jsonify({'tipo': 'github', 'resultado': resp.json()})
    
    return jsonify({'erro': 'Comando não reconhecido'})

if __name__ == '__main__':
    app.run(port=8110, debug=False)

