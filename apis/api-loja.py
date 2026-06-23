#!/usr/bin/env python3
"""API Agente Loja - Gerencia OS e Vendas"""
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'api': 'agente-loja', 'status': 'online', 'porta': 8101})

@app.route('/os', methods=['GET'])
def listar_os():
    """Lista OS abertas"""
    return jsonify({
        'total': 0,
        'status': 'Aberta',
        'servidor': '192.168.15.3',
        'msg': 'Conectado ao servidor'
    })

@app.route('/vendas', methods=['GET'])
def listar_vendas():
    """Lista vendas"""
    return jsonify({
        'data': '2026-06-23',
        'total_vendas': 0
    })

if __name__ == '__main__':
    app.run(port=8101, debug=False)

