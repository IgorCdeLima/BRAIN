---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0014
pesquisa: SEARCH-0006
confianca: media
fontes: [https://cwe.mitre.org/data/definitions/345.html, https://cwe.mitre.org/data/definitions/353.html]
verificado_em: 2026-10-02
valido_para: CWE 4.20 (entrada atualizada em 2026-04-30)
criado: 2026-10-02
decisao:
tags: [seguranca, cwe-345, cwe-354, supply-chain, hashes]
---
# CWE-345 e a classe de hash copiado sem reconferir no indice - filha mais proxima e CWE-354

## Conteudo proposto

- **CWE-345** (Insufficient Verification of Data Authenticity): o produto nao verifica o bastante a origem ou a autenticidade do dado e aceita dado invalido. E a classe-mae correta para o achado do `--reuse-hashes`.
- A MITRE **nao traz secao de mitigacao** na CWE-345; as mitigacoes estao nas filhas/pares (ex.: CWE-353 pede checksum no protocolo e calculo correto por mensagem).
- Filha mais especifica: **CWE-354** (Improper Validation of Integrity Check Value): existe um valor de integridade (o hash), mas ele nao e validado de verdade. Descreve melhor "lock tool copia hash do arquivo antigo sem reconferir com o indice". CWE-353 (ausencia do mecanismo) nao serve: o mecanismo existe.
- Outras filhas da 345 vistas e descartadas: CWE-494 (baixar codigo sem checagem de integridade; cabe ao `pip install` sem `--require-hashes`, nao ao lock), CWE-347 (assinatura criptografica), CWE-348 (fonte menos confiavel).
- Recomendacao de classificacao no SEC: `CWE-354` (classe `CWE-345`). Julgamento nosso, nao texto da MITRE.
- Controle pratico: `--no-reuse-hashes` no lock de CI, ver [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]].

## Evidencia

Entradas CWE-345 e CWE-353/354 lidas em cwe.mitre.org em 2026-10-02 (versao 4.20). A leitura das paginas foi resumida por ferramenta; confira a CWE-354 diretamente antes de citar no SEC.

## Links confiaveis

- [CWE-345](https://cwe.mitre.org/data/definitions/345.html): definicao e lista de filhas.
- [CWE-353](https://cwe.mitre.org/data/definitions/353.html): ausencia de verificacao de integridade e mitigacoes; par da CWE-354.
- [CWE-354](https://cwe.mitre.org/data/definitions/354.html): integridade existe mas e validada mal.

## Por que e reaproveitavel

Classificar achados de supply chain (lock, hash, checksum) sem escolher CWE ao acaso.

## Relacionadas no Brain

- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]

## Decisao do Bibliotecario
