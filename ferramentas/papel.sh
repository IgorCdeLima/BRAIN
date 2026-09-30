#!/bin/sh
# Lancador de papeis da equipe 01_IA (Linux/macOS). Uso: papel dev | engenheiro | revisor | designer | seguranca | pesquisador | bibliotecario | coordenador | administrador
# Pode ser chamado por um link no PATH (ex.: ~/.local/bin/papel): o caminho real e resolvido.
exec python3 "$(dirname "$(readlink -f "$0")")/papel.py" "$@"
