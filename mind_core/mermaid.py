# -*- coding: utf-8 -*-
"""Diagramas mermaid: mapa.mmd (pessoa × sinais × ativos × objetivo) e
plano.mmd (selo do juiz → 6 fases → decolagem). Texto puro, ids ASCII,
rótulos entre aspas para o mermaid não engasgar."""


def _limpo(t, n=40):
    t = " ".join((t or "").replace(chr(34), chr(39)).split())
    return t[:n].rstrip()


def mapa_mermaid(mapa, max_nos=28):
    L = ["flowchart TD"]
    nome = _limpo(mapa.get("persona_nome") or mapa.get("nome") or "a pessoa", 30)
    L.append('    P(["%s"])' % nome)
    n = 1
    for i, s in enumerate(mapa.get("sinais", [])):
        if n >= max_nos:
            break
        nid = "S%d" % (i + 1)
        L.append('    %s["Muro: %s [%s]"]' % (nid, _limpo(s["titulo"], 34), s["nivel"]))
        L.append('    P -->|"sinal"| %s' % nid)
        n += 1
    for i, a in enumerate(mapa.get("ativos", [])):
        if n >= max_nos:
            break
        nid = "A%d" % (i + 1)
        rotulo = a["tipo"].replace("_", " ").capitalize()
        L.append('    %s["Ativo: %s"]' % (nid, rotulo))
        L.append('    P -->|"prova"| %s' % nid)
        n += 1
    if mapa.get("objetivo_declarado"):
        L.append('    O["Objetivo: %s"]' % _limpo(mapa["objetivo_declarado"], 42))
        L.append("    P -->|declarado| O")
    return "\n".join(L)


def plano_mermaid(plano):
    selo = plano.get("selo_juiz", {})
    L = ["flowchart TD"]
    L.append('    J["Selo do Juiz: %d/100"]' % selo.get("confianca", 0))
    ant = "J"
    for f in plano.get("fases", []):
        fid = "F%d" % f["n"]
        L.append('    %s["Fase %d — %s"]' % (fid, f["n"], _limpo(f["titulo"], 36)))
        L.append("    %s --> %s" % (ant, fid))
        ant = fid
    L.append('    V["Decolagem: 30/60/90"]')
    L.append("    %s --> V" % ant)
    return "\n".join(L)
