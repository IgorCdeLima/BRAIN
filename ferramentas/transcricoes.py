"""Leitor comum das transcrições do Claude Code (~/.claude/projects/*/*.jsonl).

Usado por uso_brain.py (ADM-0017), consumo.py e hooks/registrar_consumo.py (ADM-0011).
Somente leitura. Devolve metadados e números; quem chama decide o que usar.
Nunca devolve o texto das mensagens, só os blocos tool_use (nome e entrada) para quem
precisa dos caminhos lidos.

Armadilha: uma resposta do modelo aparece em várias linhas (uma por bloco de conteúdo),
todas com o mesmo message.id e o mesmo usage. Para somar tokens, use só as linhas com
"usage_novo" preenchido (primeira vez daquela resposta na sessão).
"""

import json
import re
from pathlib import Path

TAREFA = re.compile(r"\bT-\d{4}\b")
CAMPOS_USAGE = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def tarefa_de(branch: str, cwd: str) -> str:
    m = TAREFA.search(branch or "") or TAREFA.search(cwd or "")
    return m.group(0) if m else ""


def do_ambiente(cwd: str, branch: str, raiz: Path) -> bool:
    """Sessão do 01_IA: na cópia principal (ou abaixo dela) ou num worktree de tarefa T-####."""
    c = (cwd or "").replace("\\", "/").lower()
    return c.startswith(raiz.as_posix().lower()) or bool(tarefa_de(branch, cwd))


def ler_arquivo(arq: Path):
    """Gera um dict por linha de resposta (type=assistant) de uma transcrição."""
    papel = None
    vistos = set()
    with Path(arq).open(encoding="utf-8", errors="replace") as f:
        for linha in f:
            try:
                r = json.loads(linha)
            except ValueError:
                continue
            if "agentSetting" in r:
                papel = r.get("agentSetting") or papel
            msg = r.get("message") or {}
            if r.get("type") != "assistant" or not isinstance(msg, dict):
                continue
            usage_novo = None
            u = msg.get("usage")
            mid = msg.get("id") or r.get("requestId") or r.get("uuid")
            if isinstance(u, dict) and mid not in vistos:
                vistos.add(mid)
                usage_novo = {k: int(u.get(k) or 0) for k in CAMPOS_USAGE}
            conteudo = msg.get("content") if isinstance(msg.get("content"), list) else []
            yield {
                "sessao": r.get("sessionId") or r.get("session_id") or "",
                "papel": papel or "sem-papel",
                "cwd": r.get("cwd") or "",
                "branch": r.get("gitBranch") or "",
                "tarefa": tarefa_de(r.get("gitBranch"), r.get("cwd")),
                "ts": r.get("timestamp") or "",
                "dia": (r.get("timestamp") or "")[:10],
                "modelo": msg.get("model") or "",
                "usage_novo": usage_novo,
                "ferramentas": [
                    {"nome": c.get("name", ""), "entrada": c.get("input") or {}}
                    for c in conteudo if isinstance(c, dict) and c.get("type") == "tool_use"
                ],
            }


def ler_transcricoes(dir_tr: Path, raiz: Path, desde: str = "", ignorar_sessoes=(), so_ambiente: bool = True):
    """Todas as transcrições (inclui subagentes em subpastas), filtradas por data e ambiente."""
    dir_tr = Path(dir_tr)
    arquivos = list(dir_tr.glob("*/*.jsonl")) + list(dir_tr.glob("*/*/subagents/*.jsonl"))
    for arq in arquivos:
        for rec in ler_arquivo(arq):
            if rec["sessao"] in ignorar_sessoes or (desde and rec["dia"] < desde):
                continue
            if so_ambiente and not do_ambiente(rec["cwd"], rec["branch"], raiz):
                continue
            yield rec


def somar(registros) -> dict:
    """{modelo: {campo: total, 'respostas': n}} somando só usage_novo."""
    total = {}
    for rec in registros:
        u = rec["usage_novo"]
        if not u or rec["modelo"] == "<synthetic>":
            continue
        t = total.setdefault(rec["modelo"] or "?", dict.fromkeys(CAMPOS_USAGE, 0) | {"respostas": 0})
        for k in CAMPOS_USAGE:
            t[k] += u[k]
        t["respostas"] += 1
    return total
