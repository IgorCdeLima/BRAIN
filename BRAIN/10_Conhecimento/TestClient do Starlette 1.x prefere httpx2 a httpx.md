---
tipo: problema-solucao
status: ativo
origem: agente/dev (candidato da tarefa T-0001, curado pelo Bibliotecário)
confianca: media
fontes: ["https://pypi.org/project/httpx2/", "https://github.com/pydantic/httpx2", "código de starlette/testclient.py na versão 1.7.0"]
verificado_em: 2026-09-28
valido_para: starlette 1.7.0 (via fastapi 0.141.1); httpx2 2.13.1
revisar_em: 2026-12-28
criado: 2026-09-28
tags: [python, fastapi, testes]
decisao: promovido
---
# TestClient do Starlette 1.x prefere httpx2 a httpx

## Sintoma

Ao rodar testes com `fastapi.testclient.TestClient` tendo só `httpx` instalado, aparece:

`StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead`

Sem nenhum dos dois pacotes, o `TestClient` falha com `RuntimeError`.

## Ambiente

fastapi 0.141.1, starlette 1.7.0, httpx 0.28.1 (com aviso) e httpx2 2.13.1 (sem aviso).

## Causa raiz

O `starlette.testclient` tenta importar `httpx2` primeiro e só cai para `httpx` como alternativa obsoleta. O `httpx2` é publicado pela Pydantic (github.com/pydantic/httpx2). Tutoriais e o conhecimento embutido em modelos ainda recomendam `httpx`.

## Solução

Declarar `httpx2` (e não `httpx`) como dependência de teste em projetos FastAPI/Starlette 1.x, por exemplo `httpx2==2.13.1`.

## Como verificar que foi resolvido

Rodar a suíte de testes: passa sem `StarletteDeprecationWarning`.

## O que não funcionou

Manter `httpx`: os testes passam, mas com aviso de depreciação, e a alternativa pode ser removida em versão futura do Starlette.

## Origem

Tarefa T-0001, projeto `lab`. Aviso reproduzido e resolvido ali; trecho conferido no fonte instalado de `starlette/testclient.py`. Confiança **média**: a evidência é de um único projeto e a fonte do `httpx2` é recente; revisar quando o Starlette ou o `httpx2` mudarem de versão.

## Decisão do Bibliotecário

**Promovido** em 2026-09-28. Sem duplicata no Brain. Reescrito no template `Problema-Solucao`, mantida a confiança média do candidato e `revisar_em` curto por ser fato volátil de versão. Relacionada: [[Imagem postgres 18+ monta o volume em var-lib-postgresql]] (mesma origem, T-0001; sem dependência técnica).
