---
tipo: candidato
origem: T-0015 (BUG-T0010-03)
status: arquivado
decisao: fundido em [[Pagina de 503 que consulta o banco vira 500 justamente quando o servidor esta sobrecarregado]]
tags: [fastapi, sqlalchemy, disponibilidade, erro-500]
---
# Pagina de erro (422/503) que lista dados do banco vira 500 se o banco cair

- **Causa raiz:** a pagina compartilhada (`_pagina`) sempre consultava o banco, inclusive ao responder erro de validacao e "servidor ocupado". Premissa errada: "se chegou ao tratamento de erro, o banco esta de pe". Sob pressao de memoria o Postgres paginou e o `connect_timeout` estourou.
- **Correcao validada:** capturar `sqlalchemy.exc.OperationalError` na consulta da lista, fazer `rollback`, renderizar com lista vazia + aviso e manter o status original (422/503); `GET /` vira 503. Commit com banco fora: remover o arquivo ja gravado e responder 503.
- **Teste:** `monkeypatch` de `sessao.scalars`/`commit` levantando `OperationalError`; nao precisa parar o banco.
- **Compose:** `mem_limit`, `cpus`, `pids_limit`, `cap_drop: [ALL]` e `no-new-privileges` no `app` nao quebraram health nem upload (porta interna 8000).

## Decisao do Bibliotecario

Fundido (2026-10-03) em [[Pagina de 503 que consulta o banco vira 500 justamente quando o servidor esta sobrecarregado]]: mesma causa raiz (BUG-T0010-03), so acrescentou a correcao validada e o teste com monkeypatch, ja incorporados. O item de Compose ja esta coberto por outras notas. Arquivado, nao apagado.
