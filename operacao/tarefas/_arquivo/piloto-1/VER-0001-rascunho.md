---
tipo: verificacao
id: VER-0001
tarefa: T-0001
commit: 0532225
verificado_por: Claude, sessão sem papel (IA_PAPEL vazio), a pedido do humano
modelo: claude-opus-5-5
data: 2026-09-28
resultado: <!-- A PREENCHER pelo humano: aprovado | reprovado | parcial (recomendação do verificador: aprovado, com as ações abaixo) -->
tags: [lab, fase-1]
---
# VER-0001 — Esqueleto FastAPI + PostgreSQL no Docker (T-0001)

Verificação independente do diff `3da20d5..0532225` (branch `T-0001-esqueleto`), feita numa sessão diferente da do Dev. As evidências abaixo foram reproduzidas pelo verificador; o que é apenas declarado pelo Dev está indicado como tal.

## Resumo para o Dev

**Nenhuma mudança de código é obrigatória para aprovar a T-0001.** Há três ações recomendadas (A1–A3, na seção "Ações para o Dev"). O humano decide se entram ainda nesta tarefa, antes do merge, ou numa tarefa futura.

## O que foi verificado

| Verificação | Obrigatória | Resultado | Evidência |
|---|---|---|---|
| Testes automáticos | sim | passou | `docker compose run --rm app pytest` → `3 passed in 0.30s` (saúde OK, saúde com banco indisponível, página inicial). A imagem usada contém exatamente o código do commit `0532225`: hash comparado em 10 arquivos (`app/*`, `tests/*`, templates, `requirements.txt`, `pyproject.toml`), ignorando CRLF. |
| Lint | sim | não feito | Nenhum linter configurado no projeto (ver lacunas e A4). |
| Revisão de código | sim | aprovado com observações | Diff inteiro lido (17 arquivos). Código simples e legível; configuração por ambiente; URL do banco montada com `URL.create`; timeout de conexão de 3 s; erro do banco registrado no log sem expor detalhes na resposta; teste de indisponibilidade com falha de conexão real. Observações em A1–A3. |
| Revisão de segurança | sim (segredos/configuração, rede, dependências) | passou | `git grep -iE 'password\|senha\|secret\|token\|api_key'` no commit: só `.env.example` (valor ilustrativo), padrões de dev marcados no `docker-compose.yml` e credenciais falsas no teste. `.env` e `.env.*` no `.gitignore` e no `.dockerignore`. A senha padrão não aparece em `docker compose logs app`. Porta 5432 do banco não publicada na máquina. Processo da app roda como `uid=10001(lab)`. |
| Critérios de aceite atendidos | sim | passou | Com o contêiner recriado a partir da imagem atual: `GET /health` → `200 {"status":"ok","banco":"ok"}`; após `docker compose stop db` → `503 {"status":"erro","banco":"indisponivel"}` em 3,34 s; após `start db` e healthcheck → `200`. `GET /` → HTML com `<title>Cadastro de produtos</title>` e `<h1>` correspondente. Healthcheck do `db` presente (`pg_isready`, 5 s/3 s/10 tentativas) e `app` com `depends_on: db: service_healthy`. Sem `.env` no worktree, o Compose sobe com os padrões de dev. README descreve subir, testar, configuração e versões. |
| Versões fixadas | sim (critério de aceite) | passou | No contêiner: Python 3.14.7, PostgreSQL 18.6; `pip freeze` confere com `requirements.txt` (fastapi 0.141.1, uvicorn 0.54.0, jinja2 3.1.6, sqlalchemy 2.1.1, psycopg 3.3.6, pytest 9.1.1, httpx2 2.13.1) e com o README. A consulta às fontes oficiais em 2026-09-28 é **declarada pelo Dev**, não refeita. |
| Diagramas coerentes com o código | não (modelo não mudou) | não se aplica | O diagrama de containers já prevê o volume de uploads, que entra na T-0003. |

## O que NÃO foi verificado

- **Build do zero** (`docker compose up -d --build` / `run --build`): falhou por falha de rede do verificador (`TLS handshake timeout` em `auth.docker.io`). Não foi confirmado que as tags `python:3.14.7-slim-trixie` e `postgres:18.6-alpine` são baixadas numa máquina limpa; os testes usaram a imagem já construída, conferida contra o commit.
- **Lint/formatação**: sem ferramenta no projeto.
- **Varredura de vulnerabilidades** das dependências e imagens (`pip-audit`, `docker scout`): sem ferramenta configurada.
- **Outra máquina/SO**: só este Windows com Docker Desktop.
- **Dependências transitivas**: não fixadas (só as diretas); não avaliadas.
- **Isolamento dos testes**: rodam no mesmo banco da aplicação. Sem impacto na T-0001 (não cria tabelas), mas relevante a partir da T-0002.
- **Persistência do volume** do PostgreSQL 18 em `/var/lib/postgresql` após `down`/`up`: não testada.

## Ações para o Dev

Nenhuma é bloqueante. Se o humano pedir a correção nesta tarefa, o Dev faz um novo commit no worktree `T-0001-esqueleto` e a verificação é refeita (quem corrige não verifica).

| # | Tipo | Arquivo | O que mudar | Por quê |
|---|---|---|---|---|
| A1 | código + teste | `app/main.py:22-27` (e `app/config.py:30-33`) | Fazer `/health` responder `503` também quando a configuração do banco está incompleta. Hoje, sem `POSTGRES_USER`/`POSTGRES_PASSWORD`/`POSTGRES_DB`, `obter_config()` lança `RuntimeError` dentro da dependência `obter_engine` e a rota responde **500**, pois o `except SQLAlchemyError` não o captura. Sugestão: obter o engine dentro do `try` (ou capturar também `RuntimeError`) e registrar no log. Adicionar teste: variável obrigatória ausente → `503`. | Verificação de saúde deve sinalizar "indisponível", não quebrar. Fora dos critérios da T-0001, por isso não bloqueia. |
| A2 | documentação | `README.md`, seção "Testar" | Deixar claro que `docker compose run --rm --build app pytest` reconstrói a imagem, mas **não** atualiza o contêiner `app` em execução; para a aplicação rodando refletir o código novo, usar `docker compose up -d --build`. | Na verificação, o `app` em execução estava numa imagem anterior à testada, e `docker compose up -d` sem `--build` não o recriou (foi preciso `--force-recreate`). |
| A3 | Dockerfile | `Dockerfile:14-15`, `requirements.txt` | Opcional: separar dependências de teste (`pytest`, `httpx2`) e não copiar `tests/` para a imagem de runtime (ex.: `requirements-dev.txt` + estágio ou alvo de teste). | Imagem de execução leva código e ferramentas de teste. Aceitável no laboratório; relevante se houver deploy. Pode virar tarefa futura. |
| A4 | tarefa futura | — | Adicionar `ruff` (lint/formatação) e uma varredura de dependências (`pip-audit`). | Fecha duas lacunas obrigatórias desta verificação. |

## Achados

- Nenhum BUG/SEC registrado. A1 é candidato a `BUG-` se o humano preferir tratá-lo como defeito em vez de ajuste nesta tarefa.
- Processo: a sessão do Dev não foi iniciada pelo Quick Command `Dev` (`IA_PAPEL` vazio, perfil `dev.json` não carregado); os trailers foram definidos manualmente nos commits.
- Processo: o rascunho deste VER foi criado pelo Dev em `qualidade/verificacoes/`, embora o cartão proíba alterar `qualidade/` (o arquivo não foi commitado).
- Processo: esta verificação também foi feita por sessão sem papel (não pelo Quick Command `Revisor`), a pedido do humano.
