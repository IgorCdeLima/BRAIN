---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/claude-desktop
tarefa: T-0001
confianca: alta
fontes: ["projetos/lab: qualidade/bugs/BUG-0001.md", "https://www.postgresql.org/support/versioning/"]
verificado_em: 2026-09-29
valido_para: "API do Docker Hub (hub.docker.com/v2/repositories/...)"
criado: 2026-09-29
decisao:
tags: [docker, versoes, pesquisa]
---
# Listagem de tags do Docker Hub é paginada - confirme a tag diretamente

## Conteúdo proposto

**Sintoma:** ao consultar as tags de uma imagem pela API do Docker Hub, a versão mais nova parece não existir (ex.: só aparece até `postgres:17`).

**Causa raiz:** a API devolve as tags em páginas; a primeira página não traz necessariamente a versão mais recente.

**Solução:** para decidir a versão atual, use a página oficial de versões do projeto (ex.: postgresql.org/support/versioning) e confirme a tag específica diretamente (`docker manifest inspect <imagem>:<tag>` ou a URL da tag na API), em vez de concluir pela ausência na listagem.

**O que não funcionou:** concluir "a 18 não existe" pela primeira página da listagem; e supor que o PostgreSQL tem versão LTS (não tem: toda versão principal tem 5 anos de suporte).

## Evidência

BUG-0001 do projeto `lab`: o Dev fixou `postgres:17.11` com essa premissa; o Revisor confirmou na página oficial e no Hub que `18.6-alpine` existia. Corrigido e verificado no VER-0002.

## Por que é reaproveitável

Qualquer tarefa que fixe versões de imagens Docker (toda stack nova) cai nessa armadilha.

## Relacionadas no Brain

- [[Imagem postgres 18+ monta o volume em var-lib-postgresql]]

## Decisão do Bibliotecário
