---
tipo: pedido-coordenador
id: COORD-0007
status: concluido
urgencia: nao-bloqueante
pedido_por: dev
tarefa: T-0008
criado: 2026-10-01
atendido_em: 2026-10-01
adm:
tags: [lab, T-0008, docker, volume]
---
# COORD-0007 - Ajustar a posse do volume uploads da copia principal e remover volume de teste (T-0008)

## Pedido

- [x] Depois do merge da T-0008, na copia principal do projeto lab (`projetos/lab`), rodar uma vez (testado no worktree da tarefa, nao apaga nada):

  ```
  docker compose run --build --rm --no-deps -u 0 --entrypoint chown app -R 10001:10001 /uploads
  ```

  Sem isso, o `app` (uid 10001) nao grava no volume `uploads` antigo (arquivos de root): cadastro com imagem falha com `PermissionError`.

- [x] Remover o volume de teste criado pelo Dev (negado ao Dev). Pasta: qualquer.

  ```
  docker volume rm t-0008-endurecer-imagem_old
  ```

  Os volumes `t-0008-endurecer-imagem_uploads` e `_db_data` (projeto Compose da tarefa) tambem podem ser removidos apos o merge: `docker compose down -v` na pasta do worktree `T-0008-endurecer-imagem` (so ali, nunca na copia principal).

## Motivo

SEC-0004: a runtime passou a rodar sem root; volume existente nao muda de dono sozinho.

---

## Atendimento

Coordenador, 2026-10-01, com aprovacao do humano: depois do merge `d9b37b1` da T-0008, em `projetos/lab` rodei `docker compose run --build --rm --no-deps -u 0 --entrypoint chown app -R 10001:10001 /uploads` (rc 0). Conferido: `/uploads` 10001:10001 e nenhum arquivo com outro dono (`find /uploads ! -uid 10001` -> 0). Nada apagado. Volumes de teste `t-0008-endurecer-imagem_old`, `_db_data` e `_uploads` removidos por nome com `docker volume rm` (o `down -v` sugerido e negado ao perfil do Coordenador; mesmo efeito). `lab_db_data` e `lab_uploads` intactos. NAO verificado: upload real na copia principal (app nao estava rodando).
