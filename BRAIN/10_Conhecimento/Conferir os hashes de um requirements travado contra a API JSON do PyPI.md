---
tipo: experimento
status: ativo
categoria: seguranca
linguagem: python
origem: agente/seguranca
tarefa: T-0014
confianca: media
fontes: [https://pypi.org]
verificado_em: 2026-10-02
valido_para: Python 3.10+, so biblioteca padrao; API JSON do PyPI (pypi.org/pypi/<nome>/<versao>/json)
ultimo_uso: 2026-10-02
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-02
tags: [experimento, seguranca, supply-chain, hashes, cwe-345, cwe-354, pip-tools]
---
# Conferir os hashes de um requirements travado contra a API JSON do PyPI

## Objetivo

Responder, de forma independente da ferramenta que gerou o travado: **todo hash `sha256` de um `requirements*.txt` travado e de um arquivo publicado no PyPI para aquele `pacote==versao`?** Mostra tambem hashes de sdist (inertes ou indesejados quando o travado usa `--only-binary :all:`) e wheels publicados que ficaram sem hash (pode quebrar a instalacao em outra plataforma).

O build com `--require-hashes` so confere os arquivos que ele baixa para a plataforma atual. Um hash adulterado de outro wheel ou de um sdist passa despercebido (ver [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]]).

## Quando usar

- Revisao de um diff que regenera ou edita travados com hash (pip-tools, `pip-compile --generate-hashes`).
- Depois de trocar opcoes de geracao (`--only-binary`, `--no-reuse-hashes`) para confirmar que so sairam hashes esperados.
- NAO serve para indice privado ou espelho (outra URL e outra API) nem para travado sem `==` exato.

## Por que este metodo e nao outro

- Rodar o build de novo so confere os arquivos da plataforma do build.
- Regenerar com a mesma ferramenta nao e independente: ela pode ter o mesmo defeito ou reaproveitar o hash antigo.
- A API JSON do PyPI traz o `sha256` de cada arquivo da versao sem baixar os arquivos (rapido, cerca de 1 requisicao por pacote).

## Ambiente

Python 3 do host, so biblioteca padrao, acesso de rede a `pypi.org` (dominio em `agentes/fontes-confiaveis.json`). Validado em 2026-10-02 com 71 pacotes e 1086 hashes.

## Como rodar

So le arquivos locais e consulta a API publica do PyPI; nao instala nada.

```bash
python3 conferir_hashes.py requirements.txt requirements-dev.txt
```

## Script

```python
"""Confere os hashes de requirements travados contra a API JSON do PyPI."""
import json
import re
import sys
import urllib.request

PADRAO = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s\\]+)")


def ler(caminho):
    # {(nome, versao): {hashes}} - os hashes vem nas linhas de continuacao do pacote
    pacotes, atual = {}, None
    for linha in open(caminho, encoding="utf-8"):
        m = PADRAO.match(linha)
        if m:
            atual = (m.group(1), m.group(2))
            pacotes[atual] = set()
        for h in re.findall(r"sha256:([0-9a-f]{64})", linha):
            pacotes[atual].add(h)
    return pacotes


def main():
    problemas = 0
    for caminho in sys.argv[1:]:
        pacotes = ler(caminho)
        for (nome, versao), travados in pacotes.items():
            url = f"https://pypi.org/pypi/{nome}/{versao}/json"
            with urllib.request.urlopen(url, timeout=30) as r:
                dados = json.load(r)
            arquivos = dados["urls"]  # arquivos desta versao
            wheels = {u["digests"]["sha256"] for u in arquivos if u["packagetype"] == "bdist_wheel"}
            sdists = {u["digests"]["sha256"] for u in arquivos if u["packagetype"] == "sdist"}
            desconhecidos = travados - wheels - sdists  # nao existe no PyPI: adulterado?
            de_sdist = travados & sdists                # inerte com --only-binary :all:
            faltam = wheels - travados                  # wheel publicado sem hash no travado
            if desconhecidos or de_sdist or faltam:
                problemas += 1
                print(f"{caminho} {nome}=={versao}: desconhecidos={len(desconhecidos)} "
                      f"sdist={len(de_sdist)} faltam_wheels={len(faltam)}")
        total = sum(len(v) for v in pacotes.values())
        print(f"{caminho}: {len(pacotes)} pacotes, {total} hashes conferidos")
    print("PROBLEMAS:", problemas)


main()
```

## Como interpretar

- `PROBLEMAS: 0`: todo hash e de wheel publicado, nenhum de sdist, nenhum wheel sem hash.
- `desconhecidos > 0`: **achado**. O hash nao corresponde a nenhum arquivo daquela versao (adulterado ou de outra versao).
- `sdist > 0`: esperado num travado sem `--only-binary`. Com `--only-binary :all:`, e hash inerte, provavelmente reaproveitado.
- `faltam_wheels > 0`: o travado nao instala naquela plataforma. Pode ser intencional, mas confira. Um wheel publicado **depois** da geracao tambem aparece aqui, sem ser defeito.

## Limites e cuidados

- Confia no PyPI e no TLS: nao detecta pacote malicioso publicado legitimamente (para isso, OSV, pip-audit e revisao da dependencia).
- Os nomes das linhas `pacote==versao` precisam ser aceitos pela API, que normaliza a maioria dos nomes.
- Arquivo apagado (yank nao apaga) ou versao removida do PyPI gera erro 404: trate como achado a investigar.
- Uma requisicao por pacote. Em travados grandes, respeite o PyPI e nao rode em laco.

## Historico de uso

| Data | Tarefa e registro | Contexto e motivo do uso | Resultado | Script mudou? |
|---|---|---|---|---|
| 2026-10-02 | T-0014, revisao de seguranca rodada 3 (cartao) | Conferir os travados regenerados com `--no-reuse-hashes` e `--only-binary :all:` | 3 travados, 71 pacotes, 1086 hashes: 0 problemas | nao (primeira versao) |
| 2026-10-02 | T-0014, VER-T0014-03 (revisor) | Conferencia independente dos travados de `e499d5a` antes de aprovar o SEC-T0014-05 | 3 travados, 71 pacotes, 1086 hashes: 0 problemas (igual a Seguranca) | nao |

## Versoes anteriores

Nenhuma.

## Relacionadas no Brain

- [[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]] - o defeito que este experimento detecta de forma independente.
- [[CWE-345 e a classe de hash copiado sem reconferir no indice - filha mais proxima e CWE-354]] - classe da fraqueza.
- [[pip-compile only-binary descarta hashes de sdist]] - explica o caso `sdist > 0`.

## Decisao do Bibliotecario

Promovido (2026-10-03). Script generalizado conferido: so biblioteca padrao, le arquivos locais e consulta a API publica do PyPI (dominio confiavel), sem dados de projeto nem segredos; nao instala nada. Historico de uso com 2 usos (T-0014: cartao da Seguranca e VER-T0014-03), `ultimo_uso: 2026-10-02` coerente. Sem duplicata. Ligado ao defeito que detecta ([[pip-compile reaproveita os hashes do travado existente e preserva um hash adulterado]]).

