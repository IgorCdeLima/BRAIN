---
tipo: problema-solucao
status: ativo
origem: T-0002 (curado pelo Bibliotecário a partir do candidato "Parser de valor monetário pt-BR")
confianca: alta
fontes: ["projetos/lab: T-0002, BUG-0003 a BUG-0005"]
verificado_em: 2026-09-29
valido_para: projetos com Docker Compose cuja imagem copia o código (COPY) em vez de montar volume
criado: 2026-09-29
tags: [docker, pytest, ambiente, armadilha]
decisao: promovido
---
# Imagem Docker que embute o código exige build antes de rodar pytest

## Sintoma

Depois de editar o código, `docker compose run --rm app pytest` roda a suíte antiga e o resultado não reflete a correção.

## Ambiente

Docker Compose com imagem da aplicação que copia o código no build (projeto `lab`).

## Causa raiz

O código está dentro da imagem; sem novo build, o contêiner usa a versão anterior.

## Solução

Rodar `docker compose build app` antes de `docker compose run --rm app pytest`.

## Como verificar que foi resolvido

O teste novo (ou a correção) aparece na execução; um teste que deveria falhar falha.

## O que não funcionou

Rodar só `run --rm app pytest` após editar.

## Vale tambem para os servicos lint, audit e test do Compose

Confirmado por experimento na T-0009 (copia descartavel; Docker 29.1.3, python:3.13.15-slim, pip 26.2.1):

- `audit`: com `urllib3==1.26.18` acrescentado ao `requirements-dev.txt`, `docker compose run --rm audit` sem `--build` diz "No known vulnerabilities found" (exit 0, imagem velha); com `--build` acusa o urllib3 (exit 1).
- `test`: mensagem de erro trocada em `app/imagens.py`; `run --rm test` sem `--build` passa 76 testes (codigo velho); com `--build` falha (exit 1).
- Regra: nos servicos que usam imagem construida, rodar `docker compose run --build --rm test|lint|audit`. O `up -d --build` so reconstroi os servicos que sobe, nao os do profile de verificacao.
- Armadilha de experimento: `urllib3==1.26.0` quebra o proprio pip-audit no Python 3.13 (`ModuleNotFoundError: urllib3.packages.six.moves`, exit 1 sem relatar vulnerabilidade). Use 1.26.18.
- Fonte: experimento na T-0009 (VER-0009 e VER-0010 levantaram a observacao O1). Documentacao da opcao `--build`: [Docker: docker compose run](https://docs.docker.com/reference/cli/docker/compose/run/) (nao aberta nesta curadoria; a prova e o experimento).

Relacionada: [[ruff e pip-audit em Docker Compose com servicos lint e audit no estagio dev]] (os servicos afetados).

## Origem

T-0002 do `lab`; ampliada em 2026-10-01 com o experimento da T-0009. Vale para Dev e Revisor ao verificar correções. Relacionada: [[Valor em reais com ponto de milhar sem virgula e ambiguo - nao converta direto para Decimal]] (bugs cuja verificação depende disso).

## Decisão do Bibliotecário

Criada em 2026-09-29 a partir do candidato do parser monetário. Sem fonte externa: é comportamento do próprio projeto.
