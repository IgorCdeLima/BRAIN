---
tipo: referencia
status: ativo
origem: humano (Igor), avaliado em sessao de manutencao do ambiente; curado pelo Bibliotecario
confianca: media
fontes: ["https://samate.nist.gov/SARD/", "https://github.com/juice-shop/juice-shop", "https://github.com/AppThreat/vulnerability-db", "https://github.com/aboutcode-org/vulnerablecode", "https://github.com/pypa/advisory-database", "https://osv.dev/"]
verificado_em: 2026-09-30
valido_para: stack do lab (Python, FastAPI, PostgreSQL, Docker); revisar a cada 6 meses
criado: 2026-09-30
revisar_em: 2027-03-30
decisao: promovido
tags: [seguranca, cwe, vulnerabilidades, dependencias, referencia]
---
# Fontes de referencia para analise de seguranca por CWE e dependencias

## Conteudo proposto

Lista de fontes para o papel Seguranca consultar ao analisar uma CWE, uma dependencia ou um abuso, e sempre que surgir oportunidade. Classificadas pelo uso na nossa stack.

### Uso diario (dependencias Python e imagens)

| Fonte | O que e | Como usar |
|---|---|---|
| [OSV.dev](https://osv.dev/) | Base aberta de vulnerabilidades de codigo aberto, esquema OSV, mais de 40 ecossistemas (PyPI, Debian, Ubuntu, Alpine...). Agrega GitHub Advisories, PyPA e outras | Consultar pacote+versao pela API ou pelo site. A ferramenta `osv-scanner` varre `requirements.txt`, diretorios e imagens de container |
| [PyPA Advisory Database](https://github.com/pypa/advisory-database) | Avisos de seguranca de pacotes do PyPI, em YAML no esquema OSV, com triagem humana dos CVE | E a fonte do `pip-audit` e alimenta o OSV.dev. Consultar direto quando um aviso de pacote Python for duvidoso |

### Ferramenta ou fonte agregada (uso eventual)

| Fonte | O que e | Quando usar |
|---|---|---|
| [VulnerableCode](https://github.com/aboutcode-org/vulnerablecode) | Base de vulnerabilidades com interface web e API (instancia publica em public.vulnerablecode.io), identifica pacotes por PURL, agrega NVD, OSV e outras | Segunda opiniao quando OSV e PyPA divergirem |
| [AppThreat vulnerability-db](https://github.com/AppThreat/vulnerability-db) | Base offline (SQLite, esquema CVE 5.2) com CLI e biblioteca Python; agrega distros Linux, OSV, NVD e GitHub | Se precisarmos varrer SBOM sem internet ou embutir a consulta numa ferramenta nossa |

### Estudo e treino (nao e consulta do dia a dia)

| Fonte | O que e | Limite |
|---|---|---|
| [NIST SARD](https://samate.nist.gov/SARD/) | Mais de 450 mil casos de teste com fraquezas documentadas, mais de 150 classes CWE | So C, C++, Java, PHP e C#: **sem Python**. Serve para entender como uma CWE aparece em codigo, nao para o nosso codigo |
| [OWASP Juice Shop](https://github.com/juice-shop/juice-shop) | Aplicacao propositalmente insegura (Node.js, Angular, Express, SQLite) para treino e CTF, cobre o OWASP Top 10 | Stack diferente da nossa. Bom para treinar o papel Seguranca em ataques reais, nao para referencia de correcao |

### Lacunas: fontes sugeridas para completar (a confirmar)

Pistas do conhecimento geral, **nao verificadas nesta sessao** (MITRE CWE e OWASP Cheat Sheets foram depois usados e lidos na pesquisa SEARCH-0001; ver [[Mapa das CWE relevantes para Python e FastAPI]]):

- **MITRE CWE** (cwe.mitre.org): definicao oficial de cada CWE, com consequencias e mitigacoes. Hoje nenhuma fonte da lista explica a CWE em si.
- **OWASP Cheat Sheet Series**: controles praticos por tema. A "File Upload Cheat Sheet" cobre exatamente o caso da T-0003.
- **OWASP ASVS**: lista de requisitos de seguranca verificaveis, util para a analise de ameacas virar criterio de aceite.
- **pip-audit**: ferramenta que o proprio PyPA indica para auditar dependencias Python.

## Evidencia

Cada fonte foi aberta em 2026-09-30 e conferida quanto a escopo, linguagens e atividade. Todas estavam ativas: commits recentes; VulnerableCode com financiamento NGI/NLnet; AppThreat na v7. O SARD nao cita Python nas linguagens suportadas.

## Por que e reaproveitavel

- O papel Seguranca precisa de fonte externa para fatos volateis (CVE, versao corrigida), conforme a hierarquia de conhecimento.
- A tabela separa consulta de estudo e evita gastar tempo com fonte fora da stack.
- Vale para qualquer projeto Python do ambiente, nao so o lab.

## Relacionadas no Brain

- [[Seguranca]]: papel que vai consultar esta lista.
- [[ADR-0016 Papeis Coordenador e Seguranca]]
- [[Recusa previa por Content-Length esconde a validacao do upload]]: exemplo de achado de seguranca da T-0003.

## Decisao do Bibliotecario

Promovido a referencia em `30_Referencias` (2026-09-30): lista conferida em sessao anterior, sem duplicata. Nota: dominios como `cwe.mitre.org` e `cheatsheetseries.owasp.org` ja constam em `agentes/fontes-confiaveis.json`; a inclusao de novos dominios propostos no SEARCH-0001 e decisao do humano.
