---
tipo: referencia
status: ativo
origem: SEARCH-0010 (Pesquisador, item 4), curado pelo Bibliotecario
pesquisa: SEARCH-0010
tarefa: T-0018
autor: Projeto containers (Podman)
url: https://github.com/containers/image_build/blob/main/podman/README.md
acessado_em: 2026-10-05
confianca: media
fontes: ["https://github.com/containers/image_build/blob/main/podman/README.md", "https://github.com/containers/podman/issues/4131"]
verificado_em: 2026-10-05
valido_para: "imagem quay.io/podman/stable, 2026-10"
revisar_em: 2027-01-05
criado: 2026-10-05
decisao: promovido
tags: [podman, rootless, docker, container, aninhado]
---
# Podman rootless dentro de container Docker - a doc oficial do Podman usa privileged e fuse, sem privileged nao esta documentado

## Resumo

- O README oficial da imagem `quay.io/podman/stable` mostra o uso aninhado com `--device /dev/fuse:rw`, `--security-opt label=disable`, `--security-opt seccomp=unconfined`, `--privileged` e um volume para `/var/lib/containers`. Se faltar o modulo `fuse`, `modprobe fuse` no host.
- Rootless exige uma faixa de UIDs em `/etc/subuid` e `/etc/subgid` do usuario (a imagem oficial ja traz o usuario `podman` configurado).
- **Sem `--privileged` nao ha receita oficial.** Fontes de terceiros (issue #4131 do Podman) relatam que o seccomp padrao do Docker bloqueia `mount`. Seria preciso `seccomp=unconfined` ou perfil proprio, `/dev/fuse` e `newuidmap`/`newgidmap` com setuid (capacidades SETUID/SETGID), o que quebra `cap_drop: ALL`.
- `podman compose` com `docker-compose` como provedor: **nao verificado**.

## O que aproveitar

Tratar Podman aninhado como **nao viavel sem abrir o seccomp**, a menos que um teste mostre o contrario. A decisao de aceitar esse custo fica com a Seguranca (T-0019). Serve de linha na matriz de opcoes de Docker/Podman dos projetos dentro do container do ambiente.

## Ressalvas

- Nada testado; README oficial e uma issue lidos. A conclusao "nao viavel sem abrir seccomp" e leitura de relato de terceiros.
- Imagem e README podem mudar; a nota vale para 2026-10.
- Links confiaveis: [README da imagem podman/stable](https://github.com/containers/image_build/blob/main/podman/README.md) e [issue podman #4131](https://github.com/containers/podman/issues/4131).

## Notas derivadas

- [[Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites]]: as outras opcoes da matriz.
- [[Proxy de socket do Docker filtra por secao da API e nao e fronteira de seguranca - a doc nao cobre compose nem o corpo das requisicoes]]
- [[USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid]]: o controle que o setuid do Podman rootless quebraria.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `30_Referencias`, reescrito no template de referencia (o candidato propunha problema-solucao, mas descreve o que a doc cobre e nao cobre). Sem duplicata: a nota de Docker em container nao trata Podman.
