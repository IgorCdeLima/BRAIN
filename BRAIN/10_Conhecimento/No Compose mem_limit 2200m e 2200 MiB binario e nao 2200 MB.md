---
tipo: aprendizado
status: ativo
origem: T-0015 (Revisor), curado pelo Bibliotecario
tarefa: T-0015
confianca: alta
fontes: ["https://docs.docker.com/engine/containers/resource_constraints/", "docker inspect medido no lab (T-0015)"]
verificado_em: 2026-10-03
valido_para: "Docker Engine / Docker Compose (mem_limit, memswap_limit, --memory)"
criado: 2026-10-03
decisao: promovido
revisar_em: 2027-04-03
tags: [docker, compose, memoria, unidades, armadilha]
---
# No Compose mem_limit 2200m e 2200 MiB binario e nao 2200 MB

## O que aconteceu

Na T-0015 (lab) a Entrega e o registro de seguranca diziam "2200m = 2098 MiB", convertendo como se fossem 2200 MB decimais. O `docker inspect <app> --format '{{.HostConfig.Memory}}'` mostrou `2306867200`, ou seja 2200 x 1048576. A margem do teto contra o pico medido ficou subestimada (19% declarado, 25% real). Erro inofensivo ali, mas no sentido inverso (achar que ha mais memoria do que ha) levaria a um teto apertado demais.

## O que aprendemos

Os sufixos `b`, `k`, `m`, `g` em `mem_limit`, `memswap_limit` e `--memory` do Docker sao **binarios**: `2200m` = 2200 MiB = 2.306.867.200 bytes. Ao comparar o teto com um pico medido em MiB (`memory.peak` / 1048576), use o numero do `mem_limit` direto, sem converter.

## O que muda a partir de agora

Ao registrar margem de teto (CS-08, testes de carga, OOM provocado), comparar MiB com MiB e conferir o valor efetivo com `docker inspect`. Complementa [[mem_limit sem memswap_limit nao e teto de memoria - o container usa X de RAM mais X de swap]], sobre o outro erro comum ao fixar o teto.

## Origem

T-0015 (lab), medicao com `docker inspect`. Documentacao: [Docker - Resource constraints](https://docs.docker.com/engine/containers/resource_constraints/), sufixos das opcoes de memoria.

## Decisao do Bibliotecario

Promovido (2026-10-03) como aprendizado. Sem duplicata. Ligado a [[Docker stats subestima pico de memoria curto - medir com ru_maxrss em container com teto]], que trata da medicao do pico.
