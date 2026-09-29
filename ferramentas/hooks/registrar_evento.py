"""Hook do Claude Code: grava eventos dos agentes em D:\\01_IA\\logs (Markdown).

Formato definido em BRAIN/70_Workflows/Rastreabilidade.md.
Chamado com o JSON do evento na entrada padrão. Nunca falha: qualquer erro
interno é ignorado para não atrapalhar o agente.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ_LOGS = Path(os.environ.get("IA_LOGS_DIR", r"D:\01_IA\logs"))
DIR_ESTADO = RAIZ_LOGS / ".estado"

FERRAMENTAS_REGISTRADAS = {"Edit", "Write", "NotebookEdit", "Bash", "PowerShell"}

_NOMES_SEGREDO = r"(?:password|passwd|pwd|senha|secret|token|api[_-]?key|access[_-]?key)"
PADROES_SEGREDO = [
    # NOME=valor, NOME: valor (inclui POSTGRES_PASSWORD=..., API_KEY: ...)
    (re.compile(rf"(?i)(\b[\w-]*{_NOMES_SEGREDO}\s*[:=]\s*)\S+"), r"\1***"),
    # --password valor, --token valor
    (re.compile(rf"(?i)(--{_NOMES_SEGREDO}\s+)\S+"), r"\1***"),
    (re.compile(r"(?i)(\bbearer\s+)\S+"), r"\1***"),
    # usuario:senha@ em URLs de conexão
    (re.compile(r"(?i)(\b[a-z][a-z0-9+.-]*://[^\s:@/]+:)[^\s@/]+@"), r"\1***@"),
    (re.compile(r"\b(?:sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})\b"), "***"),
]


def mascarar(texto: str) -> str:
    for padrao, troca in PADROES_SEGREDO:
        texto = padrao.sub(troca, texto)
    return texto


def celula(texto, limite=160) -> str:
    texto = mascarar(str(texto or ""))
    texto = texto.replace("\r", " ").replace("\n", " ⏎ ").replace("|", "\\|").strip()
    return texto if len(texto) <= limite else texto[: limite - 1] + "…"


def branch_atual(cwd: str) -> str:
    try:
        saida = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=3,
        )
        return saida.stdout.strip() if saida.returncode == 0 else ""
    except Exception:
        return ""


def carregar_estado(sessao: str) -> dict:
    arquivo = DIR_ESTADO / f"{sessao}.json"
    try:
        return json.loads(arquivo.read_text(encoding="utf-8"))
    except Exception:
        return {}


def salvar_estado(sessao: str, estado: dict) -> None:
    DIR_ESTADO.mkdir(parents=True, exist_ok=True)
    (DIR_ESTADO / f"{sessao}.json").write_text(json.dumps(estado, ensure_ascii=False), encoding="utf-8")


def arquivo_sessao(evento: dict, agora: datetime) -> Path:
    sessao = evento.get("session_id", "desconhecida")
    estado = carregar_estado(sessao)
    if estado.get("arquivo") and Path(estado["arquivo"]).exists():
        return Path(estado["arquivo"])

    agente = evento.get("agent_type") or os.environ.get("IA_PAPEL") or "sem-papel"
    cwd = evento.get("cwd", "")
    curta = sessao[:8]
    pasta = RAIZ_LOGS / "sessoes" / agora.strftime("%Y-%m")
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / f"{agora:%Y-%m-%d_%H%M}_{re.sub(r'[^A-Za-z0-9_-]', '-', agente)}_{curta}.md"
    cabecalho = (
        "---\n"
        "tipo: log-sessao\n"
        f"sessao: {curta}\n"
        f"agente: {agente}\n"
        f"modelo: {evento.get('model', '')}\n"
        f"inicio: {agora.isoformat(timespec='seconds')}\n"
        f"cwd: {cwd.replace(chr(92), '/')}\n"
        f"branch: {branch_atual(cwd) if cwd else ''}\n"
        "---\n"
        f"# Sessão {agente} — {agora:%Y-%m-%d %H:%M}\n\n"
        "| Hora | Evento | Ferramenta | Resumo |\n"
        "|---|---|---|---|\n"
    )
    arquivo.write_text(cabecalho, encoding="utf-8")
    salvar_estado(sessao, {"arquivo": str(arquivo), "agente": agente})
    return arquivo


def registrar_erro(evento: dict, agora: datetime, nome: str, ferramenta: str, resumo: str) -> None:
    pasta = RAIZ_LOGS / "erros"
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / f"{agora:%Y-%m-%d}.md"
    if not arquivo.exists():
        arquivo.write_text(
            f"---\ntipo: log-erros\ndata: {agora:%Y-%m-%d}\n---\n# Erros — {agora:%Y-%m-%d}\n\n"
            "| Hora | Agente | Sessão | Evento | Ferramenta | Resumo |\n|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    sessao = evento.get("session_id", "")
    agente = carregar_estado(sessao).get("agente") or evento.get("agent_type") or os.environ.get("IA_PAPEL") or "sem-papel"
    with arquivo.open("a", encoding="utf-8") as f:
        f.write(f"| {agora:%H:%M:%S} | {celula(agente, 40)} | {sessao[:8]} | {nome} | {celula(ferramenta, 40)} | {celula(resumo, 240)} |\n")


def resumo_entrada(ferramenta: str, entrada: dict, cwd: str) -> str:
    if ferramenta in ("Bash", "PowerShell"):
        return entrada.get("command", "")
    caminho = entrada.get("file_path") or entrada.get("notebook_path") or ""
    try:
        return Path(caminho).resolve().relative_to(Path(cwd).resolve()).as_posix()
    except Exception:
        return caminho.replace("\\", "/")


def descrever(evento: dict):
    """Retorna (nome, ferramenta, resumo, é_erro) ou None se o evento não deve ser registrado."""
    tipo = evento.get("hook_event_name", "")
    ferramenta = evento.get("tool_name", "")
    entrada = evento.get("tool_input") or {}
    cwd = evento.get("cwd", "")

    if tipo == "SessionStart":
        return "inicio_sessao", "—", f"{evento.get('source', '')} · modo {evento.get('permission_mode', '')}", False
    if tipo == "SessionEnd":
        return "fim_sessao", "—", evento.get("reason", ""), False
    if tipo == "PostToolUse":
        if ferramenta not in FERRAMENTAS_REGISTRADAS:
            return None
        return "ferramenta_usada", ferramenta, resumo_entrada(ferramenta, entrada, cwd), False
    if tipo == "PostToolUseFailure":
        erro = evento.get("error")
        if isinstance(erro, dict):
            erro = (erro.get("error") or {}).get("message") or erro.get("message") or json.dumps(erro, ensure_ascii=False)
        return "ferramenta_falhou", ferramenta, f"{resumo_entrada(ferramenta, entrada, cwd)} → {erro}", True
    if tipo == "PermissionDenied":
        return "permissao_negada", ferramenta, f"{resumo_entrada(ferramenta, entrada, cwd)} (por: {evento.get('denied_by', '?')})", True
    if tipo == "StopFailure":
        return "falha_modelo", "—", f"{evento.get('error_type', '')}: {evento.get('error_message', '')}", True
    return None


AVISO_SEM_PAPEL = (
    "ATENCAO: esta sessao do Claude foi aberta SEM PAPEL (nao foi iniciada pelo lancador "
    "D:\\01_IA\\ferramentas\\papel). Sem papel voce nao tem perfil de permissoes e seus commits "
    "serao recusados pelo hook do Git. Antes de qualquer trabalho, avise o humano: ele deve fechar "
    "esta sessao e rodar 'D:\\01_IA\\ferramentas\\papel <dev|revisor|bibliotecario>' no terminal "
    "da pasta certa. Nao tente definir IA_PAPEL por conta propria."
)


def avisar_se_sem_papel(evento: dict) -> None:
    if evento.get("hook_event_name") != "SessionStart":
        return
    if evento.get("agent_type") or os.environ.get("IA_PAPEL"):
        return
    if os.environ.get("CLAUDE_CODE_ENTRYPOINT") == "claude-desktop":
        return
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": AVISO_SEM_PAPEL}}))


def main() -> None:
    evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    avisar_se_sem_papel(evento)
    descricao = descrever(evento)
    if descricao is None:
        return
    nome, ferramenta, resumo, e_erro = descricao
    agora = datetime.now().astimezone()
    arquivo = arquivo_sessao(evento, agora)
    with arquivo.open("a", encoding="utf-8") as f:
        f.write(f"| {agora:%H:%M:%S} | {nome} | {celula(ferramenta, 40)} | {celula(resumo)} |\n")
    if e_erro:
        registrar_erro(evento, agora, nome, ferramenta, resumo)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
