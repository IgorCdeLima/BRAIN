"""Hook Stop: grava o total de tokens da sessão em <raiz>/logs/consumo/AAAA-MM.jsonl (ADM-0011).

Ligado na definição de cada papel (agentes/.claude/agents/*.md), para valer em qualquer projeto.
A cada fim de turno, soma a sessão inteira pela transcrição (transcript_path do evento), contando
cada resposta uma vez, e ACRESCENTA uma linha com o acumulado. O relatório (ferramentas/consumo.py)
usa a última linha de cada sessão. O log fica só com acréscimos, como os demais em logs/.

Linha: {"ts", "sessao", "papel", "tarefa", "modelos": {modelo: {input_tokens, cache_creation_input_tokens,
        cache_read_input_tokens, output_tokens, respostas}}}
Só números e identificadores; nunca conteúdo. Nunca falha.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from transcricoes import TAREFA, ler_arquivo, somar  # noqa: E402

RAIZ = Path(os.environ.get("IA_RAIZ") or r"D:\01_IA")
DIR_LOGS = Path(os.environ.get("IA_LOGS_DIR") or RAIZ / "logs") / "consumo"


def main() -> None:
    evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    if evento.get("hook_event_name") not in (None, "Stop", "SubagentStop", "SessionEnd"):
        return
    caminho = evento.get("transcript_path")
    if not caminho or not Path(caminho).is_file():
        return
    registros = list(ler_arquivo(Path(caminho)))
    modelos = somar(registros)
    if not modelos:
        return
    # So cartao T-####; o lancador da a papeis da copia principal rotulos como "admin-AAAA-MM-DD".
    m = TAREFA.search(os.environ.get("IA_TAREFA") or "")
    tarefa = m.group(0) if m else next((r["tarefa"] for r in registros if r["tarefa"]), "")
    agora = datetime.now().astimezone()
    linha = {
        "ts": agora.isoformat(timespec="seconds"),
        "sessao": str(evento.get("session_id") or "")[:36],
        "papel": os.environ.get("IA_PAPEL") or next((r["papel"] for r in registros if r["papel"] != "sem-papel"), "sem-papel"),
        "tarefa": tarefa,
        "modelos": modelos,
    }
    DIR_LOGS.mkdir(parents=True, exist_ok=True)
    with (DIR_LOGS / f"{agora:%Y-%m}.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
