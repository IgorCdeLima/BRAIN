---
tipo: referencia
status: ativo
origem: SEARCH-0009 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0009
tarefa: ambiente
autor: Docker; Podman (documentacao oficial)
url: https://docs.docker.com/engine/security/
acessado_em: 2026-10-05
confianca: media
fontes: ["https://docs.docker.com/engine/security/", "https://hub.docker.com/_/docker", "https://docs.docker.com/engine/security/rootless/", "https://docs.podman.io/en/latest/markdown/podman-compose.1.html"]
verificado_em: 2026-10-05
valido_para: "Docker Engine 29.x (docs de 2026-10); Podman docs latest de 2026-10"
revisar_em: 2027-01-05
criado: 2026-10-05
decisao: promovido
tags: [ambiente, container, docker, podman, seguranca, adm-0009]
---
# Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites

## Resumo

| Opcao | O que o container passa a poder no host | Requisitos / limites |
|---|---|---|
| (a) Montar `/var/run/docker.sock` do host | Quem fala com o socket tem poder equivalente a root no host: pode subir container montando `/` do host. Nao ha isolamento. | Nada alem do socket; Compose funciona normal (usa o mesmo daemon). Containers criados ficam **irmaos** do container do ambiente; caminhos de bind mount sao os do **host**, nao os do container. |
| (b) Docker-in-Docker (imagem `docker:dind`) | O container e `--privileged`: acesso quase total ao host (a propria documentacao da imagem avisa). Daemon proprio e isolado do daemon do host. | `--privileged` obrigatorio, tambem na variante `-rootless` (experimental). TLS automatico via `DOCKER_TLS_CERTDIR=/certs`. Imagens e volumes ficam dentro do dind (somem com ele, salvo volume proprio). |
| (c) Docker rootless ou Podman | O daemon roda como usuario comum: root do container nao e root do host; o dano de uma fuga fica limitado ao usuario. | Docker rootless: `newuidmap`/`newgidmap` (pacote `uidmap`), `/etc/subuid` e `/etc/subgid` com 65.536 ids ou mais, namespaces de usuario habilitados; portas <1024 bloqueadas por padrao; IP do container nao e alcancavel do host; `-p` nao propaga IP de origem; so `overlay2` (kernel 5.11+), `fuse-overlayfs`, `btrfs` ou `vfs`; `--cpus/--memory/--pids-limit` so com cgroup v2 + systemd. Podman: `podman compose` e apenas um wrapper que chama `docker-compose` ou `podman-compose` contra o socket do Podman; a compatibilidade com Compose depende do provedor. |

(a) e a mais simples e a mais perigosa; (b) isola o daemon mas custa um container privilegiado; (c) e a que mais reduz o que um agente comprometido alcanca, ao custo de configuracao e das limitacoes de rede.

## O que aproveitar

Base para decidir como um agente ou CI dentro de container sobe os containers de um projeto. Regra pratica: acesso ao socket do Docker = root no host; se o agente nao for totalmente confiavel, prefira (c).

## Ressalvas

- So leitura de documentacao em 2026-10-05; nada executado. Os limites exatos de Compose em rootless nao constam numa lista unica: validar com o `docker-compose.yml` do lab antes de decidir.
- O resumo das paginas veio de modelo pequeno do WebFetch: reconferir os trechos criticos (seguranca do socket, `--privileged`) na fonte antes de uma decisao de seguranca.

## Links confiaveis

- [Docker Engine security: daemon attack surface](https://docs.docker.com/engine/security/#docker-daemon-attack-surface): por que acesso ao daemon/socket equivale a root.
- [Docker rootless mode](https://docs.docker.com/engine/security/rootless/): requisitos Linux e instalacao; veja tambem a pagina de [troubleshooting](https://docs.docker.com/engine/security/rootless/troubleshoot/) com as limitacoes.
- [Imagem oficial docker (dind)](https://hub.docker.com/_/docker): `--privileged`, TLS e variante rootless.

## Notas derivadas

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]: o mesmo tema (root no container) visto pela aplicacao.
- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]: o que o agente alcanca de dentro do container.

## Decisao do Bibliotecario

Promovido a `30_Referencias` (2026-10-05): comparacao de fontes oficiais, sem duplicata no Brain. Confianca media mantida; a escolha da opcao e do humano, apos a analise de ameacas da Seguranca.
