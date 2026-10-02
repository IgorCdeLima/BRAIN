---
tipo: candidato
status: candidato
origem: T-0014 (Seguranca), SEC-T0014-01 do lab
confianca: media
fontes: [codigo do pip resolvelib/factory.py, pip Secure installs]
verificado_em: 2026-10-02
valido_para: pip 26.2.1; imagem python:3.13.15-slim
pesquisa: SEARCH-0005
tags: [seguranca, pip, hashes, supply-chain, cwe-829, armadilha]
---
# pip require-hashes nao confere pacote ja instalado na imagem base

## Sintoma

Travado com `pip==X \ --hash=...` (gerado com `--allow-unsafe`) e instalado com `pip install --require-hashes -r ...` numa imagem `python:*` que ja traz o mesmo pip. Adulterar o hash do pip no travado **nao** quebra o build.

## Causa

O pip ve o requisito como ja satisfeito (`Requirement already satisfied: pip==X`), nao baixa o artefato e nao tem o que conferir. Vale para qualquer pacote que ja esteja na imagem base na mesma versao (pip, e setuptools/wheel em imagens antigas). O teste usual "remover o hash e ver o build falhar" so prova os pacotes que de fato foram baixados.

## Solucao

- `pip install --require-hashes --force-reinstall -r ...` faz o pip baixar e conferir tudo (testado: hash adulterado do pip -> "THESE PACKAGES DO NOT MATCH THE HASHES"; original passa).
- Complemento: fixar a imagem base por digest, que cobre o pip embutido.
- Como testar: adulterar **so** o hash do pacote que ja vem na base, numa copia, e conferir que o build falha.

## Limites

A documentacao do pip (Secure installs, `pip install`) nao descreve o caso; nao ha issue oficial achado que o trate. A confirmacao vem do **codigo-fonte do pip** (verificado em 2026-10-02, branch main): em `resolvelib/factory.py`, `_get_installed_candidate()` devolve `None` se `force_reinstall` esta ativo e, senao, aceita o pacote instalado so pela versao; os hashes vao apenas para a busca no indice. Comportamento do codigo, nao contrato documentado: pode mudar.

## Links confiaveis

- https://github.com/pypa/pip/blob/main/src/pip/_internal/resolution/resolvelib/factory.py - logica que aceita o instalado sem conferir hash e que ignora o instalado com `--force-reinstall`.
- https://pip.pypa.io/en/stable/topics/secure-installs/ - como usar o modo de hashes (nao cobre o caso instalado).
- https://pip.pypa.io/en/stable/cli/pip_install/ - descricao de `--force-reinstall`.

## Relacionadas

- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]
- [[Servico de lock no Compose montando o repositorio inteiro alcanca os hooks do Git e executa no host]]
