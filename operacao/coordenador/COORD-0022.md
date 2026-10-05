---
tipo: pedido-coordenador
id: COORD-0022
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0014
criado: 2026-10-02
atendido_em: 2026-10-02
adm: ADM-0019
tags: [limpeza, docker]
---
# COORD-0022 - Remover volumes e imagens de teste do Revisor na T-0014

## Pedido

- [x] Remover os volumes de teste do Revisor (containers ja parados com `down`, sem `-v`). Pasta: qualquer (ex.: `projetos/lab`).
  `docker volume rm t0014-rev_db_data t0014-rev_uploads`
- [x] (Opcional) Remover as imagens de teste do Revisor: -> ADM-0019
  `docker image rm t0014-rev-app t0014-rev-test t0014-rev-lint t0014-rev-audit t0014-rev-lock-lock t0014-rev-neg-lock`

## Motivo

Sobras do VER-T0014-01 (projetos Compose `t0014-rev`, `t0014-rev-lock`, `t0014-rev-neg`). O Revisor nao remove volumes. Se houver nova revisao da T-0014, pode esperar e limpar tudo junto.

---

## Atendimento

Coordenador, 2026-10-02, com aprovacao do humano: volumes removidos (`docker volume rm t0014-rev_db_data t0014-rev_uploads t0014-seg_db_data t0014-seg_uploads`), incluindo as sobras da Seguranca (`t0014-seg_*`, Passos do humano da T-0014). Nenhum container `t0014*` existia. As imagens (`t0014-rev*`, `t0014-seg*`, `t0014-neg-lock`, `t0014-segc-lock`) ficam para o Administrador: `docker image rm` nao esta no perfil do Coordenador -> ADM-0019 (`escalado`).

Coordenador, 2026-10-05, com aprovacao do humano: ADM-0019 `concluido` (item 2, 2026-10-03: as 12 imagens `t0014-*` removidas com `docker image rm`, nenhum container usava). Pedido `concluido`.
