---
tipo: aprendizado
status: ativo
origem: agente/claude-desktop (candidato da tarefa T-0001, curado pelo Bibliotecário)
confianca: alta
fontes: ["operacao/tarefas/T-0001.md", "projetos/lab: VER-0001, VER-0002, BUG-0001, BUG-0002"]
verificado_em: 2026-09-29
valido_para: fluxo de tarefa v2
criado: 2026-09-29
tags: [retrospectiva, fluxo, agentes]
decisao: promovido
---
# Primeira tarefa com papéis mostrou que o repasse por arquivos funciona

## O que aconteceu

A T-0001 teve duas execuções. No piloto 1, as sessões rodaram sem papel e o humano copiava conversas entre elas. No piloto 2, com o lançador `papel`, o ciclo Dev → Revisor (reprovou, 2 bugs) → Dev → Revisor (aprovou) → merge → Bibliotecário correu só com cartão, commits e `qualidade/` como canal.

## O que aprendemos

- Revisor com modelo diferente (Opus) e reexecução independente achou um defeito real (versão do PostgreSQL) que o Dev (Sonnet) havia justificado com premissas erradas.
- "Um VER por commit" e "quem corrige não verifica" foram respeitados sem intervenção.
- O Revisor isolou a verificação num projeto Compose próprio (`-p`, outra porta), sem depender do ambiente do Dev.
- Agentes pararam diante de bloqueios de permissão e explicaram a causa, sem contornar.

## O que muda a partir de agora

1. **Consultar o Brain antes de pesquisar, inclusive o Inbox.** O que evitaria o BUG-0001 já estava no Inbox, e o Dev não consultou. Ver [[Imagem postgres 18+ monta o volume em var-lib-postgresql]].
2. **Worktrees em paralelo disputam porta e volumes** (8000, `db_data`): adotar nome de projeto Compose e porta por worktree.
3. **Candidatos também saem das correções**: o Dev registrou "nenhum candidato" apesar de ter aprendido algo ao corrigir (ver [[Listagem de tags do Docker Hub e paginada - confirme a tag diretamente]]).
4. **Etapas manuais do humano** (recriar volume, limpar volumes de teste, merge) devem ficar numa seção própria do cartão.

Os itens 2 e 4 dependem de mudança em workflow/template (área N4): ficam como proposta ao humano.

## Origem

Cartão T-0001 (Entrega e Revisão, rodadas 1 e 2), VER-0001/0002, BUG-0001/0002 no `lab`, merge `6a729d2`. Contexto: [[ADR-0013 Lancador de papeis e identidade dos agentes]].

## Decisão do Bibliotecário

**Promovido** em 2026-09-29. Sem duplicata. Evidência: cartão e registros de qualidade citados. Itens 2 e 4 exigem alteração em `70_Workflows`/templates de tarefa, que o Bibliotecário não edita: o humano decide.
