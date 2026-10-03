"""Mover e renomear notas do Brain sem o Obsidian, com as convencoes de link do Obsidian (ADM-0018).

O BRAIN/ continua sendo o cofre do Obsidian do humano; os agentes nao usam o aplicativo nem o CLI.
Este script grava como o Obsidian gravaria:
  - [[Nome]] acha a nota pelo nome em qualquer pasta; nome repetido exige caminho.
  - Ao mover ou renomear, so os links que deixariam de apontar para a mesma nota sao reescritos,
    preservando o estilo (wikilink ou Markdown), o embed (!), o #cabecalho, o #^bloco e o |alias.
  - Link reescrito segue newLinkFormat de BRAIN/.obsidian/app.json (padrao "shortest": so o nome
    se ele for unico no cofre, senao o caminho completo a partir do cofre).
  - Nao mexe em blocos de codigo, codigo em linha, comentarios (HTML e %%) nem em BRAIN/.obsidian/.
  - Links para notas do Brain fora do cofre (operacao/, CLAUDE.md, agentes/) tambem sao atualizados
    (so wikilinks; link Markdown fora do cofre e caminho do sistema de arquivos e fica como esta).
  - Link ambiguo (nome repetido sem caminho) ou quebrado nao e alterado; o script avisa.

Uso (caminhos relativos ao cofre; o prefixo BRAIN/ e aceito):
  python3 ferramentas/notas.py mover "00_Inbox/Nota.md" "10_Conhecimento/Nota.md" [--simular]
  python3 ferramentas/notas.py mover "00_Inbox/Nota.md" "10_Conhecimento/"        (mantem o nome)
  python3 ferramentas/notas.py orfas
  python3 ferramentas/notas.py quebrados [--todos]   (--todos: inclui arquivos fora do cofre)
  Windows: py -3 ferramentas/notas.py ...
  Teste: --raiz PASTA (repositorio) --cofre PASTA (cofre; padrao <raiz>/BRAIN)
"""

import argparse
import json
import posixpath
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote

RAIZ_PADRAO = Path(__file__).resolve().parent.parent
IGNORAR = {".git", ".obsidian", ".trash", "logs", "node_modules", "__pycache__", "projetos"}

WIKI = re.compile(r"(?P<emb>!?)\[\[(?P<alvo>[^\[\]|#^]*?)(?P<sub>#[^\[\]|]*?)?(?P<alias>\\?\|[^\[\]]*?)?\]\]")
MD = re.compile(r"(?P<emb>!?)\[(?P<texto>[^\[\]]*)\]\((?P<alvo><[^<>]*>|[^()\s]+)\)")
ESQUEMA = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
COMENTARIO = re.compile(r"<!--.*?(?:-->|\Z)|%%.*?(?:%%|\Z)", re.S)
CODIGO_LINHA = re.compile(r"(?<!`)(`+)(?!`).+?(?<!`)\1(?!`)")
CERCA = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def parar(msg: str) -> None:
    print(f"[notas] {msg}", file=sys.stderr)
    sys.exit(1)


# --------------------------------------------------------------------------- leitura do texto

def trechos_protegidos(texto: str) -> list:
    """Intervalos (ini, fim) onde o Obsidian nao ve links: cercas de codigo, codigo em linha, comentarios."""
    trechos = []
    pos, aberta, ini = 0, None, 0
    for linha in texto.splitlines(keepends=True):
        m = CERCA.match(linha)
        if aberta is None and m:
            aberta, ini = m.group(1), pos
        elif aberta is not None and m and m.group(1)[0] == aberta[0] and len(m.group(1)) >= len(aberta) \
                and not linha.strip().strip(aberta[0]):
            trechos.append((ini, pos + len(linha)))
            aberta = None
        pos += len(linha)
    if aberta is not None:
        trechos.append((ini, len(texto)))

    def livre(i: int) -> bool:
        return not any(a <= i < b for a, b in trechos)

    extras = [(m.start(), m.end()) for rx in (COMENTARIO, CODIGO_LINHA) for m in rx.finditer(texto) if livre(m.start())]
    return trechos + extras


