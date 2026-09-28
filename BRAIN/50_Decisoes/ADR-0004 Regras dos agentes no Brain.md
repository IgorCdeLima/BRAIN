---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, agentes]
---
# ADR-0004 Regras dos agentes no Brain

## Contexto

As regras de cada agente precisam ser fáceis de ler e editar pelo humano, mas as ferramentas (Orca, Claude Code) exigem arquivos em formatos próprios.

## Decisão

- A fonte de verdade das regras e prompts é `BRAIN/60_Agentes` (e processos em `BRAIN/70_Workflows`).
- Os arquivos em `01_IA/agentes/` são mínimos e apenas apontam para essas notas e definem permissões.
- Essas áreas são N4: só o humano altera. **Um agente nunca edita as próprias regras.**

## Consequências

- **Positivas:** uma única versão das regras, editável no Obsidian e versionada no Git.
- **Negativas / riscos:** a proteção precisa ser técnica (regras de permissão e hooks), não apenas escrita.
