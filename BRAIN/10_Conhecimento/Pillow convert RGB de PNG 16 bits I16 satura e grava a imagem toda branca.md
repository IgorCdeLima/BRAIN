---
tipo: problema-solucao
status: ativo
origem: T-0010 (Revisor BUG-T0010-01/02; Dev), curado pelo Bibliotecario
tarefa: T-0010
confianca: media
fontes: ["BUG-T0010-01 (lab)", "VER-T0010-01 (lab)", "BUG-T0010-02 (lab)", "VER-T0010-02 (lab)", "commit 3c35d3e (lab)"]
verificado_em: 2026-10-02
valido_para: "Pillow 12.3.0"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-02
tags: [pillow, imagem, png, armadilha]
---
# Pillow convert RGB de PNG 16 bits I16 satura e grava a imagem toda branca

## Sintoma

Um PNG de escala de cinza com 16 bits, enviado e regravado, sai praticamente **todo branco**, sem nenhum erro. Os casos comuns de teste (RGBA, P, L, 1, CMYK) nao pegam isso, e um teste de "nao gera 500" tambem nao.

## Ambiente

Pillow 12.3.0, `python:3.13-slim`.

## Causa raiz

O Pillow abre PNG de cinza com 16 bits no modo `I;16` (valores 0 a 65535). `im.convert("RGB")` (ou `"L"`) **satura** esses valores em vez de reescalar: tudo acima de 255 vira 255. Medido: `Image.new("I;16", (4,4), 30000)` salvo em PNG e regravado com `convert("RGB")` deu `(255, 255, 255)` (esperado ~117); o mesmo com 1000 e 65535. Num gradiente de 16 bits o gravado tem 1 valor distinto (esperado ~256).

## Solucao

Trate `I;16` (e `I`) explicitamente: ou mantenha o modo (o Pillow grava `I;16` como PNG de 16 bits), ou reescale antes de converter:

```python
im.convert("I").point(lambda v: v / 257 + 0.5).convert("L")
```

Detalhes do `point` em modo `I`: a lambda e avaliada **uma vez, simbolicamente**, e so aceita expressao linear `a*v + b`; `round(v / 257)` dentro da lambda levanta excecao (na T-0010 virou "imagem corrompida"). O `+ 0.5` faz o arredondamento (30000 -> 117; sem ele, 116).

**Armadilha seguinte (BUG-T0010-02):** ao reescalar, o `info["transparency"]` do PNG `I;16` com `tRNS` continua com o valor de 16 bits (ex.: 1000). O `convert("RGBA")` seguinte procura esse valor na imagem de 8 bits, nao acha, e a imagem sai toda opaca, sem erro. Reescale tambem a transparencia (`round(t / 257)`) ou monte o alfa pela mascara antes de reescalar.

## Como verificar que foi resolvido

Incluir nos testes de modo de cor um PNG `I;16` com gradiente (esperar ~256 valores distintos) e um com `tRNS` (conferir o alfa do pixel transparente).

## O que nao funcionou

- `convert("RGB")` / `convert("L")` direto sobre `I;16`.
- `point(lambda v: round(v / 257))`: nao aceita funcao nao linear em modo `I`.

## Relacionadas

- [[Regravar imagem com Pillow exige exif_transpose, info vazio e ICC reserializado]]: a receita geral de regravacao, onde o modo de cor deve ser tratado.
- [[Teste de ICC de Pillow com createProfile gerado duas vezes falha na virada de segundo]]: outro achado da mesma tarefa, sobre teste instavel.

## Origem

BUG-T0010-01 e BUG-T0010-02 (lab), com o `point` descoberto pelo Dev no commit `3c35d3e`. Falha silenciosa: a imagem e aceita e se perde. Vale para qualquer projeto que decodifica e regrava imagem (sanitizacao de upload, miniaturas).

## Decisao do Bibliotecario

Promovido (2026-10-02). Funde o item 1 do candidato do Dev "Pillow point em modo I..." (o item 2, sobre o perfil ICC, virou nota propria). Links oficiais pendentes: o candidato sugere a pagina "Concepts / Modes" da documentacao do Pillow.
