---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/claude-desktop
tarefa: F2-2.1
confianca: alta
fontes: ["https://code.claude.com/docs/en/permissions", "teste no ambiente 01_IA em 2026-09-28"]
verificado_em: 2026-09-28
valido_para: "Claude Code 2.1.28x"
criado: 2026-09-28
decisao:
tags: [claude-code, permissoes]
---
# Exceção com ! em regra deny não desfaz regra absoluta

## Conteúdo proposto

No Claude Code, uma regra `deny` que começa com `!` (negação estilo gitignore) só abre exceção em regras **relativas** à pasta da sessão (`path` ou `./path`) listadas antes dela no mesmo arquivo. Ela **não** desfaz regras ancoradas com `//` (absoluta), `~/` ou `/`.

- `Read(//**/.env.*)` + `Read(!**/.env.example)` → `.env.example` continua bloqueado.
- `Read(**/.env.*)` + `Read(!**/.env.example)` → `.env.example` liberado, `.env.local` bloqueado.

Para liberar escrita só em algumas pastas ("tudo negado exceto X"), `Edit(**)` + `Edit(!X/**)` também não funcionou. A solução confiável foi um hook `PreToolUse` com lista de permissões.

## Evidência

Testado com `claude -p` e perfil `--settings` em worktree temporário: leitura de `.env.example` negada com a regra absoluta e liberada com a relativa; escrita do Revisor negada em `qualidade/` com `Edit(**)`/`Edit(!qualidade/**)` e liberada com o hook. A documentação de permissões confirma a limitação das regras ancoradas.

## Por que é reaproveitável

Todo perfil de papel novo que precise de "bloquear tudo exceto" vai cair nessa armadilha.

## Relacionadas no Brain

- [[ADR-0013 Lancador de papeis e identidade dos agentes]]
- [[ADR-0006 Modelo de permissoes]]

## Decisão do Bibliotecário
