# -*- coding: utf-8 -*-
"""Posicionador — agente 7 de 11.

Define o território da marca: sentença de posicionamento, promessa,
diferenciadores com evidência, voz (o que faz e o que NÃO faz) e candidatos
a nome. Marca sem território é vitrine sem endereço."""
import re

from .comum import _fatos_pessoa
from mind_core import llm


def _ativos_tipo(mapa, tipo):
    return [a for a in mapa.get("ativos", []) if a["tipo"] == tipo]


def _diferencadores(mapa):
    difs = []
    esp = _ativos_tipo(mapa, "especialidade")
    if esp:
        m = re.search(r"(\d+)\s*anos", esp[0].get("trecho", ""))
        difs.append({"t": ("%s anos de estrada (não de teoria)" % m.group(1)) if m else "Anos de estrada (não de teoria)",
                     "porque": "tempo de campo não se fabrica em curso",
                     "evidencia": esp[0]["evidencia"]})
    port = _ativos_tipo(mapa, "portefolio")
    for a in port[:2]:
        difs.append({"t": a["trecho"][:70].rstrip(" ,."),
                     "porque": "ativo concreto, verificável",
                     "evidencia": a["evidencia"]})
    prova = _ativos_tipo(mapa, "prova_social")
    if prova:
        difs.append({"t": "Clientes que voltam e indicam",
                     "porque": "prova social é o único marketing que ninguém desconta",
                     "evidencia": prova[0]["evidencia"]})
    return difs[:4]


class Posicionador:
    nome = "Posicionador"
    papel = "define o território da marca: posicionamento, promessa, voz e nomes"

    def posicionar(self, mapa, mkt, ao_avisar=None):
        nome_p = mapa.get("persona_nome") or "Você"
        publico = mkt.get("publico") or "seu público-alvo"
        area = mkt.get("area") or "sua especialidade"
        categoria = "especialista em %s" % area
        difs = _diferencadores(mapa)
        topo = difs[0]["t"] if difs else "método testado em quem vive isso"
        alt = "post solto sem método" if any(c["canal"] == "Instagram" for c in mkt.get("canais", [])) else "generalista que vende para todo mundo"
        sentenca = ("Para %s que já convive com %s, %s é %s com %s. "
                    "Diferente de %s.") % (publico, area, nome_p, categoria, topo, alt)
        promessa = "Em 30 dias, o resultado que você vende — sem prometer milagre, só método e acompanhamento."
        nomes = [
            {"nome": "%s %s" % (nome_p, (categoria.split()[0].capitalize())),
             "porque": "nome + território: reconhecimento pessoal em uma palavra"},
            {"nome": "%s com %s" % (categoria.split()[0].capitalize(), nome_p),
             "porque": "categoria primeiro: quem precisa encontra o que procura"},
            {"nome": "Método %s" % nome_p.lower(),
             "porque": "nomeia o processo: quem compra leva um método, não uma aula"},
            {"nome": "%s Sem Culpa" % (categoria.split()[0].capitalize()),
             "porque": "contraste com a objeção emocional nº 1 do seu público"},
            {"nome": "Clínica de %s" % categoria,
             "porque": "soa lugar: compromisso, rotina, continuidade"},
        ]
        pos = {
            "sentenca": sentenca,
            "promessa": promessa,
            "categoria": categoria,
            "diferencadores": difs,
            "vozes": {
                "faz": ["fala como quem faz, não como quem explica",
                        "usa números e casos próprios (com permissão)",
                        "admite o que ainda não sabe — e mostra como aprende"],
                "nao_faz": ["não usa jargão de guru (‘jornada alquímica’, ‘mentorship vip’)",
                            "não promete cura mágica nem resultado garantido por e-mail",
                            "não compete por preço: compete por método e tempo de estrada"],
            },
            "nomes": nomes,
            "territorio": {
                "e": ["o prático do dia a dia do seu público",
                      "a prova de campo: casos, números, bastidores"],
                "nao_e": ["academia teórica sem contato com o problema",
                          "moda do mês: formato novo por moda, não por fit",
                          "produtinho para todo mundo (isso é o que a promessa corta)"],
            },
        }
        txt = llm.chamar("Você é consultor de marca. Em 2 frases: o maior risco de "
                         "posicionamento deste caso e o ajuste fino recomendado.",
                         _fatos_pessoa(mapa), max_caracteres=300)
        if txt:
            pos["ajuste_ia"] = txt
        return pos
