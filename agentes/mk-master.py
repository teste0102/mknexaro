#!/usr/bin/env python3
"""MK Master - Agente integrado com voz, skills e web"""
import whisper, subprocess, os, anthropic
from gtts import gTTS
from datetime import datetime

with open(os.path.expanduser('~/.mk-api-key')) as f:
    api_key = f.read().strip()

model = whisper.load_model("medium")
client = anthropic.Anthropic(api_key=api_key)

historico = []

def processar_comando(texto):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role":"user","content":texto}]
    )
    return response.content[0].text

print("🎤 MK MASTER AGENT\n")

while True:
    try:
        print("🔴 Fale agora...")
        os.system("rec -r 16000 -c 1 -b 16 /tmp/mk_audio.wav trim 0 10 2>/dev/null")
        
        resultado = model.transcribe("/tmp/mk_audio.wav", language="pt")
        texto = resultado["text"].strip()
        print(f"📝 {texto}")
        
        if "mk" not in texto.lower():
            print("⏭️  \n")
            continue
        
        comando = texto.lower().replace("mk", "").strip()
        if not comando:
            continue
        
        print(f"❓ {comando}")
        resposta = processar_comando(comando)
        print(f"🤖 {resposta}\n")
        
        tts = gTTS(resposta, lang='pt-br')
        tts.save('/tmp/mk_resposta.mp3')
        subprocess.run(["mpg123", "-q", "/tmp/mk_resposta.mp3"])
        
    except KeyboardInterrupt:
        print("\nAté logo! 👋")
        break

