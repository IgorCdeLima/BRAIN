---
tipo: padrao
status: ativo
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#24)
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [seguranca, cwe, cwe-639, idor, autorizacao]
---
# CWE-639 IDOR se evita filtrando a consulta pelo dono do objeto

## Contexto

**O que e:** o usuario troca o identificador na URL ou no corpo (`/arquivos/42` vira `/arquivos/43`) e acessa objeto de outro usuario, porque o servidor confia no id recebido (Insecure Direct Object Reference).

**Como aparece na nossa stack:**
- `db.get(Arquivo, arquivo_id)` sem comparar `dono_id` com o usuario logado.
- Rotas `/uploads/{id}` e `/{recurso}/{id}` de download, edicao e exclusao.
- Achar que id sequencial "escondido" ou UUID basta.

## Solucao

**Controle:**
1. Escopar a consulta ao usuario: `select(Arquivo).where(Arquivo.id == id, Arquivo.dono_id == usuario.id)`; nao achou = 404.
2. UUID e apenas defesa extra; nao substitui a checagem.
3. Aplicar em leitura, alteracao, exclusao e exportacao.

**Como testar:** com dois usuarios, usar o id do usuario A na sessao do B, em todos os verbos HTTP.

## Evidencia

Cheat sheet OWASP (IDOR) consultado em 2026-09-30: recomenda escopar a consulta ao usuario autenticado e testar com varias contas.

## Links confiaveis

- [CWE-639 (MITRE)](https://cwe.mitre.org/data/definitions/639.html): definicao oficial.
- [IDOR Prevention Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html): controle por objeto e abordagem de teste.

## Por que e reaproveitavel

Aparece assim que o projeto tiver mais de um usuario.

## Relacionadas no Brain

- [[CWE-862 autorizacao ausente se evita checando permissao em cada rota com Depends]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-09-30) como padrao ativo: cheat sheet OWASP de IDOR lido pelo Pesquisador; sem duplicata. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
