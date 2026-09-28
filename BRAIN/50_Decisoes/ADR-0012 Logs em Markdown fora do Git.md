---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, rastreabilidade, logs]
---
# ADR-0012 Logs em Markdown fora do Git

## Contexto

[[ADR-0009 Catalogo de qualidade]] previa logs em JSONL em `operacao/logs`, versionados. Com agentes em worktrees, logs versionados geram conflito de merge (vários branches acrescentando no mesmo arquivo) e se perdem quando a tarefa é descartada.

## Decisão

- Logs em **Markdown** com colunas fixas (legível no Obsidian e parseável por ferramenta futura).
- Pasta dedicada **`D:\01_IA\logs`**, sempre na cópia principal, **fora do Git** (só o `_LEIAME.md` é versionado).
- Um arquivo por sessão + um arquivo de erros por dia.
- Gravados apenas por hooks do Claude Code; agentes não escrevem na pasta.
- Substitui a parte de logs do ADR-0009; o restante do ADR-0009 continua válido.

## Consequências

- **Positivas:** sem conflitos de merge; logs de tarefas descartadas preservados; um único lugar para a futura ferramenta de análise.
- **Negativas / riscos:** logs não têm histórico nem backup pelo Git — perda de disco perde os logs. O catálogo curado (`qualidade/`) continua versionado.
