---
tipo: pedido-coordenador
id: COORD-0027
status: concluido
urgencia: nao-bloqueante
pedido_por: designer
tarefa: T-0013
criado: 2026-10-03
atendido_em: 2026-10-04
adm:
tags: [t-0013, fase, design, dev]
---
# COORD-0027 - T-0013: passar da fase 1 (design) para a fase 2 (Dev) apos o "sim" do humano

## Pedido

- [x] **So depois que o humano aprovar o prototipo** (Passos do humano do cartao T-0013, item "Ver o prototipo de `docs/design/T-0013/`"): no cartao `operacao/tarefas/T-0013.md`, trocar `papel: designer` por `papel: dev` e `status: aguardando-humano` por `status: pronta`. Se o humano pedir ajuste, nao trocar: voltar `status: pronta` com `papel: designer` para o Designer ajustar.

## Motivo

O cartao define que a passagem 1 -> 2 e feita pelo Coordenador com o "sim" do humano ("Fases", passagem 1 -> 2). O Designer nao muda o campo `papel:`. Fase 1 entregue no commit `14294d3` do branch `T-0013`.

---

## Atendimento

Coordenador, 2026-10-04: o humano aprovou o prototipo como entregue ("Pode ser a que ele esta fazendo"). No cartao T-0013: `papel: designer` -> `papel: dev`, `status: aguardando-humano` -> `status: pronta`, item dos Passos do humano marcado e referencia `[x]` em "Pedidos ao Coordenador". Proximo passo: `papel dev` no worktree `lab/T-0013`.
