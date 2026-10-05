"""Lançador de papéis da equipe 01_IA.

Uso (no terminal, dentro da pasta certa):
    D:\\01_IA\\ferramentas\\papel dev            -> executa a tarefa do worktree atual
    D:\\01_IA\\ferramentas\\papel engenheiro     -> requisitos, modelos e decisões da tarefa do worktree atual
    D:\\01_IA\\ferramentas\\papel revisor        -> revisa a tarefa do worktree atual
    D:\\01_IA\\ferramentas\\papel designer       -> cria o design (cartao do designer) ou faz a revisao visual
    D:\\01_IA\\ferramentas\\papel seguranca      -> analise de ameacas (cartao de seguranca) ou revisao de seguranca
    D:\\01_IA\\ferramentas\\papel bibliotecario  -> cura o Inbox (na cópia principal D:\\01_IA)
    D:\\01_IA\\ferramentas\\papel coordenador    -> panorama e proximo passo (na cópia principal D:\\01_IA)
    D:\\01_IA\\ferramentas\\papel pesquisador    -> atende os SEARCH-#### pendentes (na cópia principal D:\\01_IA)
    D:\\01_IA\\ferramentas\\papel administrador  -> manutencao do ambiente e merges, com senha (cópia principal)
Opções:
    --verificar    só confere se está tudo certo, sem abrir o Claude
    --sem-pedido   abre o Claude sem enviar o pedido inicial
    --continuar    retoma a última sessão desta pasta (mesmo papel), sem novo pedido

Antes de abrir o Claude, confere: pasta (worktree ou cópia principal), tarefa
(pelo nome do branch), existência e status do cartão. Depois define o papel
(IA_PAPEL), a tarefa e o modelo, e inicia o Claude com a definição e o perfil
de permissões do papel.

Raiz do ambiente: IA_RAIZ ou, sem ela, a pasta acima de ferramentas/ (D:\\01_IA
no Windows). Linux: ferramentas/papel.sh <papel>. As definições e perfis citam
D:\\01_IA; fora dessa raiz o perfil é reescrito para a raiz real a cada início.
"""

import getpass
import hashlib
import hmac
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

RAIZ_PADRAO = "D:/01_IA"  # caminho escrito nas definições e perfis dos papéis
RAIZ = Path(os.environ.get("IA_RAIZ") or Path(__file__).resolve().parents[1])
DIR_AGENTES = RAIZ / "agentes"
DIR_TAREFAS = RAIZ / "operacao" / "tarefas"

PAPEIS = {
    "dev": {
        "local": "worktree",
        "status": {"pronta", "em-andamento", "correcao"},
        "dono_do_cartao": True,
        "pedido": "Execute a tarefa {tarefa}.",
    },
    "engenheiro": {
        "local": "worktree",
        "status": {"pronta", "em-andamento", "correcao"},
        "dono_do_cartao": True,
        "pedido": "Execute a tarefa {tarefa}.",
    },
    "revisor": {
        "local": "worktree",
        "status": {"revisao"},
        "dono_do_cartao": False,
        "pedido": "Revise a tarefa {tarefa}.",
    },
    # Dois modos, escolhidos pelo cartão: criação (cartão do designer) ou
    # revisão visual (cartão de outro papel, em revisão, com interface: sim).
    "designer": {
        "local": "worktree",
        "status": {"pronta", "em-andamento", "correcao", "revisao"},
        "dono_do_cartao": False,
        "marca": "interface",
        "pedido": "Crie o design da tarefa {tarefa}.",
        "pedido_revisao": "Faca a revisao visual da tarefa {tarefa}.",
    },
    # Mesma lógica do designer: análise de ameaças (cartão de seguranca) ou
    # revisão de segurança (cartão de outro papel, em revisão, com seguranca: sim).
    "seguranca": {
        "local": "worktree",
        "status": {"pronta", "em-andamento", "correcao", "revisao"},
        "dono_do_cartao": False,
        "marca": "seguranca",
        "pedido": "Faca a analise de ameacas da tarefa {tarefa}.",
        "pedido_revisao": "Faca a revisao de seguranca da tarefa {tarefa}.",
    },
    "bibliotecario": {
        "local": "principal",
        "status": None,
        "tarefa": "curadoria",
        "pedido": "Processe o Inbox do Brain.",
    },
    "coordenador": {
        "local": "principal",
        "status": None,
        "tarefa": "coordenacao",
        "pedido": "Apresente o panorama das tarefas e dos pedidos (cartoes, operacao/coordenador) e proponha o proximo passo.",
    },
    "pesquisador": {
        "local": "principal",
        "status": None,
        "tarefa": "pesquisa",
        "pedido": "Atenda os pedidos de pesquisa pendentes em operacao/pesquisas.",
    },
    # Acima do Coordenador (ADR-0018): senha no terminal, branch main ou admin/<assunto>.
    "administrador": {
        "local": "principal",
        "status": None,
        "tarefa": "admin",
        "senha": True,
        "branch_extra": "admin/",
        "pedido": "Apresente os pedidos abertos em operacao/administrador e pergunte ao humano o que ele quer mudar no ambiente.",
    },
}

