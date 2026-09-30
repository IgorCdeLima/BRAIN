---
tipo: padrao
status: ativo
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org, fastapi.tiangolo.com]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#4, com CWE-863 #17 e CWE-306 #21); FastAPI atual
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [seguranca, cwe, cwe-862, cwe-863, cwe-306, autorizacao, fastapi]
---
# CWE-862 autorizacao ausente se evita checando permissao em cada rota com Depends

## Contexto

**O que e:** a rota executa a acao sem verificar se quem chama tem direito (CWE-862 Missing Authorization). Parentes: CWE-863 (checagem existe mas esta errada) e CWE-306 (funcao critica sem autenticacao). Broken Access Control e o A01 do OWASP Top 10 2025.

**Como aparece na nossa stack:**
- Rota nova criada sem `Depends(usuario_atual)`; so a rota "principal" ficou protegida.
- Checagem so no front (botao escondido) e nenhuma no endpoint.
- Rotas de administracao/listagem/exclusao esquecidas; `/docs` e `/openapi.json` expostos em producao.
- Checagem de papel feita so na primeira rota de um grupo.

## Solucao

**Controle:**
1. Negar por padrao: `APIRouter(dependencies=[Depends(exigir_login)])` no router inteiro e liberar excecoes de forma explicita.
2. Dependencia de autorizacao por papel/permissao (`Depends(exigir_papel("admin"))`), centralizada, nao copiada em cada funcao.
3. Autorizar no servidor toda vez, para toda acao (leitura, alteracao, exclusao, exportacao).
4. Teste automatizado que percorre todas as rotas e confirma 401/403 sem credencial.

**Como testar:** listar `app.routes` e chamar cada uma sem login e com usuario de papel inferior.

## Evidencia

Documentacao do FastAPI sobre seguranca com `Depends` e cheat sheet OWASP de autorizacao consultados em 2026-09-30.

## Links confiaveis

- [CWE-862 (MITRE)](https://cwe.mitre.org/data/definitions/862.html): definicao oficial (veja tambem 863 e 306 na mesma base).
- [Authorization Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): negar por padrao, checar em toda requisicao, testes.
- [FastAPI - Security](https://fastapi.tiangolo.com/tutorial/security/): esquemas de seguranca e uso de `Depends`.

## Por que e reaproveitavel

Ponto central de qualquer revisao de seguranca de API; vale para todo projeto FastAPI.

## Relacionadas no Brain

- [[CWE-639 IDOR se evita filtrando a consulta pelo dono do objeto]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-09-30) como padrao ativo: docs do FastAPI e cheat sheet OWASP de autorizacao consultados. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
