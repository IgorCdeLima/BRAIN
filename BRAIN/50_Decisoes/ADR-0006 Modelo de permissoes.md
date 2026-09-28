---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, seguranca, permissoes]
---
# ADR-0006 Modelo de permissões

## Contexto

Instruções em prompt ou `CLAUDE.md` não impedem ações; só as regras aplicadas pelo Claude Code, hooks e Git o fazem. O Orca inicia agentes com `--dangerously-skip-permissions` por padrão.

## Decisão

Defesa em camadas:

1. **Modo bypass proibido**: `disableBypassPermissionsMode` nas configurações pessoais e do projeto; opção removida do Orca.
2. **Regras comuns versionadas** em `01_IA/.claude/settings.json` (herdadas pelos worktrees):
   - **negar**: segredos (`.env`), `git push --force`, apagamentos recursivos;
   - **perguntar**: áreas N4 (`CLAUDE.md`, `.claude/`, `agentes/`, `BRAIN/60_Agentes`, `BRAIN/70_Workflows`) e `git push`.
3. **Modos por uso**: humano em Manual; agentes sem supervisão em `dontAsk` (o que perguntaria vira negado).
4. **Perfis por papel** (a validar na fase 0.12).
5. **Hooks do Git** como última proteção (fase 1).

Níveis: N0 ler · N1 propor (`00_Inbox`, `operacao/`) · N2 executar (próprio worktree) · N3 curar o Brain · N4 governar (só humano).

## Consequências

- **Positivas:** agentes sem supervisão não travam esperando aprovação nem alteram áreas críticas.
- **Negativas / riscos:** regras de comando comparam texto e podem ser contornadas — por isso a camada do Git; perfis por papel ainda não validados no Orca.
