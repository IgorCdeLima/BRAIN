---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0010
confianca: media
fontes: [https://github.com/containers/image_build/blob/main/podman/README.md, https://github.com/containers/podman/issues/4131]
verificado_em: 2026-10-05
valido_para: imagem quay.io/podman/stable, 2026-10
criado: 2026-10-05
decisao:
tags: [podman, rootless, docker, container, aninhado]
---
# Podman rootless dentro de container Docker - a doc oficial do Podman usa privileged e fuse, sem privileged nao esta documentado

## Conteudo proposto

- O README oficial da imagem `quay.io/podman/stable` (projeto containers) mostra o uso aninhado com `--device /dev/fuse:rw`, `--security-opt label=disable`, `--security-opt seccomp=unconfined`, `--privileged` e volume para `/var/lib/containers`. Se faltar o modulo `fuse`, `modprobe fuse` no host.
- Rootless exige faixa de UIDs em `/etc/subuid` e `/etc/subgid` do usuario (a imagem oficial ja traz o usuario `podman` configurado).
- **Sem `--privileged`:** nao ha receita oficial. Fontes de terceiros relatam que o seccomp padrao do Docker bloqueia `mount` (issue #4131 do Podman), logo seria preciso `seccomp=unconfined` ou perfil proprio, `/dev/fuse` e `newuidmap/newgidmap` com setuid (cap SETUID/SETGID), o que quebra `cap_drop: ALL`. Tratar como **nao viavel sem abrir seccomp**; a decisao fica com a Seguranca (T-0019).
- `podman compose` com `docker-compose` como provedor: **nao verificado** nesta pesquisa.

## Evidencia

README oficial lido; issue do projeto citada. Nada testado.

## Links confiaveis

- [README da imagem podman/stable](https://github.com/containers/image_build/blob/main/podman/README.md): flags do Podman aninhado.
- [Issue podman #4131](https://github.com/containers/podman/issues/4131): seccomp do Docker e mount.

## Por que e reaproveitavel

Matriz de opcoes de Docker/Podman dos projetos dentro do container do ambiente.

## Relacionadas no Brain

- [[Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites]]

## Decisao do Bibliotecario
