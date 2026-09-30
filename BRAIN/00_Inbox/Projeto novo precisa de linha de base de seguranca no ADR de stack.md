---
tipo: candidato
status: inbox
tipo_proposto: aprendizado
origem: agente/engenheiro
tarefa: T-0006
pesquisa:
confianca: media
fontes: ["projetos/lab: SEC-0002, SEC-0003, SEC-0004, SEC-0005", "projetos/lab: docs/adr/ADR-0001 Stack do projeto.md"]
verificado_em: 2026-09-30
valido_para: "projetos Python + Docker do ambiente"
criado: 2026-09-30
decisao:
tags: [seguranca, hardening, adr, engenheiro, seguranca-papel, proposta-n4]
---
# Projeto novo precisa de linha de base de seguranca no ADR de stack

## Conteudo proposto

Tres dos quatro SEC da T-0005 (SEC-0002 openssl da imagem base, SEC-0004 root, SEC-0005 cabecalhos) existiam desde a T-0001/T-0002, e o quarto (SEC-0003) veio de uma frase vaga do ADR de stack ("o Dev fixa as versoes"). Ninguem os procurou antes porque o papel Seguranca nasceu depois e cada revisao olha so o diff da tarefa.

**Proposta ao humano (M5, area N4):**

- O ADR de stack de todo projeto novo (Engenheiro) traz uma **linha de base de seguranca** com requisitos verificaveis: container da aplicacao sem root; cabecalhos HTTP (CSP com `frame-ancestors`, `X-Frame-Options`, `nosniff`); dependencias diretas e indiretas travadas com hash; varredura das dependencias **e** da imagem (camada do sistema); tag de imagem base com patch fixo.
- Quando um papel ou verificacao nova e criado, cada projeto existente recebe **uma** revisao de linha de base desse papel (um cartao), em vez de esperar a proxima tarefa que passe por perto.

## Evidencia

SEC-0002 a SEC-0005 (T-0005), marcados "pre-existente" pela Seguranca; ADR-0001 do lab. O lab corrige isso nas T-0007 a T-0009 (criadas na T-0006).

## Links confiaveis

- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): usuario sem privilegio (via [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]).
- [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html): cabecalhos recomendados (via [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]]).

## Por que e reaproveitavel

Todo projeto novo do ambiente e toda criacao de papel.

## Relacionadas no Brain

- [[Mapa das CWE relevantes para Python e FastAPI]]
- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]
- [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]]

## Decisao do Bibliotecario
