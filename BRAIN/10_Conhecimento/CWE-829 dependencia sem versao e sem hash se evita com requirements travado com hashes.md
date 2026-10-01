---
tipo: padrao
status: ativo
origem: SEARCH-0002 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0005
pesquisa: SEARCH-0002
confianca: media
fontes: ["https://pip.pypa.io/en/stable/topics/secure-installs/", "https://github.com/jazzband/pip-tools", "https://cwe.mitre.org/data/definitions/829.html"]
verificado_em: 2026-09-30
valido_para: pip atual (docs stable); pip-tools
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [seguranca, cwe, cwe-829, supply-chain, pip, hashes]
---
# CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes

## Contexto

**O que e:** CWE-829 e importar codigo de fonte fora da esfera de controle. Numa dependencia sem versao fixa ou sem hash, o que o `pip install` baixa pode mudar ou ser adulterado.

## Solucao

**Controle:**
1. Manter `requirements.in` com as dependencias diretas e gerar o travado: `pip-compile --generate-hashes requirements.in` (saida com `pacote==x.y \ --hash=sha256:...` para direta e transitiva).
2. Instalar com `pip install --require-hashes -r requirements.txt` (no Dockerfile). Nesse modo todo requisito precisa de `==` e de hash; um unico `--hash` ja liga o modo para tudo. So sha256 e aceito como algoritmo forte.
3. Auditar o mesmo arquivo com `pip-audit --require-hashes -r requirements.txt`.

**Como testar:** remover um hash de um pacote e ver o `pip install` falhar no build ("Hashes are required in --require-hashes mode").

**Correcao (T-0009, 2026-10-01):** trocar `==` por `>=` **mantendo os hashes nao falha**: o pip aceita e o hash continua protegendo o artefato. O teste "troque `==` por `>=`" so vale se tambem se tirar o hash; o teste confiavel e remover o hash.

**Detalhes de pip-tools 7.6.1 (experimento da T-0009):** `pip-compile` imprime `--no-index` no cabecalho e avisa que `--strip-extras` sera o padrao no 8.0 (use `--strip-extras` desde ja). Nomes sao normalizados: `pip freeze` mostra `boolean.py`, o travado mostra `boolean-py`; compare contagens normalizando. Cuidado com o servico que roda o `pip-compile`: [[Servico de lock no Compose montando o repositorio inteiro alcanca os hooks do Git e executa no host]].

## Evidencia

Documentacao do pip (secure installs) e README do pip-tools lidos em 2026-09-30.

## Links confiaveis

- [pip: Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/): modo `--require-hashes` e suas exigencias.
- [pip-tools](https://github.com/jazzband/pip-tools): `pip-compile --generate-hashes`.
- [CWE-829 (MITRE)](https://cwe.mitre.org/data/definitions/829.html): definicao e mitigacoes.

## Por que e reaproveitavel

Builds reproduziveis e protecao contra pacote adulterado em qualquer projeto Python.

## Relacionadas no Brain

- [[CWE-1395 dependencia vulneravel se evita com auditoria do arquivo travado e da camada do sistema da imagem]]

## Decisao do Bibliotecario

Promovido (2026-09-30) como padrao ativo: docs do pip e do pip-tools lidas. Ressalva: `uv pip compile --generate-hashes` nao foi confirmado em fonte primaria (limite do SEARCH-0002). Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
