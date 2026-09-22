# -*- coding: utf-8 -*-
"""Inquisidor — agente 5 de 11.

Nunca responde. Mede a nuance de quem fala (jargão, hesitação, extensão),
calibra a pergunta do nível 1 ao 5 e avança a investigação por interrogatório:
toda resposta precisa mover alguma hipótese. A resposta mora no material —
ele aponta onde."""

TECNICO = ["hipótese", "hipotese", "oferta", "mercado", "lancar", "preço", "persona",
           "niche", "produto", "funil", "lead", "público", "prova social", "validação",
           "mvp", "lucro", "ticket", "conversão", "calor", "escala"]
HESITA = ["acho", "tipo assim", "mais ou menos", "não sei", "naum", "confuso", "difícil",
          "talvez", "será que", "quase que", "travado", "bloqueado", "perdido", "atraso"]

BANCO = {
    ("abertura", 1): ["Deixa eu te entender certo: se você pudesse mudar UMA coisa na sua vida profissional amanhã, o que seria?",
                      "Faz um ano que você está exatamente aqui. O que piorou e o que melhorou desde então?"],
    ("abertura", 3): ["Qual é o resultado concreto que você quer em 90 dias — em número, entrega ou dinheiro?",
                      "O que você já tentou para chegar nele, na ordem em que tentou?"],
    ("abertura", 5): ["Formule o estado desejado como métrica: o quê, quanto e até quando — e me diga, com nome e sobrenome, o que impede.",
                      "Se só existisse uma alavanca, qual teria o maior retorno nesses 90 dias — e por quê?"],
    ("exposicao", 1): ["Imagine que aparecer não custa nada e ninguém ri. O que você gravaria ainda hoje?",
                       "Tem alguém que você admira e que cresceu aparecendo pouco? O que essa pessoa fez?"],
    ("exposicao", 3): ["Qual é o medo exato por trás da câmera: o quê, quem, onde? Descreva a cena inteira.",
                       "Qual formato MENOR de aparecer você aceita fazer essa semana — voz, bastidor, aula gravada?"],
    ("exposicao", 5): ["Separe o medo da evidência: quantas vezes você já foi julgado de fato — e o que aconteceu depois?",
                       "Desenhe o plano mínimo de exposição: 3 aparências de 5 minutos nas próximas 3 semanas. Quem é a plateia de cada uma?"],
    ("tempo", 1): ["Todo mês existe uma janela livre escondida. Onde ela anda fugindo?",
                   "Se começar fosse pequeno, o que você faria hoje antes de dormir?"],
    ("tempo", 3): ["Quando foi a última vez que você começou algo seu de verdade? Quanto durou — e o que parou?",
                   "Quais 3 compromissos desta semana protegem o adiamento? Qual deles você cancela?"],
    ("tempo", 5): ["Faça o cronograma reverso do lançamento em 30 dias: o que precisa estar pronto sexta-feira que vem — e quem te impede de chegar lá?",
                   "Se o momento perfeito nunca vier, qual é o custo mensal de esperar — em dinheiro que some?"],
    ("oferta", 1): ["Esquece nome e preço por um minuto: o que a pessoa leva para casa depois de trabalhar com você?",
                    "Se fosse de graça, o que as pessoas pediriam primeiro?"],
    ("oferta", 3): ["Monte a oferta em uma frase: para quem, em quanto tempo, qual resultado, pelo quê. Onde ela trava?",
                    "Quanto seu cliente paga HOJE para resolver isso por outra pessoa? Qual o abismo até o seu preço?"],
    ("oferta", 5): ["Defina o escopo fechado: entregáveis, prazo e o que NÃO está incluso. O que fica fora?",
                    "Estruture em três camadas: essencial, completo, premium. Qual âncora faz a do meio parecer barata?"],
    ("valor", 1): ["Se você cobrasse o dobro, o que precisaria ser diferente para você acreditar no preço?",
                   "Quem você conhece que cobra bem a mesma coisa que você?"],
    ("valor", 3): ["Liste 3 provas de que você vale mais: resultado, tempo de estrada, o que falam de você. Por que elas não estão na sua cara?",
                   "O que mudaria no seu dia com 30% a mais de preço — e o que isso compraria de volta?"],
    ("valor", 5): ["Modele o custo do cliente NÃO resolver isso. Seu preço é grande diante desse número — por que você ancora no seu custo e não no valor entregue?",
                   "Refaça a oferta ancorando no valor: qual número sai da sua boca agora?"],
    ("prova", 1): ["Pense num cliente que saiu de lá melhor do que chegou. O que essa pessoa mudou na sua vida profissional?",
                   "Se você tivesse que contar esse caso a um amigo, qual história sairia da sua boca?"],
    ("prova", 3): ["Transcreva, com as palavras de quem recebeu, os elogios mais fortes que você já teve. Qual deles vira caso com nome, número e antes/depois?",
                   "Quais 3 clientes você chamaria nesta semana só para perguntar: o que mudou?"],
    ("prova", 5): ["Sistematize a prova: 3 casos com métrica (antes → depois → tempo). Qual dos três você publica na segunda?",
                   "Monte o ativo de prova social: depoimento em vídeo, texto ou e-mail — qual formato o cliente aceita gravar sem drama?"],
    ("foco", 1): ["Se só pudesse existir UM projeto vivo agora, qual seria — e por quê?",
                  "Qual dessas ideias você ama e nunca começou? O que ela pede de você?"],
    ("foco", 3): ["Ranqueie suas frentes por duas coisas: o que gera caixa em 90 dias e o que é insubstituível só seu. Onde elas não coincidem?",
                  "Qual ideia você mata hoje, sem luto, para liberar 5 horas por semana?"],
    ("foco", 5): ["Critério escrito: para cada frente responda demanda provada × capacidade única × tempo até o caixa. Qual sobra sozinha no topo?",
                  "Defina a regra: o que entra na sua semana e o que vai para a fila — e qual gatilho reabre a fila?"],
    ("produto", 1): ["Que dor específica o seu produto apaga em uma única sessão?",
                     "Quem é a pessoa que mais sofre com essa dor? Descreva um dia dela."],
    ("produto", 3): ["Estruture o esqueleto: 5 módulos de 'está travado' para 'resolve sozinho'. Qual módulo é o divisor de águas?",
                     "Qual lição-piloto de 10 minutos provaria o método — e quem a testaria de graça?"],
    ("produto", 5): ["Projete a experiência completa: primeira aula → momento de 'ah!' → prova final. Onde o aluno quase desiste — e o que segura?",
                     "Valide antes de gravar: 5 conversas com o perfil, 1 aula ao vivo, 10 matrículas de fundador. Qual das três você agenda essa semana?"],
}

