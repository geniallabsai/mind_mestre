# -*- coding: utf-8 -*-
"""Sinais de intenção no material da pessoa — a versão vida dos riscos de código.
Nenhum sinal entra no diagnóstico sem evidência (arquivo:linha + trecho)."""
import re

from .leitura_pessoal import normalizar, trechos_ao_redor, linha_de

def _flex(norm):
    """Achata correntes de espaços/quebras em espaço único.

    Retorna (plano, mapa_pos): índice em plano -> índice em norm. Assim um
    padrão literal com espaço único casa frases quebradas no meio da linha
    (Markdown com wrapping) sem alterar nenhuma semântica de padrão."""
    chars, mapa, em_espaco = [], [], False
    for i, ch in enumerate(norm):
        if ch.isspace():
            if not em_espaco and chars:
                chars.append(" ")
                mapa.append(i)
            em_espaco = True
        else:
            em_espaco = False
            chars.append(ch)
            mapa.append(i)
    return "".join(chars), mapa


# (tipo, nivel, titulo, [regex sobre texto normalizado])
SINAIS = [
    ("exposicao", "alto", "Medo de exposição",
     [r"medo de ser visto", r"me expor", r"rirem de mim", r"zombem", r"julgarem",
      r"vergonha", r"nao gosto de aparecer", r"aparecer (me )?(desconforta|apavora)"]),
    ("falha", "alto", "Medo de falhar",
     [r"medo de fracassar", r"medo de falhar", r"e se nao der certo", r"e se der errado"]),
    ("procrastinacao", "alto", "Adiamento crônico",
     [r"adiando h[aà]", r"todo janeiro", r"todo ano", r"sempre vou (comecar|lancar)",
      r"quando eu tiver", r"quando eu conseguir", r"sempre fica para"]),
    ("oferta", "medio", "Oferta ainda não definida",
     [r"nao sei quanto cobrar", r"nao sei (o que|como) (vender|oferecer|entregar)",
      r"quanto cobrar", r"nao tenho clareza (da )?oferta"]),
    ("desvalorizacao", "medio", "Desvalorização do próprio trabalho",
     [r"sinto (culpa|culpida|culpado) de cobrar", r"dificil (subir|aumentar) o preco",
      r"nao me sinto merecedor", r"cobro (muito )?pouco"]),
    ("validacao", "medio", "Fome de validação externa",
     [r"ninguem (compra|vai comprar|me conhece)", r"pouca gente (compra|me conhece)",
      r"ja tem todo mundo fazendo", r"mercado saturado"]),
    ("tempo", "baixo", "Tempo escasso e fragmentado",
     [r"so (as? )?(manha|tarde|noite)", r"apos o trabalho", r"nao tenho tempo",
      r"\d+ horas por semana"]),
    ("dinheiro", "baixo", "Restrição financeira",
     [r"preciso de (mais )?dinheiro", r"grana (curta|apertada)", r"nao tenho como investir"]),
]

ATIVOS = [
    ("especialidade",
     [r"\d+ anos (de|como|trabalhando)",
      r"sou (fisioterapeuta|fisioterap\w*|desenvolvedor|programador|dev|designer|professor|consultor|dentista|medico|contador|advogado|arquiteto|fotografo|nutricionista|coach|psicologo|gerente|engenheiro|jornalista|empresario)"]),
    ("audiencia",
     [r"\d+(?:[.,]\d+)?\s*(mil|k)\s*(seguidores|inscritos|alunos|clientes|contatos)",
      r"seguidores (no|na)", r"lista de (e-?mail|contatos) com \d+"]),
    ("portefolio",
     [r"\d+ (workshops|palestras|clientes|projetos|edicoes|anos)",
      r"certificac\w*", r"especializa\w*", r"formacao (em|como)"]),
    ("prova_social",
     [r"agradeciment\w*", r"testemunho\w*", r"indicac\w*",
      r"e-?mails? (de|dos) (client|alun|pacient)\w*"]),
    ("demanda",
     [r"clientes? (me )?pedem", r"(me )?procuram", r"(me )?perguntam sobre",
      r"alunos? (me )?pedem", r"pacientes? (me )?pedem", r"todo mundo me (pede|pergunta)"]),
]

PRODUTOS = ["curso", "e-book", "ebook", "mentoria", "consultoria", "consulta online",
            "livro", "app", "comunidade", "palestra", "workshop", "infoproduto", "assessoria"]

OBJETIVO_RE = re.compile(
    r"(?:quero|gostaria de|pretendo) (?:criar|lancar|lançar|fazer|montar|gravar) (?:um|uma|meu|minha)? ?([^\n.]{4,90})")
NOME_RES = [re.compile(r"me chamo ([a-z][a-záéíóúâêôãõ]+)"),
            re.compile(r"sou ([a-z][a-záéíóúâêôãõ]+), \d+ anos")]


def detectar(textos):
    """textos: [(relativo, original)] → (sinais, ativos, produtos mencionados)."""
    sinais, ativos, vistos = [], [], set()
    for relativo, orig in textos:
        norm = normalizar(orig)
        plano, mapa_pos = _flex(norm)  # tolerante a quebra de linha
        for tipo, nivel, titulo, pads in SINAIS:
            n_hits = 0
            for pad in pads:
                for m in re.finditer(pad, plano):
                    if n_hits >= 2:
                        break
                    trecho = trechos_ao_redor(orig, mapa_pos[m.start()])
                    sinais.append({"tipo": tipo, "nivel": nivel, "titulo": titulo,
                                   "arquivo": relativo,
                                   "linha": linha_de(orig, trecho),
                                   "trecho": trecho})
                    n_hits += 1
        for tipo, pads in ATIVOS:
            n_hits = 0
            for pad in pads:
                for m in re.finditer(pad, plano):
                    if n_hits >= 2:
                        break
                    trecho = trechos_ao_redor(orig, mapa_pos[m.start()])
                    linha = linha_de(orig, trecho)
                    ativos.append({"tipo": tipo,
                                   "titulo": tipo.replace("_", " ").capitalize(),
                                   "evidencia": "%s:%s" % (relativo, linha or "?"),
                                   "trecho": trecho})
                    n_hits += 1
        for p in PRODUTOS:
            if p in norm:
                vistos.add(p)
    return sinais, ativos, sorted(vistos)


def objetivo(textos):
    for relativo, orig in textos:
        m = OBJETIVO_RE.search(re.sub(r"\s+", " ", normalizar(orig)))
        if m:
            alvo = m.group(1).strip(" .,;:")
            if len(alvo) >= 10:
                return {"texto": alvo, "arquivo": relativo}
    return None


def nome_pessoa(textos):
    for relativo, orig in textos:
        for rx in NOME_RES:
            m = rx.search(normalizar(orig))
            if m:
                return m.group(1).capitalize()
    return None


def numeros(textos, max_n=10):
    ach = []
    for relativo, orig in textos:
        for m in re.finditer(r"\d+(?:[.,]\d+)?", normalizar(orig)):
            contexto = trechos_ao_redor(orig, m.start(), 70)
            ach.append({"valor": m.group(0), "contexto": contexto,
                        "arquivo": relativo, "linha": linha_de(orig, contexto)})
            if len(ach) >= max_n:
                return ach
    return ach
