---
tipo: pedido-coordenador
id: COORD-0009
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0008
criado: 2026-10-01
atendido_em: 2026-10-01
adm:
tags: [lab, docker, volume, limpeza]
---
# COORD-0009 - Remover os volumes de teste da revisao do Revisor da T-0008

## Pedido

- [x] Em qualquer pasta (nomes de volume sao globais), depois de confirmar que o projeto `t0008-rev` esta parado (`docker compose -p t0008-rev ps` vazio):
  `docker volume rm t0008-rev_db_data t0008-rev_uploads`
  Resultado esperado: os dois nomes impressos. Tem so dados de teste (produtos "RevOk", "V", "V2", "G" etc. e PNGs 4x4).

## Motivo

Volumes criados pelo Revisor na verificacao da T-0008 (projeto Compose `t0008-rev`, porta 8108), ja parado com `docker compose -p t0008-rev down` (sem `-v`). Apagar volume nao e do papel Revisor. Nao confundir com os volumes da copia principal (COORD-0007), que **nao** devem ser apagados.

---

## Atendimento

Coordenador, 2026-10-01, com aprovacao do humano: nenhum container do projeto `t0008-rev` existia; `docker volume rm t0008-rev_db_data t0008-rev_uploads` imprimiu os dois nomes. Volumes da copia principal intactos.
