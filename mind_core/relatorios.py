# -*- coding: utf-8 -*-
"""Publicador: plano.md (para outros agentes), plano.pdf, plano.docx,
mapa.json, mapa.mmd, plano.mmd, obsidian/. Escreve os sete — saída não é
opção, é contrato."""
import json
import os

from . import mermaid, obsidian
from .arte import bloco
from .docx import Docx
from .pdf import Pdf


def _blocos_md(blocos):
    L = []
    for b in blocos:
        t = b["tipo"]
        if t == "p":
            L.append(b.get("texto", ""))
            L.append("")
        elif t == "lista":
            L.extend("- %s" % it for it in b.get("itens", []))
            L.append("")
        elif t == "citacao":
            L.extend(["> %s  " % b.get("texto", ""), "> — *%s*" % b.get("evidencia", ""), ""])
        elif t == "codigo":
            L.extend(["**%s**" % b.get("titulo", ""), "```"])
            L.extend(b.get("itens", []))
            L.extend(["```", ""])
        elif t == "nota":
            L.extend(["> [!note]", "> " + b.get("texto", "").replace("\n", " "), ""])
    return L


def md_plano(plano, mapa):
    L = ["# %s" % plano["titulo"], "", plano["meta"], ""]
    L.extend(["> **Selo do Juiz:** %s" % plano["selo_juiz"]["decisao"],
              "> Confiança **%d/100** `%s` · %s" % (plano["selo_juiz"]["confianca"], plano["selo_juiz"]["barra"], plano["selo_juiz"]["resumo"]), ""])
    for f in plano["fases"]:
        L.extend(["## Fase %d — %s" % (f["n"], f["titulo"]), "", "**Objetivo:** %s" % f["objetivo"], ""])
        L.extend(_blocos_md(f["blocos"]))
    curso = plano.get("curso") or {}
    if curso.get("ativo"):
        L.extend(["## O curso — %s" % curso["titulo"], ""])
        for mod in curso["modulos"]:
            L.extend(["### %s" % mod["nome"], "", mod["objetivo"], ""])
            L.extend("- %s" % a for a in mod["aulas"])
            L.extend(["", "**Resultado:** %s" % mod["resultado"], ""])
    L.extend(["## Voo 30/60/90", ""])
    for j in plano["voo_30_60_90"]:
        L.append("**%s — %s**" % (j["janela"], j["foco"]))
        L.extend("- %s" % a for a in j["acoes"])
        L.append("")
    of = plano["oferta"]
    L.extend(["## Oferta (síntese)", "",
              "**Estratégia (estágio %d):** %s" % (of["estagio_mercado"], of["estrategia"]), ""])
    L.extend(["%d. %s — *%s*" % (i + 1, h["texto"], h["tecnica"]) for i, h in enumerate(of["headlines"])])
    L.extend(["", "Promessa: %s" % of["promessa"], "", "Subtítulo: %s" % of["subtitulo"], ""])
    L.extend(["**Benefícios:**", ""])
    L.extend("- %s — %s" % (b["t"], b["sub"]) for b in of["beneficios"])
    L.extend(["", "**Bônus:**", ""])
    L.extend("- %s" % b for b in of["bonus"])
    L.extend(["", "Garantia: %s" % of["reversao_risco"], "", "Urgência: %s" % of["urgencia"], "", "CTA: %s" % of["cta"], ""])
    L.extend(["## Para outros agentes", "", "```json",
              json.dumps({
                  "plano": {"titulo": plano["titulo"], "meta": plano["meta"],
                             "selo_juiz": plano["selo_juiz"],
                             "fases": [{"n": f["n"], "slug": f["slug"], "titulo": f["titulo"]} for f in plano["fases"]]},
                  "evidencia": "mapa.json",
                  "prompts": plano["prompts"]},
                  ensure_ascii=False, indent=1),
              "```", ""])
    return "\n".join(L)


