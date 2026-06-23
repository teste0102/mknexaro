#!/usr/bin/env python3
"""API Email - Gerencia Gmail"""
from flask import Flask, request, jsonify
import imaplib, json, os

app = Flask(__name__)

# Config
EMAIL_ACCOUNT = "vinitar.usa@gmail.com"
IMAP_SERVER = "imap.gmail.com"

def conectar_gmail(senha):
    """Conecta ao Gmail"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, senha)
        return mail
    except:
        return None

@app.route('/listar', methods=['GET'])
def listar_emails():
    """Lista emails"""
    senha = request.args.get('senha')
    mail = conectar_gmail(senha)
    if not mail:
        return jsonify({'erro': 'Conexão falhou'}), 401
    
    mail.select('INBOX')
    status, messages = mail.search(None, 'ALL')
    total = len(messages[0].split())
    
    return jsonify({'total': total, 'conta': EMAIL_ACCOUNT})

@app.route('/deletar', methods=['POST'])
def deletar():
    """Deleta emails"""
    dados = request.json
    senha = dados.get('senha')
    criterio = dados.get('criterio')  # "AliExpress", "Shopee", etc
    
    mail = conectar_gmail(senha)
    if not mail:
        return jsonify({'erro': 'Conexão falhou'}), 401
    
    mail.select('INBOX')
    status, messages = mail.search(None, f'FROM "{criterio}"')
    
    deletados = 0
    for msg_id in messages[0].split():
        mail.store(msg_id, '+FLAGS', '\\Deleted')
        deletados += 1
    
    mail.expunge()
    mail.close()
    
    return jsonify({'deletados': deletados, 'criterio': criterio})

@app.route('/status', methods=['GET'])
def status():
    """Status da API"""
    return jsonify({'api': 'email-cleanup', 'status': 'online', 'porta': 8100})

if __name__ == '__main__':
    app.run(port=8100, debug=False)

