# logs — telemetria dos agentes

Registro automático do que os agentes fazem, gravado por hooks do Claude Code. Formato Markdown com colunas fixas, para leitura humana e análise futura por ferramenta própria.

- **Fora do Git** (só este `_LEIAME.md` é versionado): é telemetria de alta frequência, escrita por todos os worktrees ao mesmo tempo.
- **Somente acréscimo.** Linhas existentes nunca são alteradas ou removidas.
- Sempre gravado aqui, na cópia principal `D:\01_IA\logs`, mesmo quando o agente trabalha num worktree — assim logs de tarefas descartadas não se perdem.
- O catálogo curado (bugs, verificações, segurança) fica em `qualidade/`, versionado. Um erro do log vira `BUG-####` quando um revisor o confirma.

## Estrutura

- `sessoes/AAAA-MM/AAAA-MM-DD_HHMM_<agente>_<sessao>.md` — todos os eventos de uma sessão.
- `erros/AAAA-MM-DD.md` — somente falhas do dia, de todas as sessões.

Formato detalhado em `BRAIN/70_Workflows/Rastreabilidade.md`. **Nunca** registrar segredos.
