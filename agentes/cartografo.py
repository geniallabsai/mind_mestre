# -*- coding: utf-8 -*-
"""Cartógrafo — agente 1 de 11.

Lê TODO o material da pessoa (notas, entrevistas, ideias, conquistas) e
mapeia a vida profissional: sinais de intenção, ativos reais, objetivo
declarado, números concretos. É o único agente que toca o texto — os outros
discutem este mapa."""
import os
import re

from mind_core import leitura_pessoal, padroes


class Cartografo:
    nome = "Cartógrafo"
    papel = "lê todo o material da pessoa e mapeia a vida profissional: sinais, ativos, objetivo"

    def destrinchar(self, alvo, ao_avisar=None):
        alvo_abs = os.path.abspath(alvo)
        caminhos = leitura_pessoal.listar_arquivos(alvo_abs)
        base = alvo_abs if os.path.isdir(alvo_abs) else os.path.dirname(alvo_abs)
        if ao_avisar:
            ao_avisar("lendo o material da pessoa", 0, len(caminhos))
        textos, palavras, secoes = [], 0, []
        for i, cam in enumerate(caminhos, 1):
            txt = leitura_pessoal.ler_texto(cam)
            palavras += len(txt.split())
            rel = os.path.relpath(cam, base).replace(os.sep, "/")
            textos.append((rel, txt))
            secoes.extend(leitura_pessoal.extrair_secoes(txt, rel))
            if ao_avisar:
                ao_avisar("lendo o material da pessoa", i, len(caminhos))
        sinais, ativos, produtos = padroes.detectar(textos)
        if len(produtos) >= 3:
            prim = base
            for rel, t in textos:
                if any(p in padroes.normalizar(t) for p in produtos[:3]):
                    prim = rel
                    break
            sinais.append({"tipo": "dispersao", "nivel": "medio",
                           "titulo": "Várias frentes abertas ao mesmo tempo",
                           "arquivo": prim, "linha": None,
                           "trecho": "ideias em aberto: " + ", ".join(produtos[:5])})
        obj = padroes.objetivo(textos)
        nome = padroes.nome_pessoa(textos)
        nums = padroes.numeros(textos)
        norm_all = " ".join(padroes.normalizar(t) for _, t in textos)
        querer = bool(re.search(r"\b(quero|gostaria|pretendo|sonho de)\b", norm_all))
        quero_produto = bool(obj and any(p in padroes.normalizar(obj["texto"]) for p in padroes.PRODUTOS)) \
            or (querer and len(produtos) > 0)

        mapa = {
            "nome": os.path.basename(alvo_abs),
            "persona_nome": nome,
            "origem": alvo_abs,
            "arquivos_total": len(caminhos),
            "palavras": palavras,
            "secoes": secoes,
            "sinais": sinais,
            "ativos": ativos,
            "produtos_mentionados": produtos,
            "objetivo_declarado": obj["texto"] if obj else None,
            "quero_produto": quero_produto,
            "numeros": nums,
        }
        mapa["resumo"] = self._resumo(mapa)
        return mapa

    @staticmethod
    def _resumo(mapa):
        pecas = []
        if mapa.get("persona_nome"):
            pecas.append(mapa["persona_nome"])
        esp = next((a["trecho"] for a in mapa["ativos"] if a["tipo"] == "especialidade"), None)
        if esp:
            p = re.split(r"[.;,]", esp)[0].strip()
            pecas.append(p[:70])
        if mapa.get("objetivo_declarado"):
            pecas.append("quer: " + re.split(r"[.;,]", mapa["objetivo_declarado"])[0][:70])
        muros = [s["titulo"] for s in mapa["sinais"] if s["nivel"] == "alto"]
        if muros:
            pecas.append("muro: " + muros[0].lower())
        dem = sum(1 for a in mapa["ativos"] if a["tipo"] == "demanda")
        if dem:
            pecas.append("%d provas de demanda real" % dem)
        return " · ".join(p for p in pecas if p)[:230]
