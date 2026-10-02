---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/pesquisador
tarefa: T-0010
pesquisa: SEARCH-0004
confianca: media
fontes: [man7.org mallopt(3), manual do glibc (tunables), man7.org malloc_trim(3)]
verificado_em: 2026-10-02
valido_para: glibc 2.8+ (Debian, imagem python:3.13-slim)
criado: 2026-10-02
decisao:
tags: [memoria, glibc, malloc, docker, python, cwe-770]
---
# MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads

## Conteudo proposto

- O `malloc` do glibc cria **arenas** (pools de heap) para reduzir disputa entre threads. Com muitas threads (ex.: 40 no threadpool do FastAPI/AnyIO), cada arena guarda seus proprios blocos livres; o que uma thread libera fica na arena dela e nem sempre volta ao sistema. O pico do processo sobe de rodada em rodada mesmo sem vazamento real.
- Variavel de ambiente `MALLOC_ARENA_MAX=N` (tunable `glibc.malloc.arena_max`; `mallopt(M_ARENA_MAX)`) fixa o maximo de arenas. Padrao 0 = limite derivado de `arena_test` (8 em 64 bits), na pratica um multiplo do numero de CPUs. Exemplo no Dockerfile: `ENV MALLOC_ARENA_MAX=2`.
- `MALLOC_TRIM_THRESHOLD_` (`M_TRIM_THRESHOLD`, padrao 128 KiB) define quanto de espaco livre contiguo no topo do heap dispara devolucao. Atencao: definir esta variavel (ou `M_MMAP_THRESHOLD`, `M_TOP_PAD`, `M_MMAP_MAX`) **desliga o ajuste dinamico** do limiar de mmap; teste antes de adotar.
- As variaveis sao ignoradas em programas setuid/setgid; em container comum valem.
- Medido na T-0010 (SEC-T0010-03): com orcamento de pixels e 40 threads, o pico subiu 1572 -> 1945 MiB e deu OOM na 9a rodada; com `MALLOC_ARENA_MAX=2` o pico estabilizou em 1751 MiB e 14 rodadas passaram.

## Comparativo dos controles

| Controle | Efeito | Custo / risco |
|---|---|---|
| `MALLOC_ARENA_MAX=2` | Menos arenas, menos retencao | Mais disputa de lock no malloc; para trabalho dominado por Pillow (C, fora do GIL) o impacto costuma ser pequeno, mas medir |
| `malloc_trim(0)` via `ctypes` | Devolve paginas livres de todas as arenas (glibc >= 2.8); `pad` so vale no heap principal | Chamada cara se frequente; so alivia o que ja esta livre; chamar apos a requisicao pesada |
| jemalloc (`LD_PRELOAD` + `MALLOC_CONF`) | Devolucao por decaimento (`dirty_decay_ms`, `muzzy_decay_ms`, `narenas`) | Pacote extra na imagem, outro alocador a manter; `LD_PRELOAD` mexe em todo o processo |
| `PILLOW_BLOCKS_MAX` | Pool do Pillow retem no maximo N blocos liberados | Nao muda a retencao das arenas do glibc; ver [[PILLOW_BLOCKS_MAX vem desligado e so controla o pool do Pillow, nao as arenas do malloc]] |

## Como testar

Rodar o mesmo lote de envios (N rodadas) em container com teto de memoria, medindo `ru_maxrss` (ver [[Docker stats subestima pico de memoria curto - medir com ru_maxrss em container com teto]]), com e sem a variavel. O criterio e o pico por rodada estabilizar e nao haver OOM.

## Evidencia

Documentacao oficial do glibc e das man pages (links abaixo) para o significado das variaveis e dos padroes; resultado empirico da T-0010 para o efeito no nosso caso. A afirmacao "padrao = 8 x CPUs" vem do comportamento conhecido do glibc; o manual descreve `arena_test` (8 em 64 bits) e a man page diz "tipicamente multiplo de CPUs": confira no ambiente com `MALLOC_ARENA_MAX` explicito.

## Links confiaveis

- [mallopt(3) - man7.org](https://man7.org/linux/man-pages/man3/mallopt.3.html): `M_ARENA_MAX`, `M_ARENA_TEST`, `M_TRIM_THRESHOLD`, variaveis de ambiente e o efeito de desligar o limiar dinamico.
- [Memory Allocation Tunables - manual do glibc](https://sourceware.org/glibc/manual/latest/html_node/Memory-Allocation-Tunables.html): nomes `glibc.malloc.*` e os equivalentes `MALLOC_*`.
- [malloc_trim(3) - man7.org](https://man7.org/linux/man-pages/man3/malloc_trim.3.html): libera memoria de todas as arenas desde glibc 2.8; `pad` so no heap principal.

## Por que e reaproveitavel

Qualquer servico Python/Linux com threads e buffers grandes (imagem, PDF, upload) em container com teto de memoria. Complementa [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: limite de corpo nao basta se o alocador retem o que foi liberado.

## Relacionadas no Brain

- [[Alocador malloc e arenas por thread retem a memoria do Pillow]]
- [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]]

## Decisao do Bibliotecario

