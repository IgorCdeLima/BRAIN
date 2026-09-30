#!/bin/sh
# Lancador de papeis da equipe 01_IA (Linux/macOS). Uso: ferramentas/papel.sh dev | engenheiro | revisor | designer | seguranca | bibliotecario | coordenador
exec python3 "$(dirname "$0")/papel.py" "$@"
