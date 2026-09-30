---
tipo: pedido-coordenador
id: COORD-0001
status: escalado
urgencia: nao-bloqueante
pedido_por: engenheiro
tarefa: ambiente
criado: 2026-09-30
atendido_em: 2026-09-30
adm: ADM-0011
tags: [ambiente, tokens, custo, telemetria, proposta]
---
# COORD-0001 - Avaliar a medicao de tokens por tarefa e papel

## Pedido

Pedido do humano na sessao do Engenheiro (T-0006, 2026-09-30): **avaliar se e viavel** acompanhar quantos tokens cada tarefa gasta, por papel e por rodada. **Nada deve ser alterado agora**; e so para o Coordenador avaliar e, se fizer sentido, propor ao humano (provavelmente um `ADM-####`, porque mexe em hooks/ferramentas, area N4).

- [x] Avaliar a proposta abaixo e apresenta-la ao humano no panorama. -> ADM-0011

### Situacao atual

- Os logs do ambiente (`logs/sessoes/`, gravados por hooks) registram eventos e ferramentas, mas **nao** tokens.
- As transcricoes locais do Claude Code (`~/.claude/projects/<pasta do worktree>/<sessao>.jsonl`) ja tem, em cada resposta do modelo, o campo `usage` (`input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`) e o `model`. A pasta do worktree da a tarefa; o id da sessao casa com o nome do arquivo em `logs/sessoes/` e da o papel.

### Estimativa feita pelo Engenheiro (leitura das transcricoes, 2026-09-30)

Soma do `usage` por sessao, sem contar respostas repetidas. Em milhares de tokens (k) ou milhoes (M).

| Tarefa | Papel (modelo) | Saida | Entrada nova (sem cache + escrita de cache) | Leitura de cache |
|---|---|---|---|---|
| T-0003 (upload, normal) | Dev (sonnet) | 16k | 79k | 1,19M |
| T-0003 | Revisor (opus) | 35k | 174k | 3,41M |
| T-0004 (trivial) | Dev (sonnet) | 7k | 59k | 0,74M |
| T-0004 | Revisor (opus) | 11k | 48k | 0,86M |
| T-0005 (normal, `seguranca: sim`) | Dev (sonnet) | 10k | 46k | 1,17M |
| T-0005 | Revisor (opus) | 18k | 60k | 1,38M |
| T-0005 | Seguranca (opus) | 25k | 84k | 2,20M |
| T-0006 (engenharia) | Engenheiro (opus), sessao ainda aberta | 74k | 201k | 7,36M |

Totais por tarefa (saida / entrada nova / leitura de cache): T-0003 51k / 253k / 4,6M; T-0004 18k / 107k / 1,6M; T-0005 53k / 191k / 4,7M.

Faixas por papel nesta amostra: Dev 7k a 16k de saida e 0,7M a 1,2M de leitura de cache; Revisor 11k a 35k e 0,9M a 3,4M; Seguranca 25k e 2,2M; Engenheiro 74k e 7,4M.

**Previsao grosseira** para os cartoes novos (T-0007 a T-0010, normais, com Dev + Seguranca + Revisor): cerca de **50k de saida, 200k de entrada nova e 4,5M a 5M de leitura de cache por rodada**. Cada rodada de correcao a mais soma mais ou menos Dev + Revisor (cerca de 30k a 50k de saida e 2,5M de leitura de cache).

**Limites da estimativa (importantes):**
- Amostra pequena (1 a 3 sessoes por papel) e de um unico dia.
- Faltam sessoes: a rodada 2 da T-0003 e a segunda revisao da T-0005 nao aparecem como sessoes separadas (retomadas com `--continuar` na mesma transcricao ou em outra pasta; nao conferido). Transcricoes de subagentes nao foram somadas.
- Sessoes de Coordenador, Administrador, Bibliotecario e Pesquisador ficam na pasta do BRAIN e nao estao ligadas a uma tarefa.
- Nao ha valor em dinheiro: o preco por token e fato volatil e varia por modelo e por tipo (a leitura de cache e bem mais barata que a entrada nova). Se o humano quiser custo, consultar a tabela oficial de precos no dia.

### Proposta para avaliar

1. Um script em `ferramentas/` (somente leitura) que soma o `usage` das transcricoes por tarefa, papel, modelo e rodada, e grava um resumo em `logs/` (fora do Git), ou um hook `Stop`/`SessionEnd` que acrescenta o total da sessao ao log dela.
2. Campo opcional no cartao (ex.: "Consumo" no fechamento), preenchido pelo Coordenador ao concluir a tarefa, para comparar tarefas triviais e normais e medir o custo de uma rodada de correcao.
3. Depois de umas 10 tarefas, uma faixa esperada por tamanho (`trivial`/`normal`/`grande`) para a triagem e para achar sessoes fora da curva.

## Motivo

Pedido do humano. Nenhum papel mede isso hoje, e a retrospectiva da T-0006 registrou "tempo e custo de cada rodada: nao ha medida nos cartoes". O Engenheiro nao altera hooks, `ferramentas/` nem regras (area N4); por isso so propoe.

---

## Atendimento

Coordenador, 2026-09-30: avaliado como viavel (as transcricoes ja trazem `usage` e `model`; a pasta da a tarefa e o id da sessao da o papel). Apresentado ao humano no panorama; ele aprovou seguir. Como a solucao mexe em `ferramentas/`/hooks (N4), escalado ao Administrador: ADM-0011.
