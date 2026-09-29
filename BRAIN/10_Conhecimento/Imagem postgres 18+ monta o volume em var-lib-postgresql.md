---
tipo: problema-solucao
status: ativo
origem: agente/dev (candidato da tarefa T-0001, curado pelo Bibliotecário)
confianca: alta
fontes: ["https://github.com/docker-library/docs/blob/master/postgres/content.md (seção PGDATA)", "https://github.com/docker-library/postgres/pull/1259"]
verificado_em: 2026-09-28
valido_para: imagem oficial postgres 18.x (Docker Hub); 19+ segue a mesma regra com o número da versão no caminho
revisar_em: 2027-03-28
criado: 2026-09-28
tags: [docker, postgresql]
decisao: promovido
---
# Imagem postgres 18+ monta o volume em /var/lib/postgresql, não em /var/lib/postgresql/data

## Sintoma

Após migrar para `postgres:18` (ou superior) copiando um `docker-compose.yml` antigo, o banco sobe normalmente, mas **os dados somem** quando o contêiner é recriado. O Docker cria um volume anônimo extra e o volume nomeado declarado fica vazio.

## Ambiente

Imagem oficial `postgres` 18.x (testado com `postgres:18.6-alpine`) usada via Docker Compose.

## Causa raiz

A partir do PostgreSQL 18 a imagem oficial mudou o `PGDATA` para `/var/lib/postgresql/18/docker` (o número da versão faz parte do caminho) e o `VOLUME` declarado passou a ser `/var/lib/postgresql`. Montar o volume em `/var/lib/postgresql/data`, como até a versão 17, não cobre mais o diretório de dados real.

## Solução

Montar o volume no diretório pai:

```yaml
volumes:
  - dados:/var/lib/postgresql
```

## Como verificar que foi resolvido

- O contêiner do banco fica saudável e a aplicação conecta.
- Recriar o contêiner (`docker compose down` sem `-v`, depois `up`) mantém os dados.
- `docker volume ls` não mostra volume anônimo novo a cada `up`.

## O que não funcionou

Manter `dados:/var/lib/postgresql/data` (padrão até a 17): não dá erro visível, mas não persiste nada.

## Origem

Tarefa T-0001, projeto `lab`. Aplicado e validado ali; a regra vem da documentação oficial da imagem (seção `PGDATA`, "Important Change"). Exemplos da internet ainda usam o caminho antigo, por isso o risco de reincidência é alto.

## Decisão do Bibliotecário

**Promovido** em 2026-09-28. Sem duplicata (o Brain não tinha nota de Docker/PostgreSQL). Evidência forte: documentação oficial e validação prática na T-0001. Reescrito no template `Problema-Solucao`, com `revisar_em` por ser fato volátil de versão. Relacionada: [[TestClient do Starlette 1.x prefere httpx2 a httpx]] (mesma origem, T-0001; sem dependência técnica entre as duas).
