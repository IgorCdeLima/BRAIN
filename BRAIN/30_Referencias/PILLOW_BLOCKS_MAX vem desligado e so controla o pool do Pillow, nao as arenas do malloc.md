---
tipo: referencia
status: ativo
origem: SEARCH-0004 (Pesquisador, T-0010), curado pelo Bibliotecario
pesquisa: SEARCH-0004
tarefa: T-0010
autor: Pillow (documentacao oficial)
url: https://pillow.readthedocs.io/en/stable/reference/block_allocator.html
acessado_em: 2026-10-02
confianca: media
fontes: ["https://pillow.readthedocs.io/en/stable/reference/block_allocator.html"]
verificado_em: 2026-10-02
valido_para: "Pillow >= 10.0.0 (documentacao stable em 2026-10-02)"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [pillow, memoria, python]
---
# PILLOW_BLOCKS_MAX vem desligado e so controla o pool do Pillow, nao as arenas do malloc

## Resumo

O Pillow tem um alocador de blocos proprio com tres variaveis de ambiente:

- `PILLOW_BLOCKS_MAX` (padrao 0 = desligado): quantos blocos liberados o Pillow guarda para atender pedidos futuros; o que passar disso volta ao SO na hora.
- `PILLOW_BLOCK_SIZE` (padrao 16M): tamanho maximo de bloco em `ImagingAllocateArray`. A documentacao diz que nao afeta a devolucao de memoria ao SO.
- `PILLOW_ALIGNMENT` (padrao 1): alinhamento; tambem nao afeta a devolucao.

## O que aproveitar

- Com o pool desligado (padrao), o Pillow ja libera os blocos na hora: a retencao observada na T-0010 vem **abaixo** do Pillow, no `malloc` do glibc. Deixar `PILLOW_BLOCKS_MAX=0` e correto; aumenta-lo so pioraria. O controle que atua e `MALLOC_ARENA_MAX`: [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]].
- Evita gastar tempo ajustando variaveis do Pillow quando a causa e o alocador do sistema.

## Ressalvas

- `PILLOW_BLOCK_SIZE` menor gera blocos menores (mais abaixo do limiar de mmap) e pode mudar o padrao de fragmentacao; nao e controle documentado para este problema. Se testar, medir.
- `Image.core.set_blocks_max` nao aparece na documentacao como API publica estavel; use as variaveis de ambiente.
- A conclusao de que a retencao esta no glibc vem do experimento da T-0010, nao da pagina do Pillow.

## Links confiaveis

- [Pillow - Block allocator / variaveis de ambiente](https://pillow.readthedocs.io/en/stable/reference/block_allocator.html): defaults e efeito das tres variaveis.
- [mallopt(3)](https://man7.org/linux/man-pages/man3/mallopt.3.html): o controle que de fato atua sobre a retencao.

## Notas derivadas

- [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]]: o controle que resolve.
- [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]]: o caso medido.

## Decisao do Bibliotecario

Promovido (2026-10-02) como referencia ativa. Sem duplicata. Pedido SEARCH-0004 catalogado.
