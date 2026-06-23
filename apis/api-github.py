#!/usr/bin/env python3
"""API GitHub - Gerencia Repositórios"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'api': 'github', 'status': 'online', 'porta': 8102})

@app.route('/repos', methods=['GET'])
def listar_repos():
    """Lista repositórios"""
    return jsonify({
        'usuario': 'teste0102',
        'repos': ['mknexaro', 'Skills'],
        'total': 2
    })

@app.route('/commits/<repo>', methods=['GET'])
def commits(repo):
    """Últimos commits"""
    return jsonify({
        'repo': repo,
        'commits': 'últimos 5 commits'
    })

if __name__ == '__main__':
    app.run(port=8102, debug=False)

