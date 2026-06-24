#!/usr/bin/env python3
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'interface': 'mcpo', 'porta': 8764, 'status': 'online'})

@app.route('/executar', methods=['POST'])
def executar():
    dados = request.json
    comando = dados.get('comando', '')
    
    resp = requests.post("http://localhost:8110/executar",
                        json={"comando": comando})
    return jsonify(resp.json())

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'interface': 'mcpo', 'porta': 8764, 'integrador': 8110})

if __name__ == '__main__':
    app.run(port=8764, debug=False)

