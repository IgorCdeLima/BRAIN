---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: T-0005
pesquisa: SEARCH-0002
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/1395.html", "https://github.com/pypa/pip-audit"]
verificado_em: 2026-09-30
valido_para: pip-audit 2.x; Python 3.13; imagem python:3.13-slim
criado: 2026-09-30
decisao:
tags: [seguranca, cwe, cwe-1395, dependencias, pip-audit]
---
# CWE-1395 dependencia vulneravel se evita auditando o arquivo travado e a camada do sistema da imagem

## Conteudo proposto

**O que e:** o produto depende de componente de terceiros com vulnerabilidade conhecida. A CWE pede inventario (SBOM), monitoramento de avisos e aplicacao rapida de correcoes.

**Controle na nossa stack:**
1. Travar as dependencias (ver [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]).
2. Auditar o arquivo travado: `pip-audit --require-hashes -r requirements.txt` (falha se algo nao estiver fixado com hash; pula a resolucao de dependencias, entao e rapido). Saida 0 = nada conhecido; 1 = vulnerabilidade encontrada.
3. `--strict` faz a auditoria falhar se alguma dependencia nao puder ser coletada (evita "limpo" falso).
4. pip-audit cobre so pacotes Python: some a varredura da imagem, ver [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]].
5. CVE sem correcao: registrar (id, pacote, por que nao atinge a app) e rever quando sair a correcao; nao ignorar em silencio.

**Como testar:** rodar o comando no CI/compose; provocar falha fixando de proposito uma versao com CVE conhecida e ver saida 1.

## Evidencia

Leitura da documentacao do pip-audit e da CWE-1395 em 2026-09-30. Lab da T-0005 (SEC-0002) mostrou o caso da camada do sistema.

## Links confiaveis

- [CWE-1395 (MITRE)](https://cwe.mitre.org/data/definitions/1395.html): definicao e mitigacoes (SBOM, monitorar, corrigir).
- [pip-audit (PyPA)](https://github.com/pypa/pip-audit): opcoes `--require-hashes`, `-r`, `--strict` e codigos de saida.

## Por que e reaproveitavel

Vale para todo projeto Python do ambiente.

## Relacionadas no Brain

- [[ruff e pip-audit em Docker Compose com servicos lint e audit no estagio dev]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario
