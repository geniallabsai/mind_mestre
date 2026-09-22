# MIND MESTRE

```
███╗   ███╗  ███╗  ███╗   ███╗  ██████╗    ███╗   ███╗  ███████╗  ███████╗  ████████╗  ██████╗   ███████╗
█████ ████║  ████╗  ████╗ ████║  ██╔══██╗   █████ ████║  ██╔════╝  ██╔════╝  ╚██████╔╝  ██╔══██╗  ██╔════╝
██╔═██████║  ██╔██║  ██╔████╔██║  ███████║   ██╔═██████║  █████╗    █████╗     ╚████╔╝   ██████╔╝  █████╗  
██║ ██╔ ██║  ██║╚██║  ██║╚██╔╝██║  ██╔══██║   ██║ ██╔ ██║  ██╔══╝    ╚════╝      ╚██╔╝    ╚██████╔╝  ██╔══╝  
██║  ╚═╝ ██║  ██║ ╚██║  ██║ ╚═╝ ██║  ██║  ██║   ██║  ╚═╝ ██║  ███████╗  ███████╗     ╚═╝      ╚██╔═██╗  ███████╗
╚═╝      ╚═╝  ╚═╝  ╚═╝  ╚═╝     ╚═╝  ╚═╝  ╚═╝   ╚═╝      ╚═╝  ╚══════╝  ╚══════╝     ╚═╝       ╚═╝ ╚═╝  ╚══════╝
```

**A equipe que destrava vidas profissionais travadas.** Onze agentes leem todo o
material de uma pessoa, perguntam como socráticos, formam hipóteses do
travamento, testam cada uma contra evidência (`arquivo:linha`), passam pelo
tribunal (Cético × Convicto × Juiz) e entregam o plano estruturado:
diagnóstico validado, tesouro oculto, posicionamento e marca, oferta
irresistível, máquina de conteúdo viral e voo 30/60/90.

Por **Genial Labs** · 100% Python de biblioteca padrão · roda offline (IA opcional)

## Instalação

