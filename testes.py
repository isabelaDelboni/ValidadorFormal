"""
testes.py — Bateria completa de testes para os três reconhecedores.

Uso:
    python testes.py                  # roda todos os testes
    python testes.py --verbose        # mostra execução passo a passo
    python testes.py --nivel lr       # só testa Linguagem Regular
    python testes.py --nivel llc      # só testa Linguagem Livre de Contexto
    python testes.py --nivel r        # só testa Linguagem Recursiva

Estrutura dos arquivos de teste (.txt):
    cadeia<TAB>ACEITA|REJEITA
    Linhas com # são comentários; linhas em branco são ignoradas.
"""

import sys
import os
import argparse
import time
from pathlib import Path

# Ajusta o path para importar os módulos de src/
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from regular       import reconhece_cpf
from livre_contexto import reconhece_balanceamento
from recursiva     import reconhece_ww

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VERDE  = '\033[92m'
VERME  = '\033[91m'
AMARELO = '\033[93m'
AZUL   = '\033[94m'
RESET  = '\033[0m'
NEGRITO = '\033[1m'

def cor(texto, codigo):
    return f"{codigo}{texto}{RESET}"


def parse_test_file(path: Path) -> list[tuple[str, str]]:
    """Lê arquivo de testes e retorna lista de (cadeia, esperado)."""
    casos = []
    with open(path, encoding='utf-8') as f:
        for linha in f:
            linha = linha.rstrip('\n')
            if linha.startswith('#') or not linha.strip():
                continue
            partes = linha.split('\t')
            if len(partes) == 2:
                cadeia, esperado = partes[0], partes[1].strip()
                casos.append((cadeia, esperado))
    return casos


def roda_bateria(nome: str, reconhecedor, casos: list, verbose: bool = False) -> dict:
    """
    Executa uma bateria de testes e imprime tabela de resultados.
    Retorna dicionário com estatísticas.
    """
    print(f"\n{'='*70}")
    print(cor(f"  NÍVEL: {nome}", NEGRITO + AZUL))
    print(f"{'='*70}")
    print(f"  {'#':<4} {'Cadeia':<30} {'Esperado':<10} {'Obtido':<10} {'Passos':<8} {'Status'}")
    print(f"  {'-'*68}")

    total = 0
    corretos = 0
    total_passos = 0
    passos_por_caso = []

    for i, (cadeia, esperado) in enumerate(casos, 1):
        if verbose:
            aceito, passos = reconhecedor(cadeia, verbose=True)
        else:
            aceito, passos = reconhecedor(cadeia)

        obtido = "ACEITA" if aceito else "REJEITA"
        correto = (obtido == esperado)

        status = cor("✓ OK", VERDE) if correto else cor("✗ FALHA", VERME)
        cadeia_display = repr(cadeia) if len(cadeia) > 28 else f"'{cadeia}'"

        print(f"  {i:<4} {cadeia_display:<30} {esperado:<10} {obtido:<10} {passos:<8} {status}")

        total += 1
        corretos += correto
        total_passos += passos
        passos_por_caso.append(passos)

    taxa = corretos / total * 100 if total else 0
    print(f"  {'-'*68}")
    print(f"  Resultado: {corretos}/{total} corretos ({taxa:.0f}%) | "
          f"Total de passos: {total_passos} | Média: {total_passos/total:.1f}")

    return {
        'nome': nome,
        'total': total,
        'corretos': corretos,
        'total_passos': total_passos,
        'passos_por_caso': passos_por_caso,
    }


def execucao_passo_a_passo(nome: str, reconhecedor, aceita: str, rejeita: str):
    """Demonstra execução passo a passo de uma cadeia aceita e uma rejeitada."""
    print(f"\n{'='*70}")
    print(cor(f"  EXECUÇÃO PASSO A PASSO — {nome}", NEGRITO + AMARELO))
    print(f"{'='*70}")

    print(f"\n--- Cadeia ACEITA: '{aceita}' ---")
    reconhecedor(aceita, verbose=True)

    print(f"\n--- Cadeia REJEITADA: '{rejeita}' ---")
    reconhecedor(rejeita, verbose=True)


def resumo_final(resultados: list[dict]):
    """Imprime resumo comparativo entre os três níveis."""
    print(f"\n{'='*70}")
    print(cor("  RESUMO COMPARATIVO — Hierarquia LR ⊊ LLC ⊊ R", NEGRITO))
    print(f"{'='*70}")
    print(f"  {'Nível':<35} {'Corretos':<12} {'Total Passos':<15} {'Média Passos'}")
    print(f"  {'-'*68}")
    for r in resultados:
        media = r['total_passos'] / r['total'] if r['total'] else 0
        print(f"  {r['nome']:<35} {r['corretos']}/{r['total']:<10} "
              f"{r['total_passos']:<15} {media:.1f}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Bateria de testes — Validador Formal em Três Níveis')
    parser.add_argument('--verbose', '-v', action='store_true', help='Execução passo a passo')
    parser.add_argument('--nivel', choices=['lr', 'llc', 'r'], default=None,
                        help='Rodar apenas um nível')
    parser.add_argument('--passo-a-passo', action='store_true',
                        help='Mostra execução passo a passo de um aceito e um rejeitado por nível')
    args = parser.parse_args()

    base = Path(__file__).parent / 'testes'
    resultados = []

    niveis = [
        ('Linguagem Regular (DFA — CPF)',
         reconhece_cpf,
         base / 'testes_regular.txt',
         'lr',
         '123.456.789-00',
         '12.34.56-78'),
        ('Linguagem Livre de Contexto (PDA)',
         reconhece_balanceamento,
         base / 'testes_livre_contexto.txt',
         'llc',
         '((x+y)*z)',
         '((a+b)'),
        ('Linguagem Recursiva (MT — w#w)',
         reconhece_ww,
         base / 'testes_recursiva.txt',
         'r',
         '101#101',
         '101#100'),
    ]

    for nome, reconhecedor, arquivo, tag, ex_aceita, ex_rejeita in niveis:
        if args.nivel and args.nivel != tag:
            continue

        casos = parse_test_file(arquivo)
        resultado = roda_bateria(nome, reconhecedor, casos, verbose=args.verbose)
        resultados.append(resultado)

        if args.passo_a_passo or args.verbose:
            execucao_passo_a_passo(nome, reconhecedor, ex_aceita, ex_rejeita)

    if len(resultados) > 1:
        resumo_final(resultados)

    # Código de saída: 0 se todos corretos, 1 caso contrário
    todos_ok = all(r['corretos'] == r['total'] for r in resultados)
    sys.exit(0 if todos_ok else 1)


if __name__ == '__main__':
    main()
