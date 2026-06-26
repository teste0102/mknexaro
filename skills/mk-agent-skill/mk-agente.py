#!/usr/bin/env python3
"""MK Agent - Executa qualquer tarefa"""
import anthropic, subprocess, json

client = anthropic.Anthropic()

# Skills disponíveis
SKILLS = {
    "preço": "buscar-ml",
    "custa": "buscar-ml", 
    "shopee": "buscar-shopee",
    "buscar": "buscador"
}

def detecta_skill(comando):
    for palavra, skill in SKILLS.items():
        if palavra in comando.lower():
            return skill
    return None

def executa_skill(skill, comando):
    # Aqui seria executado a skill específica
    return f"Executando {skill} para: {comando}"

def mk_agente(comando):
    # Detecta skill
    skill = detecta_skill(comando)
    
    # Haiku processa e decide
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"Comando: {comando}\nSkill detectada: {skill or 'nenhuma'}\n\nResponda e execute a tarefa."
        }]
    )
    
    return response.content[0].text

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: mk-agente [comando]")
        sys.exit(1)
    
    comando = " ".join(sys.argv[1:])
    resultado = mk_agente(comando)
    print(resultado)

