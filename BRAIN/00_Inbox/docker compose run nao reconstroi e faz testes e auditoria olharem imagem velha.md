---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/engenheiro
tarefa: T-0006
pesquisa:
confianca: baixa
fontes: ["projetos/lab: VER-0009, VER-0010 (observacao O1)", "projetos/lab: docker-compose.yml e Dockerfile (servico test copia app/ na imagem)"]
verificado_em: 2026-09-30
valido_para: "Docker Compose com servicos run que usam imagem construida (test, lint, audit)"
criado: 2026-09-30
decisao:
tags: [docker, compose, testes, pip-audit, armadilha, proposta-n4]
---
# docker compose run nao reconstroi e faz testes e auditoria olharem imagem velha

## Conteudo proposto

**Sintoma (esperado, ainda nao reproduzido):** depois de mudar `requirements*.txt` ou o codigo de `app/`, `docker compose run --rm audit` continua "limpo" e `docker compose run --rm test` continua passando, porque o `run` usa a imagem que ja existe.

**Causa:** no lab, o servico `test` so monta `tests/` por volume; `app/` e as dependencias estao **dentro** da imagem `dev`. O `up -d --build` reconstroi so os servicos que sobe (`app`, `db`), nao os do profile `test`. E o mesmo problema da nota [[Imagem Docker que embute o codigo exige build antes de rodar pytest]], que nao foi aplicado aos servicos novos da T-0004/T-0005.

**Solucao proposta (M6):**

- Comandos documentados com `docker compose run --build --rm test|lint|audit`.
- O Revisor pode fazer experimentos numa copia descartavel no scratchpad (o VER-0009 nao reproduziu a O1 porque a alteracao da copia foi negada). Area N4: perfil do Revisor.
- Sugestao ao Bibliotecario: **fundir** com a nota existente depois que a T-0009 confirmar (Parte 1 do cartao tem o roteiro).

## Evidencia

Observacao O1 do VER-0009 e do VER-0010 (baseada no comportamento documentado do Compose, nao reproduzida). Leitura do `docker-compose.yml` e do `Dockerfile` do lab na T-0006. Confianca baixa ate a T-0009.

## Links confiaveis

- [Docker: docker compose run](https://docs.docker.com/reference/cli/docker/compose/run/): opcao `--build` (nao aberto nesta tarefa; conferir na T-0009).

## Por que e reaproveitavel

Todo projeto com servicos de verificacao no Compose sobre imagem que embute codigo ou dependencias.

## Relacionadas no Brain

- [[Imagem Docker que embute o codigo exige build antes de rodar pytest]]
- [[ruff e pip-audit em Docker Compose com servicos lint e audit no estagio dev]]

## Decisao do Bibliotecario

**Devolvido** (2026-09-30): fica no Inbox. Sintoma nao reproduzido (confianca baixa) e a propria nota pede esperar a T-0009 (status `pronta`). Quando a T-0009 confirmar, **fundir** em [[Imagem Docker que embute o codigo exige build antes de rodar pytest]] (servicos test, lint e audit, opcao `--build`), conferindo o link da doc do Docker. Nao promovido: sem evidencia.
