---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0011
confianca: media
fontes: [https://cwe.mitre.org/data/definitions/653.html, https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html]
verificado_em: 2026-10-05
valido_para: CWE 4.20
criado: 2026-10-05
decisao:
tags: [seguranca, cwe, container, isolamento]
---
# CWE-653 sessoes no mesmo container e mesmo UID so tem isolamento de processo - separe por usuario ou container

## Conteudo proposto

**O que e (MITRE):** o produto nao separa adequadamente funcoes ou recursos que exigem niveis de privilegio diferentes; uma falha na parte de menor privilegio alcanca a de maior. Consequencias: ganho de privilegio, contorno de protecoes.

**Como aparece no ambiente 01_IA:** varias tarefas/sessoes no mesmo container, mesmo UID, separadas so por sandbox de processo. Uma sessao comprometida (ex.: injecao via conteudo web) compartilha arquivos, home e credenciais com as outras.

**Mitigacoes (MITRE):** distribuir privilegios entre modulos/entidades distintos; minimizar interfaces entre componentes; controle de acesso forte nas fronteiras.
**Mitigacoes (OWASP Docker):** usuario sem privilegio (RULE #2), limitar capabilities (#3), `--security-opt=no-new-privileges` (#4), cuidado com conectividade entre containers (#5), seccomp/AppArmor/SELinux (#6).

**Controle verificavel (proposta, a validar):**
1. `docker inspect` mostra `User` nao root, `CapDrop` com `ALL` e `no-new-privileges`.
2. Teste de fronteira: de uma sessao, tentar ler o worktree e o home de outra sessao; deve ser negado (se for permitido, o isolamento e so de convencao).
3. Se o teste 2 falhar e o risco nao for aceito: UID distinto por tarefa ou um container por tarefa.

## Evidencia

Texto da pagina oficial CWE-653 (4.20) e das regras do OWASP Docker Security Cheat Sheet. Controles 1 a 3 sao inferencia do pesquisador.

## Links confiaveis

- [CWE-653](https://cwe.mitre.org/data/definitions/653.html): definicao, consequencias, mitigacoes.
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): regras 2 a 6 de endurecimento e isolamento do container.

## Por que e reaproveitavel

Decisao de isolamento entre tarefas (T-0019) e revisoes T-0020/T-0021; SEC-T0018-02.

## Relacionadas no Brain

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]
