---
tipo: pedido-coordenador
id: COORD-0035
status: escalado
urgencia: bloqueante
pedido_por: engenheiro
tarefa: T-0018
criado: 2026-10-05
atendido_em: 2026-10-05
adm: ADM-0028
tags: [ambiente, worktree, orca, engenheiro, erro-inesperado, coord-0034]
---
# COORD-0035 - Engenheiro da correcao da T-0018 tambem aberto no worktree errado (-01-2)

## Pedido

- [x] 1. **Erro inesperado (repete o COORD-0034).** A sessao do Engenheiro para a correcao da T-0018 (`status: correcao`, BUG-T0018-01 e BUG-T0018-02) foi aberta em `/home/igor/orca/workspaces/ambiente/T-0018-requisitos-arquitetura-ambiente-01-2` (branch `T-0018-requisitos-arquitetura-ambiente-01-2`, base `407f095` + `619037a`). Esse branch **nao tem** os commits `6d9544d`, `84461d1`, `2a31226`, `3612576`, `9bf11c3` e `f07d56a` (o que o Revisor verificou): `git diff --stat HEAD T-0018-requisitos-arquitetura-ambiente-01 -- docs` mostra 6 arquivos diferentes, 114 linhas a mais e 47 a menos. Corrigir aqui seria editar a versao antiga de `requisitos.md`, `fluxos.md` e do ADR-0001 e gerar conflito com o branch da tarefa. O Engenheiro **parou sem alterar `docs/`** e nao mudou o status do cartao.
- [ ] 2. -> ADM-0028 (cherry-pick ja feito). Atender o `COORD-0034` (cherry-pick do `619037a` no `-01` e remocao do worktree/branch `-2`) e corrigir a causa: o lancador/Orca esta abrindo as sessoes da T-0018 no worktree `-2`.
- [ ] 3. Reabrir o papel Engenheiro no worktree certo (o humano digita):
  - pasta: `/home/igor/01_ia/worktrees/ambiente/T-0018-requisitos-arquitetura-ambiente-01`
  - comando: `tarefa abrir T-0018 engenheiro`

## Motivo

O Engenheiro so escreve no `docs/` do worktree em que a sessao comecou e nao contorna o bloqueio (escrever no `-01` a partir daqui seria negado pelo hook, como no COORD-0034). As correcoes pedidas no VER-T0018-01 precisam ser feitas sobre o `f07d56a`.

---

## Atendimento

Coordenador, 2026-10-05, com aprovacao do humano:
- Causa: a mesma do COORD-0034 (sessao aberta pelo Orca no worktree `-2`). O branch `-01` ja tem o VER (`65a6254`), entao a correcao pode comecar sobre ele.
- Item 2: cherry-pick feito; remocao do `-2` e trava no lancador -> ADM-0028.
- Item 3: com o humano. Comando: `$IA_RAIZ/ferramentas/tarefa.sh abrir T-0018 engenheiro` (nunca pelo Orca). Nao depende do ADM-0028.
