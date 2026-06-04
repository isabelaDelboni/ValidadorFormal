"""
testes.py – Bateria completa de testes para os três reconhecedores.

Uso:
    python testes.py
    python testes.py --verbose
    python testes.py --passo-a-passo
"""

import sys
import os

# Coloca a pasta src no path pra conseguir importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from regular import reconhecer_cpf
from livre_contexto import reconhecer_expressao
from recursiva import reconhecer_copia


def carregar_testes(caminho_arquivo):
    casos = []
    with open(caminho_arquivo, encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            
            # Ignora se a linha for vazia ou só comentário puro
            if not linha or linha.startswith('#'):
                continue
                
            if '|' in linha:
                partes = linha.rsplit('|', 1)
                cadeia = partes[0].strip()
                esperado = partes[1].strip().lower()
                
                if esperado in ('aceito', 'rejeitado'):
                    casos.append((cadeia, esperado))
    return casos


def executar_bateria(nome_nivel, funcao_reconhecer, casos_de_teste, modo_verbose=False, modo_passo_a_passo=False):
    print("\n" + "="*50)
    print(f" NÍVEL: {nome_nivel}")
    print("="*50)
    print(" Cadeia | Esperado | Obtido | Passos | OK?")
    print("-"*50)

    total_corretos = 0
    total_passos = 0
    mostrou_aceito = False
    mostrou_rejeitado = False

    for i, (cadeia, esperado) in enumerate(casos_de_teste, 1):
        mostrar_detalhe = modo_verbose

        if modo_passo_a_passo:
            if esperado == 'aceito' and not mostrou_aceito:
                mostrar_detalhe = True
                mostrou_aceito = True
            elif esperado == 'rejeitado' and not mostrou_rejeitado:
                mostrar_detalhe = True
                mostrou_rejeitado = True

        resultado_bool, passos = funcao_reconhecer(cadeia, verbose=mostrar_detalhe)
        obtido = 'aceito' if resultado_bool else 'rejeitado'
        correto = (obtido == esperado)

        if correto:
            total_corretos += 1
        total_passos += passos

        simbolo = 'OK' if correto else 'ERRO'

        print(f" {cadeia} | {esperado} | {obtido} | {passos} | {simbolo}")

    total_testes = len(casos_de_teste)
    print("-"*50)
    print(f" Resultado: {total_corretos}/{total_testes} corretos | Passos totais: {total_passos}")

    return total_testes, total_corretos, total_passos


def main():
    modo_verbose = '--verbose' in sys.argv
    modo_passo_a_passo = '--passo-a-passo' in sys.argv

    base_dir = os.path.dirname(__file__)

    # Carrega as pastas de teste
    casos_regular = carregar_testes(os.path.join(base_dir, 'testes', 'testes_regular.txt'))
    casos_livre_contexto = carregar_testes(os.path.join(base_dir, 'testes', 'testes_livre_contexto.txt'))
    casos_recursiva = carregar_testes(os.path.join(base_dir, 'testes', 'testes_recursiva.txt'))

    print("\n" + "="*50)
    print("      VALIDADOR FORMAL - BATERIA DE TESTES")
    print("="*50)

    # Roda os testes para cada um
    t1, c1, p1 = executar_bateria("Regular (CPF)", reconhecer_cpf, casos_regular, modo_verbose, modo_passo_a_passo)
    t2, c2, p2 = executar_bateria("Livre Contexto (Delimitadores)", reconhecer_expressao, casos_livre_contexto, modo_verbose, modo_passo_a_passo)
    t3, c3, p3 = executar_bateria("Recursiva (w#w)", reconhecer_copia, casos_recursiva, modo_verbose, modo_passo_a_passo)

    # Resumo final
    total_t = t1 + t2 + t3
    total_c = c1 + c2 + c3
    total_p = p1 + p2 + p3

    print("\n" + "="*50)
    print(" RESUMO GERAL")
    print("="*50)
    print(f" Regular: {c1}/{t1} corretos (Passos: {p1})")
    print(f" Livre Contexto: {c2}/{t2} corretos (Passos: {p2})")
    print(f" Recursiva: {c3}/{t3} corretos (Passos: {p3})")
    print("-"*50)
    
    print(f" TOTAL: {total_c}/{total_t} corretos | Passos totais: {total_p}")
    print("="*50 + "\n")

    if total_c != total_t:
        sys.exit(1)


if __name__ == "__main__":
    main()