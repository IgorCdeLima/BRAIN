"""Consumo de tokens por tarefa, papel, modelo e rodada (ADM-0011).

Somente leitura. Fontes:
  1. logs/consumo/AAAA-MM.jsonl (hook registrar_consumo.py): última linha de cada sessão.
  2. Transcrições do Claude Code, para sessões sem log (período anterior ao hook). Só as
     sessões do 01_IA (cópia principal ou worktree T-####). Cada resposta conta uma vez.

Rodada = uma sessão de um papel (ex.: Revisor duas vezes na mesma tarefa = 2 rodadas).
Sem valor em dinheiro: preço é fato volátil (se precisar, SEARCH no dia).
O cache lido costuma ser a maior parte: as quatro colunas aparecem separadas.

Uso:
  py -3 ferramentas/consumo.py                    # todas as tarefas e o trabalho fora de tarefa
  py -3 ferramentas/consumo.py --tarefa T-0010    # bloco pronto para a secao "Consumo" do cartao
  opcoes: --desde AAAA-MM-DD  --json  --sem-transcricoes  --sem-logs  --logs DIR
"""

import argparse
import collections
import json
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transcricoes import CAMPOS_USAGE, ler_transcricoes  # noqa: E402

COLUNAS = [("input_tokens", "Entrada"), ("cache_creation_input_tokens", "Cache criado"),
           ("cache_read_input_tokens", "Cache lido"), ("output_tokens", "Saida")]


def n(v: int) -> str:
    return f"{v:,}".replace(",", ".")


def sessoes_do_log(dir_logs: Path, desde: str) -> dict:
    ultimas = {}
    for arq in sorted(dir_logs.glob("*.jsonl")) if dir_logs.is_dir() else []:
        for linha in arq.open(encoding="utf-8", errors="replace"):
            try:
                r = json.loads(linha)
            except ValueError:
                continue
            if r.get("sessao") and not (desde and r.get("ts", "")[:10] < desde):
                ultimas[r["sessao"]] = {"papel": r.get("papel") or "sem-papel", "tarefa": r.get("tarefa", ""),
                                        "dia": r.get("ts", "")[:10], "modelos": r.get("modelos") or {}, "fonte": "log"}
    return ultimas


def sessoes_das_transcricoes(dir_tr: Path, raiz: Path, desde: str, ignorar: set) -> dict:
    sessoes = {}
    for rec in ler_transcricoes(dir_tr, raiz, desde, ignorar):
        s = sessoes.setdefault(rec["sessao"], {"papel": "sem-papel", "tarefa": "", "dia": rec["dia"],
                                               "modelos": {}, "fonte": "transcricao"})
        if rec["papel"] != "sem-papel":
            s["papel"] = rec["papel"]
        s["tarefa"] = s["tarefa"] or rec["tarefa"]
        u = rec["usage_novo"]
        if u and rec["modelo"] != "<synthetic>":
            t = s["modelos"].setdefault(rec["modelo"] or "?", dict.fromkeys(CAMPOS_USAGE, 0) | {"respostas": 0})
            for k in CAMPOS_USAGE:
                t[k] += u[k]
            t["respostas"] += 1
    return {k: v for k, v in sessoes.items() if v["modelos"]}


def agrupar(sessoes: dict, chave) -> dict:
    grupos = collections.defaultdict(lambda: collections.Counter())
    rodadas = collections.defaultdict(set)
    for sid, s in sessoes.items():
        for modelo, t in s["modelos"].items():
            g = chave(s, modelo)
            grupos[g].update({k: t.get(k, 0) for k in (*CAMPOS_USAGE, "respostas")})
            rodadas[g].add(sid)
    return {g: (len(rodadas[g]), c) for g, c in grupos.items()}


def linha_tabela(rotulos, rodadas, c) -> str:
    return "| " + " | ".join(rotulos) + f" | {rodadas} | {n(c['respostas'])} | " + " | ".join(n(c[k]) for k, _ in COLUNAS) + " |"


