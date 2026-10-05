---
tipo: pedido-coordenador
id: COORD-0034
status: escalado
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0018
criado: 2026-10-05
atendido_em: 2026-10-05
adm: ADM-0028
tags: [ambiente, worktree, orca, revisor, qualidade, erro-inesperado]
---
# COORD-0034 - Revisor da T-0018 aberto no worktree errado: levar os registros de qualidade ao branch da tarefa

## Pedido

- [x] 1. **Erro inesperado.** A sessao do Revisor da T-0018 foi aberta em `/home/igor/orca/workspaces/ambiente/T-0018-requisitos-arquitetura-ambiente-01-2` (branch `T-0018-requisitos-arquitetura-ambiente-01-2`, parado em `407f095`), uma pasta do Orca, que a ADR-0026 substituiu. A entrega esta em outro worktree: `/home/igor/01_ia/worktrees/ambiente/T-0018-requisitos-arquitetura-ambiente-01` (branch `T-0018-requisitos-arquitetura-ambiente-01`, `f07d56a`). Ao gravar o BUG no `qualidade/` desse worktree, o hook negou: "Este papel so pode escrever em: qualidade, ... Prefixos relativos valem a partir da pasta em que a sessao comecou (/home/igor/orca/workspaces/ambiente/T-0018-requisitos-arquitetura-ambiente-01-2). Escrita em '/home/igor/01_ia/worktrees/ambiente/T-0018-requisitos-arquitetura-ambiente-01/qualidade/bugs/BUG-T0018-01.md' negada." Avaliar por que o lancador abriu o Revisor na pasta do Orca e se o worktree/branch `-2` deve ser removido.
- [x] 2. Levar ao branch da tarefa o commit do Revisor `docs(qualidade): VER-T0018-01 da T-0018` (feito no branch `-2`; o hash esta no cartao, secao Revisao). So arquivos novos em `qualidade/`, sem conflito esperado:
  - pasta: `/home/igor/01_ia/worktrees/ambiente/T-0018-requisitos-arquitetura-ambiente-01`
  - comando: `git cherry-pick 619037a`
- [ ] 3. -> ADM-0028. Depois do item 2, o branch `T-0018-requisitos-arquitetura-ambiente-01-2` nao tem nada que o `-01` nao tenha. Remover o worktree e o branch `-2` (com o "sim" do humano):
  - pasta: `/home/igor/Documentos/01.GITHUB/BRAIN/projetos/ambiente`
  - comandos: `git worktree remove /home/igor/orca/workspaces/ambiente/T-0018-requisitos-arquitetura-ambiente-01-2` e `git branch -D T-0018-requisitos-arquitetura-ambiente-01-2`

## Motivo

O Revisor so escreve no `qualidade/` do worktree em que a sessao comecou e nao contorna o bloqueio. O VER precisa ficar no branch que vai para a `main`. As proximas sessoes da T-0018 (Engenheiro na correcao, Seguranca, novo Revisor) precisam abrir no worktree `-01`.

---

## Atendimento

Coordenador, 2026-10-05, com aprovacao do humano:
- Item 1 (causa): o reflog mostra o branch `-2` "Created from 407f095" (a partir do branch da tarefa, nao da `main`), na pasta `~/orca/workspaces`, com o sufixo `-2` do Orca. A `ferramentas/tarefa` sempre cria a partir da `main` em `$IA_WORKTREES`: as sessoes foram abertas pelo Orca, nao por `tarefa abrir`. O lancador aceitou porque a pasta comeca com `T-0018`. Melhoria: o `papel` passa a recusar papel de worktree fora de `$IA_WORKTREES` (ADM-0028).
- Item 2: `git cherry-pick 619037a` no worktree `-01` -> `65a6254` (VER-T0018-01, BUG-T0018-01, BUG-T0018-02), sem conflito.
- Item 3: apagar worktree e branch e negado ao Coordenador -> ADM-0028.
