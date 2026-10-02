"""Hook PostToolUse: registra cada acesso ao Brain em <raiz>/logs/brain/AAAA-MM.jsonl (ADM-0017).

Ligado na definição de cada papel (agentes/.claude/agents/*.md), matcher Read|Bash|PowerShell,
para valer em qualquer projeto. Uma linha JSON por acesso:

    {"ts": "...", "papel": "...", "tarefa": "...", "sessao": "...", "ferramenta": "Read",
     "tipo": "leitura" | "busca", "pasta": "10_Conhecimento", "nota": "Titulo da nota" | null}

Grava SOMENTE o caminho resolvido. Nunca o comando inteiro nem conteúdo (pode haver segredo).
Nunca falha: qualquer erro é ignorado para não atrapalhar o agente.
O relatório fica em ferramentas/uso_brain.py, que importa extrair_acessos daqui.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(os.environ.get("IA_RAIZ") or r"D:\01_IA")
DIR_LOGS = Path(os.environ.get("IA_LOGS_DIR") or RAIZ / "logs") / "brain"

PASTA = r"\d\d_[A-Za-z_]+"
# BRAIN/<pasta>[/<subpastas>/<nota>.md] num comando (caminho relativo ou absoluto, entre aspas ou nao).
CAMINHO_CMD = re.compile(rf"BRAIN/({PASTA})(?:/([^\"'\n*?|;&<>]*?\.md))?")


def _nota(caminho: str):
    nome = Path(caminho).name
    if not nome.endswith(".md") or nome.startswith("_"):
        return None  # pasta, _LEIAME ou arquivo que nao e nota
    return Path(nome).stem


def extrair_acessos(ferramenta: str, entrada: dict, raiz: Path):
    """Lista de (tipo, pasta, nota) que esta chamada de ferramenta fez no Brain."""
    acessos = []
    if ferramenta == "Read":
        caminho = str(entrada.get("file_path") or "").replace("\\", "/")
        base = (raiz.as_posix().rstrip("/") + "/BRAIN/").lower()
        if caminho.lower().startswith(base):
            partes = caminho[len(base):].split("/")
            if re.fullmatch(PASTA, partes[0]):
                nota = _nota(caminho)
                acessos.append(("leitura" if nota else "busca", partes[0], nota))
    elif ferramenta in ("Bash", "PowerShell"):
        comando = str(entrada.get("command") or "").replace("\\", "/")
        vistos = set()
        for pasta, resto in CAMINHO_CMD.findall(comando):
            nota = _nota(resto) if resto else None
            if (pasta, nota) not in vistos:
                vistos.add((pasta, nota))
                acessos.append(("leitura" if nota else "busca", pasta, nota))
    return acessos


def main() -> None:
    evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    if evento.get("hook_event_name") not in (None, "PostToolUse"):
        return
    acessos = extrair_acessos(evento.get("tool_name", ""), evento.get("tool_input") or {}, RAIZ)
    if not acessos:
        return
    agora = datetime.now().astimezone()
    comum = {
        "ts": agora.isoformat(timespec="seconds"),
        "papel": os.environ.get("IA_PAPEL") or evento.get("agent_type") or "sem-papel",
        "tarefa": os.environ.get("IA_TAREFA") or "",
        "sessao": str(evento.get("session_id") or "")[:36],
        "ferramenta": evento.get("tool_name", ""),
    }
    DIR_LOGS.mkdir(parents=True, exist_ok=True)
    with (DIR_LOGS / f"{agora:%Y-%m}.jsonl").open("a", encoding="utf-8") as f:
        for tipo, pasta, nota in acessos:
            f.write(json.dumps({**comum, "tipo": tipo, "pasta": pasta, "nota": nota}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