TEMAS_DE_HIPOTESE = {
    "exposicao": "exposicao", "tempo": "tempo", "oferta": "oferta",
    "valor": "valor", "prova": "prova", "foco": "foco", "incompleto": "abertura",
}


def medir_nuance(texto):
    """Mede o interlocutor: nível 1–5, tom e sinais que justificam a calibração."""
    t = (texto or "").lower().strip()
    if not t:
        return {"nivel": 2, "tom": "silêncio", "sinais": []}
    sinais = [w for w in TECNICO if w.lower() in t]
    hesita = [w for w in HESITA if w.lower() in t]
    pont = min(3, len(sinais)) + (1 if len(t) > 140 else 0) - (1 if hesita else 0)
    nivel = max(1, min(5, 2 + pont))
    tom = "técnico" if sinais and not hesita else ("hesitante" if hesita else "intermediário")
    return {"nivel": nivel, "tom": tom, "sinais": (sinais + hesita)[:5]}


def tema_de(hid, quero_produto=False):
    if quero_produto and hid in ("foco", "oferta"):
        return "produto"
    return TEMAS_DE_HIPOTESE.get(hid, "abertura")


def _perguntas(tema, nivel):
    disponiveis = (1, 3, 5)
    alvo = min(disponiveis, key=lambda n: abs(n - nivel))
    return BANCO[(tema, alvo)]


class Inquisidor:
    nome = "Inquisidor"
    papel = "só pergunta: investiga o travamento por perguntas, calibra pela nuance e testa hipóteses"

    def estado_inicial(self, hid=None, quero_produto=False):
        return {"tema": tema_de(hid, quero_produto) if hid else "abertura",
                "nivel": 3, "rodada": 0, "respostas": [], "hid_foco": hid}

    def pergunta(self, estado):
        qs = _perguntas(estado["tema"], estado["nivel"])
        return qs[estado["rodada"] % len(qs)]

    def responder(self, estado, resposta, tema_seguinte=None):
        nuance = medir_nuance(resposta)
        estado["respostas"].append({"texto": resposta, "nuance": nuance})
        estado["nivel"] = nuance["nivel"]
        estado["rodada"] += 1
        if tema_seguinte:
            estado["tema"] = tema_seguinte
            estado["rodada"] = 0
        return self.pergunta(estado)

    def fechar(self, estado):
        toms = [r["nuance"]["tom"] for r in estado["respostas"]]
        dominante = max(set(toms), key=toms.count) if toms else "—"
        return {"total_rodadas": len(estado["respostas"]),
                "nivel_final": estado["nivel"],
                "tom_dominante": dominante}
