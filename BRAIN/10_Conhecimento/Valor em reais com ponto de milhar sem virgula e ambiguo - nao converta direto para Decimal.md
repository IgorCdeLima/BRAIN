---
tipo: problema-solucao
status: ativo
origem: agente/revisor + T-0002 (candidatos fundidos, curados pelo Bibliotecário)
confianca: alta
fontes: ["projetos/lab: qualidade/bugs/BUG-0003.md, BUG-0004.md, BUG-0005.md", "projetos/lab: qualidade/verificacoes/VER-0003.md, VER-0004.md"]
verificado_em: 2026-09-29
valido_para: qualquer parser de valor monetário digitado em pt-BR (Python Decimal)
criado: 2026-09-29
tags: [validacao, decimal, pt-br, dinheiro, armadilha]
decisao: promovido (fundido com o candidato "Parser de valor monetário pt-BR")
---
# Valor em reais com ponto de milhar e sem vírgula é ambíguo: não converta direto para Decimal

## Sintoma

- `POST valor=1.234` responde 303 e grava `1.23`, sem nenhum erro.
- `valor=1.234.567` responde 500 (`decimal.InvalidOperation`).
- 27 dígitos ou mais respondem 500, embora 26 passem.

## Ambiente

Python `Decimal` com contexto padrão (precisão 28); entrada digitada em pt-BR aceitando `1.234,56` e `1234.56`.

## Causa raiz

Premissa errada: "o regex valida, logo a conversão é segura". O regex aceitava milhar sem vírgula (`1.234`), mas a conversão só removia pontos quando havia vírgula. Assim:

- `Decimal("1.234").quantize(Decimal("0.01"))` arredonda para 1,23.
- `1.234.567` faz `Decimal()` lançar `InvalidOperation`.
- `quantize` usa o contexto global: resultado com mais de 28 dígitos lança `InvalidOperation` (`"1"*27` já dá 29). O teto de valor era checado **depois** do `quantize`.

## Solução

1. Um regex por formato; a conversão decorre do formato casado. Milhar (`\d{1,3}(\.\d{3})+`) remove os pontos; ponto decimal (`\d+\.\d{1,2}`) só com 1-2 casas. Grupo de 3 dígitos = milhar, 1-2 = decimal, sem ambiguidade. Ou recuse o ponto sem vírgula. Documente a escolha no requisito.
2. **Nunca use `quantize` para validar ou "consertar" casas decimais**: ele arredonda. Mais casas que o permitido é erro de validação.
3. Compare com o teto (ou limite os dígitos) **antes** do `quantize`.
4. Tudo que passa nos padrões aceitos deve converter sem exceção.

## Como verificar que foi resolvido

Testar como tabela de casos: `1.234`, `1.000`, `1.005`, `1.234.567`, `1.2345`, `1.234.56`, `"1"*27`, `"1"*30` e um número de 200 dígitos. "Valores extremos" não pode ficar como verificação não feita. Reproduzido e verificado pelo Revisor (VER-0003, VER-0004).

## O que não funcionou

Os testes do Dev cobriam `1,234` (inválido), mas não `1.234`. Validar só o regex, ou só o teto depois da conversão, deixou os três bugs passarem.

## Origem

BUG-0003 (commit `da476c0`), BUG-0004 e BUG-0005 (commit `baabd17`) do `lab`, T-0002. Relacionadas: [[Texto com caractere NUL derruba insert no PostgreSQL com erro 500]] (mesma família), [[Imagem Docker que embute o codigo exige build antes de rodar pytest]] (verificação das correções) e [[Testes com banco separado e rollback por teste funcionam no FastAPI com SQLAlchemy]] (mesma tarefa).

## Decisão do Bibliotecário

**Promovido e fundido** em 2026-09-29. Os candidatos "Valor em reais…" e "Parser de valor monetário pt-BR…" tratavam do mesmo assunto (BUG-0003 e BUG-0005); o segundo estava fora do template e foi absorvido. Suas partes sobre NUL e sobre build da imagem viraram notas próprias (uma ideia por nota).
