# -*- coding: utf-8 -*-
"""Convicto — agente 10 de 11.

Defende a leitura com evidência: história consistente entre arquivos,
ativos quantificados, demanda fora da cabeça, posição construída com tempo.
Toda defesa traz endereço — convicção sem prova é fé."""
import re


class Convicto:
    nome = "Convicto"
    papel = "defende o diagnóstico com evidência: história consistente, ativos quantificados, demanda fora da cabeça"

    def defender(self, mapa, det):
        defesas = []
        temas_arquivos = {}
        for s in mapa.get("sinais", []):
            temas_arquivos.setdefault(s["tipo"], set()).add(s["arquivo"])
        multi = [t for t, a in temas_arquivos.items() if len(a) >= 2]
        if multi:
            ev = next(s["arquivo"] for s in mapa["sinais"] if s["tipo"] in multi)
            defesas.append({"texto": "O padrão aparece em arquivos diferentes — história consistente, não piada de um dia.",
                             "evidencia": ev})
        quant = [a for a in mapa.get("ativos", []) if re.search(r"\d", a.get("trecho", ""))]
        if quant:
            defesas.append({"texto": "Ativos quantificados no material: %s" % re.sub(r"\s+", " ", quant[0]["trecho"])[:70],
                             "evidencia": quant[0]["evidencia"]})
        dem = [a for a in mapa.get("ativos", []) if a["tipo"] == "demanda"]
        if dem:
            defesas.append({"texto": "A demanda existe fora da cabeça: as pessoas pedem com a própria boca.",
                             "evidencia": dem[0]["evidencia"]})
        esp = [a for a in mapa.get("ativos", []) if a["tipo"] == "especialidade"]
        if esp:
            defesas.append({"texto": "Posição construída por tempo, não inventada por trend.",
                             "evidencia": esp[0]["evidencia"]})
        aud = [a for a in mapa.get("ativos", []) if a["tipo"] == "audiencia"]
        if aud:
            defesas.append({"texto": "Já existe plateia: o palco só falta ser ocupado.",
                             "evidencia": aud[0]["evidencia"]})
        rest = [s for s in mapa.get("sinais", []) if s["tipo"] in ("tempo", "dinheiro")]
        if rest:
            defesas.append({"texto": "Reconhece a própria restrição (tempo/dinheiro) — realismo raro em quem quer lançar.",
                             "evidencia": "%s:%s" % (rest[0]["arquivo"], rest[0].get("linha") or "?")})
        if not defesas:
            defesas.append({"texto": "Material limpo: cada afirmação do plano aponta para algo verificável no mapa.",
                             "evidencia": "mapa.json"})
        return defesas[:8]
