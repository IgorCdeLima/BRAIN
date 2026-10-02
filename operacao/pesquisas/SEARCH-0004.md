---
tipo: pesquisa
id: SEARCH-0004
status: catalogada
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0010
criado: 2026-10-02
pesquisado_por: pesquisador
pesquisado_em: 2026-10-02
catalogado_em: 2026-10-02
notas: ["[[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]]", "[[PILLOW_BLOCKS_MAX vem desligado e so controla o pool do Pillow, nao as arenas do malloc]]", "[[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]]"]
tags: [seguranca, memoria, glibc, malloc, dos, cwe-770, python, docker]
---
# SEARCH-0004 - Arenas do malloc do glibc retendo memoria em servidor Python com threads: MALLOC_ARENA_MAX, malloc_trim e alternativas

## Pergunta

1. Qual a documentacao oficial do glibc sobre arenas do `malloc` por thread, o numero padrao de arenas e as variaveis `MALLOC_ARENA_MAX` e `MALLOC_TRIM_THRESHOLD_` (e o `mallopt` equivalente)? Ela vale para a imagem `python:3.13-slim` (Debian, glibc)?
2. Para um servidor Python com threadpool (FastAPI/Starlette/AnyIO, 40 threads) que aloca e libera buffers grandes de imagem (Pillow): qual o controle recomendado para a memoria liberada voltar ao sistema? Comparar `MALLOC_ARENA_MAX=2`, `malloc_trim(0)` via `ctypes` e trocar o alocador (jemalloc), com custo de desempenho e riscos de cada um.
3. O Pillow tem configuracao propria de memoria que influencie isso (`PILLOW_BLOCK_SIZE`, `PILLOW_BLOCKS_MAX`, `Image.core.set_blocks_max`)?

## Contexto

- SEC-T0010-03 (lab, T-0010, commit `d3e4004`): mesmo com o orcamento de pixels deixando so uma decodificacao de 50 MP por vez (pico de 1291 MiB por vaga), o pico do container sobe a cada rodada (1572 -> 1945 MiB) e o OOM kill chega na 9a rodada de 10 envios com teto de 2000 MB. Com `MALLOC_ARENA_MAX=2`, o pico estabiliza em 1751 MiB e 14 rodadas passam sem OOM. Conclusao medida, mas sem fonte oficial para citar no SEC nem para o Dev escolher a correcao.
- Stack: Python 3.13 (`python:3.13.15-slim`), Pillow 12.3.0, uvicorn com 1 worker, Docker no Linux (cgroup v2).
- Formato esperado: nota de armadilha/controle com "como testar" e links oficiais (manual do glibc, `mallopt(3)`, documentacao do Pillow).

## Ja buscado no Brain

- Busca por `malloc`, `arena`, `glibc` em `BRAIN/`: nenhuma nota.
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]] cobre limites em geral, nao a retencao pelo alocador.
- [[Docker stats subestima pico de memoria curto - medir com ru_maxrss em container com teto]] (Inbox) cobre a medicao, nao a causa.
- `agentes/fontes-confiaveis.json` nao tem o dominio do manual do glibc nem das man pages.

---

## Resposta

<!-- Preenchido pelo Pesquisador. -->

- **Resumo (3 a 5 linhas):** O glibc cria arenas por thread e o que e liberado nelas nem sempre volta ao SO; `MALLOC_ARENA_MAX` (tunable `glibc.malloc.arena_max`) limita as arenas e e o controle recomendado, coerente com o medido na T-0010. `malloc_trim(0)` libera paginas livres de todas as arenas (glibc >= 2.8) mas so alivia depois do fato; jemalloc (`dirty_decay_ms`, `narenas`) e alternativa com custo de manter outro alocador. Definir `MALLOC_TRIM_THRESHOLD_` desliga o limiar dinamico de mmap. No Pillow, `PILLOW_BLOCKS_MAX` vem desligado (0) e so afeta o pool do Pillow, nao as arenas; as variaveis valem para Pillow >= 10. A imagem `python:3.13-slim` e Debian/glibc, entao se aplica.
- **Notas geradas no Inbox:** [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]], [[PILLOW_BLOCKS_MAX vem desligado e so controla o pool do Pillow, nao as arenas do malloc]]
- **Links confiaveis:** https://man7.org/linux/man-pages/man3/mallopt.3.html ; https://sourceware.org/glibc/manual/latest/html_node/Memory-Allocation-Tunables.html ; https://man7.org/linux/man-pages/man3/malloc_trim.3.html ; https://pillow.readthedocs.io/en/stable/reference/block_allocator.html ; https://github.com/jemalloc/jemalloc/blob/dev/TUNING.md
- **Sem resposta / limites:** (a) O padrao exato de arenas (8 x CPUs em 64 bits) nao ficou literal nas paginas lidas: o manual traz `arena_test`=8 e a man page diz "multiplo de CPUs"; recomendo conferir no ambiente. (b) A wiki MallocInternals do sourceware retornou pagina de acesso negado. (c) Nao encontrei `Image.core.set_blocks_max` documentado como API publica. (d) Custo de desempenho de `MALLOC_ARENA_MAX=2` nao tem fonte oficial: so medicao local. (e) Pagina do manual no gnu.org redireciona; usei a copia do sourceware.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

<!-- Dominios novos para agentes/fontes-confiaveis.json, com o motivo. O humano decide. -->

- Sugestao a confirmar: `sourceware.org` (manual do glibc), `man7.org` (man pages do Linux, `mallopt(3)`), `pillow.readthedocs.io` (documentacao do Pillow).

## Catalogacao

Decisao (Bibliotecario, 2026-10-02): promovidas as duas notas do Pesquisador e a armadilha da Seguranca, mais a pista do Dev fundida e arquivada. Links confiaveis preservados nas notas. Ressalvas mantidas: padrao exato de arenas a confirmar no ambiente; custo de desempenho so com medicao local.

- [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]] (10_Conhecimento)
- [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]] (10_Conhecimento)
- [[PILLOW_BLOCKS_MAX vem desligado e so controla o pool do Pillow, nao as arenas do malloc]] (30_Referencias)

<!-- Preenchido pelo Bibliotecario: decisao e notas finais. -->
