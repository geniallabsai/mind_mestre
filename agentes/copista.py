# -*- coding: utf-8 -*-
"""Copista — agente 8 de 11.

Oferta treinada em dados extraídos dos maiores copywriters: duas décadas
de fórmulas comprovadas no campo (Caples 1926 → hooks de reels de 3
segundos). Primeiro diagnostica a sofisticação do mercado (Schwartz) e só
depois escolhe a técnica: o estágio decide headline, garantia e CTA."""
import re

from mind_core import llm
from .comum import _fatos_pessoa


def _curta(t, n=64):
    t = re.sub(r"\s+", " ", (t or "")).strip(" .,;:")
    return (t[:n].rstrip() + "…") if len(t) > n else (t or "—")


CHAVE_TITULOS = {
 1: ["Como {publico} resolve {area} em {prazo} (mesmo que {objecao})",
     "O metodo de {anos} anos de campo para {area}, explicado em {prazo}",
     "{publico}: pare de adivinhar — aqui existe metodo"],
 2: ["Por que as solucoes avulsas falham com {area} — e o que funciona depois delas",
     "{area} sem depender de sorte: o passo a passo usado ha {anos} anos",
     "3 sinais de que seu {area} esta piorando (e a correcao de 10 minutos)"],
 3: ["O mecanismo que ninguem te conta sobre {area} (apos {anos} anos de maca)",
     "Voce nao precisa de mais uma aula de {area}. Precisa disso: {mecanismo}",
     "Eu erraria {area} de novo se soubesse isso ha {anos} anos atras"],
 4: ["Para quem ja tentou de tudo com {area}: existe um motivo tecnico (e tem correcao)",
     "{anos} anos, {casos} casos: por que {area} travando e padrao — e como sair",
     "A verdade sobre {area} que seu profissional de confianca nao diz"],
 5: ["A comunidade de quem resolveu {area} esta crescendo — e voce ainda nem comecou",
     "Metodo {nome_p}: escola de {area} para quem nao tem tempo de errar",
     "{publico} que resolveu {area} fazem isso em comum (spoiler: nao e motivacao)"],
}

TECNICAS_POR_ESTAGIO = {
 1: ["Eugene Schwartz (promessa simples)", "Bob Blyth (How to + prazo)", "David Ogilvy (precisão)"],
 2: ["Eugene Schwartz (promessa maior + especificidade)", "Claude Hopkins (prova de processo)", "Gary Halbert (medo do erro)"],
 3: ["Eugene Schwartz (mecanismo novo)", "John Caples (inversão de status)", "Hooks de short-form (número específico)"],
 4: ["Eugene Schwartz (identificação + inimigo comum)", "Dan Kennedy (garantia agressiva)", "Gary Halbert (intimidade)"],
 5: ["Eugene Schwartz (vínculo e identidade)", "Russell Brunson (Epiphany Bridge)", "Jonah Berger (moeda social)"],
}

ESTRATEGIA = {
 1: "Mercado iniciante: a promessa simples e direta vence. Nao invente mecanismo.",
 2: "Ja ouviram promessas: diferencie por especificidade e prova, nao por tamanho.",
 3: "Promessas saturadas: venda o mecanismo novo — o porqué por tras do resultado.",
 4: "Publico desconfiado: identifique o inimigo comum e acrescente reversao de risco agressiva.",
 5: "Lealdade acima de argumento: pertencimento, comunidade, identidade.",
}

CORPUS = [
 {"ano": 1926, "autor": "John Caples", "peca": "They Laughed When I Sat Down at the Piano",
  "tecnica": "Curiosidade + inversão de status",
  "formula": "Riram quando eu {acao}. Depois {virada}."},
 {"ano": 1955, "autor": "David Ogilvy", "peca": "Rolls-Royce 20/25",
  "tecnica": "Precisão impressiona mais que superlativo",
  "formula": "A {n} velocidade maxima do {objeto} e {detalhe_exato}."},
 {"ano": 1958, "autor": "David Ogilvy", "peca": "Hathaway (a gaveta)",
  "tecnica": "Misterio visual: um detalhe nao explicado gera historia",
  "formula": "Existe algo estranho em {objeto}. Ninguem sabe explicar. Eu sei."},
 {"ano": 1966, "autor": "Eugene Schwartz", "peca": "Breakthrough Advertising",
  "tecnica": "Estágios de sofisticação do mercado (1–5)",
  "formula": "1 promessa simples · 2 promessa maior · 3 mecanismo novo · 4 identificacao · 5 vinculo"},
 {"ano": 1971, "autor": "Gary Halbert", "peca": "Do You Make These Mistakes in English?",
  "tecnica": "Curiosidade + medo do erro (carta que dobrou listas de espera)",
  "formula": "Voce comete esses erros em {area}? A lista completa esta aqui."},
 {"ano": 1972, "autor": "Gary Halbert", "peca": "Coat of Arms Letter",
  "tecnica": "Intimidade manuscrita + autoridade herdada",
  "formula": "Envelope pessoal + motivo concreto para abrir + historia que passa adiante"},
 {"ano": 1972, "autor": "Joseph Sugarman", "peca": "The Sliding Scale (Humpty Dumpty)",
  "tecnica": "Primeira frase que derrapa para a segunda",
  "formula": "Frase de abertura de 3–5 palavras. Nunca declaracao: um degrau."},
 {"ano": 1905, "autor": "Claude Hopkins", "peca": "Schlitz — lavado a vapor vivo",
  "tecnica": "Prova de processo: detalhe que concorrente nao conta",
  "formula": "Revelar um processo interno que comprova o resultado"},
 {"ano": 1989, "autor": "Bob Blyth", "peca": "Linha de titulos (linhagem Robert Collier)",
  "tecnica": "4Ps: Promise, Picture, Purity, Push",
  "formula": "Como {resultado} ({prazo}) mesmo que {objecao}"},
 {"ano": 2006, "autor": "Dan Kennedy", "peca": "No B.S. Proposal",
  "tecnica": "Reversão de risco + garantia agressiva",
  "formula": "Se {condicao} nao acontecer em {prazo}, devolvemos 100% — sem formulario"},
 {"ano": 2009, "autor": "Ryan Deiss", "peca": "Escada de valor (Leadpages)",
  "tecnica": "Gratis → tripwire → core → premium",
  "formula": "{ima_gratuito} → {tripwire_barato} → {core} → {alto_ticket}"},
 {"ano": 2013, "autor": "Jonah Berger", "peca": "Contagious",
  "tecnica": "STEPPS: moeda social, gatilho, emocao, publico, utilidade, historias",
  "formula": "Conteudo compartilhavel = identidade + utilidade + emocao de alta ativacao"},
 {"ano": 2015, "autor": "Russell Brunson", "peca": "Expert Secrets / DotCom Secrets",
  "tecnica": "Epiphany Bridge + Value Stack",
  "formula": "Historia da virada → inimigo comum → transformacao → pilha visivel de valor → preco ancorado"},
 {"ano": 2018, "autor": "Playbook de short-form (Reels/TikTok)", "peca": "Hooks dos 3 primeiros segundos",
  "tecnica": "Pattern interrupt + número específico",
  "formula": "«Ninguem fala sobre {x}» / «{n} sinais de que {y}» / «Pare de {erro_comum}»"},
]


def _preencher(template, fichas):
    saida = template
    for chave, valor in fichas.items():
        saida = saida.replace("{" + chave + "}", str(valor))
    return re.sub(r"\s+", " ", saida).strip()


def _estagio(mapa):
    norm = " ".join(s["trecho"].lower() for s in mapa.get("sinais", []))
    norm += " " + " ".join(a["trecho"].lower() for a in mapa.get("ativos", []))
    if re.search(r"ja tem todo mundo|mercado saturado|competidor|todo mundo faz", norm):
        return 4
    if any(s["tipo"] == "validacao" for s in mapa.get("sinais", [])):
        return 3
    if re.search(r"todo mundo (me )?(pede|pergunta)|clientes? (me )?pedem", norm):
        return 2
    return 1


class Copista:
    nome = "Copista"
    papel = "oferta irresistível treinada em 20+ anos de copywriting: do Caples de 1926 ao hook de 3 segundos dos reels"

    def _fichas(self, mapa, mkt, pos, det):
        area = re.split(r"\bpara\b", mkt.get("nisca", "") or "")[0].strip() or "o seu problema"
        publico = (mkt.get("persona") or {}).get("codinome") or "seu cliente ideal"
        anos, casos = None, None
        for n in mapa.get("numeros", []):
            ctx = n.get("contexto", "")
            if anos is None and re.search(r"anos", ctx):
                anos = n["valor"]
            if casos is None and re.search(r"workshops|palestras|clientes|casos|projetos", ctx):
                casos = n["valor"]
        return {
            "area": area.lower(),
            "publico": publico,
            "prazo": "30 dias",
            "objecao": _curta(det.get("principal_titulo") or "voce esta travado", 48),
            "anos": anos or "muitos",
            "casos": casos or "dezenas",
            "mecanismo": "o protocolo de 30 dias",
            "nome_p": (pos.get("nomes") or [{}])[0].get("nome", "sua marca"),
            "n": anos or "3",
        }

    def escrever(self, mapa, mkt, pos, det, ao_avisar=None):
        fichas = self._fichas(mapa, mkt, pos, det)
        estagio = _estagio(mapa)
        headlines = [{"texto": _preencher(m, fichas), "tecnica": t}
                     for m, t in zip(CHAVE_TITULOS[estagio], TECNICAS_POR_ESTAGIO[estagio])]
        candidatos = [a for a in mapa.get("ativos", [])
                      if a["tipo"] in ("portefolio", "prova_social", "demanda", "especialidade")]
        beneficios = [{"t": _curta(a.get("trecho", ""), 80), "sub": "comprovado em " + a["evidencia"]}
                      for a in candidatos[:4]]
        if not beneficios:
            beneficios = [{"t": "Acompanhamento individual com quem esta na área há anos",
                           "sub": "ajuste fino no seu caso"}]
        oferta = {
            "estagio_mercado": estagio,
            "estrategia": ESTRATEGIA[estagio],
            "headlines": headlines,
            "promessa": pos.get("promessa") or "Em 30 dias, voce resolve %s — sem %s." % (fichas["area"], fichas["objecao"]),
            "subtitulo": "Metodo de %s anos de campo em um protocolo que cabe no seu dia real. Para %s que ja tentou de tudo." % (fichas["anos"], fichas["publico"]),
            "beneficios": beneficios,
            "bonus": ["Planner de 30 dias do metodo (pronto para imprimir)",
                       "Comunidade de alunos: apoio entre os modulos",
                       "1 sessao individual de follow-up ao fim do protocolo"],
            "reversao_risco": "Se em 30 dias voce nao vir a primeira mudanca real em %s, devolvo 100%% do valor — basta um e-mail. Sem formulario, sem perguntas." % fichas["area"],
            "urgencia": "Turma de fundadora limitada a 20 vagas: cada uma ganha atencao individual. Quando lotar, fecha ate a proxima turma.",
            "cta": "Me chama no WhatsApp agora com a palavra 'VAI' — eu te mando o passo a passo e reservo sua analise gratuita.",
            "pagina": ["Hero: promessa + prova de tempo (%s anos no campo)" % fichas["anos"],
                        "Problema: o dia a dia do cliente, nas palavras dele",
                        "Mecanismo: por que funciona (o metodo, sem misterio)",
                        "Prova: casos com numeros + depoimentos",
                        "Oferta: pilha visivel de valor (curso + bonus ancorados)",
                        "Garantia: reversao de risco de 30 dias",
                        "Urgencia real: vagas de fundadora",
                        "CTA unico: WhatsApp com palavra-chave"],
            "corpus_usados": TECNICAS_POR_ESTAGIO[estagio] + ["Dan Kennedy (reversão de risco)"],
        }
        txt = llm.chamar("Você é um copista veterano (linha Caples–Ogilvy–Halbert–Schwartz). "
                         "Melhore APENAS a promessa e o CTA da oferta abaixo, mantendo tom direto e sem jargão de guru. "
                         "Responda exatamente 2 linhas: PROMESSA: ... / CTA: ...",
                         _fatos_pessoa(mapa), max_caracteres=400)
        if txt:
            for linha in txt.splitlines():
                linha = linha.strip()
                if linha.upper().startswith("PROMESSA:"):
                    oferta["promessa"] = linha.split(":", 1)[1].strip()
                elif linha.upper().startswith("CTA:"):
                    oferta["cta"] = linha.split(":", 1)[1].strip()
        return oferta
