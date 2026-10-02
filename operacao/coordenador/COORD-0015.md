---
tipo: pedido-coordenador
id: COORD-0015
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0010
criado: 2026-10-01
atendido_em: 2026-10-02
adm:
tags: [lab, t-0010, volumes, limpeza]
---
# COORD-0015 - Remover volumes de teste do Revisor da T-0010 antes do merge

## Pedido

- [ ] Quando a T-0010 estiver `aprovada` e **antes do merge** (as proximas revisoes da correcao reutilizam o projeto `t0010-rev`), na pasta `/home/igor/orca/workspaces/lab/T-0010-imagem-pillow`:
  `docker compose -p t0010-rev down && docker volume rm t0010-rev_db_data t0010-rev_uploads`
  Esperado: os dois volumes removidos (`docker volume ls | grep t0010-rev` vazio). Sao so do projeto de verificacao do Revisor; nao tocam os volumes do humano (`lab_*`) nem os do Dev ou da Seguranca.

## Motivo

O Revisor usou o projeto Compose `t0010-rev` (porta 8110) no VER-T0010-01 e parou com `down` sem `-v`, como manda o `CLAUDE.md` do lab. Remover volume esta fora do perfil do Revisor.

---

## Atendimento

Coordenador, 2026-10-02, com aprovacao do humano, antes do merge da T-0010: na pasta do worktree, `docker compose -p t0010-rev down` (nenhum recurso ativo) e `docker volume rm t0010-rev_db_data t0010-rev_uploads` (removidos, junto com os do COORD-0018). `docker volume ls | grep t0010` vazio. Merge da T-0010 em seguida: `518b7c5`.
