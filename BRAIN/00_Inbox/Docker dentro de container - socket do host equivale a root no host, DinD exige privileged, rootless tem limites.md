---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: ambiente
pesquisa: SEARCH-0009
confianca: media
fontes: [https://docs.docker.com/engine/security/, https://hub.docker.com/_/docker, https://docs.docker.com/engine/security/rootless/, https://docs.podman.io/en/latest/markdown/podman-compose.1.html]
verificado_em: 2026-10-05
valido_para: Docker Engine 29.x (docs de 2026-10); Podman docs "latest" de 2026-10
criado: 2026-10-05
decisao:
tags: [ambiente, container, docker, podman, seguranca, adm-0009]
---
# Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites

## Conteudo proposto

| Opcao | O que o container passa a poder no host | Requisitos / limites |
|---|---|---|
| (a) Montar `/var/run/docker.sock` do host | Quem fala com o socket tem poder equivalente a root no host: pode subir container montando `/` do host. Nao ha isolamento. | Nada alem do socket; Compose funciona normal (usa o mesmo daemon). Containers criados ficam **irmaos** do container do ambiente; caminhos de bind mount sao os do **host**, nao os do container. |
| (b) Docker-in-Docker (imagem `docker:dind`) | O container e `--privileged`: acesso quase total ao host (a propria documentacao da imagem avisa). Daemon proprio e isolado do daemon do host. | `--privileged` obrigatorio, tambem na variante `-rootless` (experimental). TLS automatico via `DOCKER_TLS_CERTDIR=/certs`. Imagens e volumes ficam dentro do dind (somem com ele, salvo volume proprio). |
| (c) Docker rootless ou Podman | O daemon roda como usuario comum: root do container nao e root do host; o dano de uma fuga fica limitado ao usuario. | Docker rootless: `newuidmap`/`newgidmap` (pacote `uidmap`), `/etc/subuid` e `/etc/subgid` com 65.536 ids ou mais, namespaces de usuario habilitados; portas <1024 bloqueadas por padrao; IP do container nao e alcancavel do host; `-p` nao propaga IP de origem; so `overlay2` (kernel 5.11+), `fuse-overlayfs`, `btrfs` ou `vfs`; `--cpus/--memory/--pids-limit` so com cgroup v2 + systemd. Podman: `podman compose` e apenas um wrapper que chama `docker-compose` ou `podman-compose` contra o socket do Podman; nao tem logica propria, entao a compatibilidade com Compose depende do provedor. |

Resumo: (a) e a mais simples e a mais perigosa; (b) isola o daemon mas custa um container privilegiado; (c) e a que mais reduz o que um agente comprometido alcanca, ao custo de configuracao e das limitacoes de rede.

## Evidencia

Documentacao oficial do Docker (superficie de ataque do daemon, modo rootless, imagem `docker` no Docker Hub) e do Podman (`podman compose`), lida em 2026-10-05. Os limites exatos de Compose em rootless nao constam numa lista unica da documentacao; validar com o `docker-compose.yml` do lab antes de decidir.

## Links confiaveis

- [Docker Engine security: daemon attack surface](https://docs.docker.com/engine/security/#docker-daemon-attack-surface): por que acesso ao daemon/socket equivale a root.
- [Docker rootless mode](https://docs.docker.com/engine/security/rootless/): requisitos Linux e instalacao; veja tambem a pagina de [troubleshooting](https://docs.docker.com/engine/security/rootless/troubleshoot/) com as limitacoes.
- [Imagem oficial docker (dind)](https://hub.docker.com/_/docker): `--privileged`, TLS e variante rootless.

## Por que e reaproveitavel

Sempre que um agente ou CI dentro de container precisar subir os containers de um projeto.

## Relacionadas no Brain

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]

## Decisao do Bibliotecario
