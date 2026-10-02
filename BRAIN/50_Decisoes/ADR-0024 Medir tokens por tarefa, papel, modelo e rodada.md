---
tipo: decisao
status: aceita
decidido_em: 2026-10-02
decidido_por: humano
substituida_por:
criado: 2026-10-02
tags: [tokens, consumo, telemetria, hooks, coordenador, ambiente]
---
# ADR-0024 Medir tokens por tarefa, papel, modelo e rodada

## Contexto

- Nenhum papel media consumo; a retrospectiva da T-0006 registrou que nao havia medida de custo por rodada ([[ADM-0011]], escalado do COORD-0001).
- As transcricoes do Claude Code trazem o `usage` de cada resposta (entrada, cache criado, cache lido, saida), o modelo, o papel e o branch (tarefa). Sondagem de 2026-10-02: 6630 linhas com `usage`, das quais 3902 sao a mesma resposta repetida (uma linha por bloco de conteudo, `usage` identico); somar tudo dobraria o total.
- O cache lido domina (T-0010: ~23,9 M lidos, ~1 M criados, ~0,24 M de saida).
- As transcricoes sao apagadas depois de um prazo; o leitor ja existe para o [[ADR-0023 Medir o uso do Brain por acesso, citacao e utilidade declarada]].

## Decisao

1. **Leitor comum** `ferramentas/transcricoes.py`: uma resposta conta uma vez (`message.id`), so sessoes do 01_IA (copia principal ou worktree `T-####`), nunca texto de mensagem. Usado tambem pelo `uso_brain.py`.
2. **Hook `Stop`** `ferramentas/hooks/registrar_consumo.py`, na definicao de cada papel: a cada fim de turno soma a sessao pela transcricao e acrescenta o acumulado em `logs/consumo/AAAA-MM.jsonl` (vale a ultima linha da sessao; so numeros).
3. **Relatorio** `ferramentas/consumo.py`: por tarefa e papel, fora de tarefa por papel, e por modelo; `--tarefa T-####` gera o bloco do cartao. Rodada = uma sessao de um papel. Quatro colunas separadas. **Sem preco** (fato volatil; se preciso, SEARCH no dia).
4. **Cartao:** secao "Consumo", preenchida pelo Coordenador no fechamento (passo 7 do [[Fluxo de tarefa]]). O numero fica no Git mesmo depois que as transcricoes somem.
5. Depois de ~10 tarefas medidas, o Coordenador propoe faixas esperadas por tamanho (`trivial`/`normal`/`grande`).

## Alternativas consideradas

| Alternativa | Pros | Contras |
|---|---|---|
| So o campo no cartao, sem hook | Nada roda a cada turno | Sessao de transcricao apagada antes do fechamento fica sem medida; trabalho fora de tarefa nao fica guardado |
| Hook `SessionEnd` no `.claude` | Uma linha por sessao | Nas sessoes de worktree os hooks vem do `.claude` do projeto; teria de ser repetido em cada projeto |
| Total unico de tokens | Simples | Esconde que o cache lido e a maior parte; engana na comparacao |
| Valor em dinheiro | Facil de entender | Preco muda; exigiria pesquisa e manutencao constante |
| **Leitor comum + hook `Stop` no papel + campo no cartao (escolhida)** | Retencao, vale em todo projeto, numero no Git | Uma leitura da transcricao a cada fim de turno |

## Consequencias

- **Positivas:** custo de cada tarefa e de cada papel visivel; comparar Dev (Sonnet) e Revisor (Opus); base para faixas por tamanho de tarefa.
- **Negativas / riscos:** o hook rele a transcricao inteira a cada turno (sessao longa = alguns MB; timeout de 20 s, nunca falha); o log cresce uma linha por turno; sessao sem papel do 01_IA aparece como `sem-papel`.

## Relacionadas

- [[ADM-0011]] - pedido.
- [[ADR-0023 Medir o uso do Brain por acesso, citacao e utilidade declarada]] - mesmo leitor de transcricoes.
- [[Coordenador]], [[Rastreabilidade]].
