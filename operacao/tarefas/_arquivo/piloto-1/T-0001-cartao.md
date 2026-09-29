---
tipo: tarefa
id: T-0001
status: revisao
projeto: lab
papel: dev
tamanho: normal
criado: 2026-09-28
tags: [lab, fase-1, piloto]
---
# T-0001 — Esqueleto da aplicação com FastAPI e PostgreSQL no Docker

<!-- Rascunho preparado para aprovação do humano. Ao aprovar, mudar status para "pronta". -->

## Objetivo

Ter a aplicação mínima rodando no Docker Compose, conectada ao PostgreSQL, com verificação de saúde e testes automatizados — a base para as próximas tarefas.

## Contexto

- Projeto: `D:\01_IA\projetos\lab` (ler `CLAUDE.md`).
- Stack: `docs/adr/ADR-0001 Stack do projeto.md`.
- Requisito: RF-01 e RNF-01 a RNF-03 em `docs/requisitos/requisitos.md`.
- Modelos: `docs/modelos/modelos.md` (containers).

## Critérios de aceite

- [x] `docker compose up -d --build` sobe os serviços `app` e `db`; a aplicação responde em `http://localhost:8000`.
- [x] O serviço `db` tem healthcheck e o `app` só inicia depois que o banco está saudável.
- [x] `GET /health` retorna `200` com `{"status": "ok", "banco": "ok"}` quando o banco responde, e `503` quando não responde.
- [x] `GET /` retorna uma página HTML (Jinja2) com o título "Cadastro de produtos" (conteúdo provisório).
- [x] `docker compose run --rm app pytest` passa, com pelo menos: saúde OK, saúde com banco indisponível, página inicial.
- [x] Configuração por variáveis de ambiente; `.env.example` lista todas. O Compose funciona **sem** `.env`, usando valores padrão **apenas para desenvolvimento local**, marcados como tal.
- [x] Versões fixadas em `requirements.txt` e nas imagens Docker, escolhidas após consultar a documentação oficial (registrar na Entrega quais versões e onde verificou).
- [x] `README.md` do projeto atualizado com como subir e testar.

## Restrições / o que NÃO fazer

- Não implementar cadastro de produtos (é a T-0002).
- Não criar nem ler `.env` (bloqueado por permissão); usar `.env.example` e valores padrão de desenvolvimento.
- Não usar `docker compose down -v`.
- Não alterar `CLAUDE.md`, `.claude/`, `.githooks/` nem `qualidade/`. Se algo neles estiver errado, anotar em "Dúvidas em aberto".

## Verificações obrigatórias

- [x] Testes automáticos passam
- [x] Critérios de aceite atendidos
- [ ] Revisão de código (humano)
- [x] Revisão de segurança leve: nenhum segredo real versionado; valores padrão só de desenvolvimento

---

## Entrega

- **Worktree / branch:** `C:/Users/igorc/orca/workspaces/lab/T-0001-esqueleto` / `T-0001-esqueleto`
- **Commits:**
  - `5bcdda7` feat(app): esqueleto FastAPI com verificação de saúde e página inicial
  - `0532225` chore(docker): Compose com app e PostgreSQL, healthcheck e configuração por ambiente
  - `bcd65e8` fix(app): /health responde 503 quando a configuração do banco está incompleta — ações A1 e A2 do VER-0001 (a verificação precisa ser refeita sobre este commit). A3 (separar dependências de teste da imagem) e A4 (ruff + pip-audit) não foram feitas: aguardam decisão do humano, sugeridas como tarefa futura.
