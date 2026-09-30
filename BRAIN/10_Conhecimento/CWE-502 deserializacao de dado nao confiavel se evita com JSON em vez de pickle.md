---
tipo: padrao
status: rascunho
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: baixa
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org, docs.python.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#15); Python 3.x
criado: 2026-09-30
decisao: promovido
revisar_em: 2026-12-30
tags: [seguranca, cwe, cwe-502, pickle, yaml, deserializacao]
---
# CWE-502 deserializacao de dado nao confiavel se evita com JSON em vez de pickle

## Contexto

**O que e:** a aplicacao reconstroi objetos a partir de bytes controlados por terceiros, e o formato permite executar codigo durante a leitura.

**Como aparece na nossa stack:**
- `pickle.loads`/`pickle.load`, `shelve`, `marshal` em dado vindo de upload, cookie, fila ou cache compartilhado.
- `yaml.load(x)` sem `SafeLoader` (o correto e `yaml.safe_load`).
- Cookie de sessao ou cache guardando objetos serializados sem assinatura.
- Modelos de ML `.pkl` de origem desconhecida.

## Solucao

**Controle:**
1. Trocar por formato de dados puro: JSON validado com Pydantic.
2. YAML somente com `yaml.safe_load`.
3. Se pickle for inevitavel, so entre partes confiaveis e com assinatura (HMAC) verificada antes de carregar.
4. Nunca deserializar upload de usuario.

**Como testar:** grep por `pickle`, `yaml.load(`, `marshal`; revisar de onde vem cada byte carregado.

## Evidencia

O aviso de seguranca do modulo `pickle` esta na documentacao oficial do Python; cheat sheet de deserializacao da OWASP consta no indice (A08). Nota baseada nos titulos/indices consultados em 2026-09-30; abrir os links para o texto completo.

## Links confiaveis

- [CWE-502 (MITRE)](https://cwe.mitre.org/data/definitions/502.html): definicao oficial.
- [Deserialization Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html): praticas seguras.
- [pickle (Python)](https://docs.python.org/3/library/pickle.html): aviso de seguranca e alternativas.

## Por que e reaproveitavel

Cache, filas e sessoes em qualquer projeto Python.

## Relacionadas no Brain

- [[CWE-94 code injection se evita sem eval, exec e templates montados com entrada do usuario]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido como **rascunho, confianca baixa** (2026-09-30): o Pesquisador nao leu o texto completo do cheat sheet (so indice e aviso do modulo pickle). Confirmar nos links antes de tratar como regra. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
