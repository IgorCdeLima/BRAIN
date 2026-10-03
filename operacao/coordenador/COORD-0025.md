---
tipo: pedido-coordenador
id: COORD-0025
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0015
criado: 2026-10-03
atendido_em: 2026-10-03
adm:
tags: [lab, t-0015, limpeza, volumes]
---
# COORD-0025 - Remover os volumes de teste da T-0015 no fechamento

## Pedido

- [ ] Depois do merge da T-0015 (aprovada pelo Revisor em VER-T0015-02, commit `7282de6`), em qualquer pasta (comando global do Docker):

  ```bash
  docker volume rm t0015-rev_db_data t0015-rev_uploads t0015-oom_db_data t0015-oom_uploads t-0015-endurecer-app_db_data t-0015-endurecer-app_uploads
  ```

  Esperado: os seis nomes impressos, sem erro. Todos os projetos ja estao parados com `down` (sem `-v`). Se algum der "volume is in use", rodar antes `docker compose -p <projeto> down` (sem `-v`) na pasta do worktree `T-0015-endurecer-app`.

- Os volumes `t0015-seg_db_data` e `t0015-seg_uploads` (Seguranca) ja estao pedidos no COORD-0024; podem ir no mesmo comando.

## Motivo

Volumes de teste da revisao (`t0015-rev`, do Revisor), do teste de OOM do Dev (`t0015-oom`) e do projeto do Dev (`t-0015-endurecer-app`). Sao so dados de teste; nenhum e o banco da copia principal. O Revisor nao remove volumes (perfil) e nunca usa `down -v`.

---

## Atendimento

Coordenador, 2026-10-03: depois do merge da T-0015 (`ee1ba22`), com a aprovacao do humano, rodei `docker volume rm` dos seis volumes acima e tambem dos dois `t0015-seg_*` do COORD-0024. Os oito nomes foram impressos, sem erro e sem volume em uso.
