---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, git]
---
# ADR-0003 Git como fonte de verdade

## Contexto

O Vault tem o Obsidian Sync ativo, e o ambiente passa a ser versionado com Git. Duas sincronizações sobre os mesmos arquivos podem gerar conflitos.

## Decisão

- **Git é a fonte de verdade** de todo o ambiente (Brain, regras, workflows, operação).
- O Obsidian Sync é usado apenas para leitura e captura rápida no celular.
- O `.git` fica em `01_IA`, fora do Vault.
- Toda alteração de agente é rastreável: commits com trailers `Agente`, `Tarefa` e `Modelo`.

## Consequências

- **Positivas:** histórico completo e reversível de conhecimento, prompts e workflows; fluxo propor → revisar → aprovar → registrar.
- **Negativas / riscos:** edições feitas no celular precisam ser commitadas no PC; conflito possível se o mesmo arquivo for editado nos dois lados.
