# Validador Formal em Três Níveis

Projeto prático de **Teoria da Computação** que implementa três reconhecedores formais, um para cada nível da hierarquia de Chomsky: LR ⊊ LLC ⊊ R.

## Estrutura do repositório

```text
projeto/
├── README.md
├── requirements.txt
├── testes.py                      # Executor da bateria completa (18 testes)
├── src/
│   ├── regular.py                 # DFA – CPF (ddd.ddd.ddd-dd)
│   ├── livre_contexto.py          # PDA – Delimitadores balanceados
│   ├── recursiva.py               # MT  – Cópia de cadeia (w#w)
│   └── gerar_diagramas.py         # Gera os gráficos dos autômatos
├── testes/                        # Arquivos com as cadeias de teste (entradas)
│   ├── testes_regular.txt
│   ├── testes_livre_contexto.txt
│   └── testes_recursiva.txt
└── diagramas/                     # Pasta gerada automaticamente com as imagens
    ├── dfa_regular.png
    ├── pda_livre_contexto.png
    └── mt_recursiva.png

```

---

## Pré-requisitos

O projeto foi desenvolvido para rodar nativamente em Python sem dependências complexas de sistema operacional.

```bash
python --version   # Recomendado: 3.9+
pip install -r requirements.txt

```

O arquivo `requirements.txt` contém apenas a biblioteca `matplotlib` (usada exclusivamente para desenhar os diagramas). Os reconhecedores lógicos (`src/*.py`) **não possuem dependências externas** e rodam puramente com bibliotecas padrão do Python.

---

## Como rodar a bateria de testes automática

O script principal `testes.py` varre as massas de teste e valida o comportamento de todos os modelos de uma só vez.

```bash
python testes.py

```

### Para que serve a pasta `testes/`?

Esta pasta armazena os arquivos de configuração de entrada (`.txt`) que alimentam o script automático. Cada arquivo contém uma lista de cadeias (uma por linha) categorizadas por um prefixo que dita o resultado esperado pelo autômato:

* `+` : Cadeia que **deve ser aceita** pelo reconhecedor.
* `-` : Cadeia que **deve ser rejeitada** pelo reconhecedor.

Isso permite modificar ou adicionar novos cenários de testes sem precisar alterar o código-fonte dos programas.

### Modos de exibição dos testes

* **Modo passo a passo (Uma aceita e uma rejeitada por nível):**
```bash
python testes.py --passo-a-passo

```


* **Modo verboso completo (Exibe a fita/estados de todas as cadeias):**
```bash
python testes.py --verbose

```



---

## Como rodar cada reconhecedor de forma autônoma

Todos os reconhecedores podem ser chamados individualmente passando a cadeia que deseja validar diretamente como argumento no terminal.

```bash
# LR – CPF
python src/regular.py "123.456.789-00"
python src/regular.py "12.34.56-78"

# LLC – Delimitadores
python src/livre_contexto.py "((x+y)*z)"
python src/livre_contexto.py "((a+b)"

# R – Cópia de cadeia
python src/recursiva.py "101#101"
python src/recursiva.py "101#100"

```

> **Nota:** O código de saída do processo no terminal é alterado dinamicamente: retorna `0` se a cadeia for aceita e `1` se for rejeitada, permitindo a integração direta com scripts de automação (Shell/PowerShell).

---

## Como gerar os diagramas dos autômatos

O projeto possui um script integrado que gera visualmente as estruturas de estados e transições de cada modelo.

Para desenhar os gráficos, basta executar:

```bash
python src/gerar_diagramas.py

```

O script criará automaticamente a pasta `diagramas/` na raiz do projeto e salvará as imagens `.png` das três máquinas modeladas, mapeando fielmente as transições exatas do código para a representação visual.

---

## Os três reconhecedores

### 1. Linguagem Regular (LR) — `src/regular.py`

| Item | Detalhe |
| --- | --- |
| **Linguagem** | CPF no formato `ddd.ddd.ddd-dd` |
| **Definição formal** | $L = \{ w \in \Sigma^* \mid w = d_1d_2d_3.d_4d_5d_6.d_7d_8d_9-d_{10}d_{11}, d_i \in \{0..9\} \}$ |
| **Alfabeto** | $\Sigma = \{0,1,...,9, '.', '-'\}$ |
| **Modelo** | DFA com 16 estados (q0…q14 + estado morto q15) |

A tabela de transição é declarada como dicionário `(estado, símbolo) → próximo_estado`. Um **passo** equivale a uma leitura de caractere com atualização de estado.

---

### 2. Linguagem Livre de Contexto (LLC) — `src/livre_contexto.py`

| Item | Detalhe |
| --- | --- |
| **Linguagem** | Expressões com `()`, `[]`, `{}` balanceados |
| **Definição formal** | $L = \{ w \in \Sigma^* \mid \text{todo abre-delimitador possui par correspondente na ordem correta} \}$ |
| **Alfabeto** | $\Sigma = \{(, ), [, ], \{, \}, a-z, A-Z, 0-9, +, -, *, /, ...\}$ |
| **Modelo** | PDA determinístico (DPDA) focado no controle de escopo |

A estrutura utiliza o conceito de pilha baseado em uma lista interna do Python. Um **passo** equivale à leitura de um delimitador somado à sua respectiva operação de empilhamento ou desempilhamento.

---

### 3. Linguagem Recursiva (R) — `src/recursiva.py`

| Item | Detalhe |
| --- | --- |
| **Linguagem** | Cópia de cadeia (w#w) |
| **Definição formal** | $L = \{ w\#w \mid w \in \{0,1\}^* \}$ |
| **Alfabeto** | $\Sigma = \{0, 1, \#\}$ |
| **Alfabeto da Fita** | $\Gamma = \{0, 1, \#, X, Y, B\}$ |
| **Modelo** | Máquina de Turing Determinística (MTD) com 8 estados funcionais |

Um **passo** computacional equivale ao ciclo completo de uma instrução da MT: leitura do símbolo atual na fita, escrita do novo caractere marcador, atualização do estado interno e o deslocamento físico da cabeça de leitura para a esquerda ou direita.

---

## Comparação de complexidade (passos)

| Nível | Modelo | Cadeia de Exemplo | Ordem de Complexidade |
| --- | --- | --- | --- |
| **LR** | DFA | `123.456.789-00` (14 passos) | $O(n)$ |
| **LLC** | PDA | `((x+y)*z)` (~13 passos) | $O(n)$ |
| **R** | MT | `101#101` (44 passos) | $O(n^2)$ |

A Máquina de Turing apresenta crescimento quadrático ($O(n^2)$) porque, para cada símbolo processado na metade esquerda da cerquilha (`#`), a cabeça precisa varrer e rebobinar a fita inteira até localizar e marcar seu par correspondente no bloco da direita.

---

## Equipe

* David Rocha Neto
* Isabela Escolaro Delboni 
* Mateus Henrique Escolaro