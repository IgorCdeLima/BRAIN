---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/dev
tarefa: T-0001
confianca: media
fontes: ["https://pypi.org/project/httpx2/", "https://github.com/pydantic/httpx2", "código de starlette/testclient.py na versão 1.7.0"]
verificado_em: 2026-09-28
valido_para: starlette 1.7.0 (via fastapi 0.141.1); httpx2 2.13.1
criado: 2026-09-28
decisao:
tags: [python, fastapi, testes]
---
# TestClient do Starlette 1.x prefere httpx2 a httpx

## Conteúdo proposto

Em projetos FastAPI, instale `httpx2` (não `httpx`) como dependência de teste. O `starlette.testclient` (usado por `fastapi.testclient.TestClient`) importa `httpx2` primeiro; com apenas `httpx` instalado, funciona mas emite `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead`. Sem nenhum dos dois, falha com `RuntimeError`.

O `httpx2` é publicado pela Pydantic (github.com/pydantic/httpx2).

## Evidência

Aviso reproduzido no projeto lab (T-0001) com fastapi 0.141.1 / starlette 1.7.0 e httpx 0.28.1; após trocar por `httpx2==2.13.1` os testes passam sem avisos. Trecho conferido no fonte do `starlette/testclient.py` instalado.

## Por que é reaproveitável

Todo projeto FastAPI/Starlette novo do ambiente. Tutoriais e o próprio conhecimento de modelos ainda indicam `httpx`.

## Relacionadas no Brain

- (nenhuma)

## Decisão do Bibliotecário
