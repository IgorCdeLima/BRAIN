---
tipo: conceito
status: ativo
origem: SEARCH-0007 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0007
tarefa: T-0015
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/1088.html"]
verificado_em: 2026-10-03
valido_para: "CWE (pagina atual da MITRE)"
criado: 2026-10-03
decisao: promovido
revisar_em: 2027-04-03
tags: [seguranca, cwe-1088, timeout, disponibilidade]
---
# CWE-1088 chamada remota sincrona sem timeout trava o servico

## Ideia

O codigo faz chamada sincrona a recurso remoto sem timeout, ou com timeout infinito. Quando o recurso fica indisponivel, o produto trava; se um atacante provoca isso, vira negacao de servico. Nivel Base, liberado para mapeamento. Exemplos listados pela MITRE: CVE-2024-8062 (HEAD sem timeout deixa o servidor preso) e CVE-2024-8061.

A pagina **nao traz secao de mitigacoes**. A correcao implicita e definir timeout em toda chamada remota (rede, banco, HTTP). No banco: `connect_timeout` mais `statement_timeout` ([[statement_timeout via connect_args options cobre lock mas nao banco congelado]]); servidor congelado e residual ([[Nao ha controle simples no cliente para consulta presa em servidor Postgres congelado]]).

## Por que importa

Rotula achados de seguranca do tipo "sem timeout" em qualquer cliente de rede ou banco, e liga-os ao controle de disponibilidade.

## Links confiaveis

- [CWE-1088](https://cwe.mitre.org/data/definitions/1088.html): definicao, status e exemplos (pagina lida em 2026-10-03).

## Relacionadas

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: o controle generico de recursos; esta CWE e o caso de chamada remota sem prazo.
- [[statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3]]: como aplicar o timeout no Postgres.
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-10-03) como conceito. Sem duplicata (busca por `1088`: nenhuma nota). Indexado no mapa de CWE.
