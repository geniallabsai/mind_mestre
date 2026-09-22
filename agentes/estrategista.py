# -*- coding: utf-8 -*-
"""Estrategista — agente 3 de 11.

Monta tudo o que a equipe investigou num plano de voo: 6 fases (conceito
complexo entra, executável sai), módulos do curso quando a pessoa declarou
querer produto, voo de 30/60/90 e três coisas para fazer hoje. O selo do
juiz acompanha a capa."""
import re

SLUGS_FASES = [
 ("diagnostico", "Onde você está travado (e o que sustenta o muro)"),
 ("mapa-da-casa", "O que você já tem pago: experiência, prova, plateia"),
 ("posicionamento-e-oferta", "Onde você se coloca — e o que você vende"),
 ("pessoas-e-mercado", "Quem você atende: nicho, persona e mapa da empatia"),
 ("maquina-de-conteudo", "Ser visto sem virar guru: conteúdo que trabalha"),
 ("voo", "Plano de voo 30/60/90 dias"),
]

MODULOS_BASE = [
 ("Fundamentos: por que {area} quebra",
  ["Como o problema nasce (o mecanismo)", "O que você já tentou e por que falhou",
   "O método em uma visão", "Mitos vs realidade"]),
 ("O protocolo de 30 dias",
  ["Semana 1: diagnóstico e linha de base", "Semana 2: correção base",
   "Semana 3: manutenção e rotina", "Checkpoints: o que está funcionando"]),
 ("Ferramentas e ambiente",
  ["O kit mínimo (o que custa de verdade)", "Erros de setup",
   "Rotina de 10 minutos por dia", "Quando usar cada ferramenta"]),
 ("Os 5 erros que sabotam",
  ["Erro 1: coerção", "Erro 2: pressa", "Erro 3: ir sozinho",
   "Erro 4: medir errado", "Erro 5: desistir antes do efeito"]),
 ("Casos reais: do travado ao resolvido",
  ["Caso A: antes/depois com números", "Caso B: o que quase deu errado",
   "Caso C: versão acelerada", "O que extrair de cada caso"]),
 ("Do aluno ao cliente",
  ["Como documentar seus resultados", "De onde vem o próximo cliente",
   "Preço com confiança", "O próximo produto (escada de valor)"]),
]

RESULTADOS = [
 "explicar o problema para o próprio paciente em 2 minutos",
 "executar o protocolo supervisionado e registrar os indicadores",
 "montar a rotina diária sem depender de você",
 "autocorrigir os erros mais comuns",
 "contar o caso como argumento de venda",
 "transformar resultado em indicação (e em poder de preço)",
]


