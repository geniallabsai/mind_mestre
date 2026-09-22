# agentes/

O time do **Mind Mestre** — um arquivo por agente, mesmo contrato do
Instalador: cada agente recebe o `mapa` do Cartógrafo e devolve estrutura
com evidência; nenhum agente decide sozinho, e o tribunal (Cético ×
Convicto × Juiz) julga antes de qualquer coisa decolar.

| # | Agente | Arquivo | Função |
|---|--------|---------|--------|
| 1 | Cartógrafo | `cartografo.py` | Lê o material da pessoa e mapeia a vida profissional: sinais, ativos, objetivo |
| 2 | Detetive | `detetive.py` | Forma as hipóteses do travamento, testa cada uma contra a evidência, ranqueia |
| 3 | Estrategista | `estrategista.py` | Monta o plano: 6 fases, módulos do curso, voo 30/60/90, passos de hoje |
| 4 | Gênio do Marketing | `marketing.py` | Nicho ideal, persona, mapa da empatia (8 células), ICP, canais |
| 5 | Inquisidor | `inquisidor.py` | Interrogatório socrático calibrado pela nuance (níveis 1–5) |
| 6 | Posicionador | `posicionamento.py` | Território da marca: frase de posicionamento, promessa, voz, nomes |
| 7 | Conteudista | `conteudo.py` | Máquina de conteúdo viral: pilares, 10 hooks, formatos, calendário 30 dias |
| 8 | Copista | `copista.py` | Oferta irresistível: CORPUS de 20+ anos de copywriters + estágio de Schwartz |
| 9 | Cético | `cetico.py` | Ataca o diagnóstico sem evidência (cada objeção com arquivo:linha) |
| 10 | Convicto | `convicto.py` | Defende a leitura com evidência (história, ativos, demanda) |
| 11 | Juiz | `juiz.py` | Pontuação aberta (PENTO 8/5/2/1) → confiança 5–99 → veredito |

## Fluxo

`Cartógrafo → Detetive → [Cético × Convicto → Juiz] → Gênio do Marketing →
Posicionador → Copista → Conteudista → Estrategista → artefatos`

## Adicionar um agente

1. Crie `agentes/meu_agente.py` com uma classe expondo `nome` e `papel`.
2. Ele recebe o `mapa` (e o que precisar dos outros agentes) e devolve dict.
3. Registre em `agentes/__init__.py`.
4. Nada de disco dentro do agente: quem escreve são os relatórios.
