"""
Reconhecedor de Linguagem Recursiva (R)
Linguagem: L = { w#w | w pertence a {0,1}* }
Modelo: Máquina de Turing
"""

import sys

BRANCO = 'B'
MARCADOR_ESQUERDA = 'X'
MARCADOR_DIREITA = 'Y'

ESTADO_INICIAL = 'q0'
ESTADO_ACEITO = 'q_aceito'
ESTADO_REJEITA = 'q_rejeita'

ESQUERDA = 'E'
DIREITA = 'D'

# Tabela de transição da Máquina de Turing
TABELA_TRANSICAO_MT = {
    # q0: Procura 0 ou 1 não marcado na esquerda
    ('q0', '0'): ('q1', MARCADOR_ESQUERDA, DIREITA),
    ('q0', '1'): ('q2', MARCADOR_ESQUERDA, DIREITA),
    ('q0', MARCADOR_ESQUERDA): ('q0', MARCADOR_ESQUERDA, DIREITA),
    ('q0', MARCADOR_DIREITA): ('q0', MARCADOR_DIREITA, DIREITA),
    ('q0', '#'): ('q6', '#', DIREITA),

    # q1: Memorizou 0, vai para a direita até o '#'
    ('q1', '0'): ('q1', '0', DIREITA),
    ('q1', '1'): ('q1', '1', DIREITA),
    ('q1', MARCADOR_ESQUERDA): ('q1', MARCADOR_ESQUERDA, DIREITA),
    ('q1', MARCADOR_DIREITA): ('q1', MARCADOR_DIREITA, DIREITA),
    ('q1', '#'): ('q3', '#', DIREITA),

    # q2: Memorizou 1, vai para a direita até o '#'
    ('q2', '0'): ('q2', '0', DIREITA),
    ('q2', '1'): ('q2', '1', DIREITA),
    ('q2', MARCADOR_ESQUERDA): ('q2', MARCADOR_ESQUERDA, DIREITA),
    ('q2', MARCADOR_DIREITA): ('q2', MARCADOR_DIREITA, DIREITA),
    ('q2', '#'): ('q4', '#', DIREITA),

    # q3: Memorizou 0, busca o '0' correspondente na direita
    ('q3', MARCADOR_DIREITA): ('q3', MARCADOR_DIREITA, DIREITA),
    ('q3', '0'): ('q5', MARCADOR_DIREITA, ESQUERDA),
    ('q3', '1'): (ESTADO_REJEITA, '1', ESQUERDA),
    ('q3', BRANCO): (ESTADO_REJEITA, BRANCO, ESQUERDA),

    # q4: Memorizou 1, busca o '1' correspondente na direita
    ('q4', MARCADOR_DIREITA): ('q4', MARCADOR_DIREITA, DIREITA),
    ('q4', '1'): ('q5', MARCADOR_DIREITA, ESQUERDA),
    ('q4', '0'): (ESTADO_REJEITA, '0', ESQUERDA),
    ('q4', BRANCO): (ESTADO_REJEITA, BRANCO, ESQUERDA),

    # q5: Volta para a esquerda até o sentinela B
    ('q5', '0'): ('q5', '0', ESQUERDA),
    ('q5', '1'): ('q5', '1', ESQUERDA),
    ('q5', '#'): ('q5', '#', ESQUERDA),
    ('q5', MARCADOR_ESQUERDA): ('q5', MARCADOR_ESQUERDA, ESQUERDA),
    ('q5', MARCADOR_DIREITA): ('q5', MARCADOR_DIREITA, ESQUERDA),
    ('q5', BRANCO): ('q0', BRANCO, DIREITA),

    # q6: Esquerda concluída, valida se sobrou algo na direita
    ('q6', MARCADOR_DIREITA): ('q6', MARCADOR_DIREITA, DIREITA),
    ('q6', BRANCO): (ESTADO_ACEITO, BRANCO, DIREITA),
    ('q6', '0'): (ESTADO_REJEITA, '0', DIREITA),
    ('q6', '1'): (ESTADO_REJEITA, '1', DIREITA),
}


def reconhecer_copia(cadeia, verbose=False):
    # Validação simples de caracteres
    for simbolo in cadeia:
        if simbolo not in {'0', '1', '#'}:
            if verbose:
                print(f" Caractere '{simbolo}' inválido!")
            return False, 0

    # Criação da fita com os brancos nas pontas
    fita = [BRANCO] + list(cadeia) + [BRANCO]
    cabeca = 1
    estado_atual = ESTADO_INICIAL
    contador_passos = 0

    if verbose:
        print("\n" + "-"*60)
        print(" Simulação MT - Cópia de Cadeia (w#w)")
        print(f" Entrada: '{cadeia}'")
        print("-"*60)
        print(" Passo | Estado | Pos | Lê | Escreve | Move | Fita")
        print("-"*60)

    limite_passos = 10000
    while estado_atual not in {ESTADO_ACEITO, ESTADO_REJEITA}:
        if contador_passos > limite_passos:
            if verbose:
                print(" Erro: Limite de passos estourado!")
            return False, contador_passos

        if cabeca >= len(fita):
            fita.append(BRANCO)

        simbolo_lido = fita[cabeca]
        chave = (estado_atual, simbolo_lido)

        if chave not in TABELA_TRANSICAO_MT:
            if verbose:
                print(f" Erro: Transição indefinida para {chave}")
            return False, contador_passos

        proximo_estado, simbolo_escrito, movimento = TABELA_TRANSICAO_MT[chave]
        fita[cabeca] = simbolo_escrito
        contador_passos += 1

        if verbose:
            fita_str = ''.join(fita)
            print(f" {contador_passos} | {estado_atual} | {cabeca} | '{simbolo_lido}' | '{simbolo_escrito}' | {movimento} | {fita_str}")

        if movimento == DIREITA:
            cabeca += 1
        else:
            cabeca = max(0, cabeca - 1)

        estado_atual = proximo_estado

    aceito = (estado_atual == ESTADO_ACEITO)

    if verbose:
        fita_str = ''.join(fita)
        print("-"*60)
        print(f" Estado final: {estado_atual}")
        print(f" Fita final : {fita_str}")
        print(f" Resultado : {'ACEITO' if aceito else 'REJEITADO'}")
        print(f" Passos : {contador_passos}")
        print("-"*60 + "\n")

    return aceito, contador_passos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python recursiva.py <cadeia>")
        print("Ex : python recursiva.py '101#101'")
        sys.exit(1)

    entrada = sys.argv[1]
    resultado, passos = reconhecer_copia(entrada, verbose=True)
    sys.exit(0 if resultado else 1)