class Estrategista:
    nome = "Estrategista"
    papel = "monta o plano estruturado: 6 fases, módulos do curso, voo 30/60/90, passos de hoje"

    def estruturar(self, ctx, ao_avisar=None):
        mapa, det = ctx["mapa"], ctx["det"]
        mkt, pos, oferta, ct = ctx["mkt"], ctx["pos"], ctx["oferta"], ctx["ct"]
        juizo = ctx["juizo"]
        nome_p = mapa.get("persona_nome") or mapa.get("nome")
        area = (mkt.get("nisca", "") or "").split(" para ")[0].strip().lower() or "o problema"
        voo = [
            {"janela": "30 dias", "foco": "Validar (antes de investir)",
             "acoes": ["Conversar com 5 pessoas do perfil (pergunte as 2 perguntas abertas do detetive)",
                        "Gravar a lição-piloto de 10 minutos (módulo 1)",
                        "Landing page simples com a garantia de reversão de risco",
                        "Vender para 10 fundadoras a preço simbólico",
                        "Publicar o pilar 'Prova' uma vez por semana"]},
            {"janela": "60 dias", "foco": "Lançar a turma 1",
             "acoes": ["Máquina de conteúdo rodando (calendário de 30 dias)",
                        "2 lives por semana respondendo dúvidas reais",
                        "Fechar 20 vagas (urgência: turma de fundadora)",
                        "Coletar 5 depoimentos com métrica antes/depois",
                        "Subir o preço conforme a prova acumulada"]},
            {"janela": "90 dias", "foco": "Escalar ou corrigir",
             "acoes": ["Criar o tripwire (mini protocolo, preço baixo)",
                        "Programa de indicação (quem traz, ganha sessão)",
                        "Abrir a turma 2 com preço cheio",
                        "Decisão: escalar / corrigir / matar (critério: conclusão ≥ 70%)"]},
        ]
        passos = [
            "Gravar um vídeo de 90 segundos se apresentando (o muro é exposição — comece pequeno)",
            "Listar 3 clientes como caso com métrica (peça permissão)",
            "Agendar as 2 conversas de validação desta semana",
        ]
        prompts = [
            "Leia o plano.md completo (e o mapa.json quando precisar de evidência). Explique a fase 1 em 5 bullets e me faça as perguntas abertas antes de eu avançar.",
            "Usando o mapa.json, gere um quiz de 10 perguntas sobre as fases 2–5, com gabarito comentado apontando arquivo:linha.",
            "Compare este plano com o meu estado daqui a 30 dias: o que mudou, o que ficou pendente e o que o Juiz diria?",
        ]
        fases = [self._f1(det, juizo), self._f2(mapa), self._f3(pos, oferta, mapa),
                 self._f4(mkt), self._f5(ct), self._f6(voo, passos)]
        for i, (slug, titulo) in enumerate(SLUGS_FASES):
            fases[i]["n"] = i + 1
            fases[i]["slug"] = slug
            fases[i]["titulo"] = titulo
        curso = self._curso(mapa, area) if mapa.get("quero_produto") else {"ativo": False, "titulo": None, "modulos": []}
        return {
            "titulo": "Plano Mind · %s" % (nome_p or "você"),
            "meta": "De 'travado' a 'em lançamento' em 90 dias: diagnóstico validado, oferta definida, marca posicionada, máquina de conteúdo rodando.",
            "selo_juiz": {"confianca": juizo["confianca"], "decisao": juizo["decisao"], "barra": juizo["barra"],
                          "resumo": juizo["resumo"], "pena": juizo["pontuacao"]["pena"], "ganho": juizo["pontuacao"]["ganho"]},
            "tribunal": {"objecoes": juizo["objecoes"], "defesas": juizo["defesas"]},
            "diagnostico": det,
            "mkt": mkt, "pos": pos, "oferta": oferta, "conteudo": ct,
            "fases": fases, "curso": curso,
            "voo_30_60_90": voo, "passos_hoje": passos, "prompts": prompts,
        }

    def _f1(self, det, juizo):
        blocos = [{"tipo": "p", "texto": det.get("resumo", "")}]
        itens = ["%s — confiança %d (%d evidências)" % (h["titulo"], h["confianca"], h["suporte"])
                 for h in det.get("hipoteses", [])[:6]]
        blocos.append({"tipo": "lista", "itens": itens})
        evs = (det.get("hipoteses") or [{}])[0].get("evidencias", [])
        if evs:
            e = evs[0]
            blocos.append({"tipo": "citacao", "texto": e.get("trecho", ""),
                           "evidencia": "%s:%s" % (e.get("arquivo"), e.get("linha") or "?")})
        blocos.append({"tipo": "nota", "texto": "Selo do Juiz: %s (%s)" % (juizo["decisao"], juizo["resumo"])})
        return {"objetivo": "Saber exatamente onde está o muro — e o que o sustenta, com endereço da prova.", "blocos": blocos}

    def _f2(self, mapa):
        blocos = [{"tipo": "p", "texto": "Antes de inventar nada, inventário do que já está pago: anos de campo, provas, demanda, plateia. Esse ativo encurta a decolagem."}]
        itens = ["%s — (%s)" % (re.sub(r"\s+", " ", a.get("trecho", ""))[:70], a["evidencia"])
                 for a in mapa.get("ativos", [])[:8]]
        blocos.append({"tipo": "lista", "itens": itens})
        dem = [a for a in mapa.get("ativos", []) if a["tipo"] == "demanda"]
        if dem:
            blocos.append({"tipo": "citacao", "texto": dem[0]["trecho"][:120], "evidencia": dem[0]["evidencia"]})
        return {"objetivo": "Ver com clareza o que já existe, para o plano crescer em chão concreto.", "blocos": blocos}

    def _f3(self, pos, oferta, mapa):
        blocos = [
            {"tipo": "p", "texto": pos.get("sentenca", "")},
            {"tipo": "p", "texto": "Promessa: " + pos.get("promessa", "")},
            {"tipo": "lista", "itens": ["%s — %s" % (d["t"], d["porque"]) for d in pos.get("diferencadores", [])]},
        ]
        if mapa.get("quero_produto") and mapa.get("objetivo_declarado"):
            blocos.append({"tipo": "nota", "texto": "Produto declarado: %s" % mapa["objetivo_declarado"][:100]})
        hl = oferta.get("headlines", [])
        if hl:
            blocos.append({"tipo": "lista", "itens": ["Headline %d: %s *(%s)*" % (i + 1, h["texto"], h["tecnica"]) for i, h in enumerate(hl)]})
        blocos.append({"tipo": "codigo", "titulo": "Página da oferta (8 blocos)", "itens": oferta.get("pagina", [])})
        blocos.append({"tipo": "lista", "itens": ["CTA: " + oferta.get("cta", ""),
                                                  "Garantia: " + oferta.get("reversao_risco", ""),
                                                  "Urgência: " + oferta.get("urgencia", "")]})
        return {"objetivo": "Definir onde você fica e o que vende exatamente: oferta, página, CTA.", "blocos": blocos}

    def _f4(self, mkt):
        persona = mkt.get("persona", {})
        emp = mkt.get("empatia", {})
        blocos = [
            {"tipo": "p", "texto": "Nicho: %s" % mkt.get("nisca", "")},
            {"tipo": "lista", "itens": mkt.get("por_que", [])},
            {"tipo": "lista", "itens": (["Persona — %s" % persona.get("codinome", "")]
                                          + ([persona["perfil"]] if persona.get("perfil") else [])
                                          + ["Quer: " + "; ".join(persona.get("quer", [])),
                                             "Teme: " + "; ".join(persona.get("teme", []))])},
            {"tipo": "lista", "itens": ["%s: %s" % (k.replace("_", " "), v) for k, v in emp.items()]},
            {"tipo": "p", "texto": mkt.get("icp", "")},
            {"tipo": "lista", "itens": ["%s — %s" % (c["canal"], c["porque"]) for c in mkt.get("canais", [])]},
        ]
        return {"objetivo": "Saber quem você atende até na palavra que ele usa: nicho, persona, empatia, canal.", "blocos": blocos}

    def _f5(self, ct):
        blocos = [
            {"tipo": "lista", "itens": ["%s (%s): %s" % (p["nome"], p["freq"], p["porque"][:70]) for p in ct.get("pilares", [])]},
            {"tipo": "lista", "itens": ["Hook %d: %s" % (i + 1, h) for i, h in enumerate(ct.get("hooks", []))]},
            {"tipo": "lista", "itens": ["%s — %s" % (f["formato"], f["cadencia"]) for f in ct.get("formatos", [])]},
            {"tipo": "lista", "itens": ["STEPPS · %s: %s" % (s["p"], s["como"][:70]) for s in ct.get("stepps", [])]},
            {"tipo": "p", "texto": "Calendário 30 dias: " + " → ".join("S%d (%s)" % (w["semana"], w["foco"]) for w in ct.get("calendario", []))},
            {"tipo": "lista", "itens": ct.get("kpis", [])},
        ]
        return {"objetivo": "Ser visto sem queimar: conteúdo com pilar, hook, formato e cadência.", "blocos": blocos}

    def _f6(self, voo, passos):
        blocos = [{"tipo": "p", "texto": "Três janelas, um critério: evidência. Se em 30 dias não validou, não investe em 60."}]
        for j in voo:
            blocos.append({"tipo": "p", "texto": "%s — %s" % (j["janela"].upper(), j["foco"])})
            blocos.append({"tipo": "lista", "itens": j["acoes"]})
        blocos.append({"tipo": "p", "texto": "Para fazer HOJE:"})
        blocos.append({"tipo": "lista", "itens": passos})
        return {"objetivo": "Transformar o plano em calendário com critério de parada.", "blocos": blocos}

    def _curso(self, mapa, area):
        modulos = []
        for i, ((nome, aulas), resultado) in enumerate(zip(MODULOS_BASE, RESULTADOS), 1):
            modulos.append({"nome": "Módulo %d — %s" % (i, nome.format(area=area)),
                            "objetivo": "Levar o aluno do travado ao autônomo (etapa %d de %d)." % (i, len(MODULOS_BASE)),
                            "aulas": aulas, "resultado": resultado})
        obj = mapa.get("objetivo_declarado") or "seu curso"
        return {"ativo": True, "titulo": "Curso: " + re.split(r"[.;,]", obj)[0].strip()[:70], "modulos": modulos}
