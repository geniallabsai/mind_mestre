# -*- coding: utf-8 -*-
"""Cético — agente 9 de 11.

Ataca o diagnóstico que anda sem evidência: hipótese sem lastro, sinal sem
contexto, objetivo sem preço, plano sem data. Toda objeção traz endereço
(arquivo:linha) — ou confessa que aponta para o mapa."""
import re


class Cetico:
    nome = "Cético"
    papel = "ataca o diagnóstico sem evidência: hipótese sem lastro, sinal sem contexto, plano sem data"

    def objetar(self, mapa, det):
        objecoes = []
        for h in det.get("hipoteses", [])[:4]:
            if h["suporte"] < 2 and h["confianca"] > 0:
                ev = h["evidencias"][0]["arquivo"] if h["evidencias"] else "mapa.json"
                objecoes.append({"nivel": "medio", "evidencia": ev,
                                  "texto": "Hipótese '%s' com apenas %d evidência — diagnóstico apoiado em achismo." % (h["titulo"], h["suporte"])})
        vistos = {}
        for s in mapa.get("sinais", []):
            vistos.setdefault(s["tipo"], []).append(s)
        for tipo, lst in vistos.items():
            if len(lst) == 1 and lst[0]["nivel"] == "alto":
                objecoes.append({"nivel": "medio",
                                  "evidencia": "%s:%s" % (lst[0]["arquivo"], lst[0].get("linha") or "?"),
                                  "texto": "Sinal forte '%s' citado uma única vez — pode ser ruído de frase, não padrão de vida." % lst[0]["titulo"]})
        obj_declarado = mapa.get("objetivo_declarado")
        if obj_declarado and not re.search(r"(cobrar|preco|vender|matricula|valor)", obj_declarado, re.I):
            ev_src = next((s for s in mapa.get("sinais", []) if s["tipo"] == "oferta"), None)
            ev = ("%s:%s" % (ev_src["arquivo"], ev_src.get("linha") or "?")) if ev_src else "mapa.json"
            objecoes.append({"nivel": "medio", "evidencia": ev,
                              "texto": "Objetivo declarado sem formato nem preço — 'criar um curso' não é oferta, é intenção."})
        tem_data = any(re.search(r"(dias|\d{1,2}/\d{2}|que vem|fech)", n.get("contexto", ""), re.I)
                       for n in mapa.get("numeros", []))
        if not tem_data:
            objecoes.append({"nivel": "baixo", "evidencia": "mapa.json",
                              "texto": "Nenhuma data ou prazo no material — plano sem data é desejo, não compromisso."})
        if mapa.get("quero_produto") and not any(a["tipo"] == "demanda" for a in mapa.get("ativos", [])):
            objecoes.append({"nivel": "alto", "evidencia": "mapa.json",
                              "texto": "Quer produto, mas nenhuma prova de que alguém pagaria — lançar antes de validar é aposta, não negócio."})
        arquivos_fonte = {s["arquivo"] for s in mapa.get("sinais", []) if s.get("nivel") == "alto"}
        if len(arquivos_fonte) == 1:
            objecoes.append({"nivel": "medio", "evidencia": sorted(arquivos_fonte)[0] + ":?",
                              "texto": "Diagnóstico apoiado numa única fonte — triangule com a conversa antes de voar."})
        opiniao = next((s for s in mapa.get("sinais", []) if s["tipo"] == "validacao"), None)
        if opiniao:
            objecoes.append({"nivel": "baixo",
                              "evidencia": "%s:%s" % (opiniao["arquivo"], opiniao.get("linha") or "?"),
                              "texto": "Opinião externa negativa no caso ('%s') — separar o mercado da família." % opiniao["trecho"][:48]})
        if not det.get("principal") or det.get("principal") == "incompleto":
            objecoes.append({"nivel": "critico", "evidencia": "mapa.json",
                              "texto": "Material insuficiente: nenhum padrão forte. O plano será especulativo — aprofunde a conversa antes de voar."})
        return objecoes[:8]
