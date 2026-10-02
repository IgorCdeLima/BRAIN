---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0010
pesquisa: SEARCH-0004
confianca: media
fontes: [pillow.readthedocs.io block_allocator]
verificado_em: 2026-10-02
valido_para: Pillow >= 10.0.0 (conferido na documentacao stable em 2026-10-02)
criado: 2026-10-02
decisao:
tags: [pillow, memoria, python]
---
# PILLOW_BLOCKS_MAX vem desligado e so controla o pool do Pillow, nao as arenas do malloc

## Conteudo proposto

- O Pillow tem um alocador de blocos proprio com tres variaveis de ambiente:
  - `PILLOW_BLOCKS_MAX` (padrao 0 = desligado): quantos blocos liberados o Pillow guarda para atender pedidos futuros; o que passar disso volta ao SO na hora.
  - `PILLOW_BLOCK_SIZE` (padrao 16M): tamanho maximo de bloco em `ImagingAllocateArray`. A documentacao diz que nao afeta a devolucao de memoria ao SO.
  - `PILLOW_ALIGNMENT` (padrao 1): alinhamento; tambem nao afeta a devolucao.
- Com o pool desligado (padrao), o Pillow ja libera os blocos na hora: a retencao observada na T-0010 vem **abaixo** do Pillow, no `malloc` do glibc. Deixar `PILLOW_BLOCKS_MAX=0` e correto; aumenta-lo so pioraria.
- `PILLOW_BLOCK_SIZE` menor gera blocos menores (mais abaixo do limiar de mmap) e pode mudar o padrao de fragmentacao; nao e controle documentado para este problema. Se for testar, medir.
- Nao vi na documentacao `Image.core.set_blocks_max` como API publica estavel; use as variaveis de ambiente.

## Evidencia

Pagina oficial da documentacao do Pillow (link abaixo), lida em 2026-10-02. A conclusao de que a retencao esta no glibc vem do experimento da T-0010 (a variavel `MALLOC_ARENA_MAX` estabilizou o pico).

## Links confiaveis

- [Pillow - Block allocator / variaveis de ambiente](https://pillow.readthedocs.io/en/stable/reference/block_allocator.html): defaults e efeito de `PILLOW_BLOCK_SIZE`, `PILLOW_BLOCKS_MAX`, `PILLOW_ALIGNMENT`.
- [mallopt(3)](https://man7.org/linux/man-pages/man3/mallopt.3.html): o controle que de fato atua sobre a retencao.

## Por que e reaproveitavel

Evita gastar tempo ajustando variaveis do Pillow quando a causa e o alocador do sistema.

## Relacionadas no Brain

- [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]]

## Decisao do Bibliotecario