def cabecalho(rotulos) -> str:
    nomes = list(rotulos) + ["Rodadas", "Respostas"] + [t for _, t in COLUNAS]
    return "| " + " | ".join(nomes) + " |\n|" + "---|" * len(nomes)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raiz", default=os.environ.get("IA_RAIZ") or str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--logs", default="", help="pasta do log de consumo (padrao: <raiz>/logs/consumo)")
    ap.add_argument("--transcricoes", default=str(Path.home() / ".claude" / "projects"))
    ap.add_argument("--tarefa", default="")
    ap.add_argument("--desde", default="")
    ap.add_argument("--sem-transcricoes", action="store_true")
    ap.add_argument("--sem-logs", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    raiz = Path(a.raiz).resolve()

    sessoes = {} if a.sem_logs else sessoes_do_log(Path(a.logs) if a.logs else raiz / "logs" / "consumo", a.desde)
    if not a.sem_transcricoes:
        sessoes.update(sessoes_das_transcricoes(Path(a.transcricoes), raiz, a.desde, set(sessoes)))
    if a.tarefa:
        sessoes = {k: v for k, v in sessoes.items() if v["tarefa"] == a.tarefa}

    if a.json:
        print(json.dumps(sessoes, ensure_ascii=False, indent=1))
        return
    if not sessoes:
        print(f"Nenhuma sessao encontrada{' para ' + a.tarefa if a.tarefa else ''}. "
              "Transcricoes antigas podem ter sido apagadas pelo Claude Code.")
        return

    fontes = collections.Counter(s["fonte"] for s in sessoes.values())
    dias = sorted(s["dia"] for s in sessoes.values() if s["dia"])
    origem = f"{len(sessoes)} sessoes ({fontes.get('log', 0)} pelo log, {fontes.get('transcricao', 0)} pelas transcricoes), {dias[0]} a {dias[-1]}"

    if a.tarefa:
        print(f"- Medido em {date.today()} com `py -3 ferramentas/consumo.py --tarefa {a.tarefa}`: {origem}.\n")
        print(cabecalho(["Papel", "Modelo"]))
        g = agrupar(sessoes, lambda s, m: (s["papel"], m))
        for (papel, modelo), (rod, c) in sorted(g.items()):
            print(linha_tabela([papel, modelo], rod, c))
        tot = agrupar(sessoes, lambda s, m: "total")["total"]
        print(linha_tabela(["**Total**", ""], tot[0], tot[1]))
        return

    print(f"# Consumo de tokens - {date.today()}\n\n{origem}. Valores em tokens; sem preco.\n")
    em_tarefa = {k: v for k, v in sessoes.items() if v["tarefa"]}
    fora = {k: v for k, v in sessoes.items() if not v["tarefa"]}
    if em_tarefa:
        print("## Por tarefa\n\n" + cabecalho(["Tarefa", "Papel"]))
        g = agrupar(em_tarefa, lambda s, m: (s["tarefa"], s["papel"]))
        tot = agrupar(em_tarefa, lambda s, m: (s["tarefa"], "**total**"))
        for chave in sorted(set(g) | set(tot), key=lambda x: (x[0], x[1] == "**total**", x[1])):
            rod, c = (g.get(chave) or tot.get(chave))
            print(linha_tabela(list(chave), rod, c))
    if fora:
        print("\n## Fora de tarefa (copia principal: coordenacao, curadoria, pesquisa, administracao)\n\n" + cabecalho(["Papel"]))
        for (papel,), (rod, c) in sorted(agrupar(fora, lambda s, m: (s["papel"],)).items()):
            print(linha_tabela([papel], rod, c))
    print("\n## Por modelo\n\n" + cabecalho(["Modelo"]))
    for (modelo,), (rod, c) in sorted(agrupar(sessoes, lambda s, m: (m,)).items()):
        print(linha_tabela([modelo], rod, c))
    print("\nLimites: sessoes sem papel no 01_IA aparecem como 'sem-papel'; transcricoes antigas sao apagadas "
          "pelo Claude Code, e o log (logs/consumo) vale a partir da ativacao do hook.")


if __name__ == "__main__":
    main()
