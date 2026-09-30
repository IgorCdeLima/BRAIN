"""Lançador de papéis da equipe 01_IA.

Uso (no terminal, dentro da pasta certa):
    D:\\01_IA\\ferramentas\\papel dev            -> executa a tarefa do worktree atual
    D:\\01_IA\\ferramentas\\papel engenheiro     -> requisitos, modelos e decisões da tarefa do worktree atual
    D:\\01_IA\\ferramentas\\papel revisor        -> revisa a tarefa do worktree atual
    D:\\01_IA\\ferramentas\\papel designer       -> cria o design (cartao do designer) ou faz a revisao visual
    D:\\01_IA\\ferramentas\\papel seguranca      -> analise de ameacas (cartao de seguranca) ou revisao de seguranca
    D:\\01_IA\\ferramentas\\papel bibliotecario  -> cura o Inbox (na cópia principal D:\\01_IA)
    D:\\01_IA\\ferramentas\\papel coordenador    -> panorama e proximo passo (na cópia principal D:\\01_IA)
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
        "pedido": "Apresente o panorama das tarefas e proponha o proximo passo.",
    },
}


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


def obsidian_aberto() -> bool:
    """O CLI do Obsidian só funciona com o aplicativo aberto."""
    cli = shutil.which("obsidian") or str(Path.home() / "AppData" / "Local" / "Programs" / "Obsidian" / "Obsidian.com")
    try:
        r = subprocess.run([cli, "version"], capture_output=True, text=True, timeout=15, cwd=str(RAIZ / "BRAIN"))
    except Exception:
        return False
    saida = (r.stdout + r.stderr).lower()
    return r.returncode == 0 and "unable to find" not in saida and bool(saida.strip())


def raiz_e_padrao() -> bool:
    return RAIZ.as_posix().lower() == RAIZ_PADRAO.lower()


def perfil_do_papel(papel: str) -> str:
    """Caminho do perfil de permissões; fora de D:\\01_IA, uma cópia com a raiz real."""
    perfil = DIR_AGENTES / "perfis" / f"{papel}.json"
    if raiz_e_padrao():
        return str(perfil)
    raiz = RAIZ.as_posix()
    m = re.match(r"^([A-Za-z]):/(.*)$", raiz)
    raiz_regra = f"//{m.group(1).lower()}/{m.group(2)}" if m else "/" + raiz  # formato //caminho das regras
    texto = perfil.read_text(encoding="utf-8").replace("//d/01_IA", raiz_regra).replace(RAIZ_PADRAO, raiz)
    copia = Path(tempfile.gettempdir()) / f"ia-perfil-{papel}.json"
    copia.write_text(texto, encoding="utf-8")
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

    topo = git("rev-parse", "--show-toplevel")
    if not topo:
        parar(f"esta pasta nao e um repositorio Git. Abra o terminal no worktree da tarefa (ou em {RAIZ} para o bibliotecario e o coordenador).")
    topo = Path(topo)
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    em_worktree = Path(git("rev-parse", "--git-dir")).resolve() != Path(git("rev-parse", "--git-common-dir")).resolve()

    tarefa = ""
    if regra["local"] == "principal":
        if topo.resolve() != RAIZ.resolve() or branch != "main":
            parar(f"o {papel} trabalha na copia principal {RAIZ} (branch main). Pasta atual: {topo} ({branch}).")
        # Trabalho contínuo, sem cartão: a "tarefa" dos commits é a curadoria/coordenação do dia.
        tarefa = f"{regra['tarefa']}-{date.today():%Y-%m-%d}"
        if papel == "bibliotecario" and not obsidian_aberto():
            parar("o Obsidian precisa estar aberto (com o Vault BRAIN) para o bibliotecario usar o CLI. Abra o Obsidian e rode de novo.")
    else:
        if not em_worktree:
            parar(f"o {papel} trabalha num worktree de tarefa criado no Orca, nunca na copia principal. Pasta atual: {topo} ({branch}).")
        m = re.search(r"\bT-\d{4}\b", branch)
        if not m:
            parar(f"o branch '{branch}' nao tem numero de tarefa. Crie o worktree com nome 'T-####-descricao'.")
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
    if "--verificar" in opcoes:
        print("[papel] Tudo certo. (--verificar: o Claude nao foi aberto)")
        return

    ambiente = dict(os.environ, IA_PAPEL=papel, IA_TAREFA=tarefa, IA_MODELO=modelo, IA_RAIZ=RAIZ.as_posix())
    sys.exit(subprocess.call(comando, env=ambiente))


if __name__ == "__main__":
    main()
