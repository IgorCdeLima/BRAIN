"""Hooks do Git compartilhados pelos repositórios do ambiente 01_IA.

Uso (chamado pelos scripts em <repo>/.githooks/):
    py -3 verificar_commit.py pre-commit
    py -3 verificar_commit.py commit-msg <arquivo-da-mensagem>

As regras só valem para commits de agentes, identificados pela variável de
ambiente IA_PAPEL (definida pelo lancador ferramentas/papel ao iniciar cada papel).
Commits humanos (sem IA_PAPEL) passam sem restrição.

Regras de cada repositório: <repo>/.githooks/regras.json
    {
      "protegidos": ["CLAUDE.md", ".claude/"],            # nenhum agente altera
      "livres": ["BRAIN/00_Inbox/"],                       # qualquer agente altera
      "restritos": {"qualidade/": ["revisor", "seguranca"]}  # só os papéis listados
    }
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

PADRAO_TAREFA = re.compile(r"\b(T-\d{4}|F\d+-\d+(?:\.\d+)?)\b")
TRAILERS = ("Agente", "Tarefa", "Modelo")
RE_NOSSO = re.compile(r"^(Agente|Tarefa|Modelo):\s*(.+)$")
RE_TRAILER = re.compile(r"^[A-Za-z][A-Za-z0-9-]*:\s")  # linha "Chave: valor" (ex.: Co-Authored-By)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8").stdout.strip()


def falhar(mensagem: str) -> None:
    print(f"\n[01_IA] Commit recusado: {mensagem}\n", file=sys.stderr)
    sys.exit(1)


def carregar_regras() -> dict:
    arquivo = Path(git("rev-parse", "--show-toplevel")) / ".githooks" / "regras.json"
    try:
        return json.loads(arquivo.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except Exception as erro:
        falhar(f"nao consegui ler {arquivo}: {erro}")


def casa(caminho: str, prefixo: str) -> bool:
    return caminho == prefixo or (prefixo.endswith("/") and caminho.startswith(prefixo))


def pre_commit(papel: str) -> None:
    regras = carregar_regras()
    arquivos = [a for a in git("diff", "--cached", "--name-only", "--no-renames").splitlines() if a]
    violacoes = []
    if papel == "administrador":
        # ADR-0018: age no lugar do humano (cada mudança aprovada na sessão). Só as áreas
        # sem nenhum papel autorizado (ex.: logs/) continuam fechadas; os trailers seguem obrigatórios.
        fechados = [p for p, papeis in regras.get("restritos", {}).items() if not papeis]
        violacoes = [f"{c} (area fechada a agentes)" for c in arquivos if any(casa(c, p) for p in fechados)]
        if violacoes:
            falhar("o administrador nao pode alterar:\n  - " + "\n  - ".join(violacoes))
        return
    for caminho in arquivos:
        if any(casa(caminho, p) for p in regras.get("protegidos", [])):
            violacoes.append(f"{caminho} (area protegida: so o humano altera)")
            continue
        if any(casa(caminho, p) for p in regras.get("livres", [])):
            continue
        # O prefixo mais específico decide (ex.: qualidade/ux/ antes de qualidade/).
        restritos = sorted(regras.get("restritos", {}).items(), key=lambda item: len(item[0]), reverse=True)
        for prefixo, papeis in restritos:
            if casa(caminho, prefixo):
                if papel not in papeis:
                    violacoes.append(f"{caminho} (somente: {', '.join(papeis)})")
                break  # a primeira regra que casa decide, liberando ou recusando
    if violacoes:
        lista = "\n  - ".join(violacoes)
        falhar(f"o papel '{papel}' nao pode alterar:\n  - {lista}\nProponha a mudanca em BRAIN/00_Inbox ou peca ao humano.")


def normalizar_trailers(mensagem: str, valores: dict) -> str:
    """Poe Agente/Tarefa/Modelo no bloco final de trailers (ADM-0026).

    O Git so le como trailer o ultimo paragrafo. Se o agente escreveu as linhas
    no meio da mensagem (ex.: antes do Co-Authored-By), elas saem de la e entram
    no ultimo paragrafo, se ele ja for de trailers, ou num paragrafo novo.
    Linhas de comentario (#) ficam no fim, como estavam.
    """
    linhas = mensagem.splitlines()
    comentarios = [l for l in linhas if l.startswith("#")]
    corpo = [l for l in linhas if not l.startswith("#") and not RE_NOSSO.match(l.strip())]
    texto = re.sub(r"\n{3,}", "\n\n", "\n".join(l.rstrip() for l in corpo)).strip("\n")
    nossos = "\n".join(f"{nome}: {valores[nome]}" for nome in TRAILERS)
    paragrafos = texto.split("\n\n")
    ultimo = paragrafos[-1].splitlines() if len(paragrafos) > 1 else []
    juntar = bool(ultimo) and all(RE_TRAILER.match(l) for l in ultimo)
    texto += ("\n" if juntar else "\n\n") + nossos + "\n"
    if comentarios:
        texto += "\n".join(comentarios) + "\n"
    return texto


def commit_msg(papel: str, arquivo_msg: str) -> None:
    caminho = Path(arquivo_msg)
    mensagem = caminho.read_text(encoding="utf-8")
    existentes = {}
    for linha in mensagem.splitlines():
        m = RE_NOSSO.match(linha.strip())
        if m and not linha.startswith("#"):
            existentes[m.group(1)] = m.group(2).strip()

    if existentes.get("Agente") and existentes["Agente"] != papel:
        falhar(f"o trailer 'Agente: {existentes['Agente']}' nao corresponde ao papel da sessao ('{papel}').")

    tarefa = existentes.get("Tarefa") or os.environ.get("IA_TAREFA", "")
    if not tarefa:
        encontrada = PADRAO_TAREFA.search(git("rev-parse", "--abbrev-ref", "HEAD"))
        tarefa = encontrada.group(1) if encontrada else ""
    if not tarefa:
        falhar("commit de agente sem tarefa. Use um worktree com nome 'T-####-descricao' ou defina IA_TAREFA.")

    valores = {
        "Agente": papel,
        "Tarefa": tarefa,
        "Modelo": existentes.get("Modelo") or os.environ.get("IA_MODELO", "desconhecido"),
    }
    nova = normalizar_trailers(mensagem, valores)
    if nova != mensagem:
        caminho.write_text(nova, encoding="utf-8")


def sessao_claude_sem_papel() -> bool:
    """Commit feito de dentro de uma sessão do Claude que não foi iniciada por um papel.

    O Claude Code define CLAUDECODE=1 nos comandos que executa. Sessões do app
    desktop (CLAUDE_CODE_ENTRYPOINT=claude-desktop) são acompanhadas pelo humano
    no chat e contam como humanas.
    """
    return bool(os.environ.get("CLAUDECODE")) and os.environ.get("CLAUDE_CODE_ENTRYPOINT") != "claude-desktop"


def main() -> None:
    papel = os.environ.get("IA_PAPEL", "").strip()
    if not papel:
        if sessao_claude_sem_papel():
            falhar("esta sessao do Claude nao foi iniciada por um papel. "
                   "Feche-a e inicie com o lancador: D:\\01_IA\\ferramentas\\papel <papel>")
        return  # commit humano: sem restrições
    etapa = sys.argv[1] if len(sys.argv) > 1 else ""
    if etapa == "pre-commit":
        pre_commit(papel)
    elif etapa == "commit-msg" and len(sys.argv) > 2:
        commit_msg(papel, sys.argv[2])


if __name__ == "__main__":
    main()