ARQ_SENHA = Path.home() / ".config" / "01_ia" / "admin.senha"  # fora do repositório; leitura negada aos agentes
ITERACOES = 600_000


def hash_senha(senha: str, sal: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, ITERACOES).hex()


def conferir_senha(so_verificar: bool) -> None:
    """Senha do administrador, digitada no terminal (oculta). O Claude nunca a vê."""
    if so_verificar:
        print(f"[papel] senha do administrador: {'configurada' if ARQ_SENHA.exists() else 'NAO configurada (sera criada no primeiro uso)'}")
        return
    if not sys.stdin.isatty():
        parar("a senha do administrador precisa ser digitada num terminal interativo.")
    if not ARQ_SENHA.exists():
        print("[papel] Primeiro uso do administrador: crie a senha (minimo 8 caracteres).")
        senha = getpass.getpass("Nova senha: ")
        if len(senha) < 8 or senha != getpass.getpass("Repita a senha: "):
            parar("senha curta ou diferente na confirmacao.")
        sal = os.urandom(16)
        ARQ_SENHA.parent.mkdir(parents=True, exist_ok=True)
        ARQ_SENHA.write_text(f"pbkdf2_sha256${ITERACOES}${sal.hex()}${hash_senha(senha, sal)}\n", encoding="utf-8")
        ARQ_SENHA.chmod(0o600)
        print(f"[papel] Senha salva (hash) em {ARQ_SENHA}.")
        return
    _, _, sal, esperado = ARQ_SENHA.read_text(encoding="utf-8").strip().split("$")
    for _ in range(3):
        if hmac.compare_digest(hash_senha(getpass.getpass("Senha do administrador: "), bytes.fromhex(sal)), esperado):
            return
        print("[papel] Senha incorreta.", file=sys.stderr)
    parar("senha do administrador incorreta.")


def parar(mensagem: str) -> None:
    print(f"\n[papel] NAO INICIADO: {mensagem}\n", file=sys.stderr)
    sys.exit(1)


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip() if r.returncode == 0 else ""


def campo_do_cartao(cartao: Path, campo: str) -> str:
    texto = cartao.read_text(encoding="utf-8")
    m = re.search(rf"^{campo}:\s*([\w-]+)", texto, re.MULTILINE)
    return m.group(1) if m else ""


def raiz_e_padrao() -> bool:
    return RAIZ.as_posix().lower() == RAIZ_PADRAO.lower()


def perfil_do_papel(papel: str) -> str:
    """Cópia do perfil de permissões pronta para a sessão.

    - Fora de D:\\01_IA, os caminhos passam para a raiz real.
    - Internet (ADR-0017): WebFetch liberado só nos domínios de
      agentes/fontes-confiaveis.json; WebSearch negado. O Pesquisador navega livre.
    """
    perfil = DIR_AGENTES / "perfis" / f"{papel}.json"
    texto = perfil.read_text(encoding="utf-8")
    if not raiz_e_padrao():
        raiz = RAIZ.as_posix()
        m = re.match(r"^([A-Za-z]):/(.*)$", raiz)
        raiz_regra = f"//{m.group(1).lower()}/{m.group(2)}" if m else "/" + raiz  # formato //caminho das regras
        texto = texto.replace("//d/01_IA", raiz_regra).replace(RAIZ_PADRAO, raiz)
    config = json.loads(texto)
    if papel != "pesquisador":
        permissoes = config.setdefault("permissions", {})
        fontes = json.loads((DIR_AGENTES / "fontes-confiaveis.json").read_text(encoding="utf-8"))
        permissoes.setdefault("allow", []).extend(f"WebFetch(domain:{d['dominio']})" for d in fontes["dominios"])
        permissoes.setdefault("deny", []).append("WebSearch")
    copia = Path(tempfile.gettempdir()) / f"ia-perfil-{papel}.json"
    copia.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(copia)


