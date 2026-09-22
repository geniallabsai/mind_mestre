# -*- coding: utf-8 -*-
"""Juiz — agente 11 de 11.

Pontua objeções × defesas com a mesma aritmética aberta do Instalador
(PENTO crítico 8 / alto 5 / médio 2 / baixo 1; confiança = clamp(90−pena+ganho,
5, 99)) e emite o veredito: faixas e barra. A matemática está no arquivo:
ninguém esconde peso."""

NIVEL_PENTO = {"critico": 8, "alto": 5, "medio": 2, "baixo": 1}


def barra(confianca, tamanho=20):
    cheio = max(0, min(tamanho, int(round(confianca / 100.0 * tamanho))))
    return "█" * cheio + "░" * (tamanho - cheio)


class Juiz:
    nome = "Juiz"
    papel = "pontua objeções × defesas com aritmética aberta e emite o veredito"

    def decidir(self, mapa, det, objecoes, defesas):
        pena = sum(NIVEL_PENTO.get(o.get("nivel", "baixo"), 1) for o in objecoes)
        ganho = min(10, 2 * len(defesas))
        confianca = max(5, min(99, 90 - pena + ganho))
        if confianca >= 80:
            decisao = "Diagnóstico sólido — pode decolar: o plano avança com as ressalvas citadas."
        elif confianca >= 55:
            decisao = "Sólido com ressalvas — responda as perguntas abertas antes de gravar qualquer coisa."
        else:
            decisao = "Nevoeiro ainda — aprofunde a conversa (mindmestre conversa) antes de apostar o plano."
        return {"confianca": confianca, "decisao": decisao, "barra": barra(confianca),
                 "pontuacao": {"pena": pena, "ganho": ganho},
                 "resumo": "pena %d × ganho %d → confiança %d/100" % (pena, ganho, confianca),
                 "objecoes": objecoes, "defesas": defesas}
