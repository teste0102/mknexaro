#!/usr/bin/env python3
"""
Buscar Shopee - Interface Principal
Fluxo: Coleta Manual → Excel → Comparador
"""
import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

def menu_principal():
    """Menu interativo"""
    print("\n" + "="*60)
    print("  🛍️  BUSCAR SHOPEE - Sistema de Comparação de Preços")
    print("="*60)
    print("\n1. 📋 Criar template Excel para coleta")
    print("2. 🔍 Comparar preços de múltiplas fontes")
    print("3. 📖 Ver guia de coleta manual")
    print("4. 📁 Abrir pasta de dados")
    print("5. ❌ Sair")
    print("\nEscolha uma opção (1-5): ", end="")

    escolha = input().strip()
    return escolha

def criar_template(termo):
    """Criar template Excel"""
    print(f"\n📊 Criando template para: {termo}")
    try:
        result = subprocess.run(
            ['python3', 'criar_excel_coleta.py', termo],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Erro: {result.stderr}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def comparar_precos(termo):
    """Usar comparador"""
    print(f"\n🔍 Comparando preços para: {termo}")

    pasta_dados = Path.home() / 'dados_produtos'
    if not pasta_dados.exists():
        print("⚠️  Pasta de dados não encontrada!")
        print(f"   Crie em: {pasta_dados}")
        return

    print("\n📂 Pastas encontradas:")
    pastas = [d for d in pasta_dados.iterdir() if d.is_dir()]
    for i, pasta in enumerate(pastas, 1):
        count = len(list(pasta.glob('*.xlsx')))
        print(f"   {i}. {pasta.name} ({count} arquivos)")

    if not pastas:
        print("   Nenhuma pasta encontrada!")
        return

    print("\nUsando comparador.py...")
    print("(Este script precisa de GUI Tkinter para mostrar resultados)")

def ver_guia():
    """Mostrar guia"""
    guia_path = Path(__file__).parent / 'GUIA_COLETA.md'
    if guia_path.exists():
        with open(guia_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("❌ Guia não encontrado!")

def abrir_pasta():
    """Abrir pasta de dados"""
    pasta = Path.home() / 'dados_produtos'
    pasta.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Pasta: {pasta}")
    print("\nConteúdo:")

    if list(pasta.glob('**/*.xlsx')):
        for arquivo in sorted(pasta.glob('**/*.xlsx')):
            relativo = arquivo.relative_to(pasta)
            print(f"   • {relativo}")
    else:
        print("   (vazia - crie templates para começar)")

    print(f"\n💡 Dica: Abra a pasta manualmente em:")
    print(f"   xdg-open '{pasta}'  (Linux)")
    print(f"   open '{pasta}'      (Mac)")

def main():
    while True:
        escolha = menu_principal()

        if escolha == '1':
            termo = input("\n🔍 Termo de busca: ").strip()
            if termo:
                criar_template(termo)
                input("\nPressione Enter para continuar...")

        elif escolha == '2':
            termo = input("\n🔍 Termo para comparar: ").strip()
            if termo:
                comparar_precos(termo)
                input("\nPressione Enter para continuar...")

        elif escolha == '3':
            ver_guia()
            input("\nPressione Enter para continuar...")

        elif escolha == '4':
            abrir_pasta()
            input("\nPressione Enter para continuar...")

        elif escolha == '5':
            print("\n👋 Até logo!")
            break

        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Se passou argumento, usar diretamente
        if sys.argv[1] == '--help':
            print("Uso: python3 run.py [opção] [termo]")
            print("  python3 run.py                    # Menu interativo")
            print("  python3 run.py template 'termo'   # Criar template")
            print("  python3 run.py comparar 'termo'   # Comparar preços")
        elif sys.argv[1] == 'template' and len(sys.argv) > 2:
            criar_template(sys.argv[2])
        elif sys.argv[1] == 'comparar' and len(sys.argv) > 2:
            comparar_precos(sys.argv[2])
        else:
            print("❌ Opção desconhecida")
            print("Use: python3 run.py --help")
    else:
        # Menu interativo
        main()
