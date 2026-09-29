---
tipo: candidato
status: inbox
tipo_proposto: aprendizado
origem: agente/claude-desktop
tarefa: T-0001
confianca: alta
fontes: ["operacao/tarefas/T-0001.md", "operacao/tarefas/_arquivo/piloto-1", "projetos/lab: VER-0001, VER-0002, BUG-0001, BUG-0002"]
verificado_em: 2026-09-29
valido_para: "fluxo de tarefa v2"
criado: 2026-09-29
decisao:
tags: [retrospectiva, fluxo, agentes]
---
# Primeira tarefa com papéis mostrou que o repasse por arquivos funciona

## Conteúdo proposto

**O que aconteceu.** A T-0001 teve duas execuções. No piloto 1, todas as sessões rodaram sem papel e o humano copiava conversas entre elas. No piloto 2, com o lançador `papel`, o ciclo Dev → Revisor (reprovou, 2 bugs) → Dev → Revisor (aprovou) → merge → Bibliotecário aconteceu só com cartão, commits e `qualidade/` como canal.

**O que funcionou.**
- Revisor com modelo diferente (Opus) e reexecução independente achou um defeito real (versão do PostgreSQL) que o Dev (Sonnet) havia justificado com premissas erradas.
- "Um VER por commit" e "quem corrige não verifica" foram respeitados sem intervenção.
- O Revisor isolou sua verificação num projeto Compose próprio (`-p`, outra porta) para não depender do ambiente deixado pelo Dev.
- Agentes pararam diante de bloqueios de permissão e explicaram a causa, em vez de contornar.

**O que mudar.**
1. **Consultar o Brain antes de pesquisar, inclusive o Inbox.** A informação que evitaria o BUG-0001 (PostgreSQL 18 e o novo caminho do volume) já estava no `00_Inbox` e o Dev não a consultou.
2. **Worktrees em paralelo vão disputar porta e volumes** (8000, `db_data`). Convém um padrão: nome de projeto Compose e porta por worktree.
3. **O Dev registrou "nenhum candidato"** mesmo tendo aprendido algo novo na correção (listagem paginada do Docker Hub). Candidatos também devem sair das correções.
4. **Etapas manuais do humano** (recriar volume, limpar volumes de teste, merge) deveriam estar listadas numa seção própria do cartão, não espalhadas.

## Evidência

Cartão T-0001 (Entrega e Revisão, rodadas 1 e 2), VER-0001/VER-0002 e BUG-0001/BUG-0002 no repositório `lab`, merge `6a729d2`, logs de sessão de 2026-09-28.

## Por que é reaproveitável

Orienta os ajustes do fluxo antes da T-0002 e da entrada de novos papéis (Engenheiro de Software, Coordenador).

## Relacionadas no Brain

- [[ADR-0013 Lancador de papeis e identidade dos agentes]]
- [[Imagem postgres 18+ monta o volume em var-lib-postgresql]]

## Decisão do Bibliotecário
