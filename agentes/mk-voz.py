#!/usr/bin/env python3
import whisper, requests, os, subprocess, time
from gtts import gTTS

print("Carregando Whisper Medium...")
model = whisper.load_model("medium")

print("🎤 MK AGENT\n")

while True:
    try:
        print("🔴 Fale agora...")
        os.system("rec -r 16000 -c 1 -b 16 /tmp/mk_voz.wav trim 0 10 2>/dev/null")
        
        resultado = model.transcribe("/tmp/mk_voz.wav", language="pt")
        texto = resultado["text"].strip()
        print(f"📝 {texto}")
        
        if "mk" not in texto.lower():
            print("⏭️  \n")
            continue
        
        pergunta = texto.lower().replace("mk", "").strip()
        if not pergunta:
            continue
        
        print(f"❓ {pergunta}")
        print("⏳ Pensando...")
        
        # Modelo RÁPIDO
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model":"qwen3:8b", "prompt":pergunta, "stream":False},
                timeout=60
            )
            resposta = resp.json()["response"]
        except:
            resposta = "Desculpe, não consegui processar agora. Tente novamente."
        
        print(f"🤖 {resposta[:80]}...\n")
        
        tts = gTTS(resposta, lang='pt-br')
        tts.save('/tmp/mk_resposta.mp3')
        subprocess.run(["mpg123", "/tmp/mk_resposta.mp3"], stdout=subprocess.DEVNULL)
        print()
        
    except KeyboardInterrupt:
        print("\nAté logo! 👋")
        break

