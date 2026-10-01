---
tipo: pedido-coordenador
id: COORD-0008
status: concluido
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0008
criado: 2026-10-01
atendido_em: 2026-10-01
adm:
tags: [lab, docker, volume, limpeza]
---
# COORD-0008 - Remover os volumes de teste da revisao de seguranca da T-0008

## Pedido

- [x] Na pasta `/home/igor/orca/workspaces/lab/T-0008-endurecer-imagem` (ou em qualquer pasta, porque os nomes sao globais), depois de confirmar que o projeto `t0008-seg` esta parado:
  `docker volume rm t0008-seg_db_data t0008-seg_uploads`
  Resultado esperado: os dois nomes impressos. Tem so dados de teste (produtos "Teste", "Teste2", "Teste3", "Hard" e PNGs 4x4).

## Motivo

Volumes criados pela Seguranca na revisao da T-0008 (projeto Compose `t0008-seg`, porta 8308), ja parado com `docker compose -p t0008-seg down` (sem `-v`). Apagar volume e negado ao papel Seguranca. Nao confundir com os volumes da copia principal (COORD-0007), que **nao** devem ser apagados.

---

## Atendimento

Coordenador, 2026-10-01, com aprovacao do humano: nenhum container do projeto `t0008-seg` existia; `docker volume rm t0008-seg_db_data t0008-seg_uploads` imprimiu os dois nomes. Volumes da copia principal intactos.
