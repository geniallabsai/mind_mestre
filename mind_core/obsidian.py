# -*- coding: utf-8 -*-
"""Vault Obsidian — MOC, uma nota por fase, veredito do juiz e mapa estrutural.
Frontmatter YAML, [[wikilinks]] que sempre resolvem, fence mermaid nativo e
callouts. Arraste a pasta no Obsidian e abra 00-moc."""
import os


def _fm(tags, extra=None):
    linhas = ["---", "tags: [%s]" % ", ".join(tags)]
    linhas.extend(extra or [])
    linhas.append("---")
    return "\n".join(linhas) + "\n\n"


def _blocos_md(blocos):
    L = []
    for b in blocos:
        t = b["tipo"]
        if t == "p":
            L.append(b.get("texto", "") + "\n")
        elif t == "lista":
            L.extend("- %s\n" % it for it in b.get("itens", []))
            L.append("\n")
        elif t == "citacao":
            L.append("> %s  \n> — *%s*\n" % (b.get("texto", ""), b.get("evidencia", "")))
        elif t == "codigo":
            L.append("**%s**\n\n```\n" % b.get("titulo", ""))
            L.extend("%2d. %s\n" % (i + 1, x) for i, x in enumerate(b.get("itens", [])))
            L.append("```\n")
        elif t == "nota":
            L.append("> [!note]  \n")
            L.extend("> %s  \n" % l for l in b.get("texto", "").split("\n"))
    return "".join(L)


def gerar_vault(diretorio, plano, mapa, mmd_mapa, mmd_plano):
    """Escreve as 9 notas. Retorna a lista de notas criadas."""
    fases = plano["fases"]
    nomes = {"f%d" % f["n"]: "0%d-%s" % (f["n"], f["slug"]) for f in fases}

    def nota(nome, corpo):
        with open(os.path.join(diretorio, nome + ".md"), "w", encoding="utf-8", newline="") as f:
            f.write(corpo)

    selo = plano["selo_juiz"]
    moc = _fm(["mind-mestre", "plano"], ["alias: [Plano Mind Mestre]"])
    moc += "# Plano — %s\n\n" % plano["titulo"]
    moc += "> %s\n>\n> Confiança **%d/100** · %s\n\n" % (plano["meta"], selo["confianca"], selo["decisao"])
    moc += "## Fases\n\n"
    for f in fases:
        moc += "- [[%s|**Fase %d — %s**]] — %s\n" % (nomes["f%d" % f["n"]], f["n"], f["titulo"][:44], f["objetivo"][:80])
    moc += "\n- [[veredito-do-juiz|**Veredito do Juiz**]] — Cético × Convicto, aritmética aberta\n"
    moc += "- [[mapa-estrutural|**Mapa Estrutural**]] — sinais, ativos e objetivo com endereço da prova\n\n"
    moc += "## Fluxo do plano\n\n```mermaid\n%s\n```\n\n" % mmd_plano
    moc += '> Prompt para outros agentes: "Leia as 6 notas e o veredito. Me faça 3 perguntas de prova antes de eu seguir a fase 2."\n'
    nota("00-moc", moc)

    for i, f in enumerate(fases, 1):
        corpo = _fm(["mind-mestre", "fase-%d" % i], ["fase: %d" % i])
        corpo += "# Fase %d — %s\n\n**Objetivo:** %s\n\n" % (f["n"], f["titulo"], f["objetivo"])
        corpo += _blocos_md(f["blocos"])
        nav = []
        if i > 1:
            nav.append("[[%s|%d · anterior]]" % (nomes["f%d" % (i - 1)], i - 1))
        nav.append("[[00-moc|MOC]]")
        if i < len(fases):
            nav.append("[[%s|%d · próxima]]" % (nomes["f%d" % (i + 1)], i + 1))
        corpo += "\n---\n%s\n" % " · ".join(nav)
        nota(nomes["f%d" % i], corpo)

    trib = plano.get("tribunal", {})
    v = _fm(["mind-mestre", "tribunal"], ["confianca: %d" % selo["confianca"]])
    v += "# Veredito do Juiz\n\nConfiança **%d/100**\n\n```\n%s\n```\n\n%s\n\n%s\n\n" % (
        selo["confianca"], selo["barra"], selo["decisao"], selo["resumo"])
    v += "## Objeções — Cético\n\n"
    v += "".join("- [%s] %s  \n  *evidência: %s*\n" % (o["nivel"], o["texto"], o.get("evidencia", "")) for o in trib.get("objecoes", [])) or "- (nenhuma)\n"
    v += "\n## Defesas — Convicto\n\n"
    v += "".join("- %s  \n  *evidência: %s*\n" % (d["texto"], d.get("evidencia", "")) for d in trib.get("defesas", [])) or "- (nenhuma)\n"
    v += "\n---\n[[00-moc|MOC]] · [[%s|Fase 1]]\n" % nomes["f1"]
    nota("veredito-do-juiz", v)

    m = _fm(["mind-mestre", "mapa"])
    m += "# Mapa Estrutural\n\n**Pessoa:** %s · **origem:** %s\n\n" % (
        mapa.get("persona_nome") or mapa.get("nome"), mapa.get("origem", "?"))
    m += "```mermaid\n%s\n```\n\n## Sinais (com endereço)\n\n| tipo | nível | onde |\n|---|---|---|\n" % mmd_mapa
    m += "".join("| %s | %s | %s:%s |\n" % (s["tipo"], s["nivel"], s["arquivo"], s.get("linha") or "?") for s in mapa.get("sinais", []))
    m += "\n## Ativos\n\n"
    m += "".join("- **%s** — %s  \n  *%s*\n" % (a["tipo"].replace("_", " ").capitalize(), a.get("trecho", "")[:90], a["evidencia"]) for a in mapa.get("ativos", []))
    m += "\n---\n[[00-moc|MOC]]\n"
    nota("mapa-estrutural", m)
    return sorted(x[:-3] for x in os.listdir(diretorio) if x.endswith(".md"))
