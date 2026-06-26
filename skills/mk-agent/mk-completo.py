#!/usr/bin/env python3
"""MK Agent - Agente Inteligente Profissional"""
import whisper, requests, pyttsx3, os, json, time
from datetime import datetime
from pathlib import Path

# ===== CONFIGURAÇÕES =====
CONFIG = {
    "modelo": "qwen3.5:9b",
    "url": "http://localhost:11434/api/generate",
    "timeout": 120,
    "max_historico": 10,
    "arquivo_historico": os.path.expanduser("~/.mk-agent-historico.json")
}

SKILLS = {
    "preço": "buscar-ml",
    "custa": "buscar-ml",
    "valor": "buscar-ml",
    "shopee": "buscar-shopee",
    "mercado livre": "buscar-ml"
}

# ===== CARREGA WHISPER =====
print("📥 Carregando Whisper...")
model_whisper = whisper.load_model("base")

# ===== HISTÓRICO =====
def carrega_historico():
    if os.path.exists(CONFIG["arquivo_historico"]):
        with open(CONFIG["arquivo_historico"], "r") as f:
            return json.load(f)
    return []

def salva_historico(historico):
    with open(CONFIG["arquivo_historico"], "w") as f:
        json.dump(historico[-CONFIG["max_historico"]:], f, indent=2)

historico = carrega_historico()

# ===== DETECTA INTENÇÃO =====
def detecta_skill(texto):
    texto_lower = texto.lower()
    for palavra, skill in SKILLS.items():
        if palavra in texto_lower:
            return skill
    return None

# ===== PROCESSA COM QWEN3.5 =====
def mk_processa(texto, tentativa=1):
    try:
        contexto = "\n".join([f"Usuário: {h.get('usuario', '')}\nMK: {h.get('mk', '')}" 
                              for h in historico[-3:]])
        prompt = f"Contexto:\n{contexto}\n\nNova pergunta: {texto}\n\nResponda em português, objetivo e útil."
        
        resp = requests.post(
            CONFIG["url"],
            json={"model": CONFIG["modelo"], "prompt": prompt, "stream": False},
            timeout=CONFIG["timeout"]
        )
        return resp.json()["response"]
    except Exception as e:
        if tentativa < 3:
            print(f"⚠️  Retry {tentativa}...")
            time.sleep(2)
            return mk_processa(texto, tentativa + 1)
        return f"Erro ao processar: {str(e)}"

# ===== TTS =====
def mk_fala(texto):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 0.9)
        engine.say(texto[:200])
        engine.runAndWait()
    except:
        pass

# ===== MAIN =====
print("\n" + "="*60)
print("🤖 MK AGENT - Agente Inteligente")
print("="*60)
print("Comandos: [1] Falar  [2] Digitar  [3] Sair")
print("="*60 + "\n")

while True:
    try:
        modo = input("MK> ").strip()
        
        if modo == "1":
            print("🎤 Gravando (5 segundos)...")
            os.system("rec -r 16000 -c 1 -b 16 /tmp/mk_entrada.wav trim 0 5 2>/dev/null")
            resultado = model_whisper.transcribe("/tmp/mk_entrada.wav", language="pt")
            texto = resultado["text"].strip()
            
        elif modo == "2":
            texto = input("Você: ").strip()
            
        elif modo == "3":
            print("Até logo! 👋")
            break
        else:
            continue
        
        if not texto:
            continue
        
        print(f"\n📝 {texto}")
        
        # Detecta skill
        skill = detecta_skill(texto)
        if skill:
            print(f"💡 Skill detectada: {skill}")
        
        # Processa
        print("⏳ Pensando...")
        resposta = mk_processa(texto)
        
        # Salva histórico
        historico.append({
            "usuario": texto,
            "mk": resposta,
            "skill": skill,
            "timestamp": datetime.now().isoformat()
        })
        salva_historico(historico)
        
        # Exibe
        print(f"🤖 MK: {resposta[:150]}...\n")
        
        # Fala
        mk_fala(resposta)
        
    except KeyboardInterrupt:
        print("\n\nAtélogo! 👋")
        break
    except Exception as e:
        print(f"❌ Erro: {e}\n")

