"""Quadro de tarefas da equipe 01_IA: worktree e terminais (tmux) de cada tarefa.

Substitui o Orca (ADM-0009, fase 1). Cada tarefa aceita ganha um worktree do
projeto e uma sessao tmux com o nome da tarefa; cada papel abre numa janela.

Uso (terminal comum, fora do Claude):
    tarefa aceitar T-0017         cria o worktree T-0017-<descricao> a partir da main
                                  do projeto do cartao e a sessao tmux (se ja existe, reabre);
                                  cartao em backlog passa para pronta (commit so do cartao)
    tarefa abrir T-0017 dev       abre o papel numa janela da sessao T-0017 (chama o lancador)
    tarefa listar                 worktrees de tarefa, status do cartao e sessao tmux
    tarefa fechar T-0017          cartao concluida/cancelada: fecha a sessao e remove o worktree
Opcao:
    --simular                     mostra o que faria, sem mudar nada (liberado dentro do Claude)

Aceitar um cartao em backlog o passa para pronta (decisao do humano, ADM-0009):
aceitar e o "sim" para comecar. Os demais status nao mudam. Esta ferramenta nao define IA_PAPEL: quem
confere o cartao e define o papel continua sendo o lancador. Na fase 3 o quadro
web chama estas mesmas acoes.

Pastas: projetos em $IA_RAIZ/projetos/<projeto>; worktrees em
$IA_WORKTREES/<projeto>/T-####-<descricao> (padrao ~/01_ia/worktrees).
"""

import os
import re
import shlex
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(os.environ.get("IA_RAIZ") or Path(__file__).resolve().parents[1])
DIR_TAREFAS = RAIZ / "operacao" / "tarefas"
DIR_PROJETOS = RAIZ / "projetos"
DIR_WORKTREES = Path(os.environ.get("IA_WORKTREES") or Path.home() / "01_ia" / "worktrees")
LANCADOR = RAIZ / "ferramentas" / "papel.py"

PAPEIS_DE_WORKTREE = ("dev", "engenheiro", "designer", "seguranca", "revisor")
STATUS_SEM_WORKTREE = {"concluida", "cancelada"}  # aceitar recusa
STATUS_ACEITAR_MUDA = {"backlog": "pronta"}  # aceitar muda o status (so depois de criar o worktree)
STATUS_FECHAR = {"concluida", "cancelada"}
RE_TAREFA = re.compile(r"^T-\d{4}$")
RE_PROJETO = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class Erro(Exception):
    pass


# ---------------------------------------------------------------- utilitarios

def rodar(cmd, simular=False, checar=True, cwd=None):
    """Executa um comando que altera algo (ou so mostra, com --simular)."""
    print("  $ " + " ".join(shlex.quote(str(c)) for c in cmd))
    if simular:
        return ""
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, encoding="utf-8", cwd=cwd)
    if checar and r.returncode != 0:
        raise Erro(f"comando falhou ({r.returncode}): {(r.stderr or r.stdout).strip()}")
    return r.stdout.strip()


def ler(cmd, cwd=None):
    """Comando somente leitura; devolve (codigo, saida)."""
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, encoding="utf-8", cwd=cwd)
    return r.returncode, r.stdout.strip()


def tem_tmux():
    return shutil.which("tmux") is not None


def sessao_existe(nome):
    return tem_tmux() and ler(["tmux", "has-session", "-t", f"={nome}"])[0] == 0


