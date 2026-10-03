---
tipo: problema-solucao
status: ativo
origem: T-0010 (Revisor, BUG-T0010-03), curado pelo Bibliotecario
tarefa: T-0010
confianca: media
fontes: ["lab qualidade/bugs/BUG-T0010-03.md", "lab qualidade/verificacoes/VER-T0010-03.md"]
verificado_em: 2026-10-02
valido_para: "FastAPI + SQLAlchemy + psycopg (lab), Docker Compose em host pequeno"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [qualidade, disponibilidade, erro-500, banco, carga, revisao]
---
# Pagina de 503 que consulta o banco vira 500 justamente quando o servidor esta sobrecarregado

## Sintoma

Sob carga, a resposta de "servidor ocupado" (503) ou de validacao (422) vira **500** com `psycopg.errors.ConnectionTimeout`. O teste "nenhum 500 sob carga" passa num host folgado e falha num pequeno.

## Ambiente

FastAPI + SQLAlchemy + psycopg, Docker Compose em host de 3,4 GB com swap quase cheio (lab).

## Causa raiz

A resposta de erro renderiza a mesma pagina completa, que consulta o banco. Sob carga o banco fica lento (ou paginado para o swap), a conexao estoura o `connect_timeout` e a pagina de erro falha exatamente quando deveria proteger o servidor.

## Solucao

- Tratar erro de conexao do banco com um handler global que mostre uma pagina de indisponibilidade **sem consulta** ([[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]] tem o desenho do handler global).
- Fazer o caminho do 503 (e do 422) nao depender do banco nem de outro recurso disputado.
- Correcao validada na T-0015 (lab): na pagina compartilhada, capturar `sqlalchemy.exc.OperationalError` na consulta da lista, fazer `rollback` e renderizar com lista vazia mais um aviso, **mantendo o status original** (422/503); `GET /` vira 503. Num commit com o banco fora, remover o arquivo ja gravado e responder 503. A premissa errada era "se chegou ao tratamento de erro, o banco esta de pe".
- Para a consulta nao ficar presa ate o handler agir, limite-a no servidor: [[statement_timeout via connect_args options cobre lock mas nao banco congelado]].

## Como verificar que foi resolvido

Ao revisar load shedding, limite de concorrencia ou rate limit: parar o banco (`docker compose stop db`) e pedir `GET /` e um `POST` invalido. O esperado e 503 (nunca 500). Teste automatico sem parar o banco: `monkeypatch` de `sessao.scalars`/`commit` levantando `OperationalError`.

## O que nao funcionou

Confiar so no teste de carga num host folgado: ele nao reproduz a lentidao do banco.

## Relacionadas

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: o mecanismo de limite cuja resposta de erro precisa ser testada.
- [[Semaforo dentro de rota def do FastAPI prende o threadpool e trava as outras rotas]]: o limite de concorrencia que gera esse 503.
- [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]]: o mesmo teste de carga mostrou o pico de memoria estavel; o 500 veio so da consulta da pagina de erro.

## Origem

T-0010 (lab): 6 rodadas de 10 envios paralelos de WebP 50 MP; numa rodada, 2 x 500 em `_pagina`, chamada pelo 503 da fila de imagem. Reproduzido de forma deterministica com o banco parado. Registrado em BUG-T0010-03 / VER-T0010-03.

## Decisao do Bibliotecario

Promovido (2026-10-02). Sem duplicata. Fundido em 2026-10-03 o candidato da T-0015 (correcao validada e teste com monkeypatch; arquivado em `90_Arquivo`). O trecho do candidato sobre `mem_limit`, `cpus`, `pids_limit`, `cap_drop` e `no-new-privileges` nao quebrarem health nem upload ficou fora: ja coberto por [[USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid]] e [[mem_limit sem memswap_limit nao e teto de memoria - o container usa X de RAM mais X de swap]]. Serve de lembrete ao Revisor e a Seguranca: testar a resposta de erro com a dependencia indisponivel.