@dataclass
class Link:
    ini: int
    fim: int
    wiki: bool
    emb: str
    caminho: str   # texto do alvo, sem #sub, decodificado
    sub: str       # "#Cabecalho" ou "#^bloco" (como escrito) ou ""
    resto: str     # wiki: "|alias" ou "\|alias"; md: texto entre colchetes
    angular: bool = False  # md no formato (<caminho com espaco.md>)

    def escrever(self, novo: str) -> str:
        if self.wiki:
            return f"{self.emb}[[{novo}{self.sub}{self.resto}]]"
        if self.angular:
            return f"{self.emb}[{self.resto}](<{novo}{self.sub}>)"
        alvo = quote(novo, safe="/-._~!$&'*+,;=:@")
        return f"{self.emb}[{self.resto}]({alvo}{self.sub})"


def extrair_links(texto: str) -> list:
    protegidos = trechos_protegidos(texto)

    def livre(i: int) -> bool:
        return not any(a <= i < b for a, b in protegidos)

    links = []
    for m in WIKI.finditer(texto):
        if livre(m.start()) and m.group("alvo").strip():
            links.append(Link(m.start(), m.end(), True, m.group("emb"), m.group("alvo"),
                              m.group("sub") or "", m.group("alias") or ""))
    for m in MD.finditer(texto):
        bruto = m.group("alvo")
        angular = bruto.startswith("<")
        if angular:
            bruto = bruto[1:-1]
        if not livre(m.start()) or not bruto or bruto.startswith("#") or ESQUEMA.match(bruto):
            continue
        caminho, _, sub = bruto.partition("#")
        links.append(Link(m.start(), m.end(), False, m.group("emb"), unquote(caminho),
                          f"#{sub}" if sub else "", m.group("texto"), angular))
    return sorted(links, key=lambda l: l.ini)


# --------------------------------------------------------------------------- cofre

class Cofre:
    def __init__(self, pasta: Path, arquivos=None):
        self.pasta = pasta
        if arquivos is None:
            arquivos = set()
            for p in pasta.rglob("*"):
                rel = p.relative_to(pasta)
                if p.is_file() and not (set(rel.parts) & IGNORAR):
                    arquivos.add(rel.as_posix())
        self.arquivos = set(arquivos)
        self.por_caminho = {a.casefold(): a for a in self.arquivos}
        self.por_nome = {}
        for a in self.arquivos:
            self.por_nome.setdefault(posixpath.basename(a).casefold(), []).append(a)

    def com(self, sai: str, entra: str) -> "Cofre":
        return Cofre(self.pasta, (self.arquivos - {sai}) | {entra})

    def resolver(self, caminho: str, pasta_origem):
        """('ok', arquivo) | ('ambiguo', [arquivos]) | ('quebrado', None). pasta_origem None = fora do cofre."""
        caminho = caminho.strip().replace("\\", "/").lstrip("/")
        if caminho.startswith("./") and pasta_origem is not None:
            caminho = posixpath.normpath(posixpath.join(pasta_origem, caminho))
        for var in (caminho, caminho + ".md"):
            achado = self.por_caminho.get(var.casefold())
            if achado:
                return ("ok", achado)
            if pasta_origem is not None:
                rel = posixpath.normpath(posixpath.join(pasta_origem, var))
                if not rel.startswith("..") and rel.casefold() in self.por_caminho:
                    return ("ok", self.por_caminho[rel.casefold()])
            if "/" in var:
                fim = "/" + var.casefold()
                cands = [a for a in self.arquivos if a.casefold().endswith(fim)]
            else:
                cands = self.por_nome.get(var.casefold(), [])
            if len(cands) == 1:
                return ("ok", cands[0])
            if len(cands) > 1:
                return ("ambiguo", sorted(cands))
        return ("quebrado", None)

    def gerar(self, alvo: str, pasta_origem, wiki: bool, formato: str) -> str:
        """Texto do link para `alvo`, como o Obsidian escreveria."""
        base = alvo[:-3] if wiki and alvo.endswith(".md") else alvo
        if formato == "relative" and pasta_origem is not None:
            return posixpath.relpath(base, pasta_origem or ".")
        if formato == "absolute":
            return base
        nome = posixpath.basename(base)
        if self.resolver(nome, None) == ("ok", alvo):
            return nome
        return base


