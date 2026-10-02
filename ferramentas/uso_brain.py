"""Relatório de uso do Brain: o que é lido, por quem, em que tarefa, e o que foi útil (ADM-0017).

Somente leitura. Fontes:
  1. logs/brain/AAAA-MM.jsonl, gravado pelo hook registrar_brain.py (permanente).
  2. Transcrições do Claude Code (~/.claude/projects/*/*.jsonl), para o período anterior ao
     hook e para sessões sem log. Delas só se tiram papel, sessão, pasta, data e o CAMINHO
     lido; nenhum texto de mensagem. Uma sessão presente no log não é contada de novo.
  3. Wikilinks [[Nota]] nos registros de trabalho (operacao/, projetos/*/qualidade|docs):
     citação = a nota foi usada (CLAUDE.md, hierarquia de conhecimento).
  4. Linhas "Brain consultado": `[[Nota]] - ajudou: sim | parcial | nao - motivo`
     nos cartões e VER = a nota foi útil (ou não), na opinião de quem usou.

Uso:
  py -3 ferramentas/uso_brain.py [--desde AAAA-MM-DD] [--min-idade 60] [--json] [--saida ARQ]
        [--sem-transcricoes] [--sem-logs]
"""

import argparse
import collections
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "hooks"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from registrar_brain import extrair_acessos  # noqa: E402  (mesmo leitor de caminhos do hook)
from transcricoes import ler_transcricoes  # noqa: E402  (leitor comum, ADM-0011)

REGRAS = {"60_Agentes", "70_Workflows", "99_Sistema"}  # regras e templates, nao conhecimento
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
AJUDOU = re.compile(r"\[\[([^\]|#]+)[^\]]*\]\][^\n]{0,20}?ajudou:\s*(sim|parcial|nao)", re.I)


def notas_do_brain(brain: Path) -> dict:
    notas = {}
    for arq in brain.rglob("*.md"):
        rel = arq.relative_to(brain)
        if len(rel.parts) < 2 or rel.parts[0].startswith(".") or arq.name.startswith("_"):
            continue
        texto = arq.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^criado:\s*(\d{4}-\d{2}-\d{2})", texto, re.M)
        criado = m.group(1) if m else datetime.fromtimestamp(arq.stat().st_mtime).strftime("%Y-%m-%d")
        notas[arq.stem.lower()] = {
            "titulo": arq.stem, "pasta": rel.parts[0], "criado": criado,
            "links": {l.strip().lower() for l in WIKILINK.findall(texto)},
        }
    return notas


def acessos_do_log(dir_logs: Path, desde: str):
    for arq in sorted(dir_logs.glob("*.jsonl")) if dir_logs.is_dir() else []:
        for linha in arq.open(encoding="utf-8", errors="replace"):
            try:
                r = json.loads(linha)
            except ValueError:
                continue
            dia = r.get("ts", "")[:10]
            if desde and dia < desde:
                continue
            yield {"sessao": r.get("sessao", ""), "papel": r.get("papel") or "sem-papel",
                   "tarefa": r.get("tarefa", ""), "dia": dia, "tipo": r.get("tipo"),
                   "pasta": r.get("pasta"), "nota": r.get("nota")}


def acessos_das_transcricoes(dir_tr: Path, raiz: Path, desde: str, ignorar: set):
    # Sem filtro de ambiente: so contam caminhos do Brain deste ambiente, de qualquer pasta.
    for rec in ler_transcricoes(dir_tr, raiz, desde, ignorar, so_ambiente=False):
        for f in rec["ferramentas"]:
            for tipo, pasta, nota in extrair_acessos(f["nome"], f["entrada"], raiz):
                yield {"sessao": rec["sessao"], "papel": rec["papel"], "tarefa": rec["tarefa"],
                       "dia": rec["dia"], "tipo": tipo, "pasta": pasta, "nota": nota}


