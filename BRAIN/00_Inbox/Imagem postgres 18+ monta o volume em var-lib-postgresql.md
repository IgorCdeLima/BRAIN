---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/dev
tarefa: T-0001
confianca: alta
fontes: ["https://github.com/docker-library/docs/blob/master/postgres/content.md (seção PGDATA)", "https://github.com/docker-library/postgres/pull/1259"]
verificado_em: 2026-09-28
valido_para: imagem oficial postgres 18.x (Docker Hub); 19+ segue a mesma regra com outro número
criado: 2026-09-28
decisao:
tags: [docker, postgresql]
---
# Imagem postgres 18+ monta o volume em /var/lib/postgresql, não em /var/lib/postgresql/data

## Conteúdo proposto

A partir do PostgreSQL 18, a imagem oficial `postgres` mudou `PGDATA` para `/var/lib/postgresql/18/docker` e o `VOLUME` declarado para `/var/lib/postgresql`. No Compose, o volume de dados deve ser montado assim:

```yaml
volumes:
  - dados:/var/lib/postgresql
```

Até a versão 17, o caminho era `/var/lib/postgresql/data`. Copiar um exemplo antigo para a 18 faz o Docker criar um volume anônimo e os dados **não persistem** ao recriar o contêiner.

## Evidência

Documentação oficial da imagem (seção `PGDATA`, "Important Change"). Aplicado no projeto lab (T-0001) com `postgres:18.6-alpine`: banco sobe saudável e a aplicação conecta.

## Por que é reaproveitável

Qualquer projeto do ambiente que use PostgreSQL em Docker; exemplos da internet quase sempre usam o caminho antigo.

## Relacionadas no Brain

- (nenhuma nota sobre Docker/PostgreSQL no Brain em 2026-09-28)

## Decisão do Bibliotecário