def _blocos_pdf(p, blocos):
    for b in blocos:
        t = b["tipo"]
        if t == "p":
            p.texto(b.get("texto", ""))
        elif t == "lista":
            p.lista(b.get("itens", []))
        elif t == "citacao":
            p.nota(b.get("texto", ""), autor=b.get("evidencia", ""))
        elif t == "codigo":
            p.bloco_codigo(b.get("itens", []), titulo=b.get("titulo"))
        elif t == "nota":
            p.nota(b.get("texto", ""))


def pdf_plano(plano, mapa):
    p = Pdf()
    p.bloco_codigo(bloco())
    p.h1(plano["titulo"])
    p.texto(plano["meta"], tam=11)
    p.quebra_pagina()
    p.h2("Selo do Juiz")
    p.bloco_codigo([plano["selo_juiz"]["barra"]])
    p.texto(plano["selo_juiz"]["decisao"])
    p.texto(plano["selo_juiz"]["resumo"], tam=9)
    for f in plano["fases"]:
        p.quebra_pagina()
        p.h2("Fase %d — %s" % (f["n"], f["titulo"]))
        p.texto("Objetivo: " + f["objetivo"], tam=10)
        p.regua()
        _blocos_pdf(p, f["blocos"])
    curso = plano.get("curso") or {}
    if curso.get("ativo"):
        p.quebra_pagina()
        p.h1(curso["titulo"])
        for mod in curso["modulos"]:
            p.h2(mod["nome"])
            p.texto(mod["objetivo"], tam=10)
            p.lista(mod["aulas"])
            p.nota("Resultado: " + mod["resultado"])
    p.quebra_pagina()
    p.h1("Voo 30/60/90")
    for j in plano["voo_30_60_90"]:
        p.h2("%s — %s" % (j["janela"], j["foco"]))
        p.lista(j["acoes"])
    p.quebra_pagina()
    p.h1("Oferta")
    p.texto("Estratégia (estágio %d): %s" % (plano["oferta"]["estagio_mercado"], plano["oferta"]["estrategia"]), tam=10)
    p.h2("Headlines")
    p.lista(["%s  (%s)" % (h["texto"], h["tecnica"]) for h in plano["oferta"]["headlines"]])
    p.texto("Promessa: " + plano["oferta"]["promessa"], tam=10)
    p.texto(plano["oferta"]["subtitulo"], tam=10)
    p.h2("Benefícios")
    p.lista(["%s — %s" % (b["t"], b["sub"]) for b in plano["oferta"]["beneficios"]])
    p.h2("Bônus")
    p.lista(plano["oferta"]["bonus"])
    p.h2("Garantia / Urgência / CTA")
    p.nota(plano["oferta"]["reversao_risco"], autor="garantia")
    p.texto(plano["oferta"]["urgencia"], tam=10)
    p.texto("CTA: " + plano["oferta"]["cta"], tam=10)
    p.bloco_codigo(plano["oferta"]["pagina"], titulo="Página da oferta (8 blocos)")
    p.quebra_pagina()
    p.h1("Para outros agentes")
    p.lista(plano["prompts"])
    return p.para_bytes()


