---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/pesquisador
tarefa: ambiente
pesquisa: SEARCH-0009
confianca: media
fontes: [https://docs.docker.com/reference/cli/docker/container/run/, https://docs.docker.com/engine/security/userns-remap/, https://docs.podman.io/en/v4.4/markdown/options/userns.container.html]
verificado_em: 2026-10-05
valido_para: Docker Engine 29.x; Podman 4.4 ou mais novo
criado: 2026-10-05
decisao:
tags: [ambiente, container, uid, permissoes, adm-0009]
---
# Arquivos do volume montado ficam com o dono certo rodando o container com o UID do usuario do host

## Conteudo proposto

- **Docker (daemon rootful):** rodar com `--user <uid>:<gid>` (formato `<nome|uid>[:<grupo|gid>]`), por exemplo `--user "$(id -u):$(id -g)"`; no Compose, `user:` no servico. Como o bind mount nao traduz ids, arquivos criados no container saem com esse UID no host. O UID precisa existir (ou ser aceito) na imagem e o `HOME` dele precisa ser gravavel (para `~/.claude`, usar volume ou `CLAUDE_CONFIG_DIR`).
- **Podman rootless:** `--userns=keep-id` mapeia o UID:GID do usuario que chamou o Podman para o **mesmo** numero dentro do container, entao os arquivos do bind mount aparecem com o dono certo. Opcoes de montagem relacionadas: `idmap` (mount com mapeamento) e `U` (chown recursivo da origem para o usuario do container; cuidado, altera o dono no host).
- **Docker rootless / `userns-remap`:** o root do container vira um UID alto sem privilegio no host (ex.: 231072). A propria documentacao diz que isso **complica bind mounts**: a posse dos arquivos precisa ser acertada de antemao. A pagina nao recomenda `--user $(id -u):$(id -g)` como solucao; trate-a como mecanismo de isolamento, nao de posse de arquivos. Incompativel com `--pid=host`, `--network=host` e `--privileged` sem `--userns=host`.
- Sinal de erro: arquivos do repositorio (worktrees, `.git`) com dono root no host depois de rodar o container como root; corrigir uma vez com `chown` e passar a usar o usuario sem privilegio.

## Evidencia

Documentacao oficial de `docker run`, do `userns-remap` e do Podman (`--userns`), lida em 2026-10-05. A combinacao `--user` + bind mount e comportamento padrao do kernel, mas a documentacao do Docker nao a descreve num exemplo; validar no ambiente antes de adotar.

## Links confiaveis

- [docker container run: --user](https://docs.docker.com/reference/cli/docker/container/run/): formato de `--user`.
- [Isolate containers with a user namespace](https://docs.docker.com/engine/security/userns-remap/): remapeamento de UID e o custo para bind mounts.
- [Podman --userns (keep-id, idmap, U)](https://docs.podman.io/en/v4.4/markdown/options/userns.container.html): mapeia o UID do host para o mesmo UID no container.

## Por que e reaproveitavel

Qualquer container com repositorio montado, do ambiente de agentes ao lab.

## Relacionadas no Brain

- [[Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio]]
- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]

## Decisao do Bibliotecario
