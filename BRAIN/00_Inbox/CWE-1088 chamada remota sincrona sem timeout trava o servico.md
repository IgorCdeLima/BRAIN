---
tipo: candidato
status: inbox
tipo_proposto: conceito
origem: agente/pesquisador
tarefa: T-0015
pesquisa: SEARCH-0007
confianca: media
fontes: [cwe.mitre.org/data/definitions/1088.html]
verificado_em: 2026-10-03
valido_para: CWE (pagina atual da MITRE)
criado: 2026-10-03
decisao:
tags: [seguranca, cwe-1088, timeout, disponibilidade]
---
# CWE-1088 chamada remota sincrona sem timeout trava o servico

## Conteudo proposto

- Definicao: o codigo faz chamada sincrona a recurso remoto sem timeout, ou com timeout infinito.
- Efeito: o produto trava quando o recurso fica indisponivel; se um atacante provoca isso, vira negacao de servico. Nivel Base, liberado para mapeamento.
- Exemplos listados: CVE-2024-8062 (HEAD sem timeout deixa o servidor preso) e CVE-2024-8061.
- A pagina **nao traz secao de mitigacoes**; a correcao implicita e definir timeout em toda chamada remota (rede, banco, HTTP). No banco: `connect_timeout` + `statement_timeout` (ver nota relacionada); servidor congelado e residual.

## Evidencia

Pagina oficial da MITRE lida em 2026-10-03.

## Links confiaveis

- [CWE-1088](https://cwe.mitre.org/data/definitions/1088.html): definicao, status e exemplos.

## Por que e reaproveitavel

Rotula achados de seguranca de "sem timeout" em qualquer cliente de rede ou banco.

## Relacionadas no Brain

- [[statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3]]
- [[Nao ha controle simples no cliente para consulta presa em servidor Postgres congelado]]
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]

## Decisao do Bibliotecario