def docx_plano(plano, mapa):
    d = Docx()
    d.h1(plano["titulo"])
    d.texto(plano["meta"], i=True)
    d.h2("Selo do Juiz")
    d.bloco_codigo([plano["selo_juiz"]["barra"]])
    d.texto(plano["selo_juiz"]["decisao"], b=True)
    d.texto(plano["selo_juiz"]["resumo"], tam=18)
    d.quebra_pagina()
    for f in plano["fases"]:
        d.h2("Fase %d — %s" % (f["n"], f["titulo"]))
        d.texto("Objetivo: " + f["objetivo"], i=True)
        for b in f["blocos"]:
            if b["tipo"] == "p":
                d.texto(b.get("texto", ""))
            elif b["tipo"] == "lista":
                d.lista(b.get("itens", []))
            elif b["tipo"] == "citacao":
                d.nota(b.get("texto", ""), autor=b.get("evidencia", ""))
            elif b["tipo"] == "codigo":
                d.bloco_codigo(b.get("itens", []), titulo=b.get("titulo"))
            elif b["tipo"] == "nota":
                d.nota(b.get("texto", ""))
        d.quebra_pagina()
    curso = plano.get("curso") or {}
    if curso.get("ativo"):
        d.h1(curso["titulo"])
        for mod in curso["modulos"]:
            d.h2(mod["nome"])
            d.texto(mod["objetivo"])
            d.lista(mod["aulas"])
            d.nota("Resultado: " + mod["resultado"])
        d.quebra_pagina()
    d.h1("Voo 30/60/90")
    for j in plano["voo_30_60_90"]:
        d.h2("%s — %s" % (j["janela"], j["foco"]))
        d.lista(j["acoes"])
    d.h1("Oferta")
    d.texto("Estratégia (estágio %d): %s" % (plano["oferta"]["estagio_mercado"], plano["oferta"]["estrategia"]))
    d.lista(["%s  (%s)" % (h["texto"], h["tecnica"]) for h in plano["oferta"]["headlines"]])
    d.texto("Promessa: " + plano["oferta"]["promessa"])
    d.texto(plano["oferta"]["subtitulo"], i=True)
    d.h2("Benefícios")
    d.lista(["%s — %s" % (b["t"], b["sub"]) for b in plano["oferta"]["beneficios"]])
    d.h2("Bônus")
    d.lista(plano["oferta"]["bonus"])
    d.texto("Garantia: " + plano["oferta"]["reversao_risco"])
    d.texto("Urgência: " + plano["oferta"]["urgencia"])
    d.texto("CTA: " + plano["oferta"]["cta"])
    d.bloco_codigo(plano["oferta"]["pagina"], titulo="Página da oferta (8 blocos)")
    d.h1("Para outros agentes")
    d.lista(plano["prompts"])
    return d.para_bytes()


def escrever_tudo(base, plano, mapa):
    """Os 7 artefatos. Retorna {chave: caminho} na ordem do checklist."""
    os.makedirs(base, exist_ok=True)
    cam = {}
    mmd_mapa_txt = mermaid.mapa_mermaid(mapa)
    mmd_plano_txt = mermaid.plano_mermaid(plano)
    with open(os.path.join(base, "plano.md"), "w", encoding="utf-8", newline="") as f:
        f.write(md_plano(plano, mapa))
    cam["md"] = os.path.join(base, "plano.md")
    with open(os.path.join(base, "mapa.json"), "w", encoding="utf-8", newline="") as f:
        json.dump(mapa, f, ensure_ascii=False, indent=1)
    cam["mapa_json"] = os.path.join(base, "mapa.json")
    with open(os.path.join(base, "mapa.mmd"), "w", encoding="utf-8", newline="") as f:
        f.write(mmd_mapa_txt + "\n")
    cam["mmd_mapa"] = os.path.join(base, "mapa.mmd")
    with open(os.path.join(base, "plano.mmd"), "w", encoding="utf-8", newline="") as f:
        f.write(mmd_plano_txt + "\n")
    cam["mmd_plano"] = os.path.join(base, "plano.mmd")
    with open(os.path.join(base, "plano.pdf"), "wb") as f:
        f.write(pdf_plano(plano, mapa))
    cam["pdf"] = os.path.join(base, "plano.pdf")
    with open(os.path.join(base, "plano.docx"), "wb") as f:
        f.write(docx_plano(plano, mapa))
    cam["docx"] = os.path.join(base, "plano.docx")
    vault = os.path.join(base, "obsidian")
    os.makedirs(vault, exist_ok=True)
    obsidian.gerar_vault(vault, plano, mapa, mmd_mapa_txt, mmd_plano_txt)
    cam["obsidian"] = vault
    return cam
