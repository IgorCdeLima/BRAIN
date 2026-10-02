"""Hook PreToolUse: permite escrita de arquivos SOMENTE nos caminhos listados.

Uso (na definição do papel, em hooks.PreToolUse com matcher Edit|Write|NotebookEdit):
    py -3 D:/01_IA/ferramentas/hooks/restringir_escrita.py <prefixo> [<prefixo> ...]

Prefixos relativos são resolvidos a partir da pasta em que a sessão começou
(CLAUDE_PROJECT_DIR, o worktree), que não muda com `cd`; sem essa variável, a
pasta atual do evento. Prefixos absolutos valem como estão.

Token especial `@scratchpad`: libera o scratchpad DESTA sessão do Claude Code
(<pasta temporária>/claude*/<projeto>/<session_id>/scratchpad/...). O de outra
sessão continua negado; sem session_id válido, o token não libera nada.

Qualquer escrita fora deles é negada, com o motivo explicado ao agente.
Diferente de uma lista de bloqueios, isto é uma lista de permissões (ADM-0015).
"""

import json
import os
import re
import sys
import tempfile
from pathlib import Path

TOKEN_SCRATCHPAD = "@scratchpad"
SESSAO_VALIDA = re.compile(r"^[A-Za-z0-9_-]+$")


def normalizar(caminho: Path) -> str:
    return str(caminho.resolve()).replace("\\", "/").rstrip("/").lower()


def pasta_da_sessao(evento: dict) -> Path:
    # O cwd do evento é a pasta ATUAL e muda com `cd`; CLAUDE_PROJECT_DIR é a pasta
    # em que o Claude Code foi aberto. Sem a variável, mantém o comportamento antigo.
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or evento.get("cwd") or ".")


def no_scratchpad_da_sessao(alvo_n: str, evento: dict) -> bool:
    """alvo_n já está resolvido (sem links simbólicos nem `..`) e em minúsculas."""
    sessao = str(evento.get("session_id") or "")
    if not SESSAO_VALIDA.match(sessao):
        return False
    base_n = normalizar(Path(tempfile.gettempdir()))
    if not alvo_n.startswith(base_n + "/"):
        return False
    partes = alvo_n[len(base_n) + 1:].split("/")
    # claude-<uid>/<projeto>/<session_id>/scratchpad/<arquivo...>
    return (
        len(partes) >= 5
        and partes[0].startswith("claude")
        and partes[2] == sessao.lower()
        and partes[3] == "scratchpad"
    )


def main() -> None:
    evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    entrada = evento.get("tool_input") or {}
    alvo = entrada.get("file_path") or entrada.get("notebook_path")
    if not alvo:
        return
    # Alvo relativo segue a pasta atual (como a ferramenta o interpreta).
    cwd_atual = Path(evento.get("cwd") or ".")
    alvo_abs = Path(alvo) if Path(alvo).is_absolute() else cwd_atual / alvo
    alvo_n = normalizar(alvo_abs)

    raiz = pasta_da_sessao(evento)
    permitidos = []
    for prefixo in sys.argv[1:]:
        if prefixo == TOKEN_SCRATCHPAD:
            if no_scratchpad_da_sessao(alvo_n, evento):
                return
            continue
        p = Path(prefixo)
        permitidos.append(normalizar(p if p.is_absolute() else raiz / p))

    if any(alvo_n == p or alvo_n.startswith(p + "/") for p in permitidos):
        return

    lista = ", ".join(
        "@scratchpad (scratchpad desta sessao)" if a == TOKEN_SCRATCHPAD else a for a in sys.argv[1:]
    )
    motivo = (
        f"Este papel so pode escrever em: {lista}. Prefixos relativos valem a partir da pasta "
        f"em que a sessao comecou ({raiz}). "
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
