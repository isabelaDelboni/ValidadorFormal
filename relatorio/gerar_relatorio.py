"""
Gerador do Relatório Técnico em PDF.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import Image as RLImage
from pathlib import Path
import os

BASE = Path(__file__).parent.parent
OUT  = BASE / 'relatorio' / 'relatorio.pdf'
OUT.parent.mkdir(exist_ok=True)
DIAG = BASE / 'diagramas'

# ── Cores ────────────────────────────────────────────────────────────────────
AZUL      = HexColor('#1a3a5c')
AZUL_MED  = HexColor('#2e6da4')
AZUL_CLR  = HexColor('#ddeeff')
VERDE     = HexColor('#2e7d32')
VERDE_CLR = HexColor('#d4f7d4')
CINZA     = HexColor('#555555')
CINZA_CLR = HexColor('#f5f5f5')
LARANJA   = HexColor('#e65100')


def build_styles():
    base = getSampleStyleSheet()

    titulo = ParagraphStyle('Titulo', parent=base['Title'],
        fontSize=22, textColor=AZUL, spaceAfter=6, alignment=TA_CENTER,
        fontName='Helvetica-Bold')

    subtitulo = ParagraphStyle('Subtitulo', parent=base['Normal'],
        fontSize=11, textColor=CINZA, spaceAfter=16, alignment=TA_CENTER,
        fontName='Helvetica')

    h1 = ParagraphStyle('H1', parent=base['Heading1'],
        fontSize=14, textColor=white, backColor=AZUL,
        spaceAfter=8, spaceBefore=14,
        fontName='Helvetica-Bold', leftIndent=-1*cm,
        rightIndent=-1*cm, borderPadding=(4, 12, 4, 12))

    h2 = ParagraphStyle('H2', parent=base['Heading2'],
        fontSize=12, textColor=AZUL_MED,
        spaceAfter=4, spaceBefore=10,
        fontName='Helvetica-Bold',
        borderPadding=(2, 0, 2, 0))

    h3 = ParagraphStyle('H3', parent=base['Heading3'],
        fontSize=10, textColor=AZUL,
        spaceAfter=3, spaceBefore=6,
        fontName='Helvetica-Bold')

    corpo = ParagraphStyle('Corpo', parent=base['Normal'],
        fontSize=10, leading=14, textColor=black,
        spaceAfter=6, alignment=TA_JUSTIFY,
        fontName='Helvetica')

    code = ParagraphStyle('Code', parent=base['Code'],
        fontSize=8, leading=11, backColor=CINZA_CLR,
        fontName='Courier', leftIndent=0.5*cm,
        borderPadding=(4, 6, 4, 6))

    caption = ParagraphStyle('Caption', parent=base['Normal'],
        fontSize=8, textColor=CINZA, alignment=TA_CENTER,
        fontName='Helvetica-Oblique', spaceAfter=8)

    return {
        'titulo': titulo, 'subtitulo': subtitulo,
        'h1': h1, 'h2': h2, 'h3': h3,
        'corpo': corpo, 'code': code, 'caption': caption,
    }


def tabela_estilo(header_color=AZUL_MED, row_color=AZUL_CLR):
    return TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, row_color]),
        ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',   (0,1), (-1,-1), 8.5),
        ('GRID',       (0,0), (-1,-1), 0.4, HexColor('#cccccc')),
        ('ALIGN',      (0,0), (-1,-1), 'LEFT'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',(0,0), (-1,-1), 6),
        ('RIGHTPADDING',(0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWSPAN',    (0,0), (0,0), 1),
    ])


def imagem(path, w=14*cm):
    if Path(path).exists():
        return RLImage(str(path), width=w, height=w*0.6)
    return Paragraph(f"[Diagrama não encontrado: {path}]",
                     getSampleStyleSheet()['Normal'])


def build():
    S = build_styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        topMargin=2*cm, bottomMargin=2*cm,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
    )

    story = []

    # ── Capa ─────────────────────────────────────────────────────────────────
    story += [
        Spacer(1, 2*cm),
        Paragraph("Validador Formal em Três Níveis", S['titulo']),
        HRFlowable(width='100%', thickness=2, color=AZUL_MED, spaceAfter=8),
        Paragraph("Projeto Prático — Modelagem Computacional<br/>"
                  "Hierarquia de Chomsky: LR ⊊ LLC ⊊ R", S['subtitulo']),
        Spacer(1, 1*cm),
    ]

    # Tabela resumo inicial
    resumo_data = [
        ['Nível', 'Linguagem', 'Modelo', 'Aplicação'],
        ['LR', 'Regular', 'DFA (15 estados)', 'CPF — ddd.ddd.ddd-dd'],
        ['LLC', 'Livre de Contexto', 'PDA (pilha explícita)', 'Delimitadores balanceados'],
        ['R', 'Recursiva', 'Máquina de Turing', 'L = {w#w | w ∈ {0,1}*}'],
    ]
    t = Table(resumo_data, colWidths=[2*cm, 3.5*cm, 4.5*cm, 5.5*cm])
    t.setStyle(tabela_estilo())
    story += [t, Spacer(1, 1*cm), PageBreak()]

    # ── 1. Introdução ─────────────────────────────────────────────────────────
    story += [
        Paragraph("1. Introdução e Contexto Aplicado", S['h1']),
        Paragraph(
            "Toda vez que um software decide se uma entrada é válida, ele está reconhecendo uma "
            "linguagem formal. Validadores de formulário (CPF, e-mail, IPv4), parsers de protocolo "
            "(HTTP, TCP), verificadores de logs e mecanismos de detecção de intrusão fazem isso "
            "continuamente.", S['corpo']),
        Paragraph(
            "Esses validadores diferem fundamentalmente no poder computacional necessário para "
            "resolver cada problema. O presente projeto constrói três reconhecedores formais, um "
            "para cada nível relevante da Hierarquia de Chomsky, demonstrando empiricamente a "
            "relação de inclusão estrita LR ⊊ LLC ⊊ R.", S['corpo']),
        Paragraph(
            "O tema unificador é <b>validação de cadastro e integridade de dados</b>: "
            "validação de formato de CPF (Regular), verificação de delimitadores balanceados "
            "em expressões simbólicas (Livre de Contexto) e verificação de duplicação exata "
            "de cadeia binária separada por # (Recursiva).", S['corpo']),
        Spacer(1, 0.4*cm),
    ]

    # ── 2. Linguagem Regular ───────────────────────────────────────────────────
    story += [
        Paragraph("2. Linguagem Regular — DFA para CPF", S['h1']),

        Paragraph("2.1 Descrição", S['h2']),
        Paragraph(
            "A linguagem reconhece cadeias no formato <b>ddd.ddd.ddd-dd</b>, onde cada "
            "<i>d</i> representa um dígito decimal (0–9). O formato consiste em três blocos "
            "de três dígitos separados por pontos, seguidos de um hífen e dois dígitos finais. "
            "Apenas o formato textual é validado — os dígitos verificadores do CPF não são "
            "computados.", S['corpo']),

        Paragraph("2.2 Definição Formal", S['h2']),
        Paragraph(
            "Σ = {0, 1, …, 9, '.', '-'}<br/><br/>"
            "L = { w ∈ Σ* | w = d<sub>1</sub>d<sub>2</sub>d<sub>3</sub>.d<sub>4</sub>d<sub>5</sub>"
            "d<sub>6</sub>.d<sub>7</sub>d<sub>8</sub>d<sub>9</sub>-d<sub>10</sub>d<sub>11</sub>"
            ", com cada d<sub>i</sub> ∈ {0,…,9} }", S['code']),
        Spacer(1, 0.3*cm),

        Paragraph("2.3 Modelo Computacional — DFA", S['h2']),
        Paragraph(
            "O reconhecedor é um Autômato Finito Determinístico (DFA) com <b>15 estados</b> "
            "(q0–q14) e um estado morto (qDEAD). O estado inicial é q0 e o único estado de "
            "aceitação é q14, atingido exatamente após a leitura dos 14 símbolos que compõem "
            "um CPF válido.", S['corpo']),
    ]

    # Tabela de transição do DFA (trecho)
    dfa_data = [
        ['Estado', 'Símbolo lido', 'Próximo estado', 'Significado'],
        ['q0', '0–9', 'q1', '1º dígito do bloco 1'],
        ['q1', '0–9', 'q2', '2º dígito do bloco 1'],
        ['q2', '0–9', 'q3', '3º dígito do bloco 1'],
        ['q3', "'.'", 'q4', 'Ponto separador 1'],
        ['q4–q6', '0–9', 'q5–q7', 'Bloco 2 (3 dígitos)'],
        ['q7', "'.'", 'q8', 'Ponto separador 2'],
        ['q8–q10', '0–9', 'q9–q11', 'Bloco 3 (3 dígitos)'],
        ['q11', "'-'", 'q12', 'Hífen'],
        ['q12', '0–9', 'q13', '1º dígito final'],
        ['q13', '0–9', 'q14 ✓', '2º dígito final — ACEITA'],
        ['q14', 'qualquer', 'qDEAD', 'Símbolo extra — REJEITA'],
        ['qDEAD', 'qualquer', 'qDEAD', 'Estado absorvente'],
    ]
    t = Table(dfa_data, colWidths=[2.5*cm, 2.5*cm, 3.5*cm, 6*cm])
    t.setStyle(tabela_estilo())
    story += [
        Paragraph("Tabela de Transição (δ) — DFA CPF:", S['h3']),
        t, Spacer(1, 0.3*cm),
    ]

    if (DIAG / 'dfa_regular.png').exists():
        story += [
            imagem(DIAG / 'dfa_regular.png', w=13*cm),
            Paragraph("Figura 1 — Diagrama do DFA para CPF", S['caption']),
        ]

    story += [
        Paragraph("2.4 Exemplos", S['h2']),
    ]
    ex_lr = [
        ['Cadeia', 'Resultado', 'Passos'],
        ['123.456.789-00', '✓ ACEITA', '14'],
        ['000.000.000-00', '✓ ACEITA', '14'],
        ['999.999.999-99', '✓ ACEITA', '14'],
        ['12.34.56-78', '✗ REJEITA (bloco com 2 dígitos)', '11'],
        ['123.456.789-001', '✗ REJEITA (dígito extra)', '15'],
        ['12345678900', '✗ REJEITA (sem separadores)', '11'],
    ]
    t = Table(ex_lr, colWidths=[4*cm, 7*cm, 2*cm])
    t.setStyle(tabela_estilo(VERDE, VERDE_CLR))
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph("2.5 Execução Passo a Passo — '123.456.789-00' (aceita)", S['h3']),
        Paragraph(
            "q0→'1'→q1 | q1→'2'→q2 | q2→'3'→q3 | q3→'.'→q4 | q4→'4'→q5 | q5→'5'→q6 | "
            "q6→'6'→q7 | q7→'.'→q8 | q8→'7'→q9 | q9→'8'→q10 | q10→'9'→q11 | "
            "q11→'-'→q12 | q12→'0'→q13 | q13→'0'→q14 ✓  [14 passos]", S['code']),
        Paragraph("2.6 Execução Passo a Passo — '12.34.56-78' (rejeita)", S['h3']),
        Paragraph(
            "q0→'1'→q1 | q1→'2'→q2 | q2→'.'→qDEAD  "
            "[3 passos úteis + 8 absorvidos = 11 passos; terceiro símbolo deveria ser dígito]",
            S['code']),
        PageBreak(),
    ]

    # ── 3. Linguagem Livre de Contexto ─────────────────────────────────────────
    story += [
        Paragraph("3. Linguagem Livre de Contexto — PDA para Balanceamento", S['h1']),

        Paragraph("3.1 Descrição", S['h2']),
        Paragraph(
            "A linguagem reconhece expressões simbólicas em que todos os delimitadores de abertura "
            "(parênteses, colchetes e chaves) possuem um delimitador de fechamento correspondente, "
            "na ordem correta e sem sobreposição. Caracteres alfanuméricos e operadores são neutros "
            "e não afetam o balanceamento.", S['corpo']),

        Paragraph("3.2 Definição Formal", S['h2']),
        Paragraph(
            "Σ = { (, ), [, ], {, }, a–z, A–Z, 0–9, +, -, *, /, ^, … }<br/><br/>"
            "L = { w ∈ Σ* | todo abre-delimitador em w tem um fecha-delimitador "
            "correspondente, respeitando a ordem de aninhamento }<br/><br/>"
            "GLC equivalente (simplificada):<br/>"
            "S → ε | SS | '(' S ')' | '[' S ']' | '{' S '}'", S['code']),
        Spacer(1, 0.3*cm),

        Paragraph("3.3 Modelo Computacional — PDA", S['h2']),
        Paragraph(
            "O reconhecedor é um Autômato com Pilha (PDA) determinístico. A pilha contém o "
            "marcador de fundo '$' e os delimitadores de abertura ainda não fechados. "
            "O estado inicial e de aceitação é q0; a aceitação ocorre quando, ao final da "
            "entrada, a pilha contém apenas '$'.", S['corpo']),
    ]

    pda_data = [
        ['Estado', 'Símbolo lido', 'Topo da pilha', '→ Estado', 'Ação na pilha'],
        ['q0', "'('", '*', 'q0', "push '('"],
        ['q0', "'['", '*', 'q0', "push '['"],
        ['q0', "'{'", '*', 'q0', "push '{'"],
        ['q0', "')'", "'('", 'q0', 'pop'],
        ['q0', "']'", "'['", 'q0', 'pop'],
        ['q0', "'}'", "'{'", 'q0', 'pop'],
        ['q0', 'neutro', '*', 'q0', 'sem mudança'],
        ['q0', "']'/'}'/';'…", 'topo errado', 'qDEAD', 'erro de balanceamento'],
        ['qDEAD', 'qualquer', '*', 'qDEAD', 'absorvente'],
    ]
    t = Table(pda_data, colWidths=[1.8*cm, 2.5*cm, 2.5*cm, 2*cm, 5.7*cm])
    t.setStyle(tabela_estilo())
    story += [
        Paragraph("Principais Transições do PDA:", S['h3']),
        t, Spacer(1, 0.3*cm),
    ]

    if (DIAG / 'pda_livre_contexto.png').exists():
        story += [
            imagem(DIAG / 'pda_livre_contexto.png', w=12*cm),
            Paragraph("Figura 2 — Diagrama do PDA para balanceamento", S['caption']),
        ]

    story += [Paragraph("3.4 Exemplos", S['h2'])]
    ex_llc = [
        ['Cadeia', 'Resultado', 'Passos'],
        ['((x+y)*z)', '✓ ACEITA', '9'],
        ['{[a+b]*(c-d)}', '✓ ACEITA', '13'],
        ['([{}])', '✓ ACEITA', '6'],
        ['((a+b)', '✗ REJEITA (parêntese não fechado)', '6'],
        ['([)]', '✗ REJEITA (fechamento cruzado)', '3'],
        [')', '✗ REJEITA (fecha sem abrir)', '1'],
    ]
    t = Table(ex_llc, colWidths=[4*cm, 7.5*cm, 2*cm])
    t.setStyle(tabela_estilo(VERDE, VERDE_CLR))
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph("3.5 Execução Passo a Passo — '((x+y)*z)' (aceita)", S['h3']),
        Paragraph(
            "Passo 1: δ(q0,'(') → q0, push '(' | pilha=['(','$']<br/>"
            "Passo 2: δ(q0,'(') → q0, push '(' | pilha=['(','(','$']<br/>"
            "Passo 3: δ(q0,'x') → q0, neutro<br/>"
            "Passo 4: δ(q0,'+') → q0, neutro<br/>"
            "Passo 5: δ(q0,'y') → q0, neutro<br/>"
            "Passo 6: δ(q0,')') → q0, pop '(' | pilha=['(','$']<br/>"
            "Passo 7: δ(q0,'*') → q0, neutro<br/>"
            "Passo 8: δ(q0,'z') → q0, neutro<br/>"
            "Passo 9: δ(q0,')') → q0, pop '(' | pilha=['$'] → ACEITA", S['code']),
        Paragraph("3.6 Execução Passo a Passo — '([)]' (rejeita)", S['h3']),
        Paragraph(
            "Passo 1: δ(q0,'(') → q0, push '(' | pilha=['(','$']<br/>"
            "Passo 2: δ(q0,'[') → q0, push '[' | pilha=['[','(','$']<br/>"
            "Passo 3: δ(q0,')') → qDEAD (topo='[', esperava '(') → REJEITA", S['code']),
        PageBreak(),
    ]

    # ── 4. Linguagem Recursiva ─────────────────────────────────────────────────
    story += [
        Paragraph("4. Linguagem Recursiva — MT para w#w", S['h1']),

        Paragraph("4.1 Descrição", S['h2']),
        Paragraph(
            "A linguagem reconhece cadeias da forma <i>w#w</i>, onde <i>w</i> é uma palavra "
            "binária (sobre {0,1}) e '#' é o separador. As duas cópias de <i>w</i> devem ser "
            "idênticas e ter o mesmo comprimento. Esta linguagem é <b>não livre de contexto</b> "
            "— não pode ser reconhecida por nenhum PDA — pois exige comparar substrings "
            "arbitrariamente longas posicionadas em regiões distintas da entrada.", S['corpo']),
        Paragraph(
            "Esta linguagem é o exemplo clássico que demonstra a necessidade de memória "
            "de trabalho irrestrita (fita da MT) e ilustra por que LLC ⊊ R na hierarquia.", S['corpo']),

        Paragraph("4.2 Definição Formal", S['h2']),
        Paragraph(
            "Σ = {0, 1, #}<br/>"
            "Γ = {0, 1, #, X, Y, B}   (B = branco)<br/><br/>"
            "L = { w#w | w ∈ {0,1}* }", S['code']),
        Spacer(1, 0.3*cm),

        Paragraph("4.3 Modelo Computacional — Máquina de Turing", S['h2']),
        Paragraph(
            "A MT possui 7 estados operacionais (q0, q1a, q1b, q2a, q2b, q3, q4) mais "
            "os estados terminais qA (aceita) e qR (rejeita). Utiliza marcação com X (símbolo "
            "já processado à esquerda do #) e Y (símbolo já processado à direita).", S['corpo']),
        Paragraph(
            "Estratégia: em cada rodada, a MT (1) marca o próximo símbolo não marcado à "
            "esquerda com X, (2) atravessa até encontrar o par correspondente à direita do #, "
            "(3) verifica igualdade e marca com Y, (4) retorna ao início. Aceita quando todos "
            "os símbolos estão marcados; rejeita em qualquer divergência ou desbalanceamento "
            "de tamanho. Complexidade: O(n²) passos, onde n = |w|.", S['corpo']),
    ]

    mt_data = [
        ['Estado', 'Lê', 'Escreve', '→ Estado', 'Dir', 'Papel'],
        ['q0', '0', 'X', 'q1a', 'R', 'Marca 0, carrega para comparar'],
        ['q0', '1', 'X', 'q2a', 'R', 'Marca 1, carrega para comparar'],
        ['q0', 'X', 'X', 'q0',  'R', 'Pula X já marcado'],
        ['q0', '#', '#', 'q4',  'R', 'Entra em verificação final'],
        ['q1a', '0,1,X', '=', 'q1a', 'R', 'Atravessa lado esquerdo'],
        ['q1a', '#', '#', 'q1b', 'R', 'Cruzou o separador'],
        ['q1b', 'Y', 'Y', 'q1b', 'R', 'Pula Y já marcado'],
        ['q1b', '0', 'Y', 'q3',  'L', 'Par correto: 0=0, marca Y'],
        ['q1b', '1', '1', 'qR',  'R', 'Divergência: esperava 0'],
        ['q2b', '1', 'Y', 'q3',  'L', 'Par correto: 1=1, marca Y'],
        ['q2b', '0', '0', 'qR',  'R', 'Divergência: esperava 1'],
        ['q3', '0,1,X,Y,#', '=', 'q3', 'L', 'Retorna ao início'],
        ['q3', 'B', 'B', 'q0',  'R', 'Reinicia rodada'],
        ['q4', 'Y', 'Y', 'q4',  'R', 'Verifica lado direito marcado'],
        ['q4', 'B', 'B', 'qA',  'R', 'Tudo marcado → ACEITA'],
        ['q4', '0,1', '=', 'qR', 'R', 'Símbolo não marcado → REJEITA'],
    ]
    t = Table(mt_data, colWidths=[1.6*cm, 1.2*cm, 1.8*cm, 2*cm, 1*cm, 6.9*cm])
    t.setStyle(tabela_estilo())
    story += [
        Paragraph("Tabela de Transição (δ) — MT w#w:", S['h3']),
        t, Spacer(1, 0.3*cm),
    ]

    if (DIAG / 'mt_recursiva.png').exists():
        story += [
            imagem(DIAG / 'mt_recursiva.png', w=14*cm),
            Paragraph("Figura 3 — Diagrama da Máquina de Turing para w#w", S['caption']),
        ]

    story += [Paragraph("4.4 Exemplos", S['h2'])]
    ex_r = [
        ['Cadeia', 'Resultado', 'Passos'],
        ['101#101', '✓ ACEITA', '44'],
        ['0#0', '✓ ACEITA', '10'],
        ['11001#11001', '✓ ACEITA', '102'],
        ['101#100', '✗ REJEITA (divergência no 3º símbolo)', '29'],
        ['101101', '✗ REJEITA (sem separador #)', '7'],
        ['(vazio)', '✗ REJEITA', '1'],
    ]
    t = Table(ex_r, colWidths=[4*cm, 7.5*cm, 2*cm])
    t.setStyle(tabela_estilo(VERDE, VERDE_CLR))
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph("4.5 Execução Passo a Passo — '101#101' (aceita, 44 passos)", S['h3']),
        Paragraph(
            "Rodada 1 (carrega '1'):<br/>"
            "  q0,'1'→(q2a,'X',R) | q2a,'0'→(q2a,'0',R) | q2a,'1'→(q2a,'1',R) |<br/>"
            "  q2a,'#'→(q2b,'#',R) | q2b,'1'→(q3,'Y',L) | q3 volta ao início...<br/><br/>"
            "Rodada 2 (carrega '0'):<br/>"
            "  q0,'X'→(q0,'X',R) | q0,'0'→(q1a,'X',R) | ... q1b,'0'→(q3,'Y',L) | ...<br/><br/>"
            "Rodada 3 (carrega '1'):<br/>"
            "  q0,'X','X'→pula | q0,'1'→(q2a,'X',R) | ... q2b,'1'→(q3,'Y',L) | ...<br/><br/>"
            "Verificação (q4):<br/>"
            "  q0,'#'→(q4,'#',R) | q4,'Y'→... | q4,'Y'→... | q4,'Y'→... | q4,'B'→(qA,'B',R) ✓",
            S['code']),
        Paragraph("4.6 Execução Passo a Passo — '101#100' (rejeita, 29 passos)", S['h3']),
        Paragraph(
            "Rodadas 1 e 2 funcionam normalmente (comparações '1'='1' e '0'='0' corretas).<br/>"
            "Rodada 3 (carrega '1'):<br/>"
            "  q0,'X','X'→pula | q0,'1'→(q2a,'X',R) | q2a,'#'→(q2b,'#',R) |<br/>"
            "  q2b,'Y','Y'→pula | q2b,'0' — esperava '1' → (qR,'0',R) → REJEITA em 29 passos",
            S['code']),
        PageBreak(),
    ]

    # ── 5. Comparação e Conclusão ─────────────────────────────────────────────
    story += [
        Paragraph("5. Comparação e Conclusão", S['h1']),

        Paragraph("5.1 Resultados da Bateria de Testes", S['h2']),
    ]

    comp_data = [
        ['Nível', 'Modelo', 'Testes', 'Total Passos', 'Média', 'Complexidade'],
        ['LR — CPF', 'DFA', '9/9 (100%)', '106', '11,8', 'O(n) — linear'],
        ['LLC — Balanceamento', 'PDA', '8/8 (100%)', '43', '5,4', 'O(n) — linear'],
        ['R — w#w', 'MT', '8/8 (100%)', '227', '28,4', 'O(n²) — quadrático'],
    ]
    t = Table(comp_data, colWidths=[3.5*cm, 2*cm, 2.5*cm, 2.5*cm, 1.8*cm, 3.2*cm])
    t.setStyle(tabela_estilo())
    story += [t, Spacer(1, 0.4*cm)]

    story += [
        Paragraph("5.2 Análise da Hierarquia LR ⊊ LLC ⊊ R", S['h2']),
        Paragraph(
            "Os três reconhecedores demonstram na prática a hierarquia de Chomsky:", S['corpo']),
        Paragraph(
            "<b>DFA (CPF):</b> reconhece linguagens regulares sem memória auxiliar. "
            "O número de estados é fixo e proporcional ao comprimento máximo da cadeia. "
            "Não consegue reconhecer linguagens como balanceamento (exigiria infinitos estados "
            "para rastrear profundidade arbitrária) nem w#w.", S['corpo']),
        Paragraph(
            "<b>PDA (Balanceamento):</b> a pilha adiciona memória ilimitada de tipo LIFO, "
            "permitindo rastrear aninhamento arbitrário. É mais poderoso que o DFA, porém "
            "não consegue comparar duas substrings de posições arbitrárias na entrada — "
            "o que seria necessário para reconhecer w#w.", S['corpo']),
        Paragraph(
            "<b>MT (w#w):</b> a fita bidirecional com leitura e escrita permite comparação "
            "direta de substrings. A MT percorre a fita O(n) vezes, resultando em O(n²) passos "
            "total. Esta linguagem não é livre de contexto (prova pelo lema do bombeamento), "
            "confirmando que MT &gt; PDA &gt; DFA em poder expressivo.", S['corpo']),

        Paragraph("5.3 Conclusão", S['h2']),
        Paragraph(
            "O projeto implementou com sucesso três reconhecedores formais completos, cada um "
            "simulando explicitamente seu modelo computacional (estados, alfabeto, função de "
            "transição declarados como dados). Todos os 25 testes da bateria foram aprovados "
            "com 100% de acerto, e a contagem de passos confirma a diferença de complexidade "
            "prevista pela teoria: O(n) para DFA e PDA, O(n²) para MT.", S['corpo']),
        Paragraph(
            "A hierarquia LR ⊊ LLC ⊊ R é assim demonstrada tanto teoricamente (pela definição "
            "formal de cada linguagem e pela impossibilidade de reconhecê-la com modelos menos "
            "poderosos) quanto empiricamente (pela diferença no número de passos e no tipo de "
            "memória utilizada).", S['corpo']),
    ]

    doc.build(story)
    print(f"  ✓ Relatório gerado: {OUT}")


if __name__ == '__main__':
    build()