def modelo_do_papel(papel: str) -> str:
    definicao = DIR_AGENTES / ".claude" / "agents" / f"{papel}.md"
    m = re.search(r"^model:\s*(\S+)", definicao.read_text(encoding="utf-8"), re.MULTILINE)
    return m.group(1) if m else "desconhecido"


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opcoes = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 1 or args[0] not in PAPEIS:
        parar(f"informe um papel: {', '.join(PAPEIS)}. Ex.: papel dev")
    papel = args[0]
    regra = PAPEIS[papel]
    if os.environ.get("CLAUDECODE") and "--verificar" not in opcoes:
        # Agente não se atribui papel (ADR-0013): o lançador só abre o Claude a partir do terminal do humano.
        parar("o lancador foi chamado de dentro de uma sessao do Claude. Rode-o num terminal comum "
              "(ex.: a janela da tarefa no tmux, aberta com 'tarefa abrir'). Dentro do Claude, so --verificar.")

    topo = git("rev-parse", "--show-toplevel")
    if not topo:
        parar(f"esta pasta nao e um repositorio Git. Abra o terminal no worktree da tarefa (ou em {RAIZ} para o bibliotecario e o coordenador).")
    topo = Path(topo)
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    em_worktree = Path(git("rev-parse", "--git-dir")).resolve() != Path(git("rev-parse", "--git-common-dir")).resolve()

    tarefa = ""
    if regra["local"] == "principal":
        extra = regra.get("branch_extra")
        branch_ok = branch == "main" or bool(extra and branch.startswith(extra))
        if topo.resolve() != RAIZ.resolve() or not branch_ok:
            parar(f"o {papel} trabalha na copia principal {RAIZ} (branch main{f' ou {extra}*' if extra else ''}). "
                  f"Pasta atual: {topo} ({branch}).")
        # Trabalho contínuo, sem cartão: a "tarefa" dos commits é a curadoria/coordenação do dia.
        tarefa = f"{regra['tarefa']}-{date.today():%Y-%m-%d}"
        # O bibliotecario nao depende mais do Obsidian aberto: move notas com ferramentas/notas.py (ADM-0018).
    else:
        if not em_worktree:
            parar(f"o {papel} trabalha num worktree de tarefa (criado com 'tarefa aceitar T-####'), nunca na copia principal. Pasta atual: {topo} ({branch}).")
        m = re.search(r"\bT-\d{4}\b", branch)
        if not m:
            parar(f"o branch '{branch}' nao tem numero de tarefa. Crie o worktree com 'tarefa aceitar T-####'.")
        tarefa = m.group(0)
        cartao = DIR_TAREFAS / f"{tarefa}.md"
        if not cartao.exists():
            parar(f"cartao {cartao} nao existe.")
        status = campo_do_cartao(cartao, "status")
        if status not in regra["status"]:
            parar(f"o cartao {tarefa} esta com status '{status}'. O {papel} so inicia com: {', '.join(sorted(regra['status']))}.")
        dono = campo_do_cartao(cartao, "papel")
        if regra["dono_do_cartao"] and dono != papel:
            parar(f"o cartao {tarefa} e do papel '{dono}', nao do {papel}. Use: papel {dono}")
        if "marca" in regra:  # designer e seguranca: modo próprio ou revisão do cartão de outro papel
            marca = regra["marca"]
            if dono == papel and status != "revisao":
                pass  # modo próprio (criação / análise)
            elif dono != papel and status == "revisao" and campo_do_cartao(cartao, marca) == "sim":
                regra = dict(regra, pedido=regra["pedido_revisao"])  # modo revisão
            else:
                parar(f"o {papel} trabalha em cartao com 'papel: {papel}' (pronta/em-andamento/correcao) "
                      f"ou revisa cartao em 'revisao' com '{marca}: sim'. Cartao {tarefa}: papel '{dono}', status '{status}'.")

    modelo = modelo_do_papel(papel)
    comando = [
        shutil.which("claude") or str(Path.home() / ".local" / "bin" / "claude.exe"),
        "--agent", papel,
        "--add-dir", str(DIR_AGENTES),
        "--settings", perfil_do_papel(papel),
    ]
    if not raiz_e_padrao():
        comando += ["--append-system-prompt",
                    f"Nesta maquina a raiz do ambiente 01_IA e {RAIZ.as_posix()}. "
                    f"Onde as regras e definicoes citam D:\\01_IA (ou /d/01_IA), use {RAIZ.as_posix()}."]
    if "--continuar" in opcoes:
        comando.append("--continue")  # retoma a última sessão desta pasta, já no papel
    elif "--sem-pedido" not in opcoes:
        comando.append(regra["pedido"].format(tarefa=tarefa))

    print(f"[papel] {papel} | tarefa: {tarefa or '-'} | modelo: {modelo} | pasta: {topo} ({branch})")
    if regra.get("senha"):
        conferir_senha(so_verificar="--verificar" in opcoes)
    if "--verificar" in opcoes:
        print("[papel] Tudo certo. (--verificar: o Claude nao foi aberto)")
        return

    ambiente = dict(os.environ, IA_PAPEL=papel, IA_TAREFA=tarefa, IA_MODELO=modelo, IA_RAIZ=RAIZ.as_posix())
    sys.exit(subprocess.call(comando, env=ambiente))


if __name__ == "__main__":
    main()
