---
tipo: candidato
status: arquivado
tipo_proposto: aprendizado
origem: agente/dev
tarefa: T-0014
pesquisa:
confianca: media
fontes: []
verificado_em: 2026-10-02
valido_para: pip-tools 7.6.1
criado: 2026-10-02
decisao: fundido em [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]]
tags: [pip-tools, supply-chain, hashes, cwe-345]
---
# pip-compile --no-reuse-hashes recalcula os hashes e elimina hash adulterado e hash de sdist inerte

## Conteudo proposto

Ao regenerar travados com `pip-compile --generate-hashes`, o padrao `--reuse-hashes` aproveita os hashes do `.txt` existente. Isso preserva hash adulterado e hashes de sdist que ficam inertes com `--only-binary :all:`. Com `--no-reuse-hashes` as versoes continuam as do `.txt` copiado ao lado do `.in`, mas os hashes sao recalculados do zero.

Custo: a geracao fica bem mais lenta (cerca de 10 min ou mais neste projeto), pois baixa os arquivos para hashear.

## Evidencia

T-0014: starlette com hash trocado por zeros numa copia -> regeneracao com `--no-reuse-hashes` removeu o hash falso. Versoes identicas; linhas sha256: requirements.txt 744 -> 720, dev 396 -> 358, lock 16 -> 8. Segunda execucao: `git status` limpo.

## Links confiaveis

Nenhum consultado (ver SEARCH-0006, aberto pela Seguranca, para a doc oficial).

## Decisao do Bibliotecario

Fundido (2026-10-03) em [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]]: ja promovida em 2026-10-02 a partir do SEC-T0014-05 com a mesma solucao (`--no-reuse-hashes`); as medicoes do Dev e o custo de tempo foram incorporados. Arquivado, nao apagado.