- **Decisões tomadas:**
  - Versões (consultadas em 2026-09-28): imagens `python:3.14.7-slim-trixie` e `postgres:18.6-alpine` (Docker Hub; ciclo de versões conferido em endoflife.date — Python 3.15 e PostgreSQL 19 ainda em RC/beta, descartados). Pacotes no PyPI (API JSON): fastapi 0.141.1, uvicorn 0.54.0, jinja2 3.1.6, sqlalchemy 2.1.1, psycopg[binary] 3.3.6, pytest 9.1.1, httpx2 2.13.1.
  - `httpx2` no lugar de `httpx`: o Starlette 1.7.0 (dependência do FastAPI) emite aviso de depreciação com `httpx` e importa `httpx2` primeiro.
  - PostgreSQL 18: volume montado em `/var/lib/postgresql` (mudança da imagem oficial a partir da 18; o caminho antigo `.../data` não persistiria os dados).
  - A aplicação usa as mesmas variáveis `POSTGRES_*` do serviço `db` e monta a URL com `sqlalchemy.URL.create` (senha com caracteres especiais não quebra a URL). `POSTGRES_PASSWORD` não tem padrão no código; os padrões de dev ficam só no `docker-compose.yml`, comentados como "apenas para desenvolvimento local".
  - Porta do banco não publicada na máquina; contêiner da app roda com usuário sem privilégios.
  - `/health` com timeout de conexão de 3 s; em falha retorna `503 {"status": "erro", "banco": "indisponivel"}` e registra o erro no log sem expor detalhes na resposta.
  - Os testes de indisponibilidade alteram as variáveis de ambiente (fixture `ambiente`, via `monkeypatch`) e recriam config e engine: banco em `127.0.0.1:1` (falha de conexão verdadeira, sem mock) e `POSTGRES_PASSWORD` ausente. Desde `bcd65e8`, `/health` obtém o engine dentro do `try` em vez de recebê-lo por `Depends`.
  - Sem bind mount do código: o README orienta `docker compose run --rm --build app pytest` para testar a versão atual.
  - Pytest com `-p no:cacheprovider` (o usuário do contêiner não escreve em `/app`).
- **Dúvidas em aberto:**
  - O cartão estava com `status: backlog` (rascunho aguardando aprovação); executei porque o humano pediu diretamente "Execute a tarefa T-0001".
  - A sessão não foi iniciada pelo Quick Command `Dev` (`IA_PAPEL` vazio, modelo Opus em vez de Sonnet, perfil `dev.json` não carregado). Defini `IA_PAPEL=dev` e `IA_MODELO=claude-opus-5-5` só nos comandos de commit, para os trailers saírem corretos. Vale conferir se o Orca está usando o Quick Command.
  - Os testes rodam no mesmo banco da aplicação. Na T-0002 (com tabelas) provavelmente convém um banco de teste separado ou transações com rollback.
  - O modelo de containers já mostra o volume de uploads, que só entra na T-0003 — não criei o volume agora.
  - Só as dependências diretas estão fixadas; um lock das transitivas (ex.: `pip-tools`) pode virar tarefa futura.
- **Verificações feitas:**
  - `docker compose up -d --build`: `db` fica `healthy` e o `app` só inicia depois (visto na saída do Compose); `http://localhost:8000` responde.
  - `curl /health` → `200 {"status":"ok","banco":"ok"}`; com `docker compose stop db` → `503` em ~3,5 s; após `start db` volta a `200`.
  - `curl /` → HTML com `<title>Cadastro de produtos</title>`.
  - `docker compose run --rm app pytest` e `docker compose run --rm --build app pytest` → 3 passed, sem avisos. Após `bcd65e8`: `docker compose run --rm --build app pytest` → 4 passed (inclui configuração incompleta → 503); antes da correção, reproduzido `500` com `POSTGRES_USER` vazio. `docker compose up -d --build` e `/health` → 200.
  - Compose funciona sem `.env` (não existe `.env` no worktree).
  - Segurança leve: busca por `password|senha|secret|token` no repositório — só `.env.example` (valor ilustrativo), padrões de dev marcados no Compose e credenciais falsas no teste; o log da app não contém a senha.
- **Verificações NÃO feitas (e por quê):**
  - Lint/formatação (exigido pela matriz): `ruff` não está instalado na máquina nem no projeto; não adicionei ferramenta fora do escopo.
  - Revisão de código: cabe ao humano/revisor.
  - Execução em outra máquina/SO além deste Windows com Docker Desktop.
  - Varredura de vulnerabilidades das dependências e imagens (ex.: `pip-audit`, `docker scout`): fora do escopo e sem ferramenta configurada.
- **Candidatos a conhecimento:**
  - `BRAIN/00_Inbox/Imagem postgres 18+ monta o volume em var-lib-postgresql.md`
  - `BRAIN/00_Inbox/TestClient do Starlette 1.x prefere httpx2 a httpx.md`

## Revisão

- **VER:**
- **Resultado:**
- **Merge:**
