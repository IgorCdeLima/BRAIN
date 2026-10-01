---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/dev
tarefa: T-0009
pesquisa:
confianca: alta
fontes: ["projetos/lab: experimento da T-0009 em copia descartavel (Docker 29.1.3, Compose, python:3.13.15-slim, pip 26.2.1, pip-tools 7.6.1)"]
verificado_em: 2026-10-01
valido_para: Docker Compose com servicos run sobre imagem que embute app/ e dependencias; pip 26.2.1; pip-tools 7.6.1
criado: 2026-10-01
decisao:
tags: [docker, compose, pip-audit, pip-tools, require-hashes, armadilha]
---
# docker compose run sem --build testa codigo velho e audita dependencia velha

## Conteudo proposto

Para fundir em [[Imagem Docker que embute o codigo exige build antes de rodar pytest]] e confirmar o candidato [[docker compose run nao reconstroi e faz testes e auditoria olharem imagem velha]].

**Reproduzido (observacao O1 confirmada):**
- `audit`: com `urllib3==1.26.18` acrescentado ao `requirements-dev.txt`, `run --rm audit` sem `--build` -> "No known vulnerabilities found" (exit 0, imagem velha); `run --build --rm audit` -> urllib3 acusado, exit 1.
- `test`: mensagem de erro trocada em `app/imagens.py`; `run --rm test` sem `--build` -> 76 passed (codigo velho); com `--build` -> 1 failed, exit 1.
- Armadilha extra: `urllib3==1.26.0` (primeira escolha) **quebra o proprio pip-audit** no Python 3.13 (`ModuleNotFoundError: urllib3.packages.six.moves`), exit 1 sem relatar vulnerabilidade. Use 1.26.18 em experimentos.

**Travamento com hash (resultados):**
- `pip install --require-hashes` com hash removido de um pacote -> build falha ("Hashes are required in --require-hashes mode").
- Resultado negativo: trocar `==` por `>=` **mantendo os hashes** NAO falha; o pip aceita e o hash segue protegendo o artefato. O teste "troque == por >=" da nota [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]] so vale se tambem se tirar o hash; o teste confiavel e remover o hash.
- `pip-compile` padrao imprime `--no-index` no cabecalho e avisa que `--strip-extras` sera o padrao no 8.0; usar `--strip-extras` desde ja.
- Nomes normalizados: `pip freeze` mostra `boolean.py`, o travado mostra `boolean-py`; comparar contagens com normalizacao.

## Evidencia

Experimento na T-0009 (projeto lab), saidas registradas na Entrega do cartao.

## Links confiaveis

- [pip: Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/): comportamento do `--require-hashes` (nao reaberto nesta tarefa).

## Por que e reaproveitavel

Qualquer projeto com servicos de verificacao no Compose e dependencias travadas.

## Relacionadas no Brain

- [[Imagem Docker que embute o codigo exige build antes de rodar pytest]]
- [[ruff e pip-audit em Docker Compose com servicos lint e audit no estagio dev]]

## Decisao do Bibliotecario

**Fundido e arquivado** (2026-10-01): a parte do `run --build` entrou em [[Imagem Docker que embute o codigo exige build antes de rodar pytest]]; a parte do `--require-hashes` (correcao do teste `==` por `>=`, `--strip-extras`, nomes normalizados) entrou em [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]. Confianca alta (experimento reproduzido). Candidato movido para 90_Arquivo.
