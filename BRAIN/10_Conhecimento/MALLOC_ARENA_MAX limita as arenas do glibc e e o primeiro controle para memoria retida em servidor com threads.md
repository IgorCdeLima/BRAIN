---
tipo: problema-solucao
status: ativo
origem: SEARCH-0004 (Pesquisador, T-0010), curado pelo Bibliotecario
pesquisa: SEARCH-0004
tarefa: T-0010
confianca: media
fontes: ["https://man7.org/linux/man-pages/man3/mallopt.3.html", "https://sourceware.org/glibc/manual/latest/html_node/Memory-Allocation-Tunables.html", "https://man7.org/linux/man-pages/man3/malloc_trim.3.html", "SEC-T0010-03 (lab)"]
verificado_em: 2026-10-02
valido_para: "glibc 2.8+ (Debian, imagem python:3.13-slim)"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [memoria, glibc, malloc, docker, python, cwe-770]
---
# MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads

## Sintoma

Servidor Python com threadpool (FastAPI/AnyIO, 40 threads) que aloca e libera buffers grandes (imagem, PDF, compactacao): o pico de memoria do processo sobe de rodada em rodada, sem vazamento real, ate o OOM kill em container com teto.

## Ambiente

Linux com glibc >= 2.8, como a imagem `python:3.13-slim` (Debian). Pillow 12.3.0 no caso medido. Nao vale para musl (Alpine), que tem outro alocador.

## Causa raiz

O `malloc` do glibc cria **arenas** (pools de heap) para reduzir disputa entre threads. O que uma thread libera fica na arena dela e nem sempre volta ao sistema. Com muitas threads, as arenas somam picos que ja passaram. O padrao de `arena_max` e 0, com limite derivado de `arena_test` (8 em 64 bits), na pratica um multiplo do numero de CPUs.

## Solucao

Variavel de ambiente `MALLOC_ARENA_MAX=N` (tunable `glibc.malloc.arena_max`, `mallopt(M_ARENA_MAX)`). No Dockerfile: `ENV MALLOC_ARENA_MAX=2`.

| Controle | Efeito | Custo / risco |
|---|---|---|
| `MALLOC_ARENA_MAX=2` | Menos arenas, menos retencao | Mais disputa de lock no malloc; para trabalho dominado por Pillow (C, fora do GIL) o impacto costuma ser pequeno, mas medir |
| `malloc_trim(0)` via `ctypes` | Devolve paginas livres de todas as arenas (glibc >= 2.8); `pad` so vale no heap principal | Chamada cara se frequente; so alivia o que ja esta livre; chamar apos a requisicao pesada |
| jemalloc (`LD_PRELOAD` + `MALLOC_CONF`) | Devolucao por decaimento (`dirty_decay_ms`, `muzzy_decay_ms`, `narenas`) | Pacote extra na imagem, outro alocador a manter; `LD_PRELOAD` mexe em todo o processo |
| `PILLOW_BLOCKS_MAX` | Pool do Pillow retem no maximo N blocos liberados | Nao muda a retencao das arenas; ver [[PILLOW_BLOCKS_MAX vem desligado e so controla o pool do Pillow, nao as arenas do malloc]] |

Cuidados:

- `MALLOC_TRIM_THRESHOLD_` (padrao 128 KiB) define quanto de espaco livre no topo do heap dispara devolucao. Definir esta variavel (ou `M_MMAP_THRESHOLD`, `M_TOP_PAD`, `M_MMAP_MAX`) **desliga o ajuste dinamico** do limiar de mmap; teste antes de adotar.
- As variaveis sao ignoradas em programas setuid/setgid; em container comum valem.

## Como verificar que foi resolvido

Rodar o mesmo lote de envios (N rodadas) em container com teto de memoria, com e sem a variavel, medindo o pico por rodada ([[Docker stats subestima pico de memoria curto - medir com ru_maxrss em container com teto]]). Criterio: pico estavel e sem OOM. Roteiro completo em [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]].

## O que nao funcionou

Limitar a concorrencia (semaforo ou orcamento de pixels) sozinho: limita o pico de uma rodada, nao o acumulado. Medido na T-0010 (SEC-T0010-03): pico 1572 -> 1945 MiB e OOM na 9a rodada; com `MALLOC_ARENA_MAX=2` o pico estabilizou em 1751 MiB e 14 rodadas passaram.

## Links confiaveis

- [mallopt(3) - man7.org](https://man7.org/linux/man-pages/man3/mallopt.3.html): `M_ARENA_MAX`, `M_ARENA_TEST`, `M_TRIM_THRESHOLD`, variaveis de ambiente e o efeito de desligar o limiar dinamico.
- [Memory Allocation Tunables - manual do glibc](https://sourceware.org/glibc/manual/latest/html_node/Memory-Allocation-Tunables.html): nomes `glibc.malloc.*` e os equivalentes `MALLOC_*`.
- [malloc_trim(3) - man7.org](https://man7.org/linux/man-pages/man3/malloc_trim.3.html): libera memoria de todas as arenas desde glibc 2.8; `pad` so no heap principal.

## Relacionadas

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: limite de corpo nao basta se o alocador retem o que foi liberado.
- [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]]: a armadilha e o roteiro de teste.
- [[Semaforo dentro de rota def do FastAPI prende o threadpool e trava as outras rotas]]: o outro problema de concorrencia do mesmo caso.

## Origem

SEARCH-0004 (pedido da Seguranca na T-0010) e SEC-T0010-03 (lab).

## Decisao do Bibliotecario

Promovido (2026-10-02). Funde a pista curta do Dev ("Alocador malloc e arenas por thread...", arquivada). Ressalvas herdadas do Pesquisador: o padrao exato "8 x CPUs" nao ficou literal nas paginas lidas (confirme no ambiente); o custo de desempenho do `MALLOC_ARENA_MAX=2` so tem medicao local. Pedido SEARCH-0004 catalogado.
