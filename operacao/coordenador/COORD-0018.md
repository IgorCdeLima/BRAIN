---
tipo: pedido-coordenador
id: COORD-0018
status: concluido
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0010
criado: 2026-10-02
atendido_em: 2026-10-02
adm:
tags: [lab, t-0010, volumes, limpeza]
---
# COORD-0018 - Remover volumes de teste da Seguranca da T-0010 antes do merge

## Pedido

- [ ] Quando a T-0010 estiver `aprovada` e **antes do merge** (a reverificacao do SEC-T0010-03 reutiliza o projeto `t0010-seg`), na pasta `/home/igor/orca/workspaces/lab/T-0010-imagem-pillow`:
  `docker compose -p t0010-seg down && docker volume rm t0010-seg_db_data t0010-seg_uploads`
  Esperado: os dois volumes removidos (`docker volume ls | grep t0010-seg` vazio). Sao so do projeto de teste da Seguranca (porta 8310); nao tocam os volumes do humano (`lab_*`) nem os do Dev ou do Revisor (`t0010-rev_*`, COORD-0015). O volume `t0010-seg_uploads` tem centenas de imagens de teste (WebP 50 MP regravados, poliglotas ja limpos).

## Motivo

A Seguranca usou o projeto Compose `t0010-seg` nas duas revisoes da T-0010 e parou com `down` sem `-v`, como manda o `CLAUDE.md` do lab. Remover volume esta fora do perfil da Seguranca.

---

## Atendimento

Coordenador, 2026-10-02, com aprovacao do humano, antes do merge da T-0010: na pasta do worktree, `docker compose -p t0010-seg down` (nenhum recurso ativo) e `docker volume rm t0010-seg_db_data t0010-seg_uploads` (removidos). `docker volume ls | grep t0010` vazio. Merge da T-0010 em seguida: `518b7c5`.
