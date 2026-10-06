---
tipo: padrao
status: ativo
origem: agente/engenheiro (T-0018, ADM-0009), curado pelo Bibliotecario
tarefa: T-0018
confianca: media
fontes: ["https://git-scm.com/docs/git-worktree", "git help worktree (git 2.53.0, manual local do host)", "arquivo .git de um worktree real (T-0018)"]
verificado_em: 2026-10-05
valido_para: "git 2.53; worktrees criados sem --relative-paths"
criado: 2026-10-05
decisao: promovido
revisar_em: 2027-04-05
tags: [git, worktree, container, docker, volume, armadilha]
---
# Worktrees do git guardam caminho absoluto - no container monte no mesmo caminho do host

## Contexto

Um container (ou devcontainer, VM, CI) precisa usar repositorios cujos worktrees foram criados no host, ou o contrario.

## Problema

O arquivo `.git` de um worktree contem `gitdir: /caminho/absoluto/do/repo/.git/worktrees/<nome>`, e o repositorio principal guarda o caminho de volta em `.git/worktrees/<nome>/gitdir`. Montado em outro caminho, o git do container nao acha o repositorio. Pior: um `git worktree prune` (tambem disparado por `git gc`) do lado que nao enxerga o caminho marca os worktrees como `prunable` ("gitdir file points to non-existent location") e pode apagar os registros administrativos dos worktrees do outro lado.

## Solucao

Monte o repositorio principal e a pasta dos worktrees **no mesmo caminho absoluto** dentro e fora (bind mount `X:X`). De ao usuario do container o mesmo `HOME` do host se algum caminho padrao depender dele.

Ganho extra no 01_IA: com caminhos espelhados, as transcricoes do Claude Code (pasta derivada do caminho) e os bind mounts relativos de um Compose rodado pelo socket do host resolvem para os mesmos lugares.

## Trade-offs

- **Ganha:** nenhuma configuracao de git; funciona com worktrees ja existentes; sem risco de prune cruzado.
- **Perde:** o container fica acoplado ao caminho do host (a imagem nao e portatil entre maquinas com caminhos diferentes).

**Alternativa:** `git worktree add --relative-paths` ou `worktree.useRelativePaths=true` gravam caminhos relativos. Custo: ligam a extensao `relativeWorktrees` (gits antigos nao leem o repositorio) e nao valem para worktrees ja criados (precisa `git worktree repair`).

## Quando NAO usar

Quando todos os clientes do repositorio tem git recente e o repositorio nasce com `--relative-paths`; ai o espelhamento de caminho nao e necessario.

## Evidencia

- Manual do git 2.53.0 (2026-10-05): "--relative-paths, --no-relative-paths: Link worktrees using relative paths or absolute paths (default)"; secao sobre mover worktree e `git worktree repair`; "prunable: gitdir file points to non-existent location".
- `.git` do worktree da T-0018: `gitdir: <raiz>/projetos/ambiente/.git/worktrees/T-0018-requisitos-arquitetura-ambiente-01` (caminho absoluto).
- **Nao testado:** o prune efetivo dentro de um container com caminho diferente; comportamento inferido do manual.

Link confiavel: [git-worktree (manual oficial)](https://git-scm.com/docs/git-worktree): `--relative-paths`, `repair`, `prune` e o formato dos arquivos de ligacao.

## Relacionadas

- [[ADR-0026 Ferramenta tarefa substitui o Orca nos worktrees e terminais]]: a ferramenta que cria os worktrees.
- [[Arquivos do volume montado ficam com o dono certo rodando o container com o UID do usuario do host]]: outro cuidado de volume montado do host.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento` como padrao. Sem duplicata. Confianca media: manual e arquivo real, sem teste de prune em container.
