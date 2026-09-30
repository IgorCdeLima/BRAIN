---
tipo: problema-solucao
status: ativo
origem: agente/claude-desktop (candidato da tarefa T-0001, curado pelo Bibliotecário)
confianca: alta
fontes: ["projetos/lab: qualidade/bugs/BUG-0001.md", "https://www.postgresql.org/support/versioning/"]
verificado_em: 2026-09-29
valido_para: API do Docker Hub (hub.docker.com/v2/repositories/...)
revisar_em: 2027-03-29
criado: 2026-09-29
tags: [docker, versoes, pesquisa]
decisao: promovido
---
# Listagem de tags do Docker Hub é paginada: confirme a tag diretamente

## Sintoma

Ao consultar as tags de uma imagem pela API do Docker Hub, a versão mais nova parece não existir (ex.: só aparece até `postgres:17`).

## Ambiente

API do Docker Hub (`hub.docker.com/v2/repositories/...`), usada por agentes para decidir versões a fixar.

## Causa raiz

A API devolve as tags em páginas; a primeira não traz necessariamente a versão mais recente.

## Solução

Para decidir a versão atual, use a página oficial de versões do projeto (ex.: postgresql.org/support/versioning) e confirme a tag específica diretamente (`docker manifest inspect <imagem>:<tag>` ou a URL da tag na API), sem concluir pela ausência na listagem.

## Como verificar que foi resolvido

`docker manifest inspect <imagem>:<tag>` responde para a tag escolhida, e a versão coincide com a página oficial do projeto.

## O que não funcionou

- Concluir "a 18 não existe" pela primeira página da listagem.
- Supor que o PostgreSQL tem versão LTS: não tem, toda versão principal tem 5 anos de suporte.

## Origem

BUG-0001 do `lab` (T-0001): o Dev fixou `postgres:17.11` com essa premissa; o Revisor confirmou que `18.6-alpine` existia; corrigido e verificado no VER-0002. Relacionada: [[Imagem postgres 18+ monta o volume em var-lib-postgresql]] (mesmo episódio, outra armadilha da versão 18).

## Decisão do Bibliotecário

**Promovido** em 2026-09-29. Sem duplicata. Evidência: BUG-0001 verificado e página oficial. `revisar_em` por envolver API e versões.
