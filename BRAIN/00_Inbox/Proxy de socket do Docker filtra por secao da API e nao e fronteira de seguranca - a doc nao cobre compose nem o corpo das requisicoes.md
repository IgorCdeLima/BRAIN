---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0010
confianca: media
fontes: [https://github.com/Tecnativa/docker-socket-proxy]
verificado_em: 2026-10-05
valido_para: Tecnativa/docker-socket-proxy, README de 2026-10-05
criado: 2026-10-05
decisao:
tags: [docker, socket, proxy, seguranca, container]
---
# Proxy de socket do Docker filtra por secao da API e nao e fronteira de seguranca - a doc nao cobre compose nem o corpo das requisicoes

## Conteudo proposto

- Projeto mantido (`Tecnativa/docker-socket-proxy`, HAProxy na frente de `/var/run/docker.sock`): variaveis de ambiente `0/1` liberam ou negam **prefixos de URL** da API (`CONTAINERS`, `IMAGES`, `NETWORKS`, `VOLUMES`, `BUILD`, `POST`...). Por padrao so `EVENTS`, `PING` e `VERSION` estao liberados; `POST` (escrita), `BUILD`, `CONTAINERS` etc. vem negados. Negado responde `403`.
- Limites declarados: sem TLS (HTTP puro), expor so em rede Docker interna confiavel, "saiba o que esta fazendo". O proxy e controle de acesso por rota/metodo.
- **Nao documentado:** quais secoes `docker compose build/up/down` exige, e se o corpo das requisicoes e inspecionado. Inferencia (nao da doc): liberar `POST`+`CONTAINERS` permite criar container com qualquer corpo, inclusive `Privileged` ou bind de `/`; logo nao cumpre "sem privileged, sem bind de /". Para esse requisito, so um filtro que inspecione o corpo (nao encontrado aqui) ou outra abordagem (Docker rootless/Podman no host).

## Evidencia

README oficial lido; a conclusao sobre corpo e inferencia e deve ser testada pela Seguranca.

## Links confiaveis

- [docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy): variaveis, padroes e avisos.

## Por que e reaproveitavel

Evita a ilusao de que proxy de socket torna seguro dar o Docker ao agente.

## Relacionadas no Brain

- [[Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites]]

## Decisao do Bibliotecario
