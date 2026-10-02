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

## Como verificar que foi resolvido

Ao revisar load shedding, limite de concorrencia ou rate limit: parar o banco (`docker compose stop db`) e pedir `GET /` e um `POST` invalido. O esperado e 503 (nunca 500).

## O que nao funcionou

Confiar so no teste de carga num host folgado: ele nao reproduz a lentidao do banco.

## Relacionadas

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: o mecanismo de limite cuja resposta de erro precisa ser testada.
- [[Semaforo dentro de rota def do FastAPI prende o threadpool e trava as outras rotas]]: o limite de concorrencia que gera esse 503.
- [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]]: o mesmo teste de carga mostrou o pico de memoria estavel; o 500 veio so da consulta da pagina de erro.

## Origem

T-0010 (lab): 6 rodadas de 10 envios paralelos de WebP 50 MP; numa rodada, 2 x 500 em `_pagina`, chamada pelo 503 da fila de imagem. Reproduzido de forma deterministica com o banco parado. Registrado em BUG-T0010-03 / VER-T0010-03.

## Decisao do Bibliotecario

Promovido (2026-10-02). Sem duplicata. Serve de lembrete ao Revisor e a Seguranca: testar a resposta de erro com a dependencia indisponivel.
