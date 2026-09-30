---
tipo: problema-solucao
status: ativo
origem: T-0005, SEC-0002 (Seguranca), curado pelo Bibliotecario
tarefa: T-0005
pesquisa: SEARCH-0002
confianca: media
fontes: ["osv-scanner 2.6.0 e pip-audit 2.10.1 rodados no lab em 2026-09-30", "https://osv.dev/vulnerability/DEBIAN-CVE-2026-84782", "https://cwe.mitre.org/data/definitions/1395.html"]
verificado_em: 2026-09-30
valido_para: imagens python:3.13-slim (Debian 13), pip-audit 2.10.x, osv-scanner 2.6.x
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [seguranca, dependencias, docker, pip-audit, osv-scanner, armadilha]
---
# pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora

## Sintoma

`pip-audit` responde "No known vulnerabilities found", mas `osv-scanner scan image <imagem>:latest` na mesma imagem acusa dezenas de CVEs de pacotes Debian (no lab: 68 vulns em 18 pacotes; 13 do openssl com correcao disponivel).
## Causa raiz

O `pip-audit` so audita pacotes Python. Os pacotes do sistema (openssl, glibc, zlib...) vem da imagem base e ficam invisiveis para ele.
## Solucao

Somar uma varredura da imagem (`osv-scanner scan image <nome>:latest`) e conferir as correcoes com `apt list --upgradable` dentro do container. Corrigir atualizando a tag de patch da imagem base ou com `apt-get upgrade` no estagio base.
## O que nao funcionou

Armadilhas do osv-scanner: `scan image` exige a tag (sem `:latest` da "is not a tagged image name"); `-L` sobre um `pip freeze` do dev pode falhar na resolucao ("no candidates at all for: platformdirs"). Nesse caso, use `scan image`.
## Como verificar que foi resolvido

Triagem: muitas CVEs do openssl (QUIC, DTLS, SM2, CMP) nao atingem um app HTTP sem TLS. Ainda assim, registre-as e corrija quando houver pacote.

## Evidencia

Lab, T-0005, SEC-0002: `pip-audit --strict` limpo na imagem dev; `osv-scanner scan image t0005-seg-app:latest` -> 68 vulns Debian; `apt list --upgradable` -> openssl/libssl3t64 3.5.7-1~deb13u3 e libpcre2-8-0.

## Links confiaveis

- [OSV.dev - DEBIAN-CVE-2026-84782](https://osv.dev/vulnerability/DEBIAN-CVE-2026-84782)
- [MITRE CWE-1395](https://cwe.mitre.org/data/definitions/1395.html)
- [osv-scanner](https://github.com/google/osv-scanner)

## Por que e reaproveitavel

Vale para qualquer projeto Python em container do ambiente: evita que um "sem vulnerabilidades" do pip-audit seja lido como "imagem sem vulnerabilidades".

## Relacionadas no Brain

- [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]]
- [[Fontes de referencia para analise de seguranca por CWE e dependencias]]
- [[ruff e pip-audit em Docker Compose com servicos lint e audit no estagio dev]]

## Decisao do Bibliotecario

Promovido (2026-09-30) como problema-solucao ativo: reproduzido e medido no lab (T-0005, SEC-0002). Complementa, nao duplica, [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]] (outro problema: falso positivo no requirements.txt).
