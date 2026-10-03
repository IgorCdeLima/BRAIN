---
tipo: problema-solucao
status: ativo
origem: T-0015 (Seguranca, SEC-T0015-01 do lab), curado pelo Bibliotecario
tarefa: T-0015
confianca: alta
fontes: ["https://docs.docker.com/engine/containers/resource_constraints/", "https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html", "SEC-T0015-01 (lab)"]
verificado_em: 2026-10-03
valido_para: "Docker Engine 29 / Compose 2.40, cgroup v2, host com swap"
criado: 2026-10-03
decisao: promovido
revisar_em: 2027-04-03
tags: [seguranca, docker, cwe-770, memoria, swap, hardening]
---
# mem_limit sem memswap_limit nao e teto de memoria - o container usa X de RAM mais X de swap

## Sintoma

O servico tem `mem_limit: 2000m` no Compose e mesmo assim consome mais que isso, e os outros servicos do host (ex.: o banco) ficam lentos. O `docker inspect` mostra `MemorySwap` igual ao dobro do limite.

## Ambiente

Docker Engine 29 / Compose 2.40, cgroup v2, host com swap (lab de 3,4 GB).

## Causa raiz

`mem_limit` sozinho limita so a RAM. Sem `memswap_limit`, o Docker permite o mesmo valor em swap: dentro do container `memory.swap.max` = X, e `MemorySwap` = 2X. O excedente vai para o swap do host e pagina os demais servicos. O "teto" que se achou ter colocado e o dobro.

## Solucao

```yaml
mem_limit: 2000m
memswap_limit: 2000m   # igual ao mem_limit: sem swap
```

Sem swap, passar do teto vira OOM kill. Combine com `restart: on-failure:N` ou `unless-stopped`, senao o container fica parado (regra 7 do cheat sheet OWASP de Docker).

## Como verificar que foi resolvido

```bash
docker inspect <c> --format 'Mem={{.HostConfig.Memory}} Swap={{.HostConfig.MemorySwap}}'   # devem ser iguais
docker exec <c> cat /sys/fs/cgroup/memory.swap.max /sys/fs/cgroup/memory.swap.peak         # 0 e 0
```

Ao medir pico sob carga, leia `memory.peak` **e** `memory.swap.peak`: so `memory.peak` subestima o uso quando ha swap.

## O que nao funcionou

Confiar so em `mem_limit`. No lab (SEC-T0015-01), 10 rodadas de carga com `mem_limit: 2000m` sem `memswap_limit` deram `Swap=4194304000`, `memory.peak` de 1487 MiB e `memory.swap.peak` de 515 MiB.

## Relacionadas

- [[Docker stats subestima pico de memoria curto - medir com ru_maxrss em container com teto]]: os testes dessa nota ja usam `--memory-swap=X`; esta explica o motivo.
- [[No Compose mem_limit 2200m e 2200 MiB binario e nao 2200 MB]]: unidade do valor ao comparar o teto com o pico medido.
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: a classe de fraqueza que o teto de memoria mitiga.
- [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]]: o pico de memoria que o teto precisa comportar.
- [[USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid]]: o restante do hardening do servico no Compose.

## Origem

SEC-T0015-01 (lab, 2026-10-03). Documentacao do Docker ("Resource constraints") lida em 2026-10-03 confirma o comportamento.

## Decisao do Bibliotecario

Promovido (2026-10-03). Sem duplicata: a nota do `docker stats` so usa `--memory-swap`, nao descreve a armadilha. Ligado a ela e ao CWE-770.
