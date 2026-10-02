---
tipo: problema-solucao
status: ativo
origem: T-0014 (Seguranca, SEC-T0014-01) e SEARCH-0005, curado pelo Bibliotecario
pesquisa: SEARCH-0005
tarefa: T-0014
confianca: media
fontes: ["https://github.com/pypa/pip/blob/main/src/pip/_internal/resolution/resolvelib/factory.py", "https://pip.pypa.io/en/stable/topics/secure-installs/", "https://pip.pypa.io/en/stable/cli/pip_install/", "SEC-T0014-01 (lab)"]
verificado_em: 2026-10-02
valido_para: "pip 26.2.1; imagem python:3.13.15-slim"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [seguranca, pip, hashes, supply-chain, cwe-829, armadilha]
---
# pip require-hashes nao confere pacote ja instalado na imagem base

## Sintoma

Travado com `pip==X \ --hash=...` (gerado com `--allow-unsafe`) e instalado com `pip install --require-hashes -r ...` numa imagem `python:*` que ja traz o mesmo pip. Adulterar o hash do pip no travado **nao** quebra o build.

## Ambiente

pip 26.2.1, imagem `python:3.13.15-slim`.

## Causa raiz

O pip ve o requisito como ja satisfeito (`Requirement already satisfied: pip==X`), nao baixa o artefato e nao tem o que conferir. Vale para qualquer pacote que ja esteja na imagem base na mesma versao (pip, e setuptools/wheel em imagens antigas). O teste usual "remover o hash e ver o build falhar" so prova os pacotes que de fato foram baixados.

Fonte: o **codigo** do pip (branch main, 2026-10-02). Em `resolvelib/factory.py`, `_get_installed_candidate()` devolve `None` se `force_reinstall` esta ativo e, senao, aceita o pacote instalado so pela versao; os hashes vao apenas para a busca no indice. E comportamento do codigo, nao contrato documentado: pode mudar.

## Solucao

- `pip install --require-hashes --force-reinstall -r ...` faz o pip baixar e conferir tudo (testado: hash adulterado do pip -> "THESE PACKAGES DO NOT MATCH THE HASHES"; original passa).
- Complemento: fixar a imagem base por digest, que cobre o pip embutido.

## Como verificar que foi resolvido

Adulterar **so** o hash do pacote que ja vem na base, numa copia do travado, e conferir que o build falha.

## O que nao funcionou

Confiar no teste "tirar o hash e ver falhar" para os pacotes da imagem base. A documentacao do pip (Secure installs, `pip install`) nao descreve o caso e nao ha issue oficial que o trate; a issue uv #474 nao confirma o comportamento do pip.

## Links confiaveis

- [pip, resolvelib/factory.py](https://github.com/pypa/pip/blob/main/src/pip/_internal/resolution/resolvelib/factory.py): logica que aceita o instalado sem conferir hash e que ignora o instalado com `--force-reinstall`.
- [pip, Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/): como usar o modo de hashes (nao cobre o caso instalado).
- [pip install](https://pip.pypa.io/en/stable/cli/pip_install/): descricao de `--force-reinstall`.

## Relacionadas

- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]: a nota geral; este e o limite do controle.
- [[Servico de lock no Compose montando o repositorio inteiro alcanca os hooks do Git e executa no host]]: outro cuidado do mesmo trabalho de lock.
- [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]]: a mesma familia de falha no lado da geracao do travado.

## Origem

SEC-T0014-01 (lab, T-0014); pedido SEARCH-0005.

## Decisao do Bibliotecario

Promovido (2026-10-02). Sem duplicata. A leitura do codigo foi feita pelo Pesquisador via resumo de pagina; a recomendacao dele e o Revisor reconferir o trecho (por isso a confianca fica media). Pedido SEARCH-0005 catalogado.