def lesma(titulo, max_palavras=4, max_chars=40):
    """'Implementar a tela de cadastro' -> 'implementar-tela-cadastro'."""
    texto = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode().lower()
    vazias = {"a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "no", "na", "com", "para", "por", "um", "uma"}
    palavras = [p for p in re.findall(r"[a-z0-9]+", texto) if p not in vazias][:max_palavras]
    return "-".join(palavras)[:max_chars].strip("-") or "tarefa"


# ---------------------------------------------------------------- cartao

def ler_cartao(tarefa):
    if not RE_TAREFA.match(tarefa):
        raise Erro(f"'{tarefa}' nao e um id de tarefa (T-####).")
    cartao = DIR_TAREFAS / f"{tarefa}.md"
    if not cartao.exists():
        raise Erro(f"cartao {cartao} nao existe.")
    texto = cartao.read_text(encoding="utf-8")

    def campo(nome):
        m = re.search(rf"^{nome}:\s*([\w-]+)", texto, re.MULTILINE)
        return m.group(1) if m else ""

    m = re.search(rf"^#\s*{tarefa}\s*-\s*(.+)$", texto, re.MULTILINE)
    return {"id": tarefa, "status": campo("status"), "projeto": campo("projeto"),
            "papel": campo("papel"), "titulo": m.group(1).strip() if m else ""}


def repo_do_projeto(projeto):
    if not RE_PROJETO.match(projeto or ""):
        raise Erro(f"campo 'projeto:' do cartao invalido ou vazio: '{projeto}'.")
    repo = DIR_PROJETOS / projeto
    if ler(["git", "-C", repo, "rev-parse", "--git-dir"])[0] != 0:
        raise Erro(f"{repo} nao e um repositorio Git.")
    return repo


# ---------------------------------------------------------------- worktrees

def worktrees(repo):
    """[{caminho, branch}] dos worktrees do repositorio (sem o principal)."""
    _, saida = ler(["git", "-C", repo, "worktree", "list", "--porcelain"])
    lista, atual = [], {}
    for linha in saida.splitlines() + [""]:
        if linha.startswith("worktree "):
            atual = {"caminho": Path(linha[9:]), "branch": ""}
        elif linha.startswith("branch "):
            atual["branch"] = linha[7:].removeprefix("refs/heads/")
        elif not linha and atual:
            lista.append(atual)
            atual = {}
    return lista[1:]  # o primeiro e a copia principal do projeto


def worktree_da_tarefa(repo, tarefa):
    for w in worktrees(repo):
        if re.match(rf"^{tarefa}(-|$)", w["branch"]):
            return w
    return None


def branch_existente(repo, tarefa):
    _, saida = ler(["git", "-C", repo, "for-each-ref", "--format=%(refname:short)", f"refs/heads/{tarefa}*"])
    return next((b for b in saida.splitlines() if re.match(rf"^{tarefa}(-|$)", b)), "")


# ---------------------------------------------------------------- acoes

def aceitar(tarefa, simular=False):
    c = ler_cartao(tarefa)
    repo = repo_do_projeto(c["projeto"])
    w = worktree_da_tarefa(repo, tarefa)
    if w:
        print(f"[tarefa] {tarefa} ja aceita: worktree {w['caminho']} ({w['branch']}).")
        caminho = w["caminho"]
    else:
        if c["status"] in STATUS_SEM_WORKTREE:
            raise Erro(f"o cartao {tarefa} esta com status '{c['status']}'; nao se aceita tarefa em "
                       f"{', '.join(sorted(STATUS_SEM_WORKTREE))}.")
        branch = branch_existente(repo, tarefa)
        if branch:
            caminho = DIR_WORKTREES / c["projeto"] / branch
            print(f"[tarefa] {tarefa}: branch {branch} ja existe; criando so o worktree.")
            cmd = ["git", "-C", repo, "worktree", "add", caminho, branch]
        else:
            branch = f"{tarefa}-{lesma(c['titulo'])}"
            caminho = DIR_WORKTREES / c["projeto"] / branch
            print(f"[tarefa] {tarefa}: criando o branch {branch} a partir da main de {repo}.")
            cmd = ["git", "-C", repo, "worktree", "add", "-b", branch, caminho, "main"]
        if caminho.exists():
            raise Erro(f"a pasta {caminho} ja existe e nao e worktree desta tarefa. Confira antes de seguir.")
        if not simular:
            caminho.parent.mkdir(parents=True, exist_ok=True)
        rodar(cmd, simular)
    garantir_sessao(tarefa, caminho, simular)
    status = c["status"]
    if status in STATUS_ACEITAR_MUDA:
        status = mudar_status(tarefa, status, STATUS_ACEITAR_MUDA[status], simular)
    print(f"[tarefa] Pronto. Status do cartao: '{status}'.")
    print(f"         Proximo: tarefa abrir {tarefa} <{'|'.join(PAPEIS_DE_WORKTREE)}>")


def mudar_status(tarefa, de, para, simular):
    """Troca o status no frontmatter do cartao e commita so o cartao na copia principal."""
    cartao = DIR_TAREFAS / f"{tarefa}.md"
    texto = cartao.read_text(encoding="utf-8")
    novo, n = re.subn(rf"^status:\s*{re.escape(de)}\s*$", f"status: {para}", texto, count=1, flags=re.MULTILINE)
    if n != 1:
        print(f"[tarefa] AVISO: nao achei 'status: {de}' no cartao; status nao alterado.")
        return de
    print(f"[tarefa] cartao {tarefa}: status {de} -> {para}")
    if simular:
        return para
    cartao.write_text(novo, encoding="utf-8")
    relativo = cartao.relative_to(RAIZ).as_posix()
    branch = ler(["git", "-C", RAIZ, "rev-parse", "--abbrev-ref", "HEAD"])[1]
    if branch != "main":
        print(f"[tarefa] AVISO: a copia principal esta no branch '{branch}', nao na main: status alterado no arquivo, "
              f"sem commit. Commite na main: git -C {RAIZ} commit -m 'docs(tarefas): aceita {tarefa}' -- {relativo}")
        return para
    try:
        rodar(["git", "-C", RAIZ, "commit", "-q", "-m", f"docs(tarefas): aceita {tarefa} ({de} -> {para})", "--", relativo])
    except Erro as e:
        print(f"[tarefa] AVISO: status alterado no arquivo, mas o commit falhou: {e}\n"
              f"         Commite o cartao a mao: git -C {RAIZ} commit -m 'docs(tarefas): aceita {tarefa}' -- {relativo}")
    return para


def garantir_sessao(tarefa, caminho, simular):
    if not tem_tmux():
        print("[tarefa] tmux nao instalado: sessao nao criada (instale com 'sudo apt install tmux').")
        return
    if sessao_existe(tarefa):
        print(f"[tarefa] sessao tmux {tarefa} ja existe.")
        return
    rodar(["tmux", "new-session", "-d", "-s", tarefa, "-n", "terminal", "-c", caminho], simular)


def abrir(tarefa, papel, simular=False):
    if papel not in PAPEIS_DE_WORKTREE:
        raise Erro(f"papel '{papel}' nao trabalha em worktree. Use um de: {', '.join(PAPEIS_DE_WORKTREE)}. "
                   "Coordenador, Bibliotecario, Pesquisador e Administrador abrem na copia principal.")
    if not tem_tmux():
        raise Erro("tmux nao instalado. Instale com 'sudo apt install tmux'.")
    c = ler_cartao(tarefa)
    w = worktree_da_tarefa(repo_do_projeto(c["projeto"]), tarefa)
    if not w:
        raise Erro(f"{tarefa} ainda nao foi aceita (sem worktree). Rode antes: tarefa aceitar {tarefa}")
    garantir_sessao(tarefa, w["caminho"], simular)
    janelas = ler(["tmux", "list-windows", "-t", f"={tarefa}", "-F", "#{window_name}"])[1].splitlines()
    if papel in janelas:
        print(f"[tarefa] janela {papel} ja existe na sessao {tarefa}.")
    else:
        # O lancador confere pasta, cartao e status; o shell fica aberto depois que o Claude sai.
        comando = f"python3 {shlex.quote(str(LANCADOR))} {papel}; exec \"${{SHELL:-/bin/bash}}\""
        rodar(["tmux", "new-window", "-t", f"={tarefa}:", "-n", papel, "-c", w["caminho"], comando], simular)
    alvo = f"={tarefa}:{papel}"
    if os.environ.get("TMUX"):
        rodar(["tmux", "switch-client", "-t", alvo], simular, checar=False)
    else:
        print(f"[tarefa] Para entrar: tmux attach -t {tarefa}   (trocar de janela: Ctrl-b w; sair sem fechar: Ctrl-b d)")


def listar():
    projetos = sorted(p for p in DIR_PROJETOS.iterdir() if p.is_dir() and (p / ".git").exists()) if DIR_PROJETOS.exists() else []
    linhas = []
    for repo in projetos:
        for w in worktrees(repo):
            m = re.match(r"^(T-\d{4})", w["branch"])
            if not m:
                continue
            tarefa = m.group(1)
            try:
                status = ler_cartao(tarefa)["status"]
            except Erro:
                status = "(sem cartao)"
            sessao = "sim" if sessao_existe(tarefa) else "nao"
            linhas.append((tarefa, repo.name, w["branch"], status, sessao, str(w["caminho"])))
    if not linhas:
        print("[tarefa] Nenhuma tarefa aceita (nenhum worktree T-#### nos projetos).")
        return
    print("| Tarefa | Projeto | Branch | Status | tmux | Pasta |")
    print("|---|---|---|---|---|---|")
    for l in linhas:
        print("| " + " | ".join(l) + " |")
    if not tem_tmux():
        print("\n(tmux nao instalado: coluna tmux sempre 'nao')")


def fechar(tarefa, simular=False):
    c = ler_cartao(tarefa)
    if c["status"] not in STATUS_FECHAR:
        raise Erro(f"o cartao {tarefa} esta com status '{c['status']}'. So se fecha com: {', '.join(sorted(STATUS_FECHAR))}.")
    repo = repo_do_projeto(c["projeto"])
    w = worktree_da_tarefa(repo, tarefa)
    if not w:
        print(f"[tarefa] {tarefa} nao tem worktree.")
    else:
        _, sujo = ler(["git", "-C", w["caminho"], "status", "--porcelain"])
        if sujo:
            raise Erro(f"o worktree {w['caminho']} tem mudancas nao commitadas. Nada foi removido.\n{sujo}")
        na_main = ler(["git", "-C", repo, "merge-base", "--is-ancestor", w["branch"], "main"])[0] == 0
        if c["status"] == "concluida" and not na_main:
            raise Erro(f"o cartao esta 'concluida', mas o branch {w['branch']} nao esta na main. Confira o merge; nada foi removido.")
        if sessao_existe(tarefa):
            rodar(["tmux", "kill-session", "-t", f"={tarefa}"], simular)
        rodar(["git", "-C", repo, "worktree", "remove", w["caminho"]], simular)  # sem --force
        if na_main:
            rodar(["git", "-C", repo, "branch", "-d", w["branch"]], simular)  # -d: recusa se nao estiver na main
        else:
            print(f"[tarefa] branch {w['branch']} mantido: nao esta na main (tarefa {c['status']}; nada e apagado).")
    print(f"[tarefa] {tarefa} fechada.")


# ---------------------------------------------------------------- entrada

def main(argv):
    simular = "--simular" in argv
    args = [a for a in argv if a != "--simular"]
    acoes = {"aceitar": 1, "abrir": 2, "listar": 0, "fechar": 1}
    if not args or args[0] not in acoes or len(args) != acoes[args[0]] + 1:
        print(__doc__)
        return 2
    acao = args[0]
    if acao != "listar" and os.environ.get("CLAUDECODE") and not simular:
        # Mesma regra do lancador (ADR-0013): agente nao aceita tarefa nem abre papel.
        print("\n[tarefa] NAO EXECUTADO: chamado de dentro de uma sessao do Claude. "
              "Rode num terminal comum. Dentro do Claude, so 'listar' e '--simular'.\n", file=sys.stderr)
        return 1
    try:
        if acao == "aceitar":
            aceitar(args[1], simular)
        elif acao == "abrir":
            abrir(args[1], args[2], simular)
        elif acao == "listar":
            listar()
        else:
            fechar(args[1], simular)
    except Erro as e:
        print(f"\n[tarefa] NAO EXECUTADO: {e}\n", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
