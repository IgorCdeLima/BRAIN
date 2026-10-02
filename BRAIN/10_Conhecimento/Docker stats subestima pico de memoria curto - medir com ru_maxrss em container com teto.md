---
tipo: problema-solucao
status: ativo
origem: T-0010 (Revisor), curado pelo Bibliotecario
tarefa: T-0010
confianca: media
fontes: ["VER-T0010-01 (lab)", "SEC-T0010-01 (lab)"]
verificado_em: 2026-10-01
valido_para: "Docker no Linux; Python 3.13"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [docker, memoria, medicao, dos, armadilha]
---
# Docker stats subestima pico de memoria curto - medir com ru_maxrss em container com teto

## Sintoma

Um criterio como "pico abaixo de 2 GB" passa com `docker stats`, mas o container leva OOM kill em producao ou em outro host. O `docker stats` amostra cerca de uma vez por segundo, e um pico que dura menos que isso (decodificar e codificar uma imagem grande, por exemplo) nao e visto.

## Ambiente

Docker no Linux, Python 3.13, Pillow 12.3.0 (caso medido). A tecnica nao depende da linguagem, mas `ru_maxrss` em KiB e do Linux.

## Causa raiz

A amostragem periodica perde picos curtos. Na T-0010 a subestimativa mudava a conclusao: duas vagas de decodificacao ficam em ~3,3 GiB, e nao em ~2 GiB.

## Solucao

1. Rode a operacao num container isolado com teto rigido: `docker run --memory=X --memory-swap=X --network none <imagem> python -`, chamando a funcao da aplicacao.
2. Gere a entrada num **subprocesso** (gerar no mesmo processo contamina o pico).
3. Leia `resource.getrusage(resource.RUSAGE_SELF).ru_maxrss` (KiB no Linux) depois da operacao e confira `docker inspect --format '{{.State.OOMKilled}}'` (exit 137 = OOM).
4. Suba o teto ate a operacao passar: o menor teto que passa e o `ru_maxrss` delimitam o pico real.

Com teto rigido, a medicao nao derruba o host nem as outras sessoes, ao contrario de disparar requisicoes paralelas na aplicacao.

Para varias rodadas seguidas (retencao ao longo do tempo), leia tambem `/sys/fs/cgroup/memory.peak` dentro do container: veja [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]].

## Como verificar que foi resolvido

A mesma operacao, com o teto escolhido, termina com `OOMKilled=false` e o `ru_maxrss` abaixo do teto com margem registrada.

## O que nao funcionou

Confiar so no `docker stats` (1,09 GiB por decodificacao contra 1682 MiB reais).

## Links confiaveis

- Nenhum consultado (resultado medido). Fontes oficiais a anexar se o Pesquisador for acionado: documentacao do `docker stats`, do `docker run --memory` e `getrusage(2)`.

## Relacionadas

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: o tema de limites de recurso, para o qual esta medicao serve de prova.
- [[MALLOC_ARENA_MAX limita as arenas do glibc e e o primeiro controle para memoria retida em servidor com threads]]: o controle aplicado depois de medir.

## Origem

T-0010 (lab): WebP RGBA 7071 x 7071 por `processar_imagem` (Pillow 12.3.0). `docker stats` da Seguranca registrou 1,09 GiB (SEC-T0010-01); medido como acima, OOM com teto de 1400 MB e `ru_maxrss` de 1682 MiB com teto de 2000 MB (VER-T0010-01). Util para o CS-08 da T-0010 e o teto da T-0015.

## Decisao do Bibliotecario

Promovido (2026-10-02) como problema-solucao (o tipo proposto era aprendizado, mas o conteudo e uma tecnica com sintoma e solucao). Sem duplicata no Brain. Links oficiais seguem pendentes (nenhuma fonte confiavel consultada).
