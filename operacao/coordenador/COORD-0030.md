---
tipo: pedido-coordenador
id: COORD-0030
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0013
criado: 2026-10-04
atendido_em:
adm: ADM-0025
tags: [t-0013, docker, volumes, limpeza, permissao]
---
# COORD-0030 - T-0013: remover volumes de teste do Revisor e erro de permissao em comando git de leitura

## Pedido

- [x] Remover os volumes de teste da revisao da T-0013 (so produtos de teste, criados pelo Revisor; projeto ja parado com `docker compose -p t0013-rev down`, sem `-v`). Pasta: qualquer uma (ex.: `/home/igor/orca/workspaces/lab/T-0013`).
  ```
  docker volume rm t0013-rev_db_data t0013-rev_uploads
  ```
  Esperado: os dois nomes impressos de volta. Pode ser feito antes ou depois do merge; junto, se quiser, com os volumes do Designer e da Seguranca ja listados em "Passos do humano" do cartao (`t0013-des_*`, `t0013-seg_*`).
- [x] -> ADM-0025 Erro de permissao (nao bloqueante), para avaliar se o perfil do Revisor deve liberar: no worktree `/home/igor/orca/workspaces/lab/T-0013`, o comando de leitura `git merge-base --is-ancestor 79ead1c main` foi **negado** ("Permission to use Bash with command ... has been denied"). Tambem foram negados comandos compostos com `;`/`&&` que misturavam `cmp`, `grep`, `ls .env` e `docker compose ... up` (separados, passaram). Eu queria confirmar que o commit de correcao do SEC-T0008-01/SEC-T0012-01 esta na `main`; contornei conferindo o estado ao vivo do container (registrado no VER-T0013-01 como lacuna).

## Motivo

- Remover volume e comando fora do perfil do Revisor (regra do projeto: volumes de teste vao para o humano/Coordenador; nunca `down -v`).
- O erro de permissao segue a regra de erro inesperado (`CLAUDE.md`, "Pedidos de comando"): registrar, nao contornar em silencio.

---

## Atendimento

Coordenador, 2026-10-04 (depois do merge da T-0013, `c9d0f4b`):
- **Volumes:** com a aprovacao do humano, `docker volume rm t0013-rev_db_data t0013-rev_uploads t0013-des_db_data t0013-des_uploads t0013-seg_db_data t0013-seg_uploads`. Os 6 nomes voltaram, sem erro. Nenhum container usava os volumes. O volume do Dev (`t-0013_db_data`, com 3 produtos de teste) nao estava no pedido e ficou.
- **Erro de permissao, causa confirmada:** em `agentes/perfis/revisor.json` a negacao `"Bash(git merge*)"` (sem espaco) tambem casa com `git merge-base`, e a negacao prevalece sobre a liberacao. O mesmo padrao esta em 7 perfis; so Coordenador e Administrador usam `git merge *`. Escalado ao ADM-0025, item 2 (troca para `git merge *` e liberacao de `git merge-base *` no Revisor e na Seguranca). O Revisor agiu certo: registrou a lacuna e conferiu o estado ao vivo.
- **Comandos compostos com `;`/`&&` negados:** comportamento esperado. Cada parte do comando composto precisa estar liberada, e `ls .env` cai na protecao do `.env`. Aviso aos papeis: rodar comandos separados, como o Revisor acabou fazendo. Sem mudanca de regra.
- Fecha quando o ADM-0025 concluir o item 2.

Coordenador, 2026-10-05, com aprovacao do humano: ADM-0025 `concluido`. Item 2: `git merge *` (com espaco) nos 7 perfis e `git merge-base *` liberado ao Revisor e a Seguranca (`c6015c0`, merge `c08f58f`); teste em 2026-10-05 com o perfil do Revisor: `git merge-base --is-ancestor` rodou. Pedido `concluido`.
