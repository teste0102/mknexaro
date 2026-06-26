#!/usr/bin/env python3
"""MK Agent - Haiku 4.5 + Execução"""
import whisper, subprocess, os, anthropic
from gtts import gTTS

# Carrega chave
with open(os.path.expanduser('~/.mk-api-key')) as f:
    api_key = f.read().strip()

model = whisper.load_model("medium")
client = anthropic.Anthropic(api_key=api_key)

print("🎤 MK AGENT - Haiku 4.5\n")

while True:
    try:
        print("🔴 Fale agora...")
        os.system("rec -r 16000 -c 1 -b 16 /tmp/mk_voz.wav trim 0 10 2>/dev/null")
        
        resultado = model.transcribe("/tmp/mk_voz.wav", language="pt")
        texto = resultado["text"]
        print(f"📝 {texto}")
        
        if "mk" not in texto.lower():
            print("⏭️  \n")
            continue
        
        pergunta = texto.lower().replace("mk", "").strip()
        if not pergunta:
            continue
        
        print(f"❓ {pergunta}")
        print("⏳ Pensando...")
        
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role":"user","content":f"Comando: {pergunta}. Responda e execute se necessário."}]
        )
        
        resposta = response.content[0].text
        print(f"🤖 {resposta}\n")
        
        if "google" in pergunta.lower():
            os.system("firefox https://google.com &")
        
        tts = gTTS(resposta, lang='pt-br')
        tts.save('/tmp/mk_resposta.mp3')
        subprocess.run(["mpg123", "-q", "/tmp/mk_resposta.mp3"])
        print()
        
    except KeyboardInterrupt:
        print("\nAté logo! 👋")
        break

