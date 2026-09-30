---
tipo: problema-solucao
status: ativo
origem: T-0003 (curado pelo Bibliotecario a partir do candidato do Dev)
confianca: media
fontes: ["projeto lab: testes da T-0003 (73 passando) e subida real com curl"]
verificado_em: 2026-09-30
valido_para: SQLAlchemy 2.x, PostgreSQL, sem Alembic
revisar_em: 2027-03-30
criado: 2026-09-30
tags: [sqlalchemy, postgres, migracao]
decisao: promovido
---
# create_all do SQLAlchemy nao adiciona coluna em tabela existente

## Sintoma

Depois de acrescentar uma coluna a um modelo, a app quebra em bancos ja criados (ex.: volume Docker persistente), porque a coluna nao existe na tabela. Os testes passam.

## Ambiente

SQLAlchemy 2.x, PostgreSQL, projeto sem Alembic (schema criado por `Base.metadata.create_all` na inicializacao).

## Causa raiz

`create_all` so cria tabelas ausentes; nunca altera uma tabela existente. Os testes nao pegam, pois recriam o banco de teste do zero.

## Solucao

Solucao minima sem Alembic: executar `ALTER TABLE <tabela> ADD COLUMN IF NOT EXISTS ...` (idempotente) logo apos o `create_all` na inicializacao. Se o schema evoluir com frequencia, adotar Alembic.

## Como verificar que foi resolvido

Subir a app contra um volume criado com o schema antigo e conferir que a coluna aparece e a rota funciona. **Nao verificado ainda:** a migracao com tabela pre-existente nao foi testada contra volume antigo na T-0003, por isso a confianca e media.

## O que nao funcionou

Confiar so nos testes: eles partem de banco vazio e escondem o problema.

## Origem

T-0003 (projeto lab), candidato do Dev.

## Relacionadas

- [[Testes com banco separado e rollback por teste funcionam no FastAPI com SQLAlchemy]]: explica por que a suite de testes nao revela este defeito (banco recriado do zero).

## Decisao do Bibliotecario

Promovido. Uma ideia por nota: a parte sobre padrao de upload virou nota propria ([[Upload de imagem valida tipo por magic bytes e serve por nome gerado]]) e o aprendizado da correcao do BUG-0006 foi fundido em [[Recusa previa por Content-Length esconde a validacao do upload]].
