# CLAUDE.md

Briefing operacional para agentes que trabalham neste repositório (Claude Code;
vale para Codex, OpenCode, Hermes e qualquer outro que leia markdown).

## O que é

**Mind Mestre** por Genial Labs: CLI em Python puro de biblioteca padrão
(≥ 3.7, sem pip install, sem chave de API) em que 11 agentes investigam uma
vida profissional travada: lêem o material da pessoa, formam hipóteses do
travamento, testam cada uma contra evidência (`arquivo:linha`), passam pelo
tribunal (Cético × Convicto × Juiz) e entregam um plano estruturado.

## Comandos úteis

| Uso | Comando |
|---|---|
| Investigar um caso (completo) | `python3 mindmestre plano <ALVO> -o <dir>` |
| Mapa rápido (sinais/ativos/objetivo) | `python3 mindmestre mapa <ALVO> --json` |
| Conversa socrática (aceita pipe) | `printf 'resposta\n' \| python3 mindmestre conversa <ALVO> --rodadas 3` |
| Tribunal ao vivo | `python3 mindmestre debate "tema" --alvo <ALVO>` |
| Elenco + motor de IA | `python3 mindmestre status` |
| Suíte (24 testes, offline) | `python3 -m unittest discover -s testes` |

`<ALVO>` é uma pasta de notas ou um arquivo `.md/.txt/.rst`.

## Contrato de artefatos (comando plano)

O diretório `-o` recebe sempre 7 artefatos: `plano.pdf`, `plano.docx`,
`plano.md`, `mapa.json`, `plano.mmd`, `mapa.mmd`, `obsidian/` (9 notas com
wikilinks resolvidos). Sem `-o`, cai em `saida/<slug>-<timestamp>/`.
`plano.md` foi escrito para outros agentes: H2 por fase + índice JSON no fim
com prompts prontos. Evidência detalhada: `mapa.json` — toda afirmação carrega
`arquivo:linha`; sem endereço, trata como não validado.

## Invariantes (não quebrar)

- **Puro stdlib**: nenhum import de terceiros em `mind_core/` nem `agentes/`.
  A suíte roda offline e tem de continuar passando.
- **Nenhum agente abre arquivo**: só o Cartógrafo toca o texto; os dez
  restantes recebem dicts e devolvem dicts.
- **Tudo tem endereço**: afirmação sem `arquivo:linha` não entra no plano.
- **Tribunal em todo plano**: Cético objeta, Convicto defende, Juiz pontua —
  `confiança = clamp(90 − pena + ganho, 5, 99)`, pena = Σ níveis
  (crítico 8 · alto 5 · médio 2 · baixo 1), ganho = min(10, 2×defesas).
- **Offline é o caminho de default**: LLM (Ollama → OpenAI → OpenRouter) só
  acrescenta leituras independentes; nunca muda evidências nem o selo.
  `MIND_SEM_IA=1` força offline.
- **Feito = suíte verde**: nada se declara pronto sem 24/24.

## Estrutura

`mindmestre` (CLI) · `agentes/` (um arquivo por agente) · `mind_core/`
(motores: padrões, leitura pessoal, llm, pdf, docx, mermaid, obsidian,
relatórios, arte) · `exemplos/mariana-fisioterapia/` (caso demo com sinais
plantados) · `testes/`. Filosofia e detalhes de cada agente: `AGENTES.md`.