### Linux / macOS
```bash
curl -fsSL https://raw.githubusercontent.com/geniallabsai/mind_mestre/main/install.sh | bash
```

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/geniallabsai/mind_mestre/main/install.ps1 | iex
```

### Manual
```bash
git clone https://github.com/geniallabsai/mind_mestre.git && cd mind_mestre
bash install.sh        # ou: python3 mindmestre instale
```

## Primeira investigação (60 segundos)

```bash
python3 mindmestre plano exemplos/mariana-fisioterapia -o saida/demo
```

Mariana é fisioterapeuta com 8 anos de estrada, audiência de 1,2 mil seguidores
e um curso que ela adia há dois anos. O caso vem com sinais plantados (como o
da calculadora no Instalador). A equipe devolve, em `saida/<slug>-<timestamp>/`:

| Arquivo | Para quem |
|---|---|
| `plano.pdf` | humanos — capa com o selo do Juiz, 6 fases, oferta, voo 30/60/90 |
| `plano.docx` | humanos — o mesmo conteúdo, editável |
| `plano.md` | **outros agentes** — H2 por fase + índice JSON no fim |
| `mapa.json` | qualquer agente — sinais, ativos, números, objetivo; tudo com evidência |
| `plano.mmd` | mermaid do plano (fases encadeadas + selo do Juiz) |
| `mapa.mmd` | mermaid da pessoa (muros × ativos × objetivo) |
| `obsidian/` | vault de 9 notas: MOC, 6 fases, veredito, mapa estrutural |

## Comandos

| Comando | O que faz |
|---|---|
| `mindmestre` (sem argumento) | banner + menu |
| `mindmestre mapa ALVO [--json]` | só o Cartógrafo: lê o material e para no mapa (`mapa.json` + `mapa.mmd`) |
| `mindmestre plano ALVO [-o DIR] [--sem-ia]` | investigação completa dos 11 agentes → 7 artefatos, sempre |
| `mindmestre conversa [ALVO] [--rodadas N] [--mapa F]` | interrogatório socrático ao vivo, calibrado pela sua nuance (aceita pipe) |
| `mindmestre debate TEMA... [--alvo ALVO]` | Cético × Convicto × Juiz ao vivo, sobre um tema livre ou um caso |
| `mindmestre status` | elenco completo + qual motor de IA foi detectado |
| `mindmestre instale` / `desinstale` | copia o pacote para `~/.genial-mind-mestre` + wrapper (e remove) |
| `mindmestre arte` / `versao` | banner em letras bloco / versão |

`ALVO` pode ser um arquivo (`.txt`, `.md`, `.rst`) ou uma pasta de notas.

## Os 11 agentes (um arquivo por agente)

| # | Agente | Arquivo | Função |
|---|---|---|---|
| 1 | Cartógrafo | `agentes/cartografo.py` | lê TODO o material: sinais, ativos, objetivo declarado, números |
| 2 | Detetive | `agentes/detetive.py` | hipóteses do travamento, testadas contra evidência, ranqueadas |
| 3 | Estrategista | `agentes/estrategista.py` | monta o plano: 6 fases, módulos do curso, voo 30/60/90, passos de hoje |
| 4 | Conteudista | `agentes/conteudo.py` | 4 pilares, 10 hooks, formatos, STEPPS, calendário de 30 dias, KPIs |
| 5 | Inquisidor | `agentes/inquisidor.py` | só pergunta; mede nuance (níveis 1–5); cada resposta move uma hipótese |
| 6 | Gênio do Marketing | `agentes/marketing.py` | nicho ideal, persona, mapa da empatia (8 células), canais, ICP |
| 7 | Posicionador | `agentes/posicionamento.py` | sentença de posicionamento, promessa, voz, 5 nomes, território |
| 8 | Copista | `agentes/copista.py` | oferta irresistível treinada num corpus real (1926 → 2018) |
| 9 | Cético | `agentes/cetico.py` | objeta tudo que não tem evidência — com nível e `arquivo:linha` |
| 10 | Convicto | `agentes/convicto.py` | defende o diagnóstico com o melhor da evidência |
| 11 | Juiz | `agentes/juiz.py` | pontuação aberta → selo de confiança na capa de tudo |

Nenhum agente grava disco: todos recebem dicts e devolvem dicts. O único que
toca o texto é o Cartógrafo; os outros dez discutem o mapa dele. Isso é o que
torna o sistema auditável — toda afirmação carrega `arquivo:linha`.

## O tribunal

Nada sai sem passar por **Cético × Convicto × Juiz**:

- **Cético** objeta: hipótese fraca (1 evidência só), sinal isolado num único
  arquivo, objetivo declarado sem preço, plano sem data. Cada objeção tem
  nível (`crítico/alto/médio/baixo`) e endereço.
- **Convicto** defende: padrão em mais de um arquivo, ativo quantificado,
  demanda pedindo à porta, anos de estrada. Também com endereço.
- **Juiz** pontua na mesa: `pena = Σ níveis das objeções` (crítico 8 · alto 5 ·
  médio 2 · baixo 1), `ganho = min(10, 2 × defesas)`,
  `confiança = clamp(90 − pena + ganho, 5, 99)`.

≥80 **Diagnóstico sólido — pode decolar** · ≥55 **Sólido com ressalvas** ·
<55 **Nevoeiro — converse antes de voar**. O selo (barra de 20 colunas +
veredito) aparece na capa do PDF, no `plano.md`, no vault e no `plano.mmd`.

## A nuance socralética

O Inquisidor mede o interlocutor — jargão técnico × hesitação × extensão — e
calibra a pergunta entre os níveis 1 e 5: para quem está perdido, pergunta de
porta aberta; para quem já fala em funil, pergunta de alavanca. Ele nunca
responde; cada sua resposta tem de mover alguma hipótese. Ao vivo:
`mindmestre conversa` (aceita pipe: `printf 'resposta\n' | mindmestre conversa`).

## Copywriting com dados reais

`agentes/copista.py` carrega um corpus de 14 técnicas documentadas. O agente
detecta o **estágio de sofisticação do mercado** no próprio material
(Schwartz) e monta a oferta de cima a baixo: 3 headlines aplicando as fórmulas
do estágio, promessa, benefícios ancorados em ativos com evidência, bônus,
garantia com reversão de risco, urgência ética, CTA e a página em 8 blocos.

| Ano | Autor | Técnica no corpus |
|---|---|---|
| 1926 | John Caples | Curiosidade + inversão de status |
| 1955 | David Ogilvy | Precisão impressiona mais que superlativo |
| 1958 | David Ogilvy | Misterio visual: um detalhe nao explicado gera historia |
| 1966 | Eugene Schwartz | Estágios de sofisticação do mercado (1–5) |
| 1971 | Gary Halbert | Curiosidade + medo do erro (carta que dobrou listas de espera) |
| 1972 | Gary Halbert | Intimidade manuscrita + autoridade herdada |
| 1972 | Joseph Sugarman | Primeira frase que derrapa para a segunda |
| 1905 | Claude Hopkins | Prova de processo: detalhe que concorrente nao conta |
| 1989 | Bob Blyth | 4Ps: Promise, Picture, Purity, Push |
| 2006 | Dan Kennedy | Reversão de risco + garantia agressiva |
| 2009 | Ryan Deiss | Gratis → tripwire → core → premium |
| 2013 | Jonah Berger | STEPPS: moeda social, gatilho, emocao, publico, utilidade, historias |
| 2015 | Russell Brunson | Epiphany Bridge + Value Stack |
| 2018 | Playbook de short-form (Reels/TikTok) | Pattern interrupt + número específico |

## IA (opcional)

Motor determinístico de biblioteca padrão: sem nenhuma API, o plano inteiro
nasce igual. Se houver API, a ordem é Ollama local (porta 11434) → OpenAI
(`OPENAI_API_KEY`) → OpenRouter (`OPENROUTER_API_KEY`). A IA acrescenta
leituras independentes dentro dos agentes; **o tribunal e as evidências não
mudam**. `MIND_SEM_IA=1` ou `--sem-ia` força offline.

## Testes

```bash
python3 -m unittest discover -s testes    # 24 testes, todos offline
```

## Estrutura

```
mind_mestre/
├── mindmestre                      # a CLI (executável)
├── mind_core/                      # motores: arte, leitura_pessoal, padroes, llm,
│                                   #          pdf, docx, mermaid, obsidian, relatorios
├── agentes/                        # 11 agentes, um arquivo por agente
├── exemplos/mariana-fisioterapia/  # caso de demonstração com sinais plantados
├── testes/                         # suíte offline
└── install.sh · install.ps1 · uninstall.sh · uninstall.ps1
```

## Licença

MIT — Genial Labs AI
