---
tipo: problema-solucao
status: ativo
origem: SEARCH-0009 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0009
tarefa: ambiente
confianca: media
fontes: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/engine/security/userns-remap/", "https://docs.podman.io/en/v4.4/markdown/options/userns.container.html"]
verificado_em: 2026-10-05
valido_para: "Docker Engine 29.x; Podman 4.4 ou mais novo"
revisar_em: 2027-04-05
criado: 2026-10-05
decisao: promovido
tags: [ambiente, container, uid, permissoes, adm-0009]
---
# Arquivos do volume montado ficam com o dono certo rodando o container com o UID do usuario do host

## Sintoma

Depois de rodar o container como root, os arquivos do repositorio montado (worktrees, `.git`) aparecem no host com dono root e o usuario comum nao consegue editar nem commitar.

## Ambiente

Linux, container com o repositorio montado por bind mount. Docker Engine 29.x (daemon rootful) ou Podman 4.4+ (rootless). Documentacao oficial lida em 2026-10-05; nao testado em execucao.

## Causa raiz

O bind mount nao traduz ids: o UID que o processo tem dentro do container e o UID gravado no arquivo no host. Processo root no container = arquivos de root no host.

## Solucao

- **Docker (daemon rootful):** rodar com `--user <uid>:<gid>` (formato `<nome|uid>[:<grupo|gid>]`), por exemplo `--user "$(id -u):$(id -g)"`; no Compose, `user:` no servico. O UID precisa existir (ou ser aceito) na imagem e o `HOME` dele precisa ser gravavel (para `~/.claude`, usar volume ou `CLAUDE_CONFIG_DIR`).
- **Podman rootless:** `--userns=keep-id` mapeia o UID:GID de quem chamou o Podman para o **mesmo** numero dentro do container. Opcoes de montagem relacionadas: `idmap` (mount com mapeamento) e `U` (chown recursivo da origem para o usuario do container; cuidado, altera o dono no host).
- Volume que ja ficou com dono root: corrigir uma vez com `chown` e passar a usar o usuario sem privilegio (ver [[Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio]]).

## Como verificar que foi resolvido

Criar um arquivo de dentro do container e conferir no host com `ls -l`: o dono deve ser o usuario do host, nao root.

## O que nao funcionou

- **Docker rootless / `userns-remap`:** o root do container vira um UID alto sem privilegio no host (ex.: 231072). A documentacao diz que isso **complica bind mounts** (a posse precisa ser acertada de antemao) e nao recomenda `--user $(id -u):$(id -g)` como solucao. Trate-o como isolamento, nao como mecanismo de posse. Incompativel com `--pid=host`, `--network=host` e `--privileged` sem `--userns=host`.

## Origem

SEARCH-0009 (ADM-0009, rodar o ambiente em container). A combinacao `--user` + bind mount e comportamento padrao do kernel, mas a documentacao do Docker nao a mostra num exemplo: validar no ambiente antes de adotar.

## Links confiaveis

- [docker container run: --user](https://docs.docker.com/reference/cli/docker/container/run/): formato de `--user`.
- [Isolate containers with a user namespace](https://docs.docker.com/engine/security/userns-remap/): remapeamento de UID e o custo para bind mounts.
- [Podman --userns (keep-id, idmap, U)](https://docs.podman.io/en/v4.4/markdown/options/userns.container.html): mapeia o UID do host para o mesmo UID no container.

## Relacionadas

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]: o lado de seguranca (por que nao rodar como root).
- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]: o usuario sem privilegio precisa de `HOME` gravavel para o `~/.claude`.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento` como problema-solucao (2026-10-05). Sem duplicata no Brain: as notas de CWE-250 e do volume antigo tratam a aplicacao do lab, nao o ambiente dos agentes, e foram ligadas. Confianca media mantida (so documentacao, nada executado).
