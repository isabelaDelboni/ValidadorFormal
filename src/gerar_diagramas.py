"""
Gerador de diagramas para os três reconhecedores usando Matplotlib.
Gera arquivos PNG em diagramas/.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt

# Define a pasta de diagramas na raiz do projeto
OUT = Path(__file__).parent.parent / 'diagramas'
if not OUT.exists():
    OUT.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# 1. DFA — CPF (regular.py)
# -----------------------------------------------------------------------------
def dfa_cpf():
    fig, ax = plt.subplots(figsize=(14, 3))
    ax.set_title("DFA - Validador de CPF", fontsize=12, fontweight='bold')
    
    for i in range(16):
        x = i * 1.5
        y = 1.0
        if i == 15:
            x = 7.5
            y = 0.2
            circle = plt.Circle((x, y), 0.3, color='#ffeded', ec='black')
            ax.text(x, y, f"q{i}\n(morto)", ha='center', va='center', fontsize=8)
        elif i == 14:
            circle = plt.Circle((x, y), 0.3, color='#e8ffe8', ec='black', lw=3)
            ax.text(x, y, f"q{i}", ha='center', va='center', fontsize=9, fontweight='bold')
        else:
            circle = plt.Circle((x, y), 0.3, color='#f0f5ff', ec='black')
            ax.text(x, y, f"q{i}", ha='center', va='center', fontsize=9)
        ax.add_patch(circle)

    for i in range(14):
        x_start = i * 1.5 + 0.3
        x_end = (i + 1) * 1.5 - 0.3
        ax.annotate("", xy=(x_end, 1.0), xytext=(x_start, 1.0),
                    arrowprops=dict(arrowstyle="->", lw=1))
        
        label = "0-9"
        if i == 3 or i == 7:
            label = "'.'"
        elif i == 11:
            label = "'-'"
        ax.text((x_start + x_end)/2, 1.05, label, ha='center', va='bottom', fontsize=8)

    ax.annotate("start", xy=(0, 1.0), xytext=(-0.8, 1.0), arrowprops=dict(arrowstyle="->"))

    ax.set_xlim(-1, 23)
    ax.set_ylim(-0.2, 1.5)
    ax.axis('off')
    
    path = OUT / 'dfa_regular.png'
    plt.savefig(path, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"  ✓ {path.name}")


# -----------------------------------------------------------------------------
# 2. PDA — Balanceamento de delimitadores (livre_contexto.py)
# -----------------------------------------------------------------------------
def pda_balanceamento():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("PDA - Delimitadores Balanceados", fontsize=12, fontweight='bold')
    
    circle = plt.Circle((2, 2), 0.6, color='#e8ffe8', ec='black', lw=3)
    ax.add_patch(circle)
    ax.text(2, 2, "q0", ha='center', va='center', fontsize=14, fontweight='bold')
    
    ax.annotate("start", xy=(1.4, 2), xytext=(0.5, 2), arrowprops=dict(arrowstyle="->", lw=1.2))
    
    texto_regras = (
        "Transições (Loop em q0):\n\n"
        "• Se ler '(', '[', '{'  -> Empilha\n"
        "• Se ler ')', ']', '}'  -> Desempilha (se bater com o topo)\n"
        "• Se ler Caractere Neutro -> Mantém a pilha"
    )
    ax.text(2, 0.8, texto_regras, ha='center', va='top', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", fc="#f9f9f9", ec="gray", lw=0.8))

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3)
    ax.axis('off')
    
    path = OUT / 'pda_livre_contexto.png'
    plt.savefig(path, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"  ✓ {path.name}")


# -----------------------------------------------------------------------------
# 3. MT — w#w (recursiva.py)
# -----------------------------------------------------------------------------
def mt_ww():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("MT - Cópia de Cadeia (w#w)", fontsize=12, fontweight='bold')
    
    coords = {
        'q0': (1, 4), 'q1': (3, 5), 'q2': (3, 3), 
        'q3': (6, 5), 'q4': (6, 3), 'q5': (4, 1),
        'q6': (3, 4), 'q_aceito': (1, 2), 'q_rejeita': (8, 4)
    }
    
    for st, (x, y) in coords.items():
        if st == 'q_aceito':
            circle = plt.Circle((x, y), 0.4, color='#e8ffe8', ec='black', lw=3)
        elif st == 'q_rejeita':
            circle = plt.Circle((x, y), 0.4, color='#ffeded', ec='black')
        else:
            circle = plt.Circle((x, y), 0.4, color='#f0f5ff', ec='black')
        ax.add_patch(circle)
        ax.text(x, y, st, ha='center', va='center', fontsize=9)

    def ligar(de, para, label, pos_label=(0,0), rad=0.0):
        x1, y1 = coords[de]
        x2, y2 = coords[para]
        arrow = dict(arrowstyle="->", lw=1, connectionstyle=f"arc3,rad={rad}")
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow)
        ax.text((x1+x2)/2 + pos_label[0], (y1+y2)/2 + pos_label[1], label, 
                ha='center', va='center', fontsize=8, bbox=dict(fc='white', ec='none', pad=1))

    ax.annotate("start", xy=(0.6, 4), xytext=(0, 4), arrowprops=dict(arrowstyle="->"))

    ligar('q0', 'q1', "0 -> X, D", (0, 0.2))
    ligar('q0', 'q2', "1 -> X, D", (0, -0.2))
    ligar('q0', 'q6', "# -> #, D", (0, 0.15))
    
    ligar('q1', 'q3', "# -> #, D", (0, 0.15))
    ligar('q2', 'q4', "# -> #, D", (0, -0.15))
    
    ligar('q3', 'q5', "0 -> Y, E", (0.2, -0.1))
    ligar('q4', 'q5', "1 -> Y, E", (-0.2, -0.1))
    
    ligar('q5', 'q0', "B -> B, D", (0, 0.15), rad=0.2)
    ligar('q6', 'q_aceito', "B -> B, D", (-0.1, 0.15))
    
    ligar('q3', 'q_rejeita', "1 ou B -> E", (0, 0.15))
    ligar('q4', 'q_rejeita', "0 ou B -> E", (0, -0.15))
    ligar('q6', 'q_rejeita', "0 ou 1 -> D", (0, 0.15))

    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    path = OUT / 'mt_recursiva.png'
    plt.savefig(path, bbox_inches='tight', dpi=150)
    plt.close()
    print(f"  ✓ {path.name}")


if __name__ == '__main__':
    print("Gerando diagramas do projeto com Matplotlib...")
    dfa_cpf()
    pda_balanceamento()
    mt_ww()
    print("Concluído com sucesso!")