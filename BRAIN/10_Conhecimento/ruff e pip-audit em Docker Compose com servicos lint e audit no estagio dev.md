---
tipo: padrao
status: ativo
origem: T-0005 (Dev), curado pelo Bibliotecario
tarefa: T-0005
confianca: media
fontes: ["https://pypi.org/project/ruff/", "https://pypi.org/project/pip-audit/"]
verificado_em: 2026-09-30
valido_para: ruff 0.16.9, pip-audit 2.10.1, python 3.13, Docker Compose com estagio dev
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [lab, qualidade, ruff, pip-audit, docker]
---
# Lint e auditoria de dependencias entram como servicos do Compose sobre o estagio dev

## Contexto

Projeto Python do lab com Dockerfile multi-estagio (`dev` e `runtime`) e Docker Compose.

## Solucao

- `ruff` e `pip-audit` so em `requirements-dev.txt` (versoes fixas); a imagem `runtime` nao os leva.
- Servico `lint` (`ruff check .`): monta `./app`, `./tests` e `./pyproject.toml` por volume, em `/code`, porque a imagem nao leva `tests/` nem `pyproject.toml`. Sem montar `./app`, o lint olharia codigo velho da imagem.
- Servico `audit` (`pip-audit`): sem argumentos, audita o ambiente instalado (nao o `requirements.txt`), o que evita o falso positivo de dependencia indireta descrito em [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]].
- Ambos com `profiles: ["test"]`, para nao subirem com `docker compose up`.
- Ruff com `select = ["E","W","F","I","B","UP"]` e `line-length = 110`: com 100 havia 6 linhas longas no codigo existente; 110 evitou reformatar codigo so para o lint passar.

## Evidencia

Lab, 2026-09-30: `docker compose run --rm lint` -> "All checks passed!" (antes: 7 erros, 6 E501 e 1 UP017, este corrigido em `tests/test_produtos.py`); `docker compose run --rm audit` -> "No known vulnerabilities found"; `pip list` na imagem runtime sem ruff/pip-audit/pytest; 76 testes passando.

Resultado negativo: o papel `dev` nao pode editar o `CLAUDE.md` do projeto (hook de commit recusa), entao a documentacao do comando novo ficou no README e a linha do CLAUDE.md foi para o humano.

## Links confiaveis

- [ruff no PyPI](https://pypi.org/project/ruff/): ultima versao publicada.
- [pip-audit no PyPI](https://pypi.org/project/pip-audit/): ultima versao publicada.

## Por que e reaproveitavel

Qualquer projeto Python do ambiente com Dockerfile multi-estagio pode copiar o desenho.

## Relacionadas no Brain

- [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]]
- [[Fontes de referencia para analise de seguranca por CWE e dependencias]]

## Decisao do Bibliotecario

Promovido (2026-09-30) como padrao ativo: resultado medido no lab (lint limpo, 76 testes, audit limpo, imagem runtime sem as ferramentas). Sem duplicata. Ressalva: o `audit` cobre so pacotes Python; para a imagem, ver [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]].
