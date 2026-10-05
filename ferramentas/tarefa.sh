#!/bin/sh
# Quadro de tarefas da equipe 01_IA (worktree + tmux). Uso: tarefa aceitar|abrir|listar|fechar ...
# Pode ser chamado por um link no PATH (ex.: ~/.local/bin/tarefa): o caminho real e resolvido.
exec python3 "$(dirname "$(readlink -f "$0")")/tarefa.py" "$@"
