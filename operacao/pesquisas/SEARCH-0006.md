---
tipo: pesquisa
id: SEARCH-0006
status: respondida
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0014
criado: 2026-10-02
pesquisado_por: pesquisador
pesquisado_em: 2026-10-02
catalogado_em:
notas: []
tags: [seguranca, cwe-345, pip-tools, hashes, supply-chain]
---
# SEARCH-0006 - CWE-345 e o --reuse-hashes do pip-compile

## Pergunta

1. Qual a definicao oficial da CWE-345 (Insufficient Verification of Data Authenticity) e as mitigacoes que a MITRE indica? E a CWE mais adequada para "ferramenta de lock que copia hashes de um arquivo existente sem reconferir no indice", ou ha uma filha mais especifica?
2. A documentacao oficial do pip-tools confirma que `--reuse-hashes` e o padrao do `pip-compile` e recomenda `--no-reuse-hashes` em algum cenario (CI, auditoria)?

## Contexto

Revisao de seguranca da T-0014 (lab, SEC-T0014-05). Experimento: com um hash adulterado no `requirements.txt` e o `.txt` copiado ao lado do `.in`, o `pip-compile --generate-hashes` (7.6.1) preserva o hash falso; com `--no-reuse-hashes`, recalcula e o hash verdadeiro volta. Premissa usada: CWE-345 e o padrao `--reuse-hashes` (visto no `--help`).

## Ja buscado no Brain

- Busca por `CWE-345`, `CWE-353`, `reuse-hashes`: nenhuma nota.
- [[pip-compile so preserva as versoes travadas se o arquivo de saida existir ao lado do in]] (Inbox): fala dos pinos, nao dos hashes.
- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]: nao cobre a regeneracao.

---

## Resposta

- **Resumo (3 a 5 linhas):** CWE-345 = verificacao insuficiente da autenticidade dos dados (MITRE, CWE 4.20); a entrada nao tem secao de mitigacao. Filha mais adequada ao caso: CWE-354 (valor de integridade existe mas e mal validado); CWE-353 (ausencia do mecanismo) nao serve. No pip-tools, `--reuse-hashes/--no-reuse-hashes` tem padrao `True` (ajuda: reaproveitar hashes do arquivo de saida para acelerar `--generate-hashes`). A documentacao nao recomenda `--no-reuse-hashes`; isso e deducao do experimento SEC-T0014-05.
- **Notas geradas no Inbox:** [[CWE-345 e a classe de hash copiado sem reconferir no indice - filha mais proxima e CWE-354]]; links confiaveis acrescentados em [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]]
- **Links confiaveis:** https://cwe.mitre.org/data/definitions/345.html ; https://cwe.mitre.org/data/definitions/353.html ; https://github.com/jazzband/pip-tools/blob/main/piptools/scripts/options.py
- **Sem resposta / limites:** pergunta 2 parcial: padrao confirmado no codigo-fonte, mas docs oficiais (readthedocs/README) nao citam o flag nem recomendam `--no-reuse-hashes`. A pagina CWE-354 nao foi lida diretamente (so via resumo da 353).
- **Conteudo suspeito descartado:**

## Dominios propostos

- 

## Catalogacao
