---
tipo: aprendizado
status: ativo
origem: T-0006 (Engenheiro, retrospectiva T-0003 a T-0005), curado pelo Bibliotecario
tarefa: T-0006
confianca: media
fontes: ["projetos/lab: SEC-0002, SEC-0003, SEC-0004, SEC-0005", "projetos/lab: docs/adr/ADR-0001 Stack do projeto.md", "https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html", "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html"]
verificado_em: 2026-09-30
valido_para: "projetos Python + Docker do ambiente"
revisar_em: 2027-03-30
criado: 2026-09-30
decisao: promovido
tags: [seguranca, hardening, adr, engenheiro, seguranca-papel, proposta-n4]
---
# Projeto novo precisa de linha de base de seguranca no ADR de stack

## O que aconteceu

Tres dos quatro SEC da T-0005 (SEC-0002 openssl da imagem base, SEC-0004 container como root, SEC-0005 cabecalhos) existiam desde a T-0001/T-0002. O quarto (SEC-0003) veio de uma frase vaga do ADR de stack ("o Dev fixa as versoes"). Ninguem os procurou antes porque o papel Seguranca nasceu depois e cada revisao olha so o diff da tarefa. A Seguranca os marcou "pre-existente".

## O que aprendemos

Sem requisitos de seguranca verificaveis no ADR de stack, o problema fica escondido ate alguem olhar o projeto inteiro. Frase vaga no ADR vira achado depois.

## O que muda a partir de agora

**Proposta ao humano (M5, area N4; pendente):**

- O ADR de stack de todo projeto novo (Engenheiro) traz uma **linha de base de seguranca** com requisitos verificaveis: container da aplicacao sem root; cabecalhos HTTP (CSP com `frame-ancestors`, `X-Frame-Options`, `nosniff`); dependencias diretas e indiretas travadas com hash; varredura das dependencias **e** da imagem (camada do sistema); tag de imagem base com patch fixo.
- Quando um papel ou verificacao nova e criado, cada projeto existente recebe **uma** revisao de linha de base desse papel (um cartao), em vez de esperar a proxima tarefa que passe por perto.

O lab corrige isso nas T-0007 a T-0009.

## Origem

SEC-0002 a SEC-0005 (T-0005) e ADR-0001 do lab.

## Links confiaveis

- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): usuario sem privilegio (via [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]).
- [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html): cabecalhos recomendados (via [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]]).

## Relacionadas no Brain

- [[Mapa das CWE relevantes para Python e FastAPI]]: onde achar cada controle da linha de base.
- [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]]: item de dependencias travadas.
- [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]]: item de varredura da imagem.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento` (2026-09-30): evidencia em 4 SEC e no ADR do lab, sem duplicata. A mudanca no fluxo do Engenheiro e proposta ao humano (N4).
