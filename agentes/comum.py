# -*- coding: utf-8 -*-
"""comum — material compartilhado dos agentes.

O retrato `_fatos_pessoa` é o único pedaço do mapa que os agentes enxergam
em prosa ao pedir ajuda ao modelo de IA: nome, resumo, objetivo, top de
sinais, ativos e números, cortado para caber num prompt. Os agentes não
lem disco; leem esse retrato (e o mapa estruturado).
"""
import json


def _fatos_pessoa(mapa, limite=1600):
    trecho = {
        "nome": mapa.get("persona_nome") or mapa.get("nome"),
        "resumo": (mapa.get("resumo") or "")[:240],
        "objetivo": mapa.get("objetivo_declarado"),
        "produtos_mentionados": mapa.get("produtos_mentionados"),
        "sinais": [{"tipo": s["tipo"], "nivel": s["nivel"], "trecho": s["trecho"]}
                   for s in mapa.get("sinais", [])[:8]],
        "ativos": [{"tipo": a["tipo"], "evidencia": a["evidencia"]}
                   for a in mapa.get("ativos", [])[:8]],
        "numeros": [n["contexto"] for n in mapa.get("numeros", [])[:6]],
    }
    return json.dumps(trecho, ensure_ascii=False)[:limite]
