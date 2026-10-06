---
tipo: pesquisa
id: SEARCH-0011
status: respondida
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0018
criado: 2026-10-05
pesquisado_por: pesquisador
pesquisado_em: 2026-10-05
catalogado_em:
notas: []
tags: [seguranca, cwe, container, credencial, isolamento, cadeia-de-suprimento]
---
# SEARCH-0011 - Notas de referencia para CWE-522, CWE-653 e CWE-494

## Pergunta

Para cada CWE abaixo: definicao oficial (MITRE), consequencias, mitigacoes recomendadas e um controle verificavel aplicavel a um ambiente de agentes de IA num container Linux sem privilegio:

1. **CWE-522** (credenciais protegidas de forma insuficiente): credencial de ferramenta (token OAuth) legivel por processos do mesmo usuario.
2. **CWE-653** (isolamento ou compartimentacao inadequados): varias sessoes/tarefas no mesmo container, mesmo UID, separadas so por sandbox de processo.
3. **CWE-494** (download de codigo sem verificacao de integridade): instalador `curl | bash` e atualizacao automatica; como conferir manifesto assinado.

## Contexto

Revisao de seguranca da T-0018 (projeto `ambiente`): SEC-T0018-01 (CWE-522), SEC-T0018-02 (CWE-653) e SEC-T0018-04 (CWE-494) citam so o link do MITRE; o Brain nao tem nota dessas CWE. Serve para a analise de ameacas da T-0019 e as revisoes da T-0020/T-0021. Fontes esperadas: cwe.mitre.org, OWASP Cheat Sheet Series (Docker Security, Secrets Management).

## Ja buscado no Brain

Busca por `CWE-522`, `CWE-653`, `CWE-494` em `10_Conhecimento`, `30_Referencias` e `00_Inbox`: nenhuma nota. [[Mapa das CWE relevantes para Python e FastAPI]] nao as cobre. Proximas mas diferentes: [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]], [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]].

---

## Resposta

- **Resumo (3 a 5 linhas):** Definicao, consequencias e mitigacoes das tres CWE conferidas na fonte oficial (MITRE, CWE 4.20). CWE-522: proteger o token (0600, segredo injetado, escopo minimo). CWE-653: mesmo UID no mesmo container so da isolamento de processo; endurecer (USER, cap-drop, no-new-privileges) e testar a fronteira entre sessoes. CWE-494: o Claude Code publica manifesto assinado com GPG (2.1.89+), com fingerprint e passos de verificacao; fixar versao e usar DISABLE_UPDATES.
- **Notas geradas no Inbox:** [[CWE-522 token de ferramenta legivel pelo mesmo usuario se trata com permissao 0600 e escopo minimo]], [[CWE-653 sessoes no mesmo container e mesmo UID so tem isolamento de processo - separe por usuario ou container]], [[CWE-494 curl pipe bash e atualizacao automatica se mitigam conferindo o manifesto assinado com gpg]]
- **Links confiaveis:** cwe.mitre.org (522, 653, 494); cheatsheetseries.owasp.org (Docker Security); code.claude.com/docs/en/setup.
- **Sem resposta / limites:** Os "controles verificaveis" sao inferencia minha a partir das mitigacoes, marcados como proposta nas notas. Nao li o OWASP Secrets Management Cheat Sheet nem a documentacao de armazenamento de credenciais do Claude Code (local e permissoes do arquivo do token nao confirmados).
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

- cwe.mitre.org e cheatsheetseries.owasp.org (se ainda nao constarem): fonte primaria das notas de CWE.
- code.claude.com e downloads.claude.ai: documentacao e manifesto assinado do Claude Code, necessarios para a verificacao de integridade (CWE-494).

## Catalogacao
