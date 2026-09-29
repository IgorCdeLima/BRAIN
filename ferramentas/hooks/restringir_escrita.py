"""Hook PreToolUse: permite escrita de arquivos SOMENTE nos caminhos listados.

Uso (na definição do papel, em hooks.PreToolUse com matcher Edit|Write|NotebookEdit):
    py -3 D:/01_IA/ferramentas/hooks/restringir_escrita.py <prefixo> [<prefixo> ...]

Prefixos relativos são resolvidos a partir da pasta da sessão (cwd); absolutos
valem como estão. Qualquer escrita fora deles é negada, com o motivo explicado
ao agente. Diferente de uma lista de bloqueios, isto é uma lista de permissões.
"""

import json
import sys
from pathlib import Path


def normalizar(caminho: Path) -> str:
    return str(caminho.resolve()).replace("\\", "/").rstrip("/").lower()


def main() -> None:
    evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    entrada = evento.get("tool_input") or {}
    alvo = entrada.get("file_path") or entrada.get("notebook_path")
    if not alvo:
        return
    cwd = Path(evento.get("cwd") or ".")
    alvo_abs = Path(alvo) if Path(alvo).is_absolute() else cwd / alvo
    alvo_n = normalizar(alvo_abs)

    permitidos = []
    for prefixo in sys.argv[1:]:
        p = Path(prefixo)
        permitidos.append(normalizar(p if p.is_absolute() else cwd / p))

    if any(alvo_n == p or alvo_n.startswith(p + "/") for p in permitidos):
        return

    motivo = (
        f"Este papel so pode escrever em: {', '.join(sys.argv[1:])}. "
        f"Escrita em '{alvo}' negada. Nao tente outro caminho: registre o que precisa ser mudado "
        "no VER/BUG ou no cartao da tarefa."
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": motivo,
    }}))


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:
        # Na dúvida, nega: um hook de restrição quebrado não pode liberar escrita.
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"restringir_escrita falhou ({erro}); escrita negada por seguranca.",
        }}))
    sys.exit(0)
