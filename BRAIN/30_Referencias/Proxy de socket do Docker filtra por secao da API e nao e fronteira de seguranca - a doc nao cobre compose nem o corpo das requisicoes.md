---
tipo: referencia
status: ativo
origem: SEARCH-0010 (Pesquisador, item 5), curado pelo Bibliotecario
pesquisa: SEARCH-0010
tarefa: T-0018
autor: Tecnativa (projeto docker-socket-proxy)
url: https://github.com/Tecnativa/docker-socket-proxy
acessado_em: 2026-10-05
confianca: media
fontes: ["https://github.com/Tecnativa/docker-socket-proxy"]
verificado_em: 2026-10-05
valido_para: "Tecnativa/docker-socket-proxy, README de 2026-10-05"
revisar_em: 2027-01-05
criado: 2026-10-05
decisao: promovido
tags: [docker, socket, proxy, seguranca, container]
---
# Proxy de socket do Docker filtra por secao da API e nao e fronteira de seguranca - a doc nao cobre compose nem o corpo das requisicoes

## Resumo

- `Tecnativa/docker-socket-proxy` e um projeto mantido: HAProxy na frente de `/var/run/docker.sock`. Variaveis de ambiente `0/1` liberam ou negam **prefixos de URL** da API (`CONTAINERS`, `IMAGES`, `NETWORKS`, `VOLUMES`, `BUILD`, `POST`...). Por padrao so `EVENTS`, `PING` e `VERSION` estao liberados; `POST` (escrita), `BUILD`, `CONTAINERS` etc. vem negados e respondem `403`.
- Limites declarados: sem TLS (HTTP puro), expor so em rede Docker interna confiavel, "saiba o que esta fazendo". E controle de acesso por rota e metodo.
- **Nao documentado:** quais secoes `docker compose build/up/down` exige, e se o corpo das requisicoes e inspecionado.
- **Inferencia (nao esta na doc):** liberar `POST` mais `CONTAINERS` permite criar um container com qualquer corpo, inclusive `Privileged` ou bind de `/`. Logo o proxy nao cumpre o requisito "sem privileged, sem bind de /".

## O que aproveitar

Nao tratar proxy de socket como o que torna seguro dar o Docker ao agente. Para o requisito acima so serviria um filtro que inspecione o corpo (nao encontrado na pesquisa) ou outra abordagem (Docker rootless ou Podman no host).

## Ressalvas

- A conclusao sobre o corpo das requisicoes e inferencia e deve ser testada pela Seguranca (T-0019).
- So o README foi lido; nenhum teste.
- Link confiavel: [docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy) (variaveis, padroes e avisos).

## Notas derivadas

- [[Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites]]: a razao de se querer um proxy.
- [[Podman rootless dentro de container Docker - a doc oficial do Podman usa privileged e fuse, sem privileged nao esta documentado]]: a outra opcao da matriz.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `30_Referencias`. Sem duplicata. A inferencia sobre o corpo ficou marcada como tal.
