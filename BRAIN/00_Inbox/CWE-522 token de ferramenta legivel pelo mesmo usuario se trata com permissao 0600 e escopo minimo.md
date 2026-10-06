---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0011
confianca: media
fontes: [https://cwe.mitre.org/data/definitions/522.html, https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html]
verificado_em: 2026-10-05
valido_para: CWE 4.20
criado: 2026-10-05
decisao:
tags: [seguranca, cwe, credencial, container]
---
# CWE-522 token de ferramenta legivel pelo mesmo usuario se trata com permissao 0600 e escopo minimo

## Conteudo proposto

**O que e (MITRE):** o produto guarda ou transmite credenciais por metodo inseguro, sujeito a interceptacao ou leitura nao autorizada. Consequencia: assumir a identidade do dono da credencial (ganho de privilegio).

**Como aparece no ambiente 01_IA:** o token OAuth do Claude Code fica em arquivo do home do usuario. Todo processo do mesmo UID no container (outra sessao, comando do agente) consegue le-lo. O sandbox de processo reduz, mas nao elimina, esse caminho.

**Mitigacoes (MITRE + OWASP):** proteger a credencial com mecanismo adequado (cofre, keystore, segredo injetado em vez de gravado na imagem); nao baking de segredo na imagem; privilegio minimo no que a credencial permite.

**Controle verificavel (proposta, a validar):**
1. `stat -c '%a %U' <arquivo de credencial>` retorna `600` e o usuario esperado.
2. `docker history`/camadas da imagem sem o arquivo (credencial entra por volume ou segredo em tempo de execucao).
3. Sandbox de comandos nega leitura do caminho da credencial (testar com `cat` dentro de uma sessao de agente: deve falhar).
4. Token revogavel e com escopo minimo; rotacao documentada.

## Evidencia

Definicao e mitigacoes lidas na pagina oficial da CWE-522 (versao 4.20). Regra de segredos do OWASP Docker Security Cheat Sheet (RULE #12). Os itens de controle 1 a 4 sao inferencia do pesquisador, nao texto da fonte.

## Links confiaveis

- [CWE-522](https://cwe.mitre.org/data/definitions/522.html): definicao, consequencias e mitigacoes.
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): regra de segredos em containers (RULE #12) e usuario sem privilegio (RULE #2).

## Por que e reaproveitavel

Qualquer projeto com credencial de ferramenta dentro de container; base para SEC-T0018-01 e para a analise de ameacas da T-0019.

## Relacionadas no Brain

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]
- [[Mapa das CWE relevantes para Python e FastAPI]]
