---
tipo: problema-solucao
status: ativo
origem: T-0010 (Seguranca, SEC-T0010-03) e SEARCH-0004, curado pelo Bibliotecario
pesquisa: SEARCH-0004
tarefa: T-0010
confianca: media
fontes: ["SEC-T0010-03 (lab)", "SEC-T0010-01 (lab)"]
verificado_em: 2026-10-02
valido_para: "Python 3.13 em python:3.13-slim (glibc), Pillow 12.3.0, FastAPI/AnyIO com threadpool, Docker cgroup v2"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [seguranca, memoria, dos, pillow, glibc, docker, medicao, cwe-770, armadilha]
---
# Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera

## Sintoma

O container leva OOM kill depois de varias rodadas de decodificacao pesada, mesmo com um limite de concorrencia (semaforo ou orcamento em pixels) que deixa so uma decodificacao por vez. Uma rodada isolada nao mostra o defeito.

## Ambiente

Python 3.13 em `python:3.13-slim` (glibc), Pillow 12.3.0, FastAPI/AnyIO com threadpool, Docker com cgroup v2.

## Causa raiz

Limitar quantas imagens decodificam ao mesmo tempo limita o pico de **uma** rodada, nao o do processo ao longo do tempo. Cada requisicao roda numa thread diferente do threadpool, o `malloc` do glibc da uma arena a cada thread, e a memoria liberada pelo Pillow fica retida nessas arenas. A decodificacao seguinte, em outra thread, soma o seu pico ao que ficou retido nas outras. A explicacao do alocador esta em [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]].

## Solucao

`MALLOC_ARENA_MAX=2` no ambiente do container (`ENV` no Dockerfile ou `environment:` no Compose). Alternativas ainda a medir: `malloc_trim(0)` via `ctypes` depois de cada operacao grande, ou jemalloc.

## Como verificar que foi resolvido

1. Rode a aplicacao com teto rigido por um override de teste fora do repositorio (`mem_limit` e `memswap_limit` iguais).
2. Repita 15 rodadas da carga paralela e, depois de cada uma, leia `cat /sys/fs/cgroup/memory.peak` dentro do container (valor exato do kernel, melhor que o `docker stats`; ver [[Docker stats subestima pico de memoria curto - medir com ru_maxrss em container com teto]]) e `docker inspect --format '{{.State.OOMKilled}}'`.
3. Esperado: pico estavel abaixo do teto e `OOMKilled=false`. Pico subindo a cada rodada indica retencao.

## O que nao funcionou

- Confiar no semaforo ou no orcamento de pixels sozinho (premissa errada: "limitar a concorrencia basta para limitar a memoria").
- Ajustar variaveis do Pillow: a retencao esta abaixo dele ([[PILLOW_BLOCKS_MAX vem desligado e so controla o pool do Pillow, nao as arenas do malloc]]).

Evidencia (lab, commit `d3e4004`): WebP RGBA 7071 x 7071 (89 KB), 10 envios por rodada, teto de 2000 MB, orcamento de 50 MP (1291 MiB por vaga). Sem a variavel: pico 1572 -> 1700 -> 1767 -> ... -> 1945 MiB e OOM kill (exit 137) na 9a rodada. Com `MALLOC_ARENA_MAX=2`: pico estavel em 1751 MiB, 14 rodadas sem OOM.

Confirmacao (2026-10-02, commit `4ede09f`, variavel vinda do `ENV` da imagem): 15 rodadas, pico 1364 -> 1650 -> 1758 MiB e estavel da rodada 12 a 15, `OOMKilled=false`, nenhum 500. O pico ainda sobe em degraus nas primeiras rodadas; a margem sob 2000 MB e de ~240 MiB.

## Links confiaveis

- Veja os links oficiais do glibc em [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]].

## Relacionadas

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: o limite de recursos que esta armadilha completa.
- [[Semaforo dentro de rota def do FastAPI prende o threadpool e trava as outras rotas]]: o limite por quantidade e a segunda armadilha do mesmo caso.
- [[Pagina de 503 que consulta o banco vira 500 justamente quando o servidor esta sobrecarregado]]: o que acontece com o 503 desse mecanismo sob carga.

## Origem

SEC-T0010-03 e SEC-T0010-01 (lab, T-0010); pedido SEARCH-0004. Vale tambem para o teto de memoria da T-0015.

## Decisao do Bibliotecario

Promovido (2026-10-02) como problema-solucao (o tipo proposto era armadilha). Mantido separado da nota do MALLOC_ARENA_MAX: aqui o foco e a armadilha de confiar no limite de concorrencia e o roteiro de teste por varias rodadas; la, o funcionamento e a comparacao dos controles.
