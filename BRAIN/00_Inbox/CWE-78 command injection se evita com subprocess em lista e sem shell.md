---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: pauta
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org, docs.python.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#9 CWE-78, #23 CWE-77); Python 3.x
criado: 2026-09-30
decisao:
tags: [seguranca, cwe, cwe-78, cwe-77, command-injection, subprocess]
---
# CWE-78 command injection se evita com subprocess em lista e sem shell

## Conteudo proposto

**O que e:** entrada do usuario entra num comando do sistema operacional e o shell a interpreta (`; rm -rf`, `$(...)`, `|`). CWE-78 e o caso de SO; CWE-77 e a versao generica.

**Como aparece na nossa stack:**
- `os.system(f"convert {arquivo} ...")`, `subprocess.run(cmd_string, shell=True)`, `os.popen`.
- Processar imagem/PDF chamando ferramenta externa com o nome enviado pelo usuario.
- Argumento comecando com `-` interpretado como opcao (argument injection).

**Controle:**
1. Preferir biblioteca Python a chamar programa externo.
2. Se precisar: `subprocess.run(["prog", "--", arquivo], shell=False, check=True, timeout=...)`, argumentos em lista, sem shell.
3. Validar argumentos por allowlist e usar nome gerado pelo servidor, nao o do usuario.
4. Container com usuario sem privilegio e sem rede quando possivel.

**Como testar:** procurar `shell=True`, `os.system`, `os.popen` no codigo (grep/bandit); enviar `a; touch /tmp/x`, `$(id)`, `-rf` como valores e ver se nada e executado.

## Evidencia

Cheat sheet OWASP de defesa contra command injection consta no indice de cheat sheets do Top 10 (consultado em 2026-09-30); a nota nao reproduz seu texto: abrir o link para os detalhes.

## Links confiaveis

- [CWE-78 (MITRE)](https://cwe.mitre.org/data/definitions/78.html): definicao oficial (CWE-77 na mesma base).
- [OS Command Injection Defense Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html): defesas em ordem de preferencia.
- [subprocess (Python)](https://docs.python.org/3/library/subprocess.html): argumentos em lista e riscos de `shell=True`.

## Por que e reaproveitavel

Vale sempre que o codigo chamar programa externo.

## Relacionadas no Brain

- [[CWE-94 code injection se evita sem eval, exec e templates montados com entrada do usuario]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario
