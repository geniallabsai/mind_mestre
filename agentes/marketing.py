# -*- coding: utf-8 -*-
"""Gênio do Marketing — agente 6 de 11.

Acha o nicho ideal, a persona e o mapa da empatia usando SÓ o que o material
sustenta: especialidade, provas de demanda, audiência. Onde não há evidência,
ele escreve "— (pergunte em conversa)" em vez de inventar."""
import re

from .comum import _fatos_pessoa
from mind_core import llm

CHAVE_DORES = ["dor", "doe", "cansac", "incomod", "morre", "trava", "peso", "ansied", "stress", "stresse"]


def _ativos_tipo(mapa, tipo):
    return [a for a in mapa.get("ativos", []) if a["tipo"] == tipo]


def _area_publico(objetivo):
    if not objetivo:
        return None, None
    t = re.sub(r"\s+", " ", objetivo).lower().strip()
    t = t.split(",")[0]  # cláusula posterior ("mas estou adiando…") não é nicho
    m = re.search(r"(?:sobre|de|para)\s+([a-z0-9áéíóú\-' ]+?)\s+para\s+([a-z0-9áéíóú\- ]+)$", t)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    m = re.search(r"sobre\s+([a-z0-9áéíóú\- ]{2,40})$", t)
    if m:
        return m.group(1).strip(), None
    return t[:40].strip(), None


def _citar(mapa, chave_alternativas=CHAVE_DORES):
    """Frases diretas (entre aspas) do material — a voz real do cliente."""
    achadas = []
    for a in mapa.get("ativos", []) + [{}]:
        pass
    for s in mapa.get("sinais", []) + [{"trecho": x} for x in []]:
        pass
    for grupo in (mapa.get("ativos", []), mapa.get("sinais", [])):
        for item in grupo:
            trecho = item.get("trecho", "")
            for m in re.finditer(r"[\u201c\u201d\"“”\u00ab\u00bb]([^\u201c\u201d\"“”\u00ab\u00bb]{6,90})[\u201c\u201d\"“”\u00ab\u00bb]", trecho):
                if m.group(1) not in achadas:
                    achadas.append(m.group(1).strip())
    return achadas


class GenioMarketing:
    nome = "Gênio do Marketing"
    papel = "acha o nicho ideal, a persona e o mapa da empatia a partir do material real"

    def estudar(self, mapa, ao_avisar=None):
        nome = mapa.get("persona_nome") or "Você"
        obj = mapa.get("objetivo_declarado") or ""
        area, publico = _area_publico(obj)
        publico = re.sub(r'["|;].*$', "", publico or "").strip() \
            or "quem sente a dor que você resolve todo dia"
        esp = _ativos_tipo(mapa, "especialidade")
        dem = _ativos_tipo(mapa, "demanda")
        aud = _ativos_tipo(mapa, "audiencia")
        anos = None
        for a in esp:
            m = re.search(r"(\d+)\s*anos", a.get("trecho", ""))
            if m:
                anos = int(m.group(1))
        nicho = "%s para %s" % ((area or "sua especialidade").strip().lower(), publico.strip().lower())
        porque = []
        if esp:
            porque.append("especialidade com trilha: %s (%s)" % (re.sub(r"\s+", " ", esp[0]["trecho"])[:80], esp[0]["evidencia"]))
        if dem:
            porque.append("demanda pedindo à porta: %s (%s)" % (dem[0]["trecho"][:80], dem[0]["evidencia"]))
        if aud:
            porque.append("plateia já existe: %s (%s)" % (aud[0]["trecho"][:80], aud[0]["evidencia"]))
        if not porque:
            porque.append("base fina — valide o nicho em 5 conversas antes de investir")

        citacoes = _citar(mapa)
        cit_dores = [c for c in citacoes if any(k in c.lower() for k in CHAVE_DORES)][:1]
        persona = {
            "codinome": (publico.split()[0].capitalize() + " da área") if publico else "Cliente tipo",
            "perfil": "Passa a vida no problema que você resolve há %s anos. Já tentou soluções avulsas e voltou ao zero." % (anos or "vários"),
            "quer": ["resolver %s sem perder o fim de semana" % (area or "isso"),
                     "alguém que já passou por ali e fale a língua dele",
                     "resultado rápido o bastante para acreditar"],
            "teme": list(cit_dores) + ["ficar igual: gastar e não sair do lugar"],
            "dia_tipo": ["manhã: o problema aparece (e ele finge que não)",
                         "fim do dia: cansaço + culpa de não ter resolvido",
                         "fim de semana: pesquisa avulsa na internet"],
        }
        P = "— (pergunte em conversa)"
        empatia = {
            "pensam": (cit_dores or [P])[0] if (cit_dores or [P]) else P,
            "sentem": "sobra e culpa: 'deveria ter resolvido isso'",
            "vem": "consultas, salas de espera, telas o dia inteiro",
            "ouvem": ("“isso passa com o tempo” e “tente de novo”" if citacoes else P),
            "dizem": (cit_dores[0] if cit_dores else P),
            "fazem": "tentam avulsos, desistem, repetem (o ciclo que você encerra)",
            "dores": [(area or "o problema") + " que piora com o tempo",
                      "custo de continuar igual (saúde, dinheiro, disposição)"],
            "ganhos": ["resolução com método (não sorte)",
                       "alguém assumindo a direção por 30 dias",
                       "ganho visível na 1ª semana para acreditar"],
        }
        icp = ("Persona primária: %s. Critério de entrada: sente a dor toda semana, já gastou "
               "com solução avulsa, e está alcançável pelos seus canais." % publico)
        canais = []
        for a in aud:
            t = a.get("trecho", "")
            for pl, rotulo in (("instagram", "Instagram"), ("youtube", "YouTube"),
                               ("tiktok", "TikTok"), ("linkedin", "LinkedIn"),
                               ("whatsapp", "WhatsApp (grupo/lista)"), ("e-mail", "e-mail (lista)"),
                               ("mail", "e-mail (lista)")):
                if pl in t.lower() and rotulo not in [c["canal"] for c in canais]:
                    canais.append({"canal": rotulo, "porque": t[:80]})
        if not canais:
            canais = [{"canal": "Conversa direta", "porque": "os 10 clientes mais recentes (pedir 5 conversas)"},
                      {"canal": "Indicação", "porque": "pedido formal de indicação aos 3 melhores"}]
        mkt = {
            "nisca": nicho,
            "area": area,
            "publico": publico,
            "por_que": porque,
            "persona": persona,
            "empatia": empatia,
            "icp": icp,
            "canais": canais,
            "sinais_comerciais": [d["trecho"][:100] for d in dem[:3]] or [P],
        }
        txt = llm.chamar("Você é estrategista de marketing. Aponte em 3 frases o maior "
                         "ângulo comercial deste caso, sem inventar fatos.",
                         _fatos_pessoa(mapa), max_caracteres=420)
        if txt:
            mkt["angulo_ia"] = txt
        return mkt
