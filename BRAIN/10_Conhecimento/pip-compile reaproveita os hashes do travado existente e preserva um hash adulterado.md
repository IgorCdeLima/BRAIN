---
tipo: problema-solucao
status: ativo
origem: T-0014 (Seguranca, SEC-T0014-05) e SEARCH-0006, curado pelo Bibliotecario
pesquisa: SEARCH-0006
tarefa: T-0014
confianca: media
fontes: ["https://github.com/jazzband/pip-tools/blob/main/piptools/scripts/options.py", "SEC-T0014-05 (lab)"]
verificado_em: 2026-10-02
valido_para: "pip-tools 7.6.1, pip 26.2.1"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [seguranca, pip-tools, hashes, supply-chain, armadilha, cwe-354]
---
# pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado

## Sintoma

"Regenerar o travado e comparar" nao detecta um hash trocado ou acrescentado no `requirements.txt`: o `pip-compile --generate-hashes` o mantem. Adotar uma opcao que mudaria os hashes (ex.: `--only-binary=:all:`) parece nao ter efeito.

## Ambiente

pip-tools 7.6.1, pip 26.2.1.

## Causa raiz

Com o arquivo de saida presente, o `pip-compile --generate-hashes` reaproveita nao so os pinos, mas tambem os **hashes**: `--reuse-hashes` e o padrao (`True` no codigo-fonte). Para pacote cujo pino nao muda, o hash vem do arquivo antigo, nao do indice. Classificacao: [[CWE-345 e a classe de hash copiado sem reconferir no indice - filha mais proxima e CWE-354]].

## Solucao

`--no-reuse-hashes` no servico/CI de lock. Os pinos continuam preservados (vem do `.txt`); os hashes passam a ser recalculados. Custo: mais lento.

## Como verificar que foi resolvido

Numa copia descartavel, trocar o hash de um pacote por zeros e rodar o `pip-compile`: com reaproveitamento o hash falso permanece; com `--no-reuse-hashes` o verdadeiro volta, com as versoes iguais. No experimento (SEC-T0014-05), 24 hashes de sdist sairam do arquivo que tinha `--only-binary :all:`.

## O que nao funcionou

Confiar em regeneracao + `git diff` como auditoria dos hashes.

## Links confiaveis

- [pip-tools, options.py (codigo-fonte)](https://github.com/jazzband/pip-tools/blob/main/piptools/scripts/options.py): `--reuse-hashes/--no-reuse-hashes`, padrao `True`; ajuda oficial: "Improve the speed of --generate-hashes by reusing the hashes from an existing output file."
- A pagina de docs do pip-tools **nao** descreve o flag nem recomenda `--no-reuse-hashes`: a recomendacao para CI e auditoria e deducao nossa, verificada no experimento.

## Relacionadas

- [[pip-compile so preserva as versoes travadas se o arquivo de saida existir ao lado do in]]: o motivo de o `.txt` precisar estar ao lado e, portanto, de o reaproveitamento existir.
- [[pip-compile only-binary descarta hashes de sdist]]: opcao cujo efeito o reaproveitamento mascara.
- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]
- [[pip require-hashes nao confere pacote ja instalado na imagem base]]: a mesma familia de falha no lado da instalacao.

## Origem

Experimento da Seguranca (T-0014, lab, SEC-T0014-05) e `pip-compile --help` (7.6.1). Pedido SEARCH-0006.

## Decisao do Bibliotecario

Promovido (2026-10-02). Sem duplicata. Pedido SEARCH-0006 catalogado.