def registros_de_trabalho(raiz: Path):
    alvos = [raiz / "operacao"]
    for proj in (raiz / "projetos").glob("*"):
        alvos += [proj / "qualidade", proj / "docs", proj / "operacao"]
    for alvo in alvos:
        if alvo.is_dir():
            for arq in alvo.rglob("*.md"):
                yield arq, arq.read_text(encoding="utf-8", errors="replace")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raiz", default=os.environ.get("IA_RAIZ") or str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--logs", default="", help="pasta dos logs de acesso (padrao: <raiz>/logs/brain)")
    ap.add_argument("--transcricoes", default=str(Path.home() / ".claude" / "projects"))
    ap.add_argument("--desde", default="")
    ap.add_argument("--min-idade", type=int, default=60, help="dias sem uso para listar uma nota como 'sem uso'")
    ap.add_argument("--sem-transcricoes", action="store_true")
    ap.add_argument("--sem-logs", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--saida", default="", help="grava o relatorio neste arquivo em vez da tela")
    a = ap.parse_args()
    raiz = Path(a.raiz).resolve()

    notas = notas_do_brain(raiz / "BRAIN")
    backlinks = collections.Counter(l for n in notas.values() for l in n["links"])
    acessos = [] if a.sem_logs else list(acessos_do_log(Path(a.logs) if a.logs else raiz / "logs" / "brain", a.desde))
    no_log = {x["sessao"] for x in acessos}
    if not a.sem_transcricoes:
        acessos += list(acessos_das_transcricoes(Path(a.transcricoes), raiz, a.desde, no_log))

    citacoes, ajudou = collections.defaultdict(set), collections.defaultdict(collections.Counter)
    for arq, texto in registros_de_trabalho(raiz):
        for l in WIKILINK.findall(texto):
            citacoes[l.strip().lower()].add(str(arq.relative_to(raiz)))
        for l, voto in AJUDOU.findall(texto):
            ajudou[l.strip().lower()][voto.lower()] += 1

    por_pasta = collections.defaultdict(lambda: {"leitura": 0, "busca": 0, "sessoes": set()})
    por_papel = collections.defaultdict(lambda: {"regras": 0, "conhecimento": 0, "sessoes": set()})
    por_tarefa = collections.defaultdict(lambda: {"conhecimento": 0, "notas": set()})
    por_nota = collections.defaultdict(lambda: {"leituras": 0, "sessoes": set(), "papeis": set(), "ultima": ""})
    for x in acessos:
        p = por_pasta[x["pasta"]]
        p[x["tipo"]] += 1
        p["sessoes"].add(x["sessao"])
        tipo_area = "regras" if x["pasta"] in REGRAS else "conhecimento"
        por_papel[x["papel"]][tipo_area] += 1
        por_papel[x["papel"]]["sessoes"].add(x["sessao"])
        if x["tarefa"] and tipo_area == "conhecimento":
            por_tarefa[x["tarefa"]]["conhecimento"] += 1
            if x["nota"]:
                por_tarefa[x["tarefa"]]["notas"].add(x["nota"])
        if x["nota"]:
            n = por_nota[x["nota"].lower()]
            n["leituras"] += 1
            n["sessoes"].add(x["sessao"])
            n["papeis"].add(x["papel"])
            n["ultima"] = max(n["ultima"], x["dia"])

    hoje = date.today()
    linhas = []
    for chave, info in notas.items():
        if info["pasta"] in REGRAS:
            continue
        u = por_nota.get(chave, {"leituras": 0, "sessoes": set(), "papeis": set(), "ultima": ""})
        idade = (hoje - date.fromisoformat(info["criado"])).days
        n_cit, votos = len(citacoes.get(chave, ())), ajudou.get(chave, collections.Counter())
        if votos.get("sim") or votos.get("parcial"):
            situacao = "util (declarada)"
        elif n_cit:
            situacao = "usada (citada)"
        elif u["leituras"]:
            situacao = "lida, nao citada"
        elif idade < a.min_idade:
            situacao = "recente, ainda sem uso"
        else:
            situacao = "sem uso"
        linhas.append({"nota": info["titulo"], "pasta": info["pasta"], "idade_dias": idade,
                       "leituras": u["leituras"], "sessoes": len(u["sessoes"]), "papeis": sorted(u["papeis"]),
                       "ultima_leitura": u["ultima"], "citacoes": n_cit, "backlinks": backlinks.get(chave, 0),
                       "ajudou": dict(votos), "situacao": situacao})

    if a.json:
        texto = json.dumps({"gerado_em": hoje.isoformat(), "acessos": len(acessos), "notas": linhas}, ensure_ascii=False, indent=1)
    else:
        texto = relatorio(a, hoje, acessos, no_log, por_pasta, por_papel, por_tarefa, linhas)
    if a.saida:
        Path(a.saida).write_text(texto + "\n", encoding="utf-8")
        print(f"[uso_brain] relatorio gravado em {a.saida}")
    else:
        print(texto)


def relatorio(a, hoje, acessos, no_log, por_pasta, por_papel, por_tarefa, linhas) -> str:
    out = []
    w = out.append
    dias = sorted(x["dia"] for x in acessos if x["dia"])
    w(f"# Uso do Brain - {hoje}\n")
    w(f"Periodo com dados: {dias[0]} a {dias[-1]}." if dias else "Periodo com dados: nenhum.")
    sessoes = {x['sessao'] for x in acessos}
    w(f"Acessos: {len(acessos)} em {len(sessoes)} sessoes ({len(no_log)} pelo log permanente, "
      f"{len(sessoes - no_log)} pelas transcricoes). Notas de conhecimento: {len(linhas)}.\n")

    w("## Por pasta\n\n| Pasta | Area | Leituras de nota | Buscas na pasta | Sessoes |\n|---|---|---|---|---|")
    for pasta, c in sorted(por_pasta.items(), key=lambda x: -(x[1]["leitura"] + x[1]["busca"])):
        w(f"| {pasta} | {'regras' if pasta in REGRAS else 'conhecimento'} | {c['leitura']} | {c['busca']} | {len(c['sessoes'])} |")

    w("\n## Por papel\n\n| Papel | Sessoes | Acessos a regras | Acessos a conhecimento |\n|---|---|---|---|")
    for papel, c in sorted(por_papel.items(), key=lambda x: -x[1]["conhecimento"]):
        w(f"| {papel} | {len(c['sessoes'])} | {c['regras']} | {c['conhecimento']} |")

    if por_tarefa:
        w("\n## Por tarefa (so conhecimento)\n\n| Tarefa | Acessos | Notas distintas |\n|---|---|---|")
        for t, c in sorted(por_tarefa.items()):
            w(f"| {t} | {c['conhecimento']} | {len(c['notas'])} |")

    resumo = collections.Counter(l["situacao"] for l in linhas)
    w("\n## Situacao das notas de conhecimento\n\n| Situacao | Notas | O que significa |\n|---|---|---|")
    sentido = {
        "util (declarada)": "alguem marcou 'ajudou: sim/parcial' em Brain consultado",
        "usada (citada)": "citada com [[link]] num cartao, VER, SEC ou doc",
        "lida, nao citada": "consultada, mas sem registro de uso",
        "recente, ainda sem uso": f"criada ha menos de {a.min_idade} dias",
        "sem uso": f"nunca lida nem citada, com mais de {a.min_idade} dias",
    }
    for s, txt in sentido.items():
        w(f"| {s} | {resumo.get(s, 0)} | {txt} |")

    def tabela(titulo, filtro, chave, limite=15):
        sel = sorted((l for l in linhas if filtro(l)), key=chave)[:limite]
        if not sel:
            return
        w(f"\n## {titulo}\n\n| Nota | Pasta | Leituras | Sessoes | Citacoes | Ajudou | Ultima leitura |\n|---|---|---|---|---|---|---|")
        for l in sel:
            aj = ", ".join(f"{k} {v}" for k, v in l["ajudou"].items()) or "-"
            w(f"| {l['nota'][:70]} | {l['pasta']} | {l['leituras']} | {l['sessoes']} | {l['citacoes']} | {aj} | {l['ultima_leitura'] or '-'} |")

    tabela("Mais lidas", lambda l: l["leituras"], lambda l: (-l["leituras"], -l["citacoes"]))
    tabela("Lidas e nunca citadas (conferir se ajudaram)", lambda l: l["situacao"] == "lida, nao citada", lambda l: -l["leituras"])
    tabela("Arquivadas que ainda sao lidas (apontar para a substituta)", lambda l: l["pasta"] == "90_Arquivo" and l["leituras"], lambda l: -l["leituras"])
    tabela("Inbox mais lido (prioridade de curadoria)", lambda l: l["pasta"] == "00_Inbox" and l["leituras"], lambda l: -l["leituras"])
    tabela("Marcadas como nao ajudaram", lambda l: l["ajudou"].get("nao"), lambda l: -l["ajudou"]["nao"])
    sem_uso = sorted((l for l in linhas if l["situacao"] == "sem uso"), key=lambda l: (l["pasta"], l["nota"]))
    if sem_uso:
        w(f"\n## Sem uso ha mais de {a.min_idade} dias (revisar: fundir, ligar melhor ou arquivar)\n")
        for l in sem_uso:
            w(f"- {l['pasta']} / {l['nota']} ({l['idade_dias']} dias, {l['backlinks']} backlinks)")
    w("\nLimites: leitura por `grep` que so lista arquivos conta como busca na pasta; nota achada pela busca e "
      "nao aberta nao conta como leitura. A pasta e a atual da nota: leitura feita no Inbox antes de a nota "
      "ser promovida ou arquivada aparece na pasta nova. Transcricoes sao apagadas pelo Claude Code depois de um prazo; "
      "o log permanente (logs/brain) vale a partir da ativacao do hook.")
    return "\n".join(out)


if __name__ == "__main__":
    main()