def formato_de_link(cofre: Path) -> str:
    try:
        cfg = json.loads((cofre / ".obsidian" / "app.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        cfg = {}
    return cfg.get("newLinkFormat", "shortest")


def arquivos_md(raiz: Path) -> list:
    """Todo .md do repositorio (versionado ou novo, fora dos ignorados do Git)."""
    r = subprocess.run(["git", "-C", str(raiz), "ls-files", "-co", "--exclude-standard", "-z", "--", "*.md"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode == 0:
        nomes = [n for n in r.stdout.split("\0") if n]
    else:
        nomes = [p.relative_to(raiz).as_posix() for p in raiz.rglob("*.md")]
    saida = []
    for n in sorted(set(nomes)):
        if not (set(Path(n).parts) & IGNORAR) and (raiz / n).is_file():
            saida.append(raiz / n)
    return saida


def ler(arq: Path):
    try:
        with open(arq, encoding="utf-8", newline="") as f:
            return f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"[notas] aviso: ignorado {arq} ({e})", file=sys.stderr)
        return None


def no_cofre(arq: Path, cofre: Path):
    """Caminho relativo ao cofre (posix) ou None se o arquivo estiver fora."""
    try:
        return arq.resolve().relative_to(cofre.resolve()).as_posix()
    except ValueError:
        return None


def linha_de(texto: str, i: int) -> int:
    return texto.count("\n", 0, i) + 1


# --------------------------------------------------------------------------- comandos

def normalizar(caminho: str, cofre: Path) -> str:
    c = caminho.replace("\\", "/").strip()
    prefixo = cofre.name + "/"
    if c.startswith(prefixo):
        c = c[len(prefixo):]
    return posixpath.normpath(c.lstrip("/"))


def cmd_mover(raiz: Path, cofre_dir: Path, origem: str, destino: str, simular: bool) -> None:
    destino_pasta = destino.replace("\\", "/").endswith("/")
    origem, destino = normalizar(origem, cofre_dir), normalizar(destino, cofre_dir)
    if destino_pasta or (cofre_dir / destino).is_dir():
        destino = posixpath.join(destino, posixpath.basename(origem)) if destino != "." else posixpath.basename(origem)
    for c in (origem, destino):
        if c.startswith("..") or set(c.split("/")) & IGNORAR:
            parar(f"caminho fora do cofre ou em pasta reservada: {c}")
    if not (cofre_dir / origem).is_file():
        parar(f"origem nao existe no cofre: {origem}")
    if (cofre_dir / destino).exists():
        parar(f"destino ja existe: {destino}")
    if posixpath.splitext(origem)[1].casefold() != posixpath.splitext(destino)[1].casefold():
        parar(f"a extensao muda de {origem} para {destino}; confira o destino")
    if origem == destino:
        parar("origem e destino iguais")

    antes = Cofre(cofre_dir)
    if origem not in antes.arquivos:
        parar(f"origem em pasta ignorada: {origem}")
    depois = antes.com(origem, destino)
    formato = formato_de_link(cofre_dir)

    repetidos = [a for a in antes.por_nome.get(posixpath.basename(destino).casefold(), []) if a != origem]
    if repetidos:
        print(f"[notas] aviso: o nome {posixpath.basename(destino)} ja existe em {', '.join(repetidos)}; "
              "links para essas notas so pelo nome ficam ambiguos e passam a usar caminho.")

    mudancas = {}   # arquivo final -> (texto novo, [(linha, antes, depois)])
    avisos = []
    for arq in arquivos_md(raiz):
        texto = ler(arq)
        if texto is None:
            continue
        rel = no_cofre(arq, cofre_dir)
        fora = rel is None
        pasta_antes = None if fora else posixpath.dirname(rel)
        rel_depois = destino if rel == origem else rel
        pasta_depois = None if fora else posixpath.dirname(rel_depois)
        novo, ultimo, trocas = [], 0, []
        for link in extrair_links(texto):
            if fora and not link.wiki:
                continue
            st, alvo = antes.resolver(link.caminho, pasta_antes)
            if st == "ambiguo" and (origem in alvo or any(posixpath.basename(a) == posixpath.basename(destino) for a in alvo)):
                avisos.append(f"{arq.relative_to(raiz).as_posix()}:{linha_de(texto, link.ini)} link ambiguo nao alterado: "
                              f"{texto[link.ini:link.fim]}")
            if st != "ok":
                continue
            alvo_depois = destino if alvo == origem else alvo
            if depois.resolver(link.caminho, pasta_depois) == ("ok", alvo_depois):
                continue
            escrito = link.escrever(depois.gerar(alvo_depois, pasta_depois, link.wiki, formato))
            novo.append(texto[ultimo:link.ini] + escrito)
            ultimo = link.fim
            trocas.append((linha_de(texto, link.ini), texto[link.ini:link.fim], escrito))
        if trocas:
            novo.append(texto[ultimo:])
            final = (cofre_dir / rel_depois) if rel == origem else arq
            mudancas[final] = ("".join(novo), trocas)

    print(f"[notas] {'simulacao: ' if simular else ''}mover {origem} -> {destino} (formato de link: {formato})")
    for arq, (_, trocas) in sorted(mudancas.items()):
        print(f"  {arq.relative_to(raiz).as_posix() if arq.is_relative_to(raiz) else arq}: {len(trocas)} link(s)")
        for linha, a, d in trocas:
            print(f"    l.{linha}: {a} -> {d}")
    for a in avisos:
        print(f"[notas] aviso: {a}")
    if not mudancas:
        print("  nenhum link precisou mudar")
    if simular:
        return

    origem_abs, destino_abs = cofre_dir / origem, cofre_dir / destino
    destino_abs.parent.mkdir(parents=True, exist_ok=True)
    versionado = subprocess.run(["git", "-C", str(raiz), "ls-files", "--error-unmatch", "--", str(origem_abs)],
                                capture_output=True).returncode == 0
    if versionado:
        r = subprocess.run(["git", "-C", str(raiz), "mv", "--", str(origem_abs), str(destino_abs)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            parar(f"git mv falhou: {r.stderr.strip()}")
    else:
        origem_abs.rename(destino_abs)
    for arq, (texto, _) in mudancas.items():
        with open(arq, "w", encoding="utf-8", newline="") as f:
            f.write(texto)
    print(f"[notas] movido ({'git mv' if versionado else 'arquivo nao versionado'}); {len(mudancas)} arquivo(s) atualizado(s)")


def cmd_orfas(raiz: Path, cofre_dir: Path) -> None:
    cofre = Cofre(cofre_dir)
    recebe = set()
    for arq in arquivos_md(raiz):
        rel = no_cofre(arq, cofre_dir)
        texto = ler(arq) if rel is not None else None
        if texto is None:
            continue
        for link in extrair_links(texto):
            st, alvo = cofre.resolver(link.caminho, posixpath.dirname(rel))
            if st == "ok" and alvo != rel:
                recebe.add(alvo)
    orfas = sorted(a for a in cofre.arquivos if a.endswith(".md") and a not in recebe)
    for a in orfas:
        print(a)
    print(f"[notas] {len(orfas)} nota(s) sem link de entrada no cofre", file=sys.stderr)


def cmd_quebrados(raiz: Path, cofre_dir: Path, todos: bool) -> None:
    cofre = Cofre(cofre_dir)
    total = 0
    for arq in arquivos_md(raiz):
        rel = no_cofre(arq, cofre_dir)
        if rel is None and not todos:
            continue
        texto = ler(arq)
        if texto is None:
            continue
        for link in extrair_links(texto):
            if rel is None and not link.wiki:
                continue
            st, alvo = cofre.resolver(link.caminho, None if rel is None else posixpath.dirname(rel))
            if st == "ok":
                continue
            total += 1
            extra = f" ({', '.join(alvo)})" if st == "ambiguo" else ""
            print(f"{arq.relative_to(raiz).as_posix()}:{linha_de(texto, link.ini)}\t{st}\t{texto[link.ini:link.fim]}{extra}")
    print(f"[notas] {total} link(s) quebrado(s) ou ambiguo(s)", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description="Notas do Brain sem o Obsidian (ADM-0018).")
    ap.add_argument("--raiz", type=Path, default=RAIZ_PADRAO)
    ap.add_argument("--cofre", type=Path)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mover")
    m.add_argument("origem")
    m.add_argument("destino")
    m.add_argument("--simular", action="store_true")
    sub.add_parser("orfas")
    q = sub.add_parser("quebrados")
    q.add_argument("--todos", action="store_true")
    a = ap.parse_args()
    raiz = a.raiz.resolve()
    cofre = (a.cofre or raiz / "BRAIN").resolve()
    if not cofre.is_dir():
        parar(f"cofre nao encontrado: {cofre}")
    if a.cmd == "mover":
        cmd_mover(raiz, cofre, a.origem, a.destino, a.simular)
    elif a.cmd == "orfas":
        cmd_orfas(raiz, cofre)
    else:
        cmd_quebrados(raiz, cofre, a.todos)


if __name__ == "__main__":
    main()
