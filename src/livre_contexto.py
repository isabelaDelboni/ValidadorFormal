"""
Reconhecedor de Linguagem Livre de Contexto (LLC)
Expressões com parênteses, colchetes e chaves balanceados
Modelo: PDA (Autômato com Pilha)
"""

import sys

# Configurações dos delimitadores e símbolos aceitos
MARCADOR_FUNDO = '$'
ABRE_DELIMITADOR = {'(': '(', '[': '[', '{': '{'}
FECHA_DELIMITADOR = {')': '(', ']': '[', '}': '{'}

SIMBOLOS_NEUTROS = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "+-*/^=_. ,!?;:|@#%&~"
)
ALFABETO_ENTRADA = set(ABRE_DELIMITADOR) | set(FECHA_DELIMITADOR) | SIMBOLOS_NEUTROS

ESTADO_INICIAL = 'q0'
ESTADOS_FINAIS = {'q0'}


def _transicao_pda(estado, simbolo, topo_pilha):
    """
    Função de transição do autômato.
    Retorna o próximo estado e a ação que deve ser feita na pilha.
    """
    if estado == 'q0':
        if simbolo in ABRE_DELIMITADOR:
            return ('q0', 'empilhar')
        elif simbolo in FECHA_DELIMITADOR:
            esperado = FECHA_DELIMITADOR[simbolo]
            if topo_pilha == esperado:
                return ('q0', 'desempilhar')
            else:
                return ('q0', 'rejeitar')
        elif simbolo in SIMBOLOS_NEUTROS:
            return ('q0', 'manter')
        else:
            return ('q0', 'rejeitar')
    return (estado, 'rejeitar')


def reconhecer_expressao(cadeia, verbose=False):
    estado_atual = ESTADO_INICIAL
    pilha = [MARCADOR_FUNDO]
    contador_passos = 0

    if verbose:
        print("\n" + "-"*50)
        print(" Simulação PDA - Delimitadores Balanceados")
        print(f" Entrada : '{cadeia}'")
        print("-"*50)
        print(" Passo | Símbolo | Estado | Ação | Pilha")
        print("-"*50)

    for simbolo in cadeia:
        if simbolo not in ALFABETO_ENTRADA:
            if verbose:
                print(f" Símbolo '{simbolo}' inválido -> REJEITADO")
            return False, contador_passos

        topo_pilha = pilha[-1] if pilha else None
        proximo_estado, acao = _transicao_pda(estado_atual, simbolo, topo_pilha)
        contador_passos += 1

        if acao == 'rejeitar':
            if verbose:
                print(f" {contador_passos} | {simbolo} | {estado_atual} | rejeitar | {pilha}")
                print("-"*50)
                print(" Resultado: REJEITADO (Erro de fechamento)")
                print(f" Passos : {contador_passos}")
                print("-"*50 + "\n")
            return False, contador_passos

        elif acao == 'empilhar':
            pilha.append(simbolo)
            contador_passos += 1

        elif acao == 'desempilhar':
            pilha.pop()
            contador_passos += 1

        if verbose:
            print(f" {contador_passos} | {simbolo} | {estado_atual} | {acao} | {pilha}")

        estado_atual = proximo_estado

    # Checa se terminou no estado certo e se limpou os delimitadores da pilha
    aceito = (estado_atual in ESTADOS_FINAIS) and (pilha == [MARCADOR_FUNDO])

    if verbose:
        print("-"*50)
        print(f" Estado final: {estado_atual} | Pilha final: {pilha}")
        if aceito:
            print(" Resultado : ACEITO")
        else:
            print(" Resultado : REJEITADO (Sobrou delimitador aberto)")
        print(f" Passos : {contador_passos}")
        print("-"*50 + "\n")

    return aceito, contador_passos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python livre_contexto.py <cadeia>")
        print("Ex : python livre_contexto.py '((x+y)*z)'")
        sys.exit(1)

    entrada = sys.argv[1]
    resultado, passos = reconhecer_expressao(entrada, verbose=True)
    sys.exit(0 if resultado else 1)