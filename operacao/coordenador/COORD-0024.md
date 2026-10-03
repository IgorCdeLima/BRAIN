---
tipo: pedido-coordenador
id: COORD-0024
status: concluido
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0015
criado: 2026-10-03
atendido_em: 2026-10-03
adm:
tags: [lab, t-0015, seguranca, correcao]
---
# COORD-0024 - Devolver a T-0015 ao Dev para corrigir SEC-T0015-01, -02 e -03

## Pedido

- [ ] Levar a T-0015 (lab, branch `T-0015-endurecer-app`) de volta ao Dev, no fluxo normal (status `correcao` ou o que o Fluxo de tarefa definir), para implementar os criterios da secao "SEC da revisao de seguranca" do cartao. A Seguranca nao muda status.
- [ ] Avisar o humano para relancar o Dev no worktree da tarefa (`ferramentas/papel.sh dev`).
- [ ] No fechamento da tarefa: `docker volume rm t0015-seg_db_data t0015-seg_uploads` (volumes de teste da Seguranca; o humano decidiu remover ao final). Sem `-v` em nenhum `down`.

## Motivo

Na revisao de seguranca do commit `79ead1c`, a Seguranca registrou tres achados de severidade baixa, commitados no branch:

- SEC-T0015-01: teto de memoria sem `memswap_limit`, que deixa o container usar swap do host.
- SEC-T0015-02: `app` sem `restart`.
- SEC-T0015-03: consulta ao banco sem `statement_timeout`.

Em 2026-10-03, o humano decidiu que os tres entram na T-0015. Os criterios de aceite ja estao no cartao, com valores e roteiro de teste. Mudar status e acionar o Dev nao e papel da Seguranca. Depois da correcao, a Seguranca revisa de novo antes do Revisor fechar.

O SEARCH-0007 (nao bloqueante) so trata o residual do SEC-T0015-03 (banco congelado) e nao segura o Dev.

---

## Atendimento

Coordenador, 2026-10-03:
- Itens 1 e 2: o Dev foi relancado e corrigiu os tres SEC no `7282de6`. A Seguranca fez a 2a rodada e o Revisor aprovou no VER-T0015-02.
- Item 3: com a aprovacao do humano, rodei `docker volume rm t0015-seg_db_data t0015-seg_uploads` junto com os volumes do COORD-0025. Os dois nomes foram impressos, sem erro.
- Merge da T-0015 na `main` do lab: `ee1ba22`.
