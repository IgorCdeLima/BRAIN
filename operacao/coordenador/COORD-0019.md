---
tipo: pedido-coordenador
id: COORD-0019
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0010
criado: 2026-10-02
atendido_em: 2026-10-02
adm:
tags: [lab, t-0010, banco, erro-500, pre-existente]
---
# COORD-0019 - Encaminhar o BUG-T0010-03 (banco lento ou fora vira 500) para uma tarefa

## Pedido

- [x] Encaminhar o `qualidade/bugs/BUG-T0010-03.md` (lab, branch `T-0010-imagem-pillow`, commit `c1a17d1`) para uma tarefa: incluir na **T-0015** (limites de memoria e `restart` do `app`, que trata da mesma carga) ou criar uma tarefa propria para o Dev. Decisao de triagem do Coordenador (com o humano, se precisar).

## Motivo

No teste manual do CS-08 da T-0010, com o host em swap, o Postgres demorou a aceitar conexao (`connect_timeout: 3`) e 2 de 60 envios receberam **500** em vez do 503 de "Servidor ocupado": a pagina do 503 (e a do 422) lista os produtos do banco sem tratar erro de conexao. Reproduzido com o banco parado (`GET /` -> 500). O comportamento ja existe na `main`, por isso **nao bloqueia** a T-0010 (aprovada no VER-T0010-03). Sem tarefa, o bug fica so no branch e se perde.

---

## Atendimento

Coordenador, 2026-10-02: o humano decidiu incluir o BUG-T0010-03 na **T-0015** (o registro esta na `main` do lab pelo merge `518b7c5`). Objetivo, criterios de aceite e restricao da T-0015 atualizados; a T-0015 continua em `backlog` ate a triagem.
