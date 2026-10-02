---
tipo: candidato
origem: dev T-0010 (SEC-T0010-03, medicao da Seguranca)
status: arquivado
decisao: fundido em [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]] e [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]] (2026-10-02)
pesquisa: SEARCH-0004
---
# Arenas do malloc retem a memoria liberada pelo Pillow em servidor com threadpool

- Sintoma: pico de memoria do container subia a cada rodada de decodificacao pesada (WebP 50 MP) e acabava em OOM, mesmo com orcamento de pixels limitando a concorrencia.
- Causa: cada thread do threadpool usa uma arena do malloc (glibc) e nao devolve ao SO o que o Pillow libera.
- Correcao medida: `MALLOC_ARENA_MAX=2` no ambiente (Dockerfile): pico estavel em 1751 MiB em 14 rodadas.
- Premissa errada: "limitar a concorrencia basta para limitar a memoria". Fonte oficial do glibc pendente (SEARCH-0004); alternativas nao testadas: `malloc_trim`, jemalloc.
