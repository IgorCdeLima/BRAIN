---
tipo: candidato
status: arquivado
origem: T-0002 (BUG-0003, BUG-0004)
confianca: alta
criado: 2026-09-29
tags: [python, decimal, validacao, postgresql]
---
# Parser de valor monetário pt-BR: ponto ambíguo, `Decimal` e NUL

## Causa raiz e premissa errada
- Premissa errada: "o regex valida, logo a conversão é segura". O regex aceitava milhar sem vírgula (`1.234`), mas a conversão só removia pontos quando havia vírgula. `Decimal("1.234").quantize(0.01)` gravou 1,23 (arredondou); `1.234.567` levantou `InvalidOperation` (500).
- Segunda: validar só tamanho/vazio em texto. PostgreSQL recusa NUL (`\x00`) em `varchar` (`psycopg.DataError`), gerando 500.

## Regra que funciona
- Um regex por formato, e a conversão decorre do formato casado: milhar (`\d{1,3}(\.\d{3})+`) remove pontos; ponto decimal (`\d+\.\d{1,2}`) só com 1-2 casas. Grupo de 3 dígitos = milhar, 1-2 = decimal: sem ambiguidade.
- Nunca `quantize` para "consertar" entrada: mais casas que o permitido é erro de validação.
- Recusar caracteres de controle (`[\x00-\x1f\x7f]`) em campos de texto com 422.
- Testar como tabela de casos: `1.234`, `1.000`, `1.005`, `1.234.567`, `1.2345`, `1.234.56`.

## Ambiente
- A imagem Docker do projeto embute o código: após editar, `docker compose build app` antes de `run --rm app pytest`, senão roda a suíte antiga.

## Terceira lição (BUG-0005)
- `Decimal.quantize` usa o contexto global (precisão 28): resultado com mais de 28 dígitos levanta `InvalidOperation`. Premissa errada: "o teto de valor é checado depois, então a conversão não falha". Correção: comparar com o teto **antes** do `quantize` (ou limitar dígitos). Incluir `"1" * 27`, `"1" * 30` e um número de 200 dígitos nos casos de teste de "valor inválido"; "valores extremos" não pode ficar como verificação não feita.

## Decisão do Bibliotecário

**Fundido e arquivado** em 2026-09-29. Conteúdo absorvido em [[Valor em reais com ponto de milhar sem virgula e ambiguo - nao converta direto para Decimal]] (regras do parser e BUG-0005), [[Texto com caractere NUL derruba insert no PostgreSQL com erro 500]] e [[Imagem Docker que embute o codigo exige build antes de rodar pytest]]. Estava fora do template Candidato e sem fontes.
