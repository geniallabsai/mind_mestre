# -*- coding: utf-8 -*-
"""Conteudista — agente 7 de 11.

Máquina de conteúdo viral construída sobre STEPPS (Jonah Berger): pilares
nasco do material real da pessoa, banco de 10 hooks preenchidos, formatos
e cadência, calendário de 30 dias e KPIs. Conteúdo que vende sem
transformá-la em guru."""
import re

HOOKS = [
 "Ninguem fala sobre {area}: os 5 erros que aparecem em 90% dos casos",
 "{anos} anos tratando {area}. O que eu faria diferente comecando hoje",
 "Pare de fazer {erro_comum} com {area} (custa caro e todo mundo faz)",
 "Se {area} te trava, o problema nao e {culpa_injusta}",
 "{n} sinais de que seu {area} esta piorando (o 3o quase ninguem percebe)",
 "O que um cliente me contou ontem sobre {area} (e me fez repensar o metodo)",
 "Antes/depois real: {area} em {prazo} — o que mudou na rotina",
 "A pergunta que todo mundo tem medo de fazer sobre {area} (e a resposta honesta)",
 "3 coisas que eu pararia de facer amanha em {area} — se comeconsse de novo",
 "O que aprendi cobrando barato: a lição de preço depois de {anos} anos",
]

STEPPS = [
 ("Moeda social", "post que faz o publico parecer esperto por compartilhar: lista de sinais"),
 ("Gatilho", "amarrar o conteudo a rotina: antes do cafe, no horario do almoco"),
 ("Emocao de alta ativacao", "surpresa + indignacao contra o erro comum (evitar tristeza)"),
 ("Publico", "print de resultado, antes/depois — sempre com permisso"),
 ("Utilidade pratica", "um exercicio/protocolo que funciona sem comprar nada"),
 ("Historia", "a propria trajetoria: anos de maca para cá"),
]


class Conteudista:
    nome = "Conteudista"
    papel = "máquina de conteúdo viral: pilares, hooks, formatos, calendário de 30 dias e métricas"

    def montar(self, mapa, mkt, ao_avisar=None):
        area = re.split(r"\bpara\b", mkt.get("nisca", "") or "")[0].strip().lower() or "o problema"
        anos = None
        for n in mapa.get("numeros", []):
            if re.search(r"anos", n.get("contexto", "")):
                anos = n["valor"]
                break
        fichas = {"area": area, "anos": anos or "muitos", "n": anos or "5",
                  "prazo": "30 dias", "erro_comum": "exagero",
                  "culpa_injusta": "falta de forca de vontade"}
        hooks = []
        for h in HOOKS:
            s = h
            for k, v in fichas.items():
                s = s.replace("{" + k + "}", str(v))
            hooks.append(re.sub(r"\s+", " ", s).strip())
        esp = next((a for a in mapa.get("ativos", []) if a["tipo"] == "especialidade"), None)
        prova = next((a for a in mapa.get("ativos", []) if a["tipo"] == "prova_social"), None)
        pilares = [
            {"nome": "Educar (mostrar que sabe)",
             "porque": (esp["trecho"][:60] if esp else "a especialidade declarada no material"),
             "freq": "2x/semana"},
            {"nome": "Prova (casos e bastidores)",
             "porque": (prova["trecho"][:60] if prova else "pedir 3 depoimentos esta semana"),
             "freq": "1x/semana"},
            {"nome": "Pessoa (quem faz e por que)",
             "porque": "o muro era exposicao — aparecer gradualmente destrava a venda",
             "freq": "1x/semana"},
            {"nome": "Oferta (o que se vende)",
             "porque": "produto declarado: " + (mapa.get("objetivo_declarado") or "a definir")[:60],
             "freq": "1x/quincena"},
        ]
        formatos = [
            {"formato": "Video curto (Reels/TikTok/Shorts)", "cadencia": "3x/semana", "objetivo": "alcance: hook nos 3 primeiros segundos"},
            {"formato": "Carrossel (educacao profunda)", "cadencia": "1x/semana", "objetivo": "autoridade + salvamentos"},
            {"formato": "Stories diarios (bastidor)", "cadencia": "diario", "objetivo": "intimidade: enquete, caixinha, CTA suave"},
        ]
        if any(re.search(r"e-?mail", a.get("trecho", "")) for a in mapa.get("ativos", [])
               if a["tipo"] == "audiencia"):
            formatos.append({"formato": "Newsletter semanal", "cadencia": "1x/semana",
                             "objetivo": "relacionamento + oferta no fim do funil"})
        stepps = [{"p": p, "como": c} for p, c in STEPPS]
        calendario = [
            {"semana": 1, "foco": "Fundacao: apresentacao + pilar Educar",
             "posts": [hooks[0], hooks[3], hooks[7]]},
            {"semana": 2, "foco": "Prova social: casos + enquete nos stories",
             "posts": [hooks[1], hooks[6], hooks[5]]},
            {"semana": 3, "foco": "Mecanismo: 3 videos do metodo + live de duvidas",
             "posts": [hooks[4], hooks[2], hooks[8]]},
            {"semana": 4, "foco": "Oferta: bastidores do lancamento + CTA forte",
             "posts": [hooks[9], hooks[6], hooks[0]]},
        ]
        kpis = ["salvamentos (utilidade pratica)",
                 "compartilhamentos (moeda social)",
                 "DMs com palavra-chave (intencao de compra)",
                 "cliques no link da bio (oferta)"]
        return {"pilares": pilares, "hooks": hooks, "formatos": formatos,
                 "stepps": stepps, "calendario": calendario, "kpis": kpis}
