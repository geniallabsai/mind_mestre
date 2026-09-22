# -*- coding: utf-8 -*-
"""Detetive — agente 2 de 11.

Transforma o mapa em hipóteses do travamento, testa cada uma contra
evidência e ranqueia. Hipótese sem evidência é achismo; achismo não entra
no diagnóstico."""
import re

from mind_core import llm
from .comum import _fatos_pessoa

# id: (titulo, [tipos de sinal que sustentam], [tipos de ativo que refutam])
HIPOTESES = [
    ("exposicao", "O muro é o medo de exposição", ["exposicao"], ["audiencia"]),
    ("tempo", "Esperando o momento perfeito que nunca chega", ["procrastinacao", "tempo"], []),
    ("oferta", "A oferta ainda não existe (existe só a ideia)", ["oferta"], []),
    ("valor", "Preço baixo esconde desvalorização", ["desvalorizacao", "dinheiro"], []),
    ("foco", "Muitas frentes abertas, nenhuma principal", ["dispersao"], []),
    ("prova", "Falta prova — e falta ouvir quem já compraria", ["validacao"], ["prova_social"]),
]

PESO = {"alto": 3, "medio": 2, "baixo": 1}

# Taxa-base de cada parede em travamentos profissionais (prior bayesiano):
# medo de exposição é a parede mais documentada em quem quer lançar pela
# primeira vez — entra no score antes da evidência, não depois dela.
PRIOR = {"exposicao": 20}


def _dedup_contraria(lista):
    """A mesma plateia citada duas vezes não refuta duas vezes."""
    vistos, out = set(), []
    for a in lista:
        chave = re.sub(r"\D", "", a.get("trecho", ""))[:24] or a.get("evidencia", "")[:20]
        if chave in vistos:
            continue
        vistos.add(chave)
        out.append(a)
    return out


class Detetive:
    nome = "Detetive"
    papel = "forma hipóteses do travamento, testa cada uma contra evidência e ranqueia o diagnóstico"

    def investigar(self, mapa, ao_avisar=None):
        hipoteses = []
        for hid, titulo, suporta, refuta in HIPOTESES:
            suporte = [s for s in mapa.get("sinais", []) if s["tipo"] in suporta]
            contra = _dedup_contraria([a for a in mapa.get("ativos", []) if a["tipo"] in refuta])
            pont = sum(PESO.get(s["nivel"], 1) for s in suporte)
            if not suporte:
                continue
            conf = 15 * pont + 8 * max(0, min(len(suporte), 3) - 1) + PRIOR.get(hid, 0)
            if len({s["tipo"] for s in suporte}) > 1:
                conf -= 8
            conf -= 10 * len(contra)
            hipoteses.append({
                "id": hid,
                "titulo": titulo,
                "confianca": max(0, min(95, conf)),
                "status": "em teste",
                "suporte": len(suporte),
                "evidencias": [{"arquivo": s["arquivo"], "linha": s.get("linha"),
                                "trecho": s["trecho"]} for s in suporte[:4]],
                "contra": [{"tipo": a["tipo"], "evidencia": a["evidencia"]} for a in contra[:2]],
            })
        hipoteses.sort(key=lambda h: (-h["confianca"], -h["suporte"], -PRIOR.get(h["id"], 0)))
        if not hipoteses:
            hipoteses.append({"id": "incompleto", "titulo": "Material insuficiente — aprofundar conversa",
                              "confianca": 5, "status": "em teste", "suporte": 0,
                              "evidencias": [], "contra": []})
        principal = hipoteses[0]
        det = {
            "hipoteses": hipoteses,
            "principal": principal["id"],
            "principal_titulo": principal["titulo"],
            "perguntas_abertas": _perguntas_abertas(principal["id"]),
            "resumo": "diagnóstico principal: %s (confiança %d) · %d hipóteses testadas"
                      % (principal["titulo"], principal["confianca"], len(hipoteses)),
        }
        txt = llm.chamar("Você é um detetive de carreiras. Dê uma leitura independente "
                         "do caso em 5 frases curtas, sem jargão.",
                         _fatos_pessoa(mapa), max_caracteres=700)
        if txt:
            det["leitura_ia"] = txt
        return det


def _perguntas_abertas(hid):
    BANCO = {
        "exposicao": ["Qual seria o formato MENOR de aparecer (voz, bastidor, aula gravada) que você aceita fazer esta semana?",
                      "Quem, exatamente, você tem medo que veja — e o que essa pessoa já viu de você?"],
        "tempo": ["Qual é a data real que te impede de começar — e quem escolheu ela?",
                  "Se o lançamento fosse em 30 dias, o que você gravaria amanhã?"],
        "oferta": ["Se você cobrasse hoje pelo que resolve, qual número sairia da sua boca?",
                   "Descreva UMA entrega concreta: em quantas sessões, o aluno sai com o quê?"],
        "valor": ["Quanto seu cliente já paga para quem resolve isso hoje?",
                  "Qual prova você tem de que vale mais que o preço que cobra?"],
        "foco": ["Das suas frentes, qual paga a primeira fatura em 90 dias?",
                 "Que frente você mataria hoje, sem culpa?"],
        "prova": ["Quais 3 clientes recentes você citaria como caso (com permissão)?",
                  "O que eles disseram com suas palavras — pode transcrever?"],
    }
    return BANCO.get(hid, ["Conte-me o último dia em que esse travamento apareceu, do começo ao fim."])[:2]
