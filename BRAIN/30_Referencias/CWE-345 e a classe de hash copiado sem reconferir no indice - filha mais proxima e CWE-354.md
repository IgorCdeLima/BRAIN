---
tipo: referencia
status: ativo
origem: SEARCH-0006 (Pesquisador, T-0014), curado pelo Bibliotecario
pesquisa: SEARCH-0006
tarefa: T-0014
autor: MITRE (CWE)
url: https://cwe.mitre.org/data/definitions/345.html
acessado_em: 2026-10-02
confianca: media
fontes: [https://cwe.mitre.org/data/definitions/345.html, https://cwe.mitre.org/data/definitions/353.html]
verificado_em: 2026-10-02
valido_para: CWE 4.20 (entrada atualizada em 2026-04-30)
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [seguranca, cwe-345, cwe-354, supply-chain, hashes]
---
# CWE-345 e a classe de hash copiado sem reconferir no indice - filha mais proxima e CWE-354

## Resumo

- **CWE-345** (Insufficient Verification of Data Authenticity): o produto nao verifica o bastante a origem ou a autenticidade do dado e aceita dado invalido. E a classe-mae correta para o achado do `--reuse-hashes` do pip-compile.
- A MITRE **nao traz secao de mitigacao** na CWE-345; as mitigacoes estao nas filhas e pares (ex.: CWE-353 pede checksum no protocolo e calculo correto por mensagem).
- **CWE-354** (Improper Validation of Integrity Check Value) e a filha mais especifica: o valor de integridade (o hash) existe, mas nao e validado de verdade. Descreve bem "lock tool copia o hash do arquivo antigo sem reconferir com o indice". A CWE-353 (ausencia do mecanismo) nao serve, porque o mecanismo existe.
- Filhas da 345 vistas e descartadas: CWE-494 (baixar codigo sem checagem de integridade; cabe ao `pip install` sem `--require-hashes`, nao ao lock), CWE-347 (assinatura criptografica), CWE-348 (fonte menos confiavel).

## O que aproveitar

- No SEC, classificar como `CWE-354` (classe `CWE-345`). Esta recomendacao e **julgamento nosso**, nao texto da MITRE.
- Controle pratico: `--no-reuse-hashes` no lock de CI, ver [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]].
- Para o caso vizinho (hash que o `pip install` nao confere) veja [[pip require-hashes nao confere pacote ja instalado na imagem base]] e a nota geral [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]].

## Ressalvas

- A CWE-354 **nao foi lida diretamente** pelo Pesquisador; o que se sabe dela vem da pagina da CWE-353 (par) e de resumo de ferramenta. Confira a pagina da CWE-354 antes de citar no SEC.
- CWE 4.20: a taxonomia muda entre versoes; revisar na data indicada.

## Links confiaveis

- [CWE-345](https://cwe.mitre.org/data/definitions/345.html): definicao e lista de filhas.
- [CWE-353](https://cwe.mitre.org/data/definitions/353.html): ausencia de verificacao de integridade e mitigacoes; par da CWE-354.
- [CWE-354](https://cwe.mitre.org/data/definitions/354.html): integridade existe mas e validada mal.

## Notas derivadas

- [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]]: o achado que motivou a classificacao.
- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]: a classe vizinha (origem nao confiavel).

## Decisao do Bibliotecario

Promovido (2026-10-02) como referencia ativa em `30_Referencias`. Sem duplicata no Brain (busca por CWE-345, CWE-353, CWE-354). Pedido SEARCH-0006 catalogado. Confianca fica media pela leitura indireta da CWE-354.
