"""
Reconhecedor de Linguagem Regular (LR)
Linguagem: CPF no formato ddd.ddd.ddd-dd
Modelo: Autômato Finito Determinístico (DFA)
"""

import sys

ALFABETO = set("0123456789.-")

# Definição dos estados do autômato
ESTADO_INICIAL = 0
ESTADOS_FINAIS = {14}
ESTADO_MORTO = 15

DIGITOS = set("0123456789")


def _construir_tabela_de_transicao():
    """Constrói a tabela de transição do DFA como dicionário."""
    tabela = {}

    # Inicializa tudo enviando para o estado morto por padrão
    for estado in range(16):
        for simbolo in ALFABETO:
            tabela[(estado, simbolo)] = ESTADO_MORTO
            
    # Estado morto continua nele mesmo
    for simbolo in ALFABETO:
        tabela[(ESTADO_MORTO, simbolo)] = ESTADO_MORTO

    # Transições para leitura de cada dígito do CPF
    pares_digito = [
        (0, 1), (1, 2), (2, 3),          # Primeiro bloco: ddd
        (4, 5), (5, 6), (6, 7),          # Segundo bloco: ddd
        (8, 9), (9, 10), (10, 11),       # Terceiro bloco: ddd
        (12, 13), (13, 14)               # Dígitos verificadores: dd
    ]
    
    for (origem, destino) in pares_digito:
        for d in DIGITOS:
            tabela[(origem, d)] = destino

    # Transições dos caracteres separadores
    tabela[(3, '.')] = 4
    tabela[(7, '.')] = 8
    tabela[(11, '-')] = 12

    return tabela


TABELA_TRANSICAO = _construir_tabela_de_transicao()


def reconhecer_cpf(cadeia, verbose=False):
    estado_atual = ESTADO_INICIAL
    contador_passos = 0

    if verbose:
        print("\n" + "-"*55)
        print(" Simulação DFA - Validador de CPF")
        print(f" Entrada : '{cadeia}'")
        print("-"*55)
        print(" Passo | Símbolo | Estado Anterior | Próximo Estado")
        print("-"*55)

    for simbolo in cadeia:
        if simbolo not in ALFABETO:
            if verbose:
                print(f" Símbolo '{simbolo}' inválido -> REJEITADO")
            return False, contador_passos

        proximo_estado = TABELA_TRANSICAO[(estado_atual, simbolo)]
        contador_passos += 1

        if verbose:
            print(f" {contador_passos} | '{simbolo}' | q{estado_atual} | q{proximo_estado}")

        estado_atual = proximo_estado

    aceito = estado_atual in ESTADOS_FINAIS

    if verbose:
        print("-"*55)
        print(f" Estado final: q{estado_atual}")
        if aceito:
            print(" Resultado : ACEITO")
        else:
            print(" Resultado : REJEITADO")
        print(f" Passos : {contador_passos}")
        print("-"*55 + "\n")

    return aceito, contador_passos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python regular.py <cadeia>")
        print("Ex : python regular.py '123.456.789-00'")
        sys.exit(1)

    entrada = sys.argv[1]
    resultado, passos = reconhecer_cpf(entrada, verbose=True)
    sys.exit(0 if resultado else 1